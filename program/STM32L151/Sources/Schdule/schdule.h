#ifndef __SCHDULE_H
#define __SCHDULE_H
#include "interface.h"

typedef struct  {
    uint32_t address;
    uint16_t AMR;
    uint8_t  reed;
}SensorData_s;


extern SensorData_s SensorData;
#endif
