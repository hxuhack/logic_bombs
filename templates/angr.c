int main(int argc, char** argv) {
    {%
        for {<type>}, {<var>} in {<vp>}:
            {<type>} {<var>};

        for {<index>}, {<var>} in {<enumerate(vars)>}:
            {<index>} = {<index>} + {<1d>}
            {<var>} \= atoi(argv[{<index>}]);

        return sym_checker({<params>});
    %}
}
