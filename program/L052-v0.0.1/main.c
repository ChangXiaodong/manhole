#include "common.h"
uint16 time = 0;
//#define TX
uint8 semd_test[4]={1,2,3,4};


void main()
{

    disableInterrupts();
    Init_System();
    enableInterrupts();
    
    while(1)
    {
//        Radio.Send(semd_test,4);
//        while(Radio.sendNotDone());
        delay_ms(100);
        
    }
}

