#include "common.h"

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

