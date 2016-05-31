#include "common.h"
uint8 data[]={1,2,3,4,5,6,7,8,9};

void main(void)
{
    DISABLE_INTERRUPTS;
    Init_System();
    ENABLE_INTERRUPTS;
    
    while (1)
    {
        OS.executeTask();
    }
}