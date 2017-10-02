int main() {
    {%
        for {<type>}, {<var>} in {<vp>}:
            {<type>} {<var>};

        for {<var>} in {<vars>}:
            klee_make_symbolic(&{<var>}, sizeof({<var>}), "{<var>}");

        return sym_checker({<params>});
    %}
}
