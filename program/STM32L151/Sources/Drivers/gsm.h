#ifndef __GSM_H
#define __GSM_H

#define GPRS_UART_RX_ENABLE TRUE
#define GPRS_RX_BUFFER_SIZE  150

extern void Init_GPRS();


typedef struct{
    uint8_t receive[GPRS_RX_BUFFER_SIZE];
    uint8_t receive_count;
    uint8_t pakcet_finished;
 
    void  ( *PowerOn )();
    void  (*Send) (uint32_t address,uint8_t data_type, uint16_t data);
}GPRS_s;
extern GPRS_s GPRS;

#endif