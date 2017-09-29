import os
import re
import template_parser as tpp


allowed_funcs = ['len', 'enumerate', 'range', 'not']


class ScriptRunner:
    def __init__(self, init_values: dict, allowed_funcs: list=allowed_funcs):
        self.allowed_funcs = allowed_funcs
        self.scope = []
        self.inits = init_values
        self.variables = [self.inits, ]

    def __get_var__(self, key):
        flag = False
        res = None
        for v_table in reversed(self.variables):
            try:
                res = v_table[key]
                flag = True
            except KeyError:
                continue
        if not flag:
            raise KeyError(key, self.variables)
        else:
            return res

    def __parser__(self, stm, token_tables):
        for key in token_tables:
            res = self.evaluate(token_tables[key])
            token_tables[key] = res
        print(token_tables)
        return stm.format(**token_tables)

    def run(self, stms: list, index=0, scope=None, expected_indent=None):
        if scope:
            self.scope = scope

        # Stop iteration
        if index == len(stms):
            return ''

        results = []
        base_indent = stms[index][1]
        for i in range(index, len(stms)):
            stm, indent = stms[i]
            if indent != base_indent:
                raise RuntimeError(stm, indent)

            if stm.s_type == 'str':
                results.append()

    def evaluate(self, tpv: tpp.TPVariable, token=None):
        if token is None:
            token = tpv.token.call_stack
            # print(token)
        func = token[0]
        values = token[1:]
        if func is None and type(values[0]) != list:
            tp_type = type(values[0])
            if tp_type != str:
                return values[0]
            elif tpp.TemplateParser.str_pattern.match(values[0]):
                return values[0][1:-1]
            else:
                return self.__get_var__(values[0])

        param_list = [self.evaluate(tpv, _) for _ in values]
        if func is None and len(param_list) == 1:
            return param_list[0]
        elif func in self.allowed_funcs:
            if func == 'not' and len(param_list) == 1:
                return not param_list[0]
            elif func == 'len':
                return len(*param_list)
            elif func == 'range':
                return range(*param_list)
            elif func == 'enumerate':
                return enumerate(*param_list)
            else:
                raise RuntimeError(str(func), str(param_list))
        else:
            raise RuntimeError(str(func), str(param_list))


if __name__ == '__main__':
    tp = tpp.TemplateParser('templates/test.c')
    sr = ScriptRunner(dict(vars=[1,2,3,4], index='play'))
    for stm, indent in tp.parse()[0]:
        stm = stm.parsed
        print(stm)
        print(sr.__parser__(stm[0], stm[-1]))

    # tpv = tpp.TPVariable(256, 'test', [None, ['len', [None, 'c']]])
    # s = ScriptRunner({'c': [1,2,34]})
    # print(s.evaluate(tpv))
