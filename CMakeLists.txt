#
#This is the CMAKE FILE for building LOGIC BOMBS
#

cmake_minimum_required(VERSION 2.8)
PROJECT(logic_bombs)

INCLUDE_DIRECTORIES(include)

set(CMAKE_EXE_LINKER_FLAGS "-lm")

#MESSAGE(STATUS, "Building time_bomb")
ADD_EXECUTABLE(time_bomb ../src/simple_time.c)

ADD_EXECUTABLE(sha_bomb 
		../src/sha1.c
		../src/sha_bomb.c)




