#ifndef __MAC_H
#define __MAC_H

#define BACKOFF_TIMES  10
#define BROADCAST_ADDRESS 0xFFFFFFFF
#define MAX_RESEND_TIMES  10

/*|des_address|src_address|packet_type|data_type|data_cmd|
* |   32 bit  |   32 bit  |    8 bit  |   4 bit | 12 bit |
* des_address:0x0001--0xFFFE
* src_address:0x0001--0xFFFE
* packet_type:DATA_PACK,DATA_ACK_PACK;
* data_cmd:sensor data & command from server
* data_type:DATA_DATA,RSSI_DATA,SNR_DATA,BATTERY_DATA
*/
#define DATA_PACKET_LENGTH  11
typedef struct{
    uint32  des_address;                 
    uint32  src_address;    
    uint8   packet_type;
    uint8   data_type:4;
    uint16  data_cmd:12;                     
}DataPacketStruct;


typedef struct{
  uint8 ack_received;
  uint8 resend_times;
  uint8 send_failed;
  uint8 data_sending;
}ProtocolStruct;

typedef enum 
{
    DATA_PACK          = 1, 
    DATA_ACK_PACK      = 2, 
} PACK_TYPE;

typedef enum 
{
    DATA_DATA          = 1, 
    CMD_DATA           = 2,
    RSSI_DATA          = 3, 
    SNR_DATA           = 4,
    BATTERY_DATA       = 5,
} DATA_TYPE;

extern ProtocolStruct Protocol;
extern const struct Link_interface Link;
#endif
