#include "common.h"

static uint8_t  fac_us=0;
static uint16_t fac_ms=0;	

void Init_Delay()	 
{
    SysTick_CLKSourceConfig(SysTick_CLKSource_HCLK_Div8);	
    fac_us=SystemCoreClock/8000000;
    fac_ms=(uint16_t)fac_us*1000;
}

void delay_us(uint32_t nus)
{		
    uint32_t temp;	    	 
    SysTick->LOAD=nus*fac_us;  		 
    SysTick->VAL=0x00;   
    SysTick->CTRL|=SysTick_CTRL_ENABLE_Msk; 
    do
    {
        temp=SysTick->CTRL;
    }
    while(temp&0x01&&!(temp&(1<<16)));
    SysTick->CTRL&=~SysTick_CTRL_ENABLE_Msk;
    SysTick->VAL =0X00;   
}

void delay_ms(uint16_t nms)
{	 		  	  
    uint32_t temp;		   
    SysTick->LOAD=(uint32_t)nms*fac_ms;
    SysTick->VAL =0x00;    
    SysTick->CTRL|=SysTick_CTRL_ENABLE_Msk ;
    do
    {
        temp=SysTick->CTRL;
    }
    while(temp&0x01&&!(temp&(1<<16))); 
    SysTick->CTRL&=~SysTick_CTRL_ENABLE_Msk;
    SysTick->VAL =0X00;	  	    
}

void delay_s(uint8_t ns)
{
    for(uint8_t i=0;i<ns;i++)
    {
        delay_ms(1000);
    }
}

void delay_1us()
{
    for(uint8_t i=0;i<3;i++)
    {
        __ASM("nop");
    }
}

void delay_10us()
{
    delay_1us();
    delay_1us();
    delay_1us();
    delay_1us();
    delay_1us();
    delay_1us();
    delay_1us();
    delay_1us();
    delay_1us();
    delay_1us();   
}

void delay_1ms()
{
    for(uint16_t i=0;i<4600;i++)
    {
        __ASM("nop");
    }
}
