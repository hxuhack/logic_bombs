#
#This is the CMAKE FILE for building LOGIC BOMBS
#

cmake_minimum_required(VERSION 2.8)
PROJECT(logic_bombs)

INCLUDE_DIRECTORIES(include)

file(MAKE_DIRECTORY build/bombs)


ADD_EXECUTABLE(bombs/pure_sha  
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/pure_sha.c)

TARGET_LINK_LIBRARIES(bombs/pure_sha m)

ADD_EXECUTABLE(bombs/pure_time 
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/pure_time.c)

ADD_EXECUTABLE(bombs/pure_net 
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/pure_net.c)

ADD_EXECUTABLE(bombs/time_sha  
		../src/utils/sha1.c 
		../src/utils/utils.c 
		../src/time_sha.c)

TARGET_LINK_LIBRARIES(bombs/time_sha m)
