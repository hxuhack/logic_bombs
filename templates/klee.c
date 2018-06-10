int main(int argc, char** argv) {
    {%
        for {<type>}, {<var>}, {<size>} in {<vp>}:
            if {<type>} == {<"char*">}:
                {<size>} = {<size>} + {<1d>}
                char {<var>}[{<size>}];
            else:
                {<type>} {<var>};

        for {<type>}, {<var>}, {<size>} in {<vp>}:
            klee_make_symbolic(&{<var>}, sizeof({<var>}), "{<var>}");
            if {<type>} == {<"char*">}:
                klee_assume({<var>}[{<size>}]=='\0');

        return logic_bomb({<params>});
    %}
}
