#include "common.h"
inline void delay_ms(uint16 time)
{
    uint16 i=time/10;
    for(;i>0;i--)
    {
        delay_us(10000);
    }
    delay_us(time%10);
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
