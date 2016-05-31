#include "common.h"
TQStruct TQ[MAX_TASK_NUM];
unsigned int current_tsk;
unsigned int last_tsk;
TQStruct emptytask;
static void Init_TQ(void)
{
    int i;
    
    for (i=0; i<MAX_TASK_NUM; i++)
    {
        TQ[i].event = 0;
        memset( TQ[i].data, 0, ( size_t )MAX_PACK_LENGTH );
    }
    current_tsk = 0;
    last_tsk = 0;
    memset( emptytask.data, 0, ( size_t )MAX_PACK_LENGTH );
    emptytask.event = 0;
}


static uint8 PostTask(TQStruct task)
{
    if (TQ[last_tsk].event == 0)
    {
        TQ[last_tsk].event = task.event;
        memcpy(TQ[last_tsk].data, task.data, MAX_PACK_LENGTH);
        last_tsk = (last_tsk + 1) % MAX_TASK_NUM;
        return TQ_SUCCESS;
    }
    else
    {
        //printf("TQ is FULL!\n");
        Init_TQ();
        return TQ_FULL;		
    }
}
static uint8 isEmpty()
{
    uint8 i=0;
    uint8 emptycount = 0;
    for(i=0; i<MAX_TASK_NUM; i++)
    {
        if(TQ[i].event == 0)
        {
            emptycount++;
        }
    }
    if(emptycount == MAX_TASK_NUM)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}


static uint8 Pop_T(TQStruct* task)
{
    if (TQ[current_tsk].event != 0)
    {
        *task = TQ[current_tsk];
        TQ[current_tsk].event = 0;
        current_tsk = (current_tsk + 1) % MAX_TASK_NUM;
        return TQ_SUCCESS;
    }
    else
    {
        //printf("TQ is EMPTY!\n");
        current_tsk = (current_tsk + 1) % MAX_TASK_NUM;
        *task = emptytask;
        return TQ_EMPTY;
    }
}

static uint8 Process_Event()
{
    TQStruct current_event;
    uint32 src_address = 0;
    uint8 data_type = 0;
    uint16 data = 0;
    
    Pop_T(&current_event);
    switch(current_event.event)
    {
    case COLLECT_DATA:
        break;
    case EXECUTE_CMD:
        break;
    case SEND_DATA:
        break;
    case RECEIVE_DATA_PACKET:
        Link.sendDataACK(current_event.data);
        break;
    case SEND_XBEE:
        src_address = current_event.data[0]<<24|current_event.data[1]<<16|
                      current_event.data[2]<<8 |current_event.data[3];
        data_type = current_event.data[4];
        data = current_event.data[5]<<8 | current_event.data[6];
        Xbee.send(src_address,data_type,data);
        break;

    }
    return current_event.event;
}

const struct TaskQuene_inferface OS =
{
    Process_Event,
    PostTask,
    isEmpty,
    Init_TQ,
};