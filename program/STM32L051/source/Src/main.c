#include "common.h"

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