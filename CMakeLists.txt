#
#This is the CMAKE FILE for building LOGIC BOMBS
#

cmake_minimum_required(VERSION 2.8)
PROJECT(logic_bombs)

INCLUDE_DIRECTORIES(include)

file(MAKE_DIRECTORY build/bombs)


ADD_EXECUTABLE(bombs/sha  
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/sha.c)

TARGET_LINK_LIBRARIES(bombs/sha m)

ADD_EXECUTABLE(bombs/time 
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/time.c)

ADD_EXECUTABLE(bombs/website 
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/website.c)

ADD_EXECUTABLE(bombs/cpu 
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/cpu.c)

ADD_EXECUTABLE(bombs/sys 
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/sys.c)

ADD_EXECUTABLE(bombs/vm 
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/vm.c)

ADD_EXECUTABLE(bombs/jmp_indirect
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/jmp_indirect.c)

ADD_EXECUTABLE(bombs/jmp_array
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/jmp_array.c)

ADD_EXECUTABLE(bombs/exception_handling
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/exception_handling.cpp)

ADD_EXECUTABLE(bombs/exception_lib
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/exception_lib.cpp)

ADD_EXECUTABLE(bombs/time_sha  
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/time_sha.c)

TARGET_LINK_LIBRARIES(bombs/time_sha m)
