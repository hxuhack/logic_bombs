#
#This is the CMAKE FILE for building LOGIC BOMBS
#

cmake_minimum_required(VERSION 2.8)
PROJECT(logic_bombs)

INCLUDE_DIRECTORIES(include)

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

ADD_EXECUTABLE(bombs/symarray
		../src/utils/utils.c 
		../src/symarray.c)

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

#####Symbolic Array########
#####Symbolic Jump########
ADD_EXECUTABLE(bombs/input_indijump
		../src/utils/utils.c 
		../src/input_indijump.c)

ADD_EXECUTABLE(bombs/input_indijump_array
		../src/utils/utils.c 
		../src/input_indijump_array.c)

#####Floating-point Numbers########

ADD_EXECUTABLE(bombs/input_float  
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/input_float.c)

ADD_EXECUTABLE(bombs/input_float2  
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/input_float2.c)

#####External Function Calls########
ADD_EXECUTABLE(bombs/input_strcmp  
		../src/utils/utils.c 
		../src/input_strcmp.c)

#####Crypto Functions########
ADD_EXECUTABLE(bombs/input_sha  
		../src/utils/sha1.c 
		../src/utils/crypto_utils.c 
		../src/utils/utils.c 
		../src/input_sha.c)


#####Exceptions########
ADD_EXECUTABLE(bombs/input_exception
		../src/utils/utils.c 
		../src/input_exception.cpp)

ADD_EXECUTABLE(bombs/file_exception
		../src/utils/utils.c 
		../src/file_exception.cpp)

#TARGET_LINK_LIBRARIES(bombs/time_sha m)
