#include "common.h"
uint16 ad_test = 0;

void main()
{

    disableInterrupts();
    Init_System(); 
    enableInterrupts();
    
    while(1)
    {
        OS.executeTask();    
    }
}

