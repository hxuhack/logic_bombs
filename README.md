# A Dataset of Logic Bombs
## Project Overview
This project consists of a set of small programs with logic bombs.  The logic bomb can be triggered when certain conditions are met.  

## Structure
logic_bombs  
|--src: the source codes of logic bombs with C  
|--src_cpp: the source codes of logic bombs with C++  
|--scripts: batch evaluation of symbolic execution tools on the logic bombs  
 
## Usage
The project is for linux platform. To compiler the logic bombs, you have to install python3.4.  
```
pip3 install termcolor
python3 compile.py -a
```

## Details of the bombs
Below we list these programs and the conditions to trigger each bomb. 

| Type | Case  | Trigger Condition |
|---|---|---|
| Symbolic Variable Declaration | cpu_svd.c | the program runs on an Intel CPU |
|       			| vm_svd.c | the program runs on an virtual machine |
|       			| web_svd.c | if a remote website contains the string "trigger the bomb" |
|       			| time_svd.c | current time is after Jan 1st, 2050 |
|       			| syscall_ls_svd.c | the number of files under a current directory is 7 |
| Contextual Symbolic Value  	| file_csv.c | if stdin points to a file |
| 			  	| ping_csv.c | if stdin points to a live IP |
| 			  	| syscall_csv.c | if stdin is a Linux command |
| Covert Propagation  		| file_cp.c | data propagate via a file (expected stdin: 7) | 
| 		  		| stack_cp.c | data propagation via direct push/pop (expected stdin: 7) | 
| 		  		| echo_cp.c | data propagation via echo (expected stdin: 7) | 
| 		  		| echofile_cp.c | data propagation via echo and file (expected stdin: 0) | 
| 		  		| socket_cp.c | data propagation via socket (expected stdin: 0) | 
| 		  		| toy_eh_cp_cp.cpp | data propagation via exception handling (expected stdin: 0) | 
| 		  		| div0_eh_cp.cpp | raise an exceptions when divided by 0 (expected stdin: 0) | 
| 		  		| file_eh_cp.cpp | raise an exception when a file doesn't exist| 
| Symbolic Memory  		| l1array_sm.c | if stdin points to an array element (expected stdin: 7) |
| 		  		| l2array_sm.c | two arrays (expected stdin: 7) |
| 		  		| malloc_sm.c | allocate memory with malloc (expected stdin: 7)|
| 		  		| realloc_sm.c | allocate memory with realloc (expected stdin: 7)|
| 		  		| outofbound_sm.c | if stdin > array size (expected stdin: 7)|
| Parallel Program 		| pthread_pp.c | multi-thread program (expected stdin: 7)  |
| 		 		| fork_pp.c | multi-process program (expected stdin: 7)  |
| Floating-point Number  	| case1_fp.c  | condition: 1024 + x == 1024 && x>0  |
| 	       		  	| case2_fp.c  | condition: 1 + x == 2 && x != 1  |
| Symbolic Jump 		| jmp_sj.c | jump to an address related to stdin |
| 		 		| arrayjmp_sj.c | a more complex case with an array |
| Data Overflow 		| plus_do.c | a + 2147483640 < 0 && a > 0  |
| 			  	| multiply_do.c | 3 * a < 0 && a > 0 |
| External Function Call  	| rand_ef.c | rand()%100 == 7 |
| 			  	| pow_ef.c | pow(i, 2) == 49 |
| 			  	| sin_ef.c | sin(i * PI / 180) == 0.5 |
| 			  	| ln_ef.c | 1.94 < log(i) && log(i) < 1.95 |
| Crypto Function 		| sha_cf.c | if sha1(i) equals to a predefined value |
| 		 		| aes_cf.c | if aes(i, plaintext) equals to a ciphertext |
| Loop 				|   |   |


## Evaluation Scripts

## Add New Logic Bombs 

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

