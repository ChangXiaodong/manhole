#ifndef __DELAY_H__
#define __DELAY_H__

#define delay_500us     delay_us(500);
#define delay_1ms       delay_ms(1);

extern void delay_ms(uint32_t ms);
extern void delay_us(uint32_t us);
extern void Init_Delay();
#endif