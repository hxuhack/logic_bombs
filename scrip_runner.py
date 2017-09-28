import os
import re
import template_parser as tpp


allowed_funcs = ['len', 'enumerate', 'range']


class ScriptRunner:
    def __init__(self, init_values: dict, allowed_funcs: list):
        self.allowed_funcs = allowed_funcs
        self.scope = []
        self.inits = init_values

    def run(self, stms: list, index=0, scope=None):
        if scope:
            self.scope = scope

        # Stop iteration
        if index == len(stms):
            return ''

    def evaluate(self, tpv: tpp.TPVariable, v_table: dict):
        pass


