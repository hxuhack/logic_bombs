# Project Overview
This project consists of a set of small programs with logic bombs.  The logic bomb can be triggered when certain conditions are met.  


## Usage
The project is for linux platform. To compiler the logic bombs, you have to install python3.4.  
```
python3 compile.py -a
```

## Details of the bombs
Below we list these programs and the conditions to trigger each bomb. 

| Type | Case  | Trigger Condition
|---|---|---|---|
| Symbolic Variable Declaration  | cpu_cvd | the program runs on an Intel CPU | |
|       | vm_svd | the program runs on an virtual machine | |
|       | web_svd | if a remote website contains the string "trigger the bomb" | |
|       | time_svd | current time is after Jan 1st, 2050 | |
|       | syscall_svd | the number of files under a current directory is > 2 | |
| Contextual Symbolic Value  |   |   |   |
| Covert Propagation  |   |   |   |
| Symbolic Memory  |   |   |   |
| Parallel Program |   |   |   |
| Floating-point Number  |   |   |   |
| Symbolic Jump |   |   |   |
| Data Overflow |   |   |   |
| External Function Call  |   |   |   |
| Crypto Function |   |   |   |
| Loop |   |   |   |

# Forrest Runner
## **NOTE**
Now we support a **Pythonic** grammar for template generation!!!

## Motivation

- Automatic run all test cases corresponding to user configure file.
- Makefile of Makefile
- Reduce repeated work for some common test settings.

## How to use

This core of this tool is the **config.py**, you can define a lot of rules for compiling, running and dependencies. This tool is intended for C program unit symbolic test, all test files should NOT contain main function. The main function should be generated from the templates.

## PTL (Pythonic Template Language)

### At a glance

PTL is a python-like script language to generate a readable file from template. Here is an simple example:

```c
// Template we used
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
```

```c
// After running
int main() {
NULL; // 5
scanf("%d", &test2);
printf("%d", 2);
printf("%d", 3);
}
```



## How to convert my program

As I mentioned above, to use this tool you may need do some changes to your codes. There are several principles to follow:

- Each file contains only one **test** function.
- Test function only have two return value with signed integer type.
- Return value should use pre-defined value in header file **a_tester.h**

Here is an example:

```C
// Original file
#include <stdio.h>

int sym_checker(int i) {
    int a[] = {1, 2, 3, 4, 5, 6};

    if (a[i] > 6) {
        a[i] = 1;
        return 1;
    }
    else {
        return 0;
    }

}

int main(int argc, char**argv) {
    int i = atoi(argv[1]);

    return check(i);
}
```

```c
// After altering
#include <stdio.h>
#include "a_tester.h"

int sym_checker(int i) {
    int a[] = {1, 2, 3, 4, 5, 6};

    if (a[i] > 6) {
        a[i] = 1;
        return BOMB_ENDING;
    }
    else {
        return NORMAL_ENDING;
    }
}
```

Here is another example require divide one file into two files:

```c
// Original file
#include <stdio.h>

int check(int a) {
    if (3 * a < 0 && a > 0)
        return 1;
    else if (a + b < 0 && a > 0)
        return 2;
    else
        return 0;
}

int main(int argc, char** argv) {
    int i = atoi(argv[1]);

    return check(i);
}
```

```c
// File 1
#include "a_tester.h"

int sym_checker(int a) {
    if (3 * a < 0 && a > 0)
        return BOMB_ENDING;
    else
        return NORMAL_ENDING;

```

```c
// File 2
#include "a_tester.h"

int sym_checker(int a) {
    int b = 2147483640;

    if (a + b < 0 && a > 0)
        return BOMB_ENDING;
    else
        return NORMAL_ENDING;
}
```

