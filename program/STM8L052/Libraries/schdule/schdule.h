#ifndef __SCHDULE_H
#define __SCHDULE_H
#include "interface.h"


typedef struct
{
    uint8 reed;
    uint8 reed_memory;
    uint16 TMR;
    uint16 TMR_memory;
}SensorData_s;

typedef struct
{
    uint8         Status;
    SensorData_s  Data;
    uint8  Reed;
    SensorData_s (*getData)();
    bool         (*ifStatusChanged)();
    uint8        (*getStatus)();
    void         (*InitSensor)();
}Sensor_s;


extern Sensor_s Sensor;
extern SensorData_s getSensorData();
extern bool ifStatusChanged();
extern uint8 getStatus();
#endif