#include "common.h"
static void sendByCSMA();
static uint8 ifPacketValid(uint8* data);
static void receiveDataCallback(uint8* data);
DataPacketStruct DataPacket;
DataPacketStruct DataACKPacket;
ProtocolStruct Protocol;
const struct Link_interface Link = 
{
    sendByCSMA,
    receiveDataCallback,
    ifPacketValid,
};

static void creatSendPacket(uint8* data, DataPacketStruct Packet)
{
    *data++ = (uint32)Packet.des_address >> 24;
    *data++ = (uint32)Packet.des_address >> 16;
    *data++ = (uint32)Packet.des_address >> 8;
    *data++ = (uint32)Packet.des_address;
    *data++ = (uint32)Packet.src_address >> 24;
    *data++ = (uint32)Packet.src_address >> 16;
    *data++ = (uint32)Packet.src_address >> 8;
    *data++ = (uint32)Packet.src_address;
    *data++ = Packet.packet_type;
    *data = 0;
    *data = Packet.data_type << 4;
    *data++ |= Packet.data_cmd >> 8;
    *data++ = Packet.data_cmd;
    *data = Packet.data_type;
}

static void papredDataPacket(uint8* data)
{

}

static void papredDataACKPacket(uint8* rxdata,uint8* packet_data)
{
    DataACKPacket.des_address = (uint32)*(rxdata+4)<<24|(uint32)*(rxdata+5)<<16|
                                (uint32)*(rxdata+6)<<8 |(uint32)*(rxdata+7);
    DataACKPacket.src_address = SX1276.Settings.Address;
    DataACKPacket.packet_type = DATA_ACK_PACK;
    DataACKPacket.data_type = CMD_DATA;
    DataACKPacket.data_cmd = SX1276.Settings.sta_cmd;
    
    creatSendPacket(packet_data,DataACKPacket);
    
}

static void receiveDataCallback(uint8* data)
{
    uint8 data_ack_packet[DATA_PACKET_LENGTH];  
    LED1_TOGGLE;
    papredDataACKPacket(data,data_ack_packet);
    Radio.Send(data_ack_packet,sizeof(DataPacket)-1);
    while(Radio.sendNotDone());
    Radio.setRxState(RX_TIMEOUT_VALUE);
}
uint32 address = 0;
static uint8 ifPacketValid(uint8* data)
{
#define VALID     1
#define INVALID   0
    
    
    address = (uint32)*data<<24|(uint32)*(data+1)<<16|
              (uint32)*(data+2)<<8|(uint32)*(data+3);
    if((address == SX1276.Settings.Address)|
       (address == BROADCAST_ADDRESS))
    {
        return VALID;
    }   
    else
    {
        return INVALID;
    }
}


//unfinished
static void systemSleep()
{

}

void sendByCSMA()
{

}

