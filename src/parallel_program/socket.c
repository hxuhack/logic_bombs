/*
TOY:
*/
#include "utils.h"
#include <unistd.h> 
#include "a_tester.h"

int server(){
    int server_sockfd,client_sockfd;  
    int server_len,client_len;  
    struct sockaddr_in server_address;  
    struct sockaddr_in client_address;  
    int i,btye;  
    char char_recv,char_send;  
      
    server_address.sin_family = AF_INET;  
    server_address.sin_addr.s_addr = inet_addr("127.0.0.1");  
    server_address.sin_port = 8080;  
    server_len = sizeof(server_address);  
      
    server_sockfd = socket(AF_INET,SOCK_STREAM,0);  
      
    bind(server_sockfd,(struct sockaddr *)&server_address,server_len);  
      
    listen(server_sockfd,5);  
    printf("server waiting for connect\n");  
      
    client_len = sizeof(client_address);  
    client_sockfd = accept(server_sockfd,(struct sockaddr *)&client_address,(socklen_t *)&client_len);  
      
    if(btye = recv(client_sockfd,&char_recv,1,0) == -1)  
    {  
        perror("recv");  
        exit(EXIT_FAILURE);  
    }  
    printf("receive from client is %c\n",char_recv);  

    char_send = char_recv;  
    if(btye = send(client_sockfd,&char_send,1,0) == -1)  
    {  
        perror("send");  
        exit(EXIT_FAILURE);  
    }  
  
    shutdown(client_sockfd,2);  
    shutdown(server_sockfd,2);   
}

int client_send(char char_send){
    printf("client start\n");  
    int sockfd;  
    int len;  
    struct sockaddr_in address;  
    int result;  
    int i,byte;  
    char char_recv;  
    if((sockfd = socket(AF_INET,SOCK_STREAM,0)) == -1)  
    {  
        perror("socket");  
        exit(EXIT_FAILURE);  
    }  
    address.sin_family = AF_INET;  
    address.sin_addr.s_addr = inet_addr("127.0.0.1");  
    address.sin_port = 8080;  
    len = sizeof(address);  
    if((result = connect(sockfd,(struct sockaddr *)&address,len)) == -1)  
    {  
        perror("connect");  
        exit(EXIT_FAILURE);  
    }  
  
    if(byte = send(sockfd,&char_send,1,0) == -1)  
    {  
        perror("send");  
        exit(EXIT_FAILURE);  
    }  
    if(byte = recv(sockfd,&char_recv,1,0) == -1)  
    {  
        perror("recv");  
        exit(EXIT_FAILURE);  
    }  
    printf("receive from server %c\n",char_recv);  
    close(sockfd);  
    return atoi(char_recv);
}

// {"s":{"length": 16}}
int sym_checker(char* s) {
    int pid1,pid2,i=0;
    if((pid1=fork())==-1)
	return -1;
    if(pid1 == 0){
        server();
    } else{
        if((pid2=fork())==-1)
	    return -1;
        if(pid2 == 0){
            sleep(1);
            i=client_send(s[0]); 
            printf("i=%d\n",i);
    	    if(i==7){
                return BOMB_ENDING;
    	    }else{
                return NORMAL_ENDING;
    	    }
        }
    }
}
