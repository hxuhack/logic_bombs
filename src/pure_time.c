#include "utils.h"

int main(){
    long v1 = GetSecSince1970();
    if(v1 == 2524608000){ //Jan 1st, 2050, 00:00::00
       Bomb();
    }else{
       Foobar();
    }
}
