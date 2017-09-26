import os
import re
import template_parser as tpp


allowed_funcs = ['len', 'enumerate', 'range']


class ScriptRunner:
    def __init__(self, allowed_funcs: list):
        self.allowed_funcs = allowed_funcs
        self.scope = []

    def run(self, stms: list, index=0, scope=None):
        if scope:
            self.scope = scope

        # Stop iteration
        if index == len(stms):
            return ''



