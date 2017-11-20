/*
*VM Bomb
*If the code is runming on an virtual machine, the bomb will be triggered.
*code reference https://github.com/JakenHerman
* VM status is used as symbolic variables.
*Evaluation:
--Triton: fail
--Angr:
--BAP:
*/

#include "utils.h"

int vm_score = 0;

void number_of_cores() {
    if(sysconf(_SC_NPROCESSORS_ONLN) <= 1){
        //check if number of processors is less than or equal to one.
        vm_score++;
    }
} 

void run_command(char *cmd, char *detphrase, int dp_length){
    #define BUFSIZE 128
    char buf[BUFSIZE];
    FILE *fp;

    if((fp = popen(cmd, "r")) == NULL){
        //printf("Error");
    }

    if(fgets(buf, BUFSIZE, fp) != NULL){
        char detection[(dp_length +1 )]; //one extra char for null terminator
        strncpy(detection, detphrase, dp_length);
        detection[dp_length] = '\0'; //place the null terminator

        if(strcmp(detphrase, detection) == 0){ //0 means detphrase = detection
            vm_score++; //increment the vm_score variable.
        }
    }

    if(pclose(fp)){
        //printf("Command not found or exited with error status \n");
    }
}

#include "a_tester.h"

int logic_bomb() {
    number_of_cores();
    //run the dmesg command and pipe to find hypervisor, 34 is how long string should be.
    run_command("dmesg |grep -i hypervisor", "[   0.000000 Hypervisor detected]", 34);
    //run dmidecode command and find system manufacturer, 6 is how long the string should be.
    run_command("sudo dmidecode -s system-manufacturer", "VMware", 6);
    /*If vm_score is less than 3, we are likely running on physical hardware*/
    if(vm_score < 3){
        //printf("No virtual machine detected\n");
        return NORMAL_ENDING;
    }
    else{
        //printf("Virtual Machine detected\n");
        return BOMB_ENDING;
    }
    return 0;
}
