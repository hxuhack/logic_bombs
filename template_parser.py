import os
import re
import logging


class TemplateParser:
    statement_pattern = re.compile(r'[ \t\r]*\{\%(\%+[^}]|[^%])+\%\}')

    condition_str = r'((not +)*\{\<(\>+[^}]|[^>])+\>\} +(\>|\<|\>\=|\<\=|\=\=|!=|\+|\-|\*|\/|and|or|is|in|not)+ +)*((not +)?\{\<(\>+[^}]|[^>])+\>\} *)'
    condition_token = r'((not +)*\{\<(\>+[^}]|[^>])+\>\})'
    func_call_token = r'\{\<(\>+[^}]|[^>])+\>\}'

    for_pattern = re.compile(r'for +((\{\<([\w][\w\d]*)\>\} *,? *)*) +in +\{\<(\>+[^}]|[^>])+\>\}:$')
    if_pattern = re.compile(r'if +(%s):$' % condition_str)
    elif_pattern = re.compile(r'elif +(%s):$' % condition_str)
    else_pattern = re.compile(r'else *:$')
    while_pattern = re.compile(r'while +(%s):$' % condition_str)
    exp_pattern = re.compile(r'\{\<([\w][\w\d]*)\>\} +\= +(%s)' % condition_str)
    escape_equal_pt = re.compile(r'\{\<([\w][\w\d]*)\>\} +\\\= +(%s)' % condition_str)

    func_pattern = re.compile(r'[\w][\w\d]*\(')
    param_list_pattern = re.compile(r'([\w][\w\d]*\(.*\)|[^(, ]+)')
    var_pattern = re.compile(r'\{\<([\w][\w\d]*)\>\}')
    in_bracket_pattern = re.compile(r'\{\<(\>+[^}]|[^>])+\>\}')
    valid_pattern = re.compile(r'[\w][\w\d]*')

    int_pattern = re.compile(r'^((\+|\-)?[\d]+)d$')
    float_pattern = re.compile(r'^(\+|\-)?([\d]+(\.[\d]*)?|\.[\d]+)([Ee](\+|\-)[\d]+)?f$')
    str_pattern = re.compile(r'^(\'[^\']*\'|\"[^\"]*\")$')

    condition_tk_pt = re.compile(condition_token)
    condition_pt = re.compile(condition_str)
    func_call_pattern = re.compile(func_call_token)
    left_v_pt = re.compile(r'^[ \t]*\{\<([\w][\w\d]*)\>\} *\=')

    ALLOWED_FUNCS = ['enumerate', 'len', 'str', 'range']
    IF = 1
    ELIF = 2
    ELSE = 4
    FOR = 8
    WHILE = 16

    INT = 32
    DOUBLE = 64
    STR = 128
    UNV = 256

    def __init__(self, path: str, indent=4):
        """
        :param path: path to template
        :param indent: the indent you are using, must in [2, 4, 8]
        """
        assert indent in [2, 4, 8]

        self.path = path
        self.indent = indent
        self.contents = ''
        with open(self.path) as f:
            for l in f:
                self.contents += l

        if self.indent != 4:
            logging.info('You are using indent at %d.' % self.indent)

    def parse(self):
        res = []
        for s in self.statement_pattern.finditer(self.contents):
            stm_list = s.group().replace('{%', '  ').replace('%}', '  ').split('\n')
            stms = self.__statements_pre_process__(stm_list)
            res.append([(self.__statement_parser__(s[0].strip()), s[1]) for s in stms])
        return res

    def replace(self, replace_texts: list):
        res = self.contents
        for index, s in enumerate(self.statement_pattern.finditer(self.contents)):
            res = res.replace(s.group(), replace_texts[index])
        res = res.replace(r'\=', '=')
        return res

    def __double_bracket_replace__(self, stm: str, params: dict):
        vars_raw = [i.group() for i in self.var_pattern.finditer(stm)]
        vars_dict = {}
        for var_raw in vars_raw:
            key = var_raw[2:-2].strip()
            if self.valid_pattern.match(key) is None:
                raise SyntaxError(var_raw)
            if not key in vars_dict:
                vars_dict[key] = [var_raw, ]
            else:
                vars_dict[key].append(var_raw)

        for var, var_raw in vars_dict.items():
            value = params[var]
            for _ in var_raw:
                stm = stm.replace(_, value)
        return stm

    def __statement_parser__(self, stm: str):
        check_priorities = {
            self.__exp_parser__: 'exp',
            self.__for_parser__: 'for',
            self.__while_parser__: 'while',
            self.__if_parser__: 'if',
            self.__elif_parser__: 'elif',
            self.__else_parser__: 'else',

        }
        stm_type = 'str'
        res = stm

        for parser in check_priorities:
            res = parser(stm)
            if res:
                stm_type = check_priorities[parser]
                break
            else:
                continue
        if stm_type == 'str':
            vars_table = {}
            bak = stm
            res = self.__variable_replacer__(bak)
            # for index, token in enumerate(self.func_call_pattern.finditer(stm)):
            #     var_name = 'TMP%d' % index
            #     token = token.group()
            #     bak = bak.replace(token, '{%s}' % var_name)
            #     tpk = self.__token_parser__(token)
            #     vars_table[var_name] = TPVariable(self.UNV, var_name, tpk)

        return TPStatement(stm_type, stm, res)

    def __statements_pre_process__(self, stms: list):
        """
        :param stms: A list of statements to be processed
        :return: A list filled with tuple, (statement, indent)
        """
        def trim(stm: str):
            stm = stm.replace('\t', ' ' * self.indent)
            stm = stm.replace('{%', '   ')
            stm = stm.replace('%}', '   ')
            return stm

        def get_indent(stm: str):
            spaces = len(stm) - len(stm.lstrip())
            if spaces % self.indent != 0:
                raise IndentationError(stm + ', Indent Error!')
            else:
                return spaces // self.indent

        stms = list(filter(lambda x: len(x.strip()) != 0, map(trim, stms)))
        return [(_, get_indent(_)) for _ in stms]

    # Sub-statement
    def __token_parser__(self, token: str):
        def call_stack_analysis(calls):
            calls = calls.strip()
            core = calls
            for func in self.func_pattern.finditer(calls):
                if core[-1] != ')':
                    raise SyntaxError(token)
                else:
                    func = func.group()
                    core = core.replace(func, '')
                    core = core[:-1].strip()
                    func = func[:-1]
                    stack = [func, ]
                    sub_tokens = [_.group() for _ in self.param_list_pattern.finditer(core)]
                    stack.extend([call_stack_analysis(_) for _ in sub_tokens])
                    for st in sub_tokens:
                        core = core.replace(st, '')
                    core = core.replace(',', '')
                    if len(core.strip()) != 0:
                        raise SyntaxError(calls)
                    return stack
            # Single variable or constant
            if self.int_pattern.match(calls):
                calls = int(self.int_pattern.search(calls).group()[:-1])
            elif self.float_pattern.match(calls):
                calls = float(self.float_pattern.search(calls).group()[:-1])
            elif self.str_pattern.match(calls):
                calls = calls
            elif not calls.isidentifier():
                raise SyntaxError(calls)

            return [None, calls]

        not_cnt = 0
        token = token.strip()
        while token.startswith('not'):
            not_cnt += 1
            token = token[3:].strip()

        calls = [_.group() for _ in self.in_bracket_pattern.finditer(token)]
        if len(calls) != 1:
            raise SyntaxError(token)
        calls = calls[0][2:-2].strip()
        try:
            call_stack = call_stack_analysis(calls)
        except SyntaxError as e:
            print(e)
            raise SyntaxError(calls)

        return TPToken(['not' if not_cnt % 2 else None, call_stack])

    def __condition_parser__(self, stm: str):
        vars_table = {}
        for index, token in enumerate(self.condition_tk_pt.finditer(stm)):
            var_name = 'TMP%d' % index
            token = token.group()
            stm = stm.replace(token, '{%s}' % var_name)
            tpk = self.__token_parser__(token)
            vars_table[var_name] = TPVariable(self.UNV, var_name, tpk)

        return stm, vars_table

    def __variable_replacer__(self, stm: str, vars_table: dict=None):
        if not vars_table:
            vars_table = {}

        stm = stm.replace('{', '{{')
        stm = stm.replace('}', '}}')
        for index, var in enumerate(self.func_call_pattern.finditer(stm)):
            var_name = 'VAR%d' % index
            var = var.group()
            stm = stm.replace(var, var_name)
            tpk = self.__token_parser__(var)
            vars_table[var_name] = TPVariable(self.UNV, var_name, tpk)
        return stm, vars_table

    def __exp_parser__(self, stm: str):
        res = self.escape_equal_pt.match(stm)
        if res:
            return None
        res = self.exp_pattern.match(stm)
        if not res:
            return None
        else:
            left_v = self.left_v_pt.findall(stm)[0]
            remained = '='.join(stm.split('=')[1:])
            cd_str = self.condition_pt.search(remained).group().strip()
            cd_res = self.__condition_parser__(cd_str)
            return stm.replace(cd_str, cd_res[0]), left_v, cd_res[1]

    def __for_parser__(self, stm: str):
        res = self.for_pattern.match(stm)
        if not res:
            return None
        else:
            unpacked_vars = []
            tokens = [_.group() for _ in self.in_bracket_pattern.finditer(stm)]
            for i in tokens[:-1]:
                if not i[2:-2].strip().isidentifier():
                    raise SyntaxError(stm)
                else:
                    unpacked_vars.append(i[2:-2].strip())

            cd_res = self.__condition_parser__(tokens[-1].strip())
            key = next(iter(cd_res[1]))
            return stm.replace(tokens[-1], cd_res[0]), unpacked_vars, cd_res[1][key]

    def __while_parser__(self, stm: str):
        res = self.while_pattern.match(stm)
        if not res:
            return None
        else:
            cd_str = self.condition_pt.search(stm).group().strip()
            cd_res = self.__condition_parser__(cd_str)
            return stm.replace(cd_str, cd_res[0]), cd_res[1]

    def __if_parser__(self, stm: str):
        res = self.if_pattern.match(stm)
        if not res:
            return None
        else:
            cd_str = self.condition_pt.search(stm).group().strip()
            cd_res = self.__condition_parser__(cd_str)
            return stm.replace(cd_str, cd_res[0]).replace('if', '').replace(':', '').strip(), cd_res[1]

    def __elif_parser__(self, stm: str):
        res = self.elif_pattern.match(stm)
        if not res:
            return None
        else:
            cd_str = self.condition_pt.search(stm).group().strip()
            cd_res = self.__condition_parser__(cd_str)
            return stm.replace(cd_str, cd_res[0]).replace('elif', '').replace(':', '').strip(), cd_res[1]

    def __else_parser__(self, stm: str):
        res = self.else_pattern.match(stm)
        if not res:
            return None
        else:
            return True

    def __call_func__(self, stm):
        pass

    def appender_parser(self, params: dict):
        pattern = self.statement_pattern
        tp_replace = [_.group() for _ in re.finditer(pattern, self.contents)]
        for replace in tp_replace:
            tmp = self.statement_parser(replace, params, 2)
            self.contents = self.contents.replace(replace, tmp)

        self.contents = self.__double_bracket_replace__(self.contents, params)
        return self.contents

    def statement_parser(self, stm: str,  params: dict, base_indent:int):
        def pre_process(stm_list):
            def trim(st: str):
                st = st.replace('\t', '    ')
                st = st.replace('\r', ' ')
                st = st.replace('{%', '   ')
                st = st.replace('%}', '   ')
                return st

            def get_indent(line: str):
                spaces = len(line) - len(line.lstrip())
                if spaces % 4 != 0:
                    raise IndentationError(line + ', Indent Error!')
                else:
                    return spaces // 4

            stm_list = list(map(trim, stm_list))
            stm_list = list(filter(lambda x: len(x.strip()) != 0, stm_list))
            return [(_, get_indent(_)) for _ in stm_list]

        def iter_generator(index, stm_list, params, base_indent):
            cur_stm = stm_list[index]
            for_params = re.findall(self.for_pattern, cur_stm[0])

            res = []
            if len(for_params) > 1:
                raise SyntaxError(cur_stm[0])
            elif len(for_params) == 1:
                if index == len(stm_list) - 1:
                    raise SyntaxError(cur_stm[0])

                next_stm = stm_list[index + 1]
                if next_stm[1] != cur_stm[1] + 1:
                    raise SyntaxError(next_stm[0])

                inner_name, outer_name = for_params[0]

                outer = params.get(outer_name, [])
                for _ in outer:
                    params[inner_name] = _
                    for i in range(index + 1, len(stm_list)):
                        if stm_list[i][1] == cur_stm[1] + 1:
                            res.append(iter_generator(i, stm_list, params, base_indent))
                        elif stm_list[i][1] <= cur_stm[1]:
                            break
                return '\n'.join(res)
            else:
                stm = cur_stm[0].strip()
                indent = cur_stm[1] - base_indent
                stm = self.__double_bracket_replace__(stm, params)
                stm = ' ' * indent * 4 + stm
                if index != len(stm_list) - 1 and stm_list[index + 1][1] == cur_stm[1]:
                    next_stm = iter_generator(index + 1, stm_list, params, base_indent)
                    return stm + '\n' + next_stm
                else:
                    return stm

        stm_list = stm.split('\n')
        stm_list = pre_process(stm_list)
        append = iter_generator(0, stm_list, params, base_indent)
        return append

    def test(self):
        res1 = self.__condition_parser__('not not {<A>} >= {<enumerate(B, 2d, len(C), 2.3f, "test")>} is {<D>}')
        res2 = self.__while_parser__('elif {<index>} == {<3d>} and {<var>} == {<"test">}:')
        for i, var in res1[1].items():
            print(i, var)


class TPStatement:
    def __init__(self, s_type, stm, parsed):
        self.s_type = s_type
        self.stm = stm
        self.parsed = parsed

    def __str__(self):
        return '\t'.join([str(self.s_type), str(self.stm), str(self.parsed)])


class TPVariable:
    def __init__(self, v_type, name, token, value=None):
        self.v_type = v_type
        self.name = name
        self.token = token
        self.value = value

    def __str__(self):
        return '; '.join([str(self.v_type), self.name, str(self.token), str(self.value)])

    def __repr__(self):
        return self.__str__()


class TPToken:
    def __init__(self, call_stack):
        self.call_stack = call_stack

    def __str__(self):
        return str(self.call_stack)
