#ifndef _TASKQ_h_
#define _TASKQ_h_

#include "mac.h"
#define MAX_PACK_LENGTH DATA_PACKET_LENGTH
typedef struct{
    uint8_t  data[MAX_PACK_LENGTH];		
    uint8_t  event;						
}TQStruct;
//
#define    MAX_TASK_NUM    5 
#define    TQ_SUCCESS      0
#define    TQ_FULL         1
#define    TQ_EMPTY        2

typedef enum 
{
    COLLECT_DATA             = 1, 
    EXECUTE_CMD              = 2, 
    SEND_DATA                = 3,
    RECEIVE_DATA_PACKET      = 4,
    SEND_XBEE                = 5,
    SEND_GPRS                = 6,
} EVENT_t;

//extern void Init_TQ(void);
//extern uint8 PostTask(uint8 *data,uint8 event);
//extern uint8 Process_Event();
//extern uint8 isEmpty();
//extern TQStruct TQ[MAX_TASK_NUM];
//
extern const struct TaskQuene_inferface OS;
#endif
