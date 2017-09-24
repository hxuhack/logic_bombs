import os
import re
import logging


class TemplateParser:
    statement_pattern = re.compile(r'[ \t\r]*\{\%(\%+[^}]|[^%])+\%\}')

    condition_str = r'((not +)?\{\<[\w][\w\d]*\>\} *(\>|\<|\>\=|\<\=|\=\=|and|or|is) *)*((not +)?\{\<[\w][\w\d]*\>\} *)'
    condition_token = r'((not +)?\{\<[\w][\w\d]*\>\})'

    for_pattern = re.compile(r'for +(\{\<([\w][\w\d]*)\>\} *,? *)* +in +\{\<([\w][\w\d]*)\>\}:')
    if_pattern = re.compile(r'if +%s:' % condition_str)
    elif_pattern = re.compile(r'elif +%s:' % condition_str)
    else_pattern = re.compile(r'else *:')
    while_pattern = re.compile('while +%s:' % condition_str)

    func_call_pattern = re.compile('')
    var_pattern = re.compile(r'\{\<(\>+[^}]|[^>])+\>\}')
    valid_pattern = re.compile(r'[\w][\w\d]*')

    ALLOWED_FUNCS = ['enumerate', 'len', 'str', 'range']
    IF = 1
    ELIF = 2
    ELSE = 4
    FOR = 8
    WHILE = 16

    INT = 32
    DOUBLE = 64
    STR = 128

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

    def __double_bracket_replace__(self, stm: str, params: dict):
        vars_raw = [i.group() for i in self.var_pattern.finditer(stm)]
        vars = {}
        for var_raw in vars_raw:
            key = var_raw[2:-2].strip()
            if self.valid_pattern.match(key) is None:
                raise SyntaxError(var_raw)
            if not key in vars:
                vars[key] = [var_raw, ]
            else:
                vars[key].append(var_raw)

        for var, var_raw in vars.items():
            value = params[var]
            for _ in var_raw:
                stm = stm.replace(_, value)
        return stm

    def __statement_parser__(self, stm: str):
        pass

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

        stms = list(filter(lambda x: len(x.strip) != 0, map(trim, stms)))
        return [(_, get_indent(_)) for _ in stms]

    # Sub-statement
    def __condition__parser__(self, stm: str):
        pass

    def __for_parser__(self, stm: str):
        pass

    def __while_parser__(self, stm: str):
        pass

    def __if_parser__(self, stm: str):
        pass

    def __elif_parser__(self, stm: str):
        pass

    def __else_parser__(self, stm: str):
        pass

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

if __name__ == '__main__':
    params = dict(
        vars=['a', 'b', 'c'],
        params='a, b, c',
        defs='int a = 0;'
    )
    tp = TemplateParser('templates/klee.c')
    print(tp.appender_parser(params))
