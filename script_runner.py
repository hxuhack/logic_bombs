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

    def run(self, stms: list, index=0, scope=None):
        if scope:
            self.scope = scope

        # Stop iteration
        if index == len(stms):
            return ''

    def evaluate(self, tpv: tpp.TPVariable, v_table: dict, token=None):
        if token is None:
            token = tpv.token
        func = token[0]
        values = token[1:]
        if func is None and type(values[0]) != list:
            tp_type = type(values[0])
            if tp_type != str:
                return values[0]
            elif tpp.TemplateParser.str_pattern.match(values[0]):
                return values[0][1:-1]
            else:
                return v_table[values[0]]

        param_list = [self.evaluate(tpv, v_table, _) for _ in values]
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
    tpv = tpp.TPVariable(256, 'test', [None, '"casgfd"'])
    s = ScriptRunner({'c': 8})
    print(s.evaluate(tpv, {'c': [1, 2, 3, 43, 54]}))
