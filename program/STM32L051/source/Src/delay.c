#include "common.h"
#define SystemCoreClock 8000000

void Init_Delay()
{
    SysTick_Config(0);
}
void delay_ms(uint32_t ms) 
{
    uint32_t temp;
    Init_Delay();
    SysTick->LOAD =    (SystemCoreClock/8000)*ms-1;     
    SysTick->VAL   =     0;                  
    SysTick->CTRL  |=  (1<<0);  
    do
    {
        temp=SysTick->CTRL;
    }
    while(temp&0x01&&!(temp&(1<<16)));
    
    SysTick->CTRL =0;   
}

void delay_us(uint32_t us) 
{
    uint32_t temp;
    SysTick->LOAD =    us-1;     
    SysTick->VAL   =     0;                  
    SysTick->CTRL  |=  (1<<0);   
    do
    {
        temp=SysTick->CTRL;
    }
    while(temp&0x01&&!(temp&(1<<16)));
    
    SysTick->CTRL =0;   
}