#ifndef __SCHDULE_H
#define __SCHDULE_H
#include "interface.h"

typedef struct  {
    uint32 address;
    uint16 AMR;
    uint8  reed;
}SensorData_s;


extern SensorData_s SensorData;
#endif
