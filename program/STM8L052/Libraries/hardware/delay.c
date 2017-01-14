#include "common.h"



inline void delay_us(uint16 n)
{
    TIM2->CNTRH = 0;
    TIM2->CNTRL = 0;
    TIM2_Cmd(ENABLE);
    while((TIM2->CNTRH << 8|TIM2->CNTRL)<n);
    TIM2_Cmd(DISABLE);
}
inline void delay_ms(uint16 time)
{
    uint16 i=0;
    for(i=0;i<time;i++)
    {
        delay_us(1000);
    }
    
}

inline void delay_us_T5(uint16 n)
{
    TIM5->CNTRH = 0;
    TIM5->CNTRL = 0;
    TIM5_Cmd(ENABLE);
    while((TIM5->CNTRH << 8|TIM5->CNTRL)<n);
    TIM5_Cmd(DISABLE);
}

inline void delay_ms_T5(uint16 time)
{
    uint16 i=time/10;
    for(;i>0;i--)
    {
        delay_us_T5(10000);
    }
    delay_us_T5(time%10);
}
