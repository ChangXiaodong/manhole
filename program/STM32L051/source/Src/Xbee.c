#include "common.h"

//#define SRC_64_ADDRESS 0x0013A20040B59E05
#define DES_64_ADDRESS 0x0013A20040B59E03

static void XbeeSend(uint32 src_address,uint8 data_type,uint16 data);

Xbee_interface Xbee;
uint8 xbee_packet[25];
uint8 xbee_receive[20];
void Init_Xbee()
{
    Init_XBEE_GPIO();
    Xbee.send = XbeeSend;
    Xbee.values.des_address = DES_64_ADDRESS;
    //Xbee.values.src_address = SRC_64_ADDRESS;
}
void XbeeUSARTSend(uint8* data,uint16 size)
{
    uint16 i=0;
    for(i=0;i<size;i++)
    {
        USART_SendData(&huart1,*data++);
        delay_ms(1);
    }
}

uint8 creatXbeePacket(uint32 src_address,uint8 data_type,uint16 data)
{
    uint8 index = 0;
    uint8 check_sum = 0;
    
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
    xbee_packet[index++] = (uint32)src_address>>24;
    xbee_packet[index++] = (uint32)src_address>>16;
    xbee_packet[index++] = (uint32)src_address>>8;
    xbee_packet[index++] = (uint32)src_address;
    xbee_packet[index++] = data_type;
    xbee_packet[index++] = data>>8;
    xbee_packet[index++] = data;
    
    for(uint8 i=3;i<index;i++)
    {
        check_sum+=xbee_packet[i];
    }

    xbee_packet[index++] = 0xFF - check_sum;
    
    return index;
}
    
static void XbeeSend(uint32 src_address,uint8 data_type,uint16 data)
{
    uint8 size = 0;
    Xbee.values.ack = 0;
    memset(xbee_receive, 0, ( size_t )sizeof(xbee_receive));
    size = creatXbeePacket(src_address,data_type,data);
    XbeeUSARTSend(xbee_packet,size);
}
    