#include "common.h"
uint16 time = 0;
//#define TX
uint8 semd_test[4]={1,2,3,4};
uint8 rx_once = 0;

void main()
{

    disableInterrupts();
    Init_System();
    enableInterrupts();
    
    while(1)
    {
#ifdef TX
        Radio.Send(semd_test,4);
        while(Radio.sendNotDone());
#else
        if(rx_once)
        {
            rx_once = 0;
            Radio.setRxState(RX_TIMEOUT_VALUE);
        }
        
#endif
        delay_ms(500);
        
    }
}

