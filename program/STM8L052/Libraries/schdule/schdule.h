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
    bool         (*ifStatusChanged)();
    uint8        (*getStatus)();
    void         (*InitSensor)();
}Sensor_s;


extern Sensor_s Sensor;
extern void getSensorData();
extern bool ifStatusChanged();
extern uint8 getStatus();
extern void SystemSleep();
extern void SystemWake();

extern void Deinit_UART();
extern void Deinit_ADC();
extern void Deinit_TIMER();
#endif