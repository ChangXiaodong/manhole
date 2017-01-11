#include "common.h"

//#define SRC_64_ADDRESS 0x0013A20040B59E05
#define DES_64_ADDRESS 0x0013A20040B59E03

static void XbeeSend(uint32_t src_address,uint8_t data_type,uint16_t data);

Xbee_interface Xbee;
uint8_t xbee_packet[25];
uint8_t xbee_receive[20];
void Init_Xbee()
{
    Init_XBEE_GPIO();
    Xbee.send = XbeeSend;
    Xbee.values.des_address = DES_64_ADDRESS;
    //Xbee.values.src_address = SRC_64_ADDRESS;
}
void XbeeUSARTSend(uint8_t* data,uint16_t size)
{
    uint16_t i=0;
    for(i=0;i<size;i++)
    {
        USART_SendData(USART1,*data++);
        while (USART_GetFlagStatus(USART1, USART_FLAG_TC) == RESET);
    }
}

uint8_t creatXbeePacket(uint32_t src_address,uint8_t data_type,uint16_t data)
{
    uint8_t index = 0;
    uint8_t check_sum = 0;
    
    xbee_packet[index++] = 0x7E;  //start delimiter
    xbee_packet[index++] = 0x00;
    xbee_packet[index++] = 0x15;  //length
    xbee_packet[index++] = 0x10;  //frame type
    xbee_packet[index++] = 0x01;  //freme ID
    xbee_packet[index++] = Xbee.values.des_address>>56;
    xbee_packet[index++] = Xbee.values.des_address>>48;
    xbee_packet[index++] = Xbee.values.des_address>>40;
    xbee_packet[index++] = Xbee.values.des_address>>32;
    xbee_packet[index++] = Xbee.values.des_address>>24;
    xbee_packet[index++] = Xbee.values.des_address>>16;
    xbee_packet[index++] = Xbee.values.des_address>>8;
    xbee_packet[index++] = Xbee.values.des_address;  //64-bit address
    xbee_packet[index++] = 0xFF;
    xbee_packet[index++] = 0xFE;  //16-bit address
    xbee_packet[index++] = 0x00;  //broadcast radius
    xbee_packet[index++] = 0x00;  //options
    xbee_packet[index++] = (uint32_t)src_address>>24;
    xbee_packet[index++] = (uint32_t)src_address>>16;
    xbee_packet[index++] = (uint32_t)src_address>>8;
    xbee_packet[index++] = (uint32_t)src_address;
    xbee_packet[index++] = data_type;
    xbee_packet[index++] = data>>8;
    xbee_packet[index++] = data;
     
    
    for(uint8_t i=3;i<index;i++)
    {
        check_sum+=xbee_packet[i];
    }

    xbee_packet[index++] = 0xFF - check_sum;
    
    return index;
}
    
static void XbeeSend(uint32_t src_address,uint8_t data_type,uint16_t data)
{
    uint8_t size = 0;
    Xbee.values.ack = 0;
    memset(xbee_receive, 0, ( size_t )sizeof(xbee_receive));
    size = creatXbeePacket(src_address,data_type,data);
    XbeeUSARTSend(xbee_packet,size);
}
    