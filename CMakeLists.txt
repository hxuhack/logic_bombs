#
#This is the CMAKE FILE for building LOGIC BOMBS
#

cmake_minimum_required(VERSION 2.8)
PROJECT(logic_bombs)

INCLUDE_DIRECTORIES(include)
#set (CMAKE_CXX_FLAGS "-m32")

file(MAKE_DIRECTORY build/bombs)

#####Contextual Symbolic Variables########
ADD_EXECUTABLE(bombs/symvar_time 
		../src/utils/utils.c 
		../src/symvar_time.c)

ADD_EXECUTABLE(bombs/symvar_web 
		../src/utils/utils.c 
		../src/symvar_web.c)

ADD_EXECUTABLE(bombs/symvar_ping
		../src/utils/utils.c 
		../src/symvar_ping.c)

ADD_EXECUTABLE(bombs/symvar_cpu 
		../src/utils/utils.c 
		../src/symvar_cpu.c)

ADD_EXECUTABLE(bombs/symvar_syscall 
		../src/utils/utils.c 
		../src/symvar_syscall.c)

ADD_EXECUTABLE(bombs/symvar_vm 
		../src/utils/utils.c 
		../src/symvar_vm.c)

#####Covert Symbolic Propagations########

ADD_EXECUTABLE(bombs/covpro_stack  
		../src/utils/utils.c 
		../src/covpro_stack.c)

ADD_EXECUTABLE(bombs/covpro_file  
		../src/utils/utils.c 
		../src/covpro_file.c)

ADD_EXECUTABLE(bombs/covpro_syscall  
		../src/utils/utils.c 
		../src/covpro_syscall.c)

#####Parallel Programs########

ADD_EXECUTABLE(bombs/paraprog_fork
		../src/utils/utils.c 
		../src/paraprog_fork.c)

ADD_EXECUTABLE(bombs/paraprog_pthread 
		../src/utils/utils.c 
		../src/paraprog_pthread.c)
TARGET_LINK_LIBRARIES(bombs/paraprog_pthread pthread)

ADD_EXECUTABLE(bombs/paraprog_socket 
		../src/utils/utils.c 
		../src/paraprog_socket.c)
#####Symbolic Array########

ADD_EXECUTABLE(bombs/symarray_l1
		../src/utils/utils.c 
		../src/symarray_l1.c)

ADD_EXECUTABLE(bombs/symarray_l2
		../src/utils/utils.c 
		../src/symarray_l2.c)

#####Contextual Symbolic Value########

ADD_EXECUTABLE(bombs/symval_file
		../src/utils/utils.c 
		../src/symval_file.c)

ADD_EXECUTABLE(bombs/symval_syscall
		../src/utils/utils.c 
		../src/symval_syscall.c)
#####Symbolic Jump########

ADD_EXECUTABLE(bombs/symjmp
		../src/utils/utils.c 
		../src/symjmp.c)

ADD_EXECUTABLE(bombs/symjmp_array
		../src/utils/utils.c 
		../src/symjmp_array.c)

#####Floating-point Numbers########

ADD_EXECUTABLE(bombs/floatpoint_1  
		../src/utils/utils.c 
		../src/floatpoint_1.c)

ADD_EXECUTABLE(bombs/floatpoint_2  
		../src/utils/utils.c 
		../src/floatpoint_2.c)

#####External Function Calls########
ADD_EXECUTABLE(bombs/extfun_pow
		../src/utils/utils.c 
		../src/extfun_pow.c)
TARGET_LINK_LIBRARIES(bombs/extfun_pow m)

ADD_EXECUTABLE(bombs/extfun_rand
		../src/utils/utils.c 
		../src/extfun_rand.c)

ADD_EXECUTABLE(bombs/extfun_sin
		../src/utils/utils.c 
		../src/extfun_sin.c)
TARGET_LINK_LIBRARIES(bombs/extfun_sin m)

#####Crypto Functions########
ADD_EXECUTABLE(bombs/crypto_sha  
		../src/utils/sha1.c 
		../src/utils/crypto_utils.c 
		../src/utils/utils.c 
		../src/crypto_sha.c)

ADD_EXECUTABLE(bombs/crypto_aes  
		../src/utils/aes.c 
		../src/utils/utils.c 
		../src/crypto_aes.c)

#####Exceptions########
ADD_EXECUTABLE(bombs/excp_1
		../src/utils/utils.c 
		../src/excp_1.cpp)

ADD_EXECUTABLE(bombs/excp_file  
		../src/utils/utils.c 
		../src/excp_file.cpp)

ADD_EXECUTABLE(bombs/excp_div0  
		../src/utils/utils.c 
		../src/excp_div0.cpp)
