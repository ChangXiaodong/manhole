#ifndef __DELAY_H
#define __DELAY_H

extern inline void delay_ms(uint16 time);
extern inline void delay_ms_T5(uint16 time);
extern inline void delay_us(uint16 n);
extern inline void delay_us_T5(uint16 n);
#define RESET_TIME3 TIM3->CNTRH = 0;TIM3->CNTRL = 0;TIM3->CR1 |= TIM_CR1_CEN;
#define GET_TIME3 (TIM3->CNTRH << 8|TIM3->CNTRL)  //(n us)less than 65 ms

#define delay_1us nop();
//#define delay_1us nop();nop();nop();nop();nop();nop();nop();nop();nop();nop();nop()
#define delay_5us   {for(uint16 i=0;i<10;i++);}
#define delay_10us  {for(uint16 i=0;i<20;i++);}
#define delay_20us  {for(uint16 i=0;i<40;i++);}
#define delay_50us  {for(uint16 i=0;i<110;i++);}
#define delay_100us {for(uint16 i=0;i<220;i++);}
#define delay_200us {for(uint16 i=0;i<440;i++);}
#define delay_500us {for(uint16 i=0;i<1000;i++);}
#define delay_1ms   {{for(uint16 i=0;i<2300;i++);}}

#endif