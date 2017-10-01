import os
import re
import template_parser as tpp
from copy import copy
from IPython import embed

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
        cp_table = copy(token_tables)
        for key in cp_table:
            print("TKT", str([(key, str(cp_table[key])) for key in token_tables]))
            res = self.evaluate(cp_table[key])
            cp_table[key] = res
        return stm.format(**cp_table)

    def run(self, stms: list, index=0, expected_indent=None, ignore=False):
        """
            stm: 
        """
        # Stop iteration
        if index == len(stms):
            return ''
        elif index > len(stms):
            raise RuntimeError(stms[-1])

        is_branch = False
        branch_true = False
        used_to_be_true = False

        results = []
        base_indent = stms[index][1] if not expected_indent else expected_indent
        if ignore:
            for i in range(index, len(stms)):
                if stms[i][1] >= base_indent:
                    continue
            return i, []

        i = index
        while i < len(stms):
            print()
            stm, indent = stms[i]
            print(stm, self.variables)

            if indent > base_indent:
                raise RuntimeError(stm, indent)
            elif indent < base_indent:
                break

            if stm.s_type not in ['if', 'else', 'elif']:
                is_branch = False

            if stm.s_type == 'str':
                print(self.__parser__(*stm.parsed))
                results.append(self.__parser__(*stm.parsed))
            elif stm.s_type == 'for':
                tmp_iter = self.evaluate(stm.parsed[-1])
                for tmp in tmp_iter:
                    print('tmp', tmp)
                    self.variables.append({key: tmp[index] for index, key in enumerate(stm.parsed[1])})
                    results.extend(self.run(stms, index + 1, base_indent + 1)[1])
                    self.variables.pop(-1)
            elif stm.s_type == 'while':
                while self.evaluate(stm.parsed[-1]):
                    self.variables.append({})
                    results.extend(self.run(stms, index + 1, base_indent + 1)[1])
                    self.variables.pop(-1)
            elif stm.s_type == 'exp':
                self.variables[-1][stm.parsed[1]] = self.evaluate(stm.parsed[-1])
            elif stm.s_type == 'if':
                is_branch = True
                used_to_be_true, branch_true = [self.evaluate(stm.parsed[-1]), ] * 2
                end, res = self.run(stms, index + 1, base_indent + 1, not branch_true)
                i = end
                results.extend(res)
                continue
            elif stm.s_type == 'elif':
                if not is_branch:
                    raise SyntaxError(stm)
                is_branch = True
                branch_true = False if used_to_be_true else self.evaluate(stm.parsed[-1])
                used_to_be_true = True if used_to_be_true else  branch_true
                end, res = self.run(stms, index + 1, base_indent + 1, not branch_true)
                i = end
                results.extend(res)
                continue
            elif stm.s_type == 'else':
                if not is_branch:
                    raise SyntaxError(stm)
                end, res = self.run(stms, index + 1, base_indent + 1, used_to_be_true)
                i = end
                results.extend(res)
                continue
            else:
                raise RuntimeError('Unknow type ' + str(stm))
            i += 1
        return i, results

    def evaluate(self, tpv: tpp.TPVariable, token=None):
        print('eval', tpv)
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
    sr = ScriptRunner(dict(vars=[1,2,3,5]))
    # print(tp.parse()[0])
    res = sr.run(tp.parse()[0], 0)
    print('\n'.join(res))
    # for stm, indent in tp.parse()[0]:
    #     stm = stm.parsed
    #     print(stm)
    #     print(sr.__parser__(stm[0], stm[-1]))

    # tpv = tpp.TPVariable(256, 'test', [None, ['len', [None, 'c']]])
    # s = ScriptRunner({'c': [1,2,34]})
    # print(s.evaluate(tpv))
