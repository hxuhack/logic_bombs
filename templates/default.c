int main(int argc, char** argv) {
    int rt_value;
    {%
        for {<type>}, {<var>}, {<size>} in {<vp>}:
            if {<str(type)>} != {<"char**">}:
                {<type>} {<var>};

        {<index>} = {<0d>}
        for {<type>}, {<var>}, {<size>} in {<vp>}:
            {<index>} = {<index>} + {<1d>}
            if {<str(type)>} == {<"char**">}:
                {<var>} \= argv;
            elif {<str(type)>} == {<"char*">}:
                {<var>} \= argv[{<index>}];
            elif {<str(type)>} == {<"float">}:
                {<var>} \= atof(argv[{<index>}]);
            elif {<str(type)>} == {<"int">}:
                {<var>} \= atoi(argv[{<index>}]);

        rt_value = logic_bomb({<params>});
    %}

    switch (rt_value) {
        case 0: printf("Normal ending\n"); break;
        case 1: printf("Bomb ending\n"); break;
    }
    return rt_value;
}
