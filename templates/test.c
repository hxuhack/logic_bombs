int main() {
    {%
        for {<index>}, {<var>} in {<enumerate(vars)>}:
            printf("%d", {<index>});
            if {<index>} >= {<4d>}:
                hhh {<var>}
            elif {<index>} == {<3d>} and {<var>} == {<"test">}:
                ttt {<var>}
            else:
                ppp {<var>}
        
        {<index>} = {<3d>}
        while {<len(vars)>} > {<index>}:
            www {<index>}
    %}
}