#ifndef __DELAY_H
#define __DELAY_H

extern void Init_Delay();
extern void delay_us(uint32_t nus);
extern void delay_ms(uint16_t nms);
extern void delay_1us();
extern void delay_1ms();
extern void delay_10us();
extern void delay_s(uint8_t ns);
#endif