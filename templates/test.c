int main() {
    {%
        for {<index>}, {<var>} in {<enumerate(vars)>}:
            if {<index>} >= {<2d>}:
                printf("%d", {<index>});
            elif {<index>} == {<1d>}:
                scanf("%d", &test{<var>});
            else:
                {<index>} = {<5d>}
                NULL; // {<index>}
    %}
}



for {<index>}, {<var>} in {<enumerate(vars)>}:
            if {<index>} >= {<2d>}:
                hhh {<var>}
            elif {<index>} == {<3d>} and {<var>} == {<"test">}:
                ttt {<var>}
            else:
                ppp {<var>}