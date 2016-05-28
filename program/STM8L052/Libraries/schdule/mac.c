#include "common.h"
static void sendByCSMA();
static uint8 ifPacketValid(uint8* data);
static void receiveDataackCallback(uint8* data);
DataPacketStruct DataPacket;
ProtocolStruct Protocol;
const struct Link_interface Link = 
{
    sendByCSMA,
    receiveDataackCallback,
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
    DataPacket.des_address = 0x00001111;
    DataPacket.src_address = SX1276.Settings.Address;
    DataPacket.packet_type = DATA_PACK;
    DataPacket.data_type = DATA_DATA;
    DataPacket.data_cmd = Sensor.Data.TMR;
    
    creatSendPacket(data,DataPacket);
}

static void CSMABackOff()
{
    delay_ms_T5(1000);
}

static void receiveDataackCallback(uint8* data)
{
    //处理返回命令 （未完成）
}

static uint8 ifPacketValid(uint8* data)
{
#define VALID     1
#define INVALID   0
    
    uint32 address = 0;
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
    uint8 packet_data[DATA_PACKET_LENGTH];
    LED1_TOGGLE;
    papredDataPacket(packet_data);
    for(uint8 i=0;i<BACKOFF_TIMES;i++)
    {
        if(isChannelFree(-30))
        {
            Radio.Send(packet_data,sizeof(DataPacket)-1);
            while(Radio.sendNotDone());
            Radio.setRxState(RX_TIMEOUT_VALUE);
            if(!receivedACK())
            {
                TQStruct task;
                RTC_WakeUpCmd(DISABLE);
                task.event = SEND_DATA;
                if(Protocol.resend_times<MAX_RESEND_TIMES)
                {
                    OS.postTask(task);
                }
                else
                {
                    RadioEvents.ResendFailed();
                }
            }
            else
            {
                RTC_WakeUpCmd(ENABLE);
                //SystemSleep();
            }
            break;
        }
        else
        {
            CSMABackOff();
        }
    }
    systemSleep();
}

