int main(int argc, char** argv) {
    {%
        for {<type>}, {<var>} in {<vp>}:
            {<type>} {<var>};

        {<index>} = {<0d>}
        for {<type>}, {<var>} in {<vp>}:
            {<index>} = {<index>} + {<1d>}
            if {<str(type)>} == {<"char**">}:
                {<var>} = argv;
            elif {<str(type)>} == {<"char*">}:
                {<var>} = argv[{<index>}];
            elif {<str(type)>} == {<"float">}:
                {<var>} \= atoi(argv[{<index>}]);

        return sym_checker({<params>});
    %}
}
