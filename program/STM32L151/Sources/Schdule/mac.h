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
    uint32_t  des_address;                 
    uint32_t  src_address;    
    uint8_t   packet_type;
    uint8_t   data_type:4;
    uint16_t  data_cmd:12;                     
}DataPacketStruct;


typedef struct{
  uint8_t ack_received;
  uint8_t resend_times;
  uint8_t send_failed;
  uint8_t data_sending;
}ProtocolStruct;

typedef enum 
{
    DATA_PACK          = 1, 
    DATA_ACK_PACK      = 2, 
} PACK_TYPE;

typedef enum 
{
    TMR_DATA           = 1, 
    REED_DATA          = 2, 
    CMD_DATA           = 3,
    RSSI_DATA          = 4, 
    SNR_DATA           = 5,
    BATTERY_DATA       = 6,
} DATA_TYPE;

extern ProtocolStruct Protocol;
extern const struct Link_interface Link;
#endif
