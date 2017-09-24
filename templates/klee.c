int main() {
    {<defs>}
    {%
        for {<var>} in {<vars>}:
            klee_make_symbolic(&{<var>}, sizeof({<var>}), "{<var>}");

        for {<var>},  in {<enumerate(vars)>}

        for {<exp>} in {<exceptions>}:
            klee_assume({<exp>});
    %}
    sym_checker({<params>});
}
