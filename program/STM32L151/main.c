#include "common.h"
uint8_t send = 0;
int main(void)
{
    DISABLE_INTERRUPTS;
    Init_Delay();
    Init_GPIO();
    Init_Radio();
    Init_Xbee();
    Init_XBEE_UART();
    Init_GPRS_UART();
    Init_GPRS();
    Init_Finished();
    
    ENABLE_INTERRUPTS;
    
#ifdef GPRS_EN
    DISABLE_DIO0;
    GPRS.PowerOn();
    ENABLE_DIO0;
    SX1276WriteBuffer( REG_LR_IRQFLAGS, RFLR_IRQFLAGS_RXDONE );
#endif
    
    while (1)
    {
        OS.executeTask();
//        if(send == 1)
//        {
//            send = 0;
//            setURL(0x00000001,0x01,119);
//        }
//        else if(send == 2)
//        {
//            send = 0;
//            getRequest();
//        }
    }
}

