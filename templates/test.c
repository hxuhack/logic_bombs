int main() {
    {%
        for {<index>}, {<var>} in {<enumerate(vars)>}:
            if {<index>} >= {<2d>}:
                printf("%d", {<index>});
            elif {<index>} == {<1d>}:
                scanf("%d", &test{<var>});
                {<index>} = {<index>} + {<1d>}
                {<var>} \= {<index>};
            else:
                {<index>} = {<5d>}
                NULL; // {<index>}
    %}
}
