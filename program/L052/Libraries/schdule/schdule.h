#ifndef __SCHDULE_H
#define __SCHDULE_H
#include "interface.h"



typedef struct
{
    uint8  Status;
    uint16 Data;
    uint16 (*getData)();
    uint8  (*ifStatusChanged)();
    uint8  (*getStatus)();
    void   (*InitSensor)();
}Sensor_s;

extern void Init_Sensor();
extern Sensor_s Sensor;
#endif