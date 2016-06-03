#include "common.h"
static void sendByCSMA();
static uint8_t ifPacketValid(uint8_t* data);
static void receiveDataCallback(uint8_t* data);
DataPacketStruct DataPacket;
DataPacketStruct DataACKPacket;
ProtocolStruct Protocol;
const struct Link_interface Link = 
{
    sendByCSMA,
    receiveDataCallback,
    ifPacketValid,
};

static void creatSendPacket(uint8_t* data, DataPacketStruct Packet)
{
    *data++ = (uint32_t)Packet.des_address >> 24;
    *data++ = (uint32_t)Packet.des_address >> 16;
    *data++ = (uint32_t)Packet.des_address >> 8;
    *data++ = (uint32_t)Packet.des_address;
    *data++ = (uint32_t)Packet.src_address >> 24;
    *data++ = (uint32_t)Packet.src_address >> 16;
    *data++ = (uint32_t)Packet.src_address >> 8;
    *data++ = (uint32_t)Packet.src_address;
    *data++ = Packet.packet_type;
    *data = 0;
    *data = Packet.data_type << 4;
    *data++ |= Packet.data_cmd >> 8;
    *data++ = Packet.data_cmd;
    *data = Packet.data_type;
}


static void papredDataACKPacket(uint8_t* rxdata,uint8_t* packet_data)
{
    DataACKPacket.des_address = (uint32_t)*(rxdata+4)<<24|(uint32_t)*(rxdata+5)<<16|
                                (uint32_t)*(rxdata+6)<<8 |(uint32_t)*(rxdata+7);
    DataACKPacket.src_address = SX1276.Settings.Address;
    DataACKPacket.packet_type = DATA_ACK_PACK;
    DataACKPacket.data_type = CMD_DATA;
    DataACKPacket.data_cmd = SX1276.Settings.sta_cmd;
    
    creatSendPacket(packet_data,DataACKPacket);
    
}


static void receiveDataCallback(uint8_t* data)
{
    uint8_t data_ack_packet[DATA_PACKET_LENGTH];
    uint8_t data_type = 0;
    uint16_t sensor_data = 0;
    TQStruct task;
    LED1_TOGGLE;
    SensorData.address = (uint32_t)*(data+4)<<24|(uint32_t)*(data+5)<<16|
                         (uint32_t)*(data+6)<<8 |(uint32_t)*(data+7);
    

    data_type = *(data+9) >> 4;
    sensor_data = ((*(data+9) << 8)|*(data+10)) & 0x0FFF;
    switch(data_type)
    {
    case TMR_DATA:
        SensorData.AMR = sensor_data;
        break;
    case REED_DATA:
        SensorData.reed = sensor_data;
        break;
    }
    papredDataACKPacket(data,data_ack_packet);
    Radio.Send(data_ack_packet,sizeof(DataPacket)-1);
    while(Radio.sendNotDone());
    
    Radio.setRxState(RX_TIMEOUT_VALUE);
#ifdef GPRS_EN
    task.event = SEND_GPRS;
#else
    task.event = SEND_XBEE;
#endif
    task.data[0] = *(data+4);
    task.data[1] = *(data+5);
    task.data[2] = *(data+6);
    task.data[3] = *(data+7);
    task.data[4] = data_type;
    task.data[5] = sensor_data>>8;
    task.data[6] = sensor_data;
    OS.postTask(task);
}
uint32_t address = 0;
static uint8_t ifPacketValid(uint8_t* data)
{
#define VALID     1
#define INVALID   0
    
    
    address = (uint32_t)*data<<24|(uint32_t)*(data+1)<<16|
              (uint32_t)*(data+2)<<8|(uint32_t)*(data+3);
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



void sendByCSMA()
{

}

