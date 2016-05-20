#ifndef __DELAY_H
#define __DELAY_H

extern inline void delay_ms(uint16 time);
extern inline void delay_50us();

#define RESET_TIM3 TIM3->CNTRH = 0;TIM3->CNTRL = 0;TIM3->CR1 |= TIM_CR1_CEN;
#define GET_TIME3 (TIM3->CNTRH << 8|TIM3->CNTRL)  //(n us)less than 65 ms

#define RESET_TIM2 TIM2->CNTRH = 0;TIM2->CNTRL = 0
#define GET_TIME2 (TIM2->CNTRH << 8|TIM2->CNTRL)
#define delay_us(n) {RESET_TIM2;\
                       TIM2_Cmd(ENABLE);\
                       while(GET_TIME2<n);\
                       TIM2_Cmd(DISABLE);\
                      }

#define delay_1us nop()
#define delay_5us nop();nop();nop();nop();nop();
#define delay_10us delay_5us;delay_5us;
#define delay_20us delay_10us;delay_10us;
#define delay_50us delay_20us;delay_20us;delay_10us;
#define delay_100us delay_50us;delay_50us;
#define delay_200us delay_100us;delay_100us;
#define delay_500us delay_200us;delay_200us;delay_100us;
#define delay_1ms delay_500us;delay_500us;

#endif