#include "common.h"
static void sendByCSMA();
static uint8 ifPacketValid(uint8* data);
static void receiveDataackCallback(uint8* data);
static void receiveDataCallback(uint8* data);
DataPacketStruct DataPacket;
DataPacketStruct DataACKPacket;
ProtocolStruct Protocol;
const struct Link_interface Link = 
{
    sendByCSMA,
    receiveDataCallback,
    receiveDataackCallback,
    ifPacketValid,
};

static void creatSendPacket(uint8* data, DataPacketStruct Packet)
{
    *data++ = Packet.des_address >> 8;
    *data++ = Packet.des_address;
    *data++ = Packet.src_address >> 8;
    *data++ = Packet.src_address;
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

static void CSMABackOff()
{
    //delay_ms_T5(1000);
}

static void receiveDataackCallback(uint8* data)
{
    //处理返回命令 （未完成）
}

static void papredDataACKPacket(uint8* rxdata,uint8* packet_data)
{
    DataACKPacket.des_address = *(rxdata+2)<<8|*(rxdata+3);
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

static uint8 ifPacketValid(uint8* data)
{
#define VALID     1
#define INVALID   0
    
    uint16 address = 0;
    address = *data<<8|*(data+1);
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

static uint8 receivedACK()
{
#define SUCCESS 1
#define FAILED  0
    while((Protocol.ack_received == 0)&&(Protocol.send_failed == 0));
    if(Protocol.ack_received)
    {
        
        return SUCCESS;
    }   
    else
    {
        return FAILED;
    }   
}
static bool isChannelFree(int16_t threshold)
{
    return Radio.getRssi() < threshold;
}

//unfinished
static void systemSleep()
{

}

void sendByCSMA()
{

}

