int main(int argc, char** argv) {
    {<defs>}
    {%
        for {<var>} in {<vars>}:
            {<var>} = atoi(argv[1]);
    %}
    sym_checker({<params>});
}
