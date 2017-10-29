# Project Overview
This project consists of a set of small programs with logic bombs.  The logic bomb can be triggered when certain conditions are met.  
To find out more details, please visit our [wiki](https://github.com/hxuhack/logic_bombs/wiki).

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
