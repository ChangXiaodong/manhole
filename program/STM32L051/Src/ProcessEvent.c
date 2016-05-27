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
        break;
    case RECEIVE_DATAACK_PACKET:
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