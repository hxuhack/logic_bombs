#
#This is the CMAKE FILE for building LOGIC BOMBS
#

cmake_minimum_required(VERSION 2.8)
PROJECT(logic_bombs)

INCLUDE_DIRECTORIES(include)

file(MAKE_DIRECTORY build/bombs)

ADD_EXECUTABLE(bombs/symvar_time 
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/symvar_time.c)

ADD_EXECUTABLE(bombs/symvar_web 
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/symvar_web.c)

ADD_EXECUTABLE(bombs/symvar_ping
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/symvar_ping.c)

ADD_EXECUTABLE(bombs/symvar_cpu 
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/symvar_cpu.c)

ADD_EXECUTABLE(bombs/symvar_syscall 
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/symvar_syscall.c)

ADD_EXECUTABLE(bombs/symvar_vm 
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/symvar_vm.c)

ADD_EXECUTABLE(bombs/input_strcmp  
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/input_strcmp.c)

ADD_EXECUTABLE(bombs/input_float  
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/input_float.c)

ADD_EXECUTABLE(bombs/input_float2  
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/input_float2.c)

ADD_EXECUTABLE(bombs/input_sha  
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/input_sha.c)

#TARGET_LINK_LIBRARIES(bombs/input_sha m)

ADD_EXECUTABLE(bombs/input_indijump
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/input_indijump.c)

ADD_EXECUTABLE(bombs/input_indijump_array
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/input_indijump_array.c)

ADD_EXECUTABLE(bombs/input_exception
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/input_exception.cpp)

ADD_EXECUTABLE(bombs/file_exception
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/file_exception.cpp)

ADD_EXECUTABLE(bombs/time_sha  
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/time_sha.c)

TARGET_LINK_LIBRARIES(bombs/time_sha m)
