#
#This is the CMAKE FILE for building LOGIC BOMBS
#

cmake_minimum_required(VERSION 2.8)
PROJECT(logic_bombs)

INCLUDE_DIRECTORIES(include)

file(MAKE_DIRECTORY build/bombs)

ADD_EXECUTABLE(bombs/input_strcmp  
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/input_strcmp.c)

ADD_EXECUTABLE(bombs/input_sha  
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/input_sha.c)

#TARGET_LINK_LIBRARIES(bombs/input_sha m)

ADD_EXECUTABLE(bombs/time 
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/time.c)

ADD_EXECUTABLE(bombs/website 
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/website.c)

ADD_EXECUTABLE(bombs/ping
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/ping.c)

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
