#include "common.h"
uint16 time = 0;
//#define TX
uint8 semd_test[4]={1,2,3,4};
void main()
{
    disableInterrupts();
    Init_System();
    enableInterrupts();
    RF_SEELP();
    while(1)
    {
        
        halt();
        
//#ifdef TX 
//        tx_complete_flag = 0;
//        FUN_RF_SENDPACKET(semd_test,4);
//        while(tx_complete_flag!=1);
//        delay_ms(2000);
//        LED1_TOGGLE;
//#endif
    }
}