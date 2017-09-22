import os
import re
import logging


class TemplateParser:
    for_pattern = re.compile(r'for +\{\<([a-zA-Z_][a-zA-Z0-9_]*)\>\} +in +\{\<([a-zA-Z_][a-zA-Z0-9_]*)\>\}:')

    @staticmethod
    def doule_bracket_replace(stm: str, params: dict):
        pattern = re.compile(r'\{\<(\>+[^}]|[^>])+\>\}')
        vars_raw = [i.group() for i in pattern.finditer(stm)]
        vars = {}
        for var_raw in vars_raw:
            key = var_raw[2:-2].strip()
            if not key in vars:
                vars[key] = [var_raw, ]
            else:
                vars[key].append(var_raw)
        # print(stm, vars)
        for var, var_raw in vars.items():
            value = params[var]
            for _ in var_raw:
                stm = stm.replace(_, value)
        return stm

    @staticmethod
    def appender_parser(tp_path: str, params: dict):
        with open(tp_path) as f:
            tp = f.read()

        pattern = re.compile(r'[ \t\r]*\{\%(\%+[^}]|[^%])+\%\}')
        tp_replace = [_.group() for _ in re.finditer(pattern, tp)]
        for replace in tp_replace:
            tmp = TemplateParser.statement_parser(replace, params, 2)
            tp = tp.replace(replace, tmp)

        tp = TemplateParser.doule_bracket_replace(tp, params)
        return tp

    @staticmethod
    def statement_parser(stm: str,  params: dict, base_indent:int):
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
            for_params = re.findall(TemplateParser.for_pattern, cur_stm[0])

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
                stm = TemplateParser.doule_bracket_replace(stm, params)
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
        params='a, b, c'
    )
    TemplateParser.appender_parser('templates/klee.c', params)
