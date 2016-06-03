#ifndef __XBEE_H
#define __XBEE_H

#define XBEE_UART_RX_ENABLE  TRUE 

typedef struct {
    uint64_t  src_address;
    uint64_t  des_address;
    uint8_t   ack;
} Xbee_s;

typedef struct
{
    void (*send)(uint32_t src_address,uint8_t data_type,uint16_t data);
    Xbee_s values;
}Xbee_interface;



extern Xbee_interface Xbee;
extern uint8_t xbee_receive[20];
extern void Init_Xbee();
#endif