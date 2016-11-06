#
#This is the CMAKE FILE for building LOGIC BOMBS
#

cmake_minimum_required(VERSION 2.8)
PROJECT(logic_bombs)

INCLUDE_DIRECTORIES(include)

file(MAKE_DIRECTORY build/bombs)

set(CMAKE_EXE_LINKER_FLAGS "-lm")

ADD_EXECUTABLE(bombs/pure_sha  
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/pure_sha.c)

ADD_EXECUTABLE(bombs/pure_time 
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/pure_time.c)

ADD_EXECUTABLE(bombs/time_sha  
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/time_sha.c)




