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

    def __get_var__(self, key: str):
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

    def __parser__(self, stm: str, token_tables: dict):
        cp_table = copy(token_tables)
        for key in cp_table:
            # print("TKT", str([(key, str(cp_table[key])) for key in token_tables]))
            res = self.evaluate(cp_table[key])
            cp_table[key] = res
        return stm.format(**cp_table)

    def __step_out__(self, stms, i, base_indent):
        while i < len(stms):
            if stms[i][1] <= base_indent:
                break
            i += 1
        return i

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
        base_indent = stms[index][1] if expected_indent is None else expected_indent
        if ignore:
            i = 0
            for i in range(index, len(stms)):
                if stms[i][1] >= base_indent:
                    continue
            return i, []

        i = index
        while i < len(stms):
            # print(i)
            stm, indent = stms[i]
            # print(stm.stm, indent)

            if indent > base_indent:
                raise RuntimeError(stm.stm, 'with indent %d, but expect indent %d' % (indent, base_indent))
            elif indent < base_indent:
                break

            if stm.s_type not in ['if', 'else', 'elif']:
                is_branch = False

            if stm.s_type == 'str':
                print(self.__parser__(*stm.parsed))
                results.append(self.__parser__(*stm.parsed))
                i += 1
            elif stm.s_type == 'for':
                in_index = i
                if i == len(stms) - 1:
                    raise SyntaxError(stm.stm)
                tmp_iter = self.evaluate(stm.parsed[-1])
                for tmp in tmp_iter:
                    print('tmp', tmp)
                    self.variables.append({key: tmp[index] for index, key in enumerate(stm.parsed[1])})
                    results.extend(self.run(stms, i + 1, base_indent + 1)[1])
                    self.variables.pop(-1)
                i = self.__step_out__(stms, in_index + 1, base_indent)
            elif stm.s_type == 'while':
                in_index = i
                while self.evaluate(stm.parsed[-1]):
                    self.variables.append({})
                    results.extend(self.run(stms, i + 1, base_indent + 1)[1])
                    self.variables.pop(-1)
                i = self.__step_out__(stms, in_index + 1, base_indent)
            elif stm.s_type == 'exp':
                self.variables[-1][stm.parsed[1]] = eval(self.__parser__('='.join(stm.parsed[0].split('=')[1:]), stm.parsed[-1]))
                i += 1
            elif stm.s_type == 'if':
                in_index = i
                is_branch = True
                b_res = eval(self.__parser__(stm.parsed[0], stm.parsed[-1]))
                used_to_be_true, branch_true = [b_res, ] * 2
                if branch_true:
                    end, res = self.run(stms, i + 1, base_indent + 1, not branch_true)
                    results.extend(res)
                i = self.__step_out__(stms, in_index + 1, base_indent)
                print(i)
            elif stm.s_type == 'elif':
                in_index = i
                if not is_branch:
                    raise SyntaxError(stm)
                is_branch = True
                branch_true = False if used_to_be_true else eval(self.__parser__(stm.parsed[0], stm.parsed[-1]))
                used_to_be_true = True if used_to_be_true else  branch_true
                if branch_true:
                    end, res = self.run(stms, i + 1, base_indent + 1, not branch_true)
                    results.extend(res)
                i = self.__step_out__(stms, in_index + 1, base_indent)
            elif stm.s_type == 'else':
                in_index = i
                if not is_branch:
                    raise SyntaxError(stm)
                if not used_to_be_true:
                    end, res = self.run(stms, i + 1, base_indent + 1, used_to_be_true)
                    results.extend(res)
                i = self.__step_out__(stms, in_index + 1, base_indent)
                print(i)
            else:
                raise RuntimeError('Unknow type ' + str(stm))
        return i, results

    def evaluate(self, tpv: tpp.TPVariable, token=None):
        if token is None:
            token = tpv.token.call_stack
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

    res = sr.run(tp.parse()[0])
    print('\n==================================\n')
    res = '\n'.join(res[1])
    print(tp.replace([res, ]))
    # for stm, indent in tp.parse()[0]:
    #     stm = stm.parsed
    #     print(stm)
    #     print(sr.__parser__(stm[0], stm[-1]))

    # tpv = tpp.TPVariable(256, 'test', [None, ['len', [None, 'c']]])
    # s = ScriptRunner({'c': [1,2,34]})
    # print(s.evaluate(tpv))
