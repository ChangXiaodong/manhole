#include "common.h"
Sensor_s Sensor;

//unfinished
static uint16 getSensorData()
{
    uint16 data = 4095;
    Sensor.Data = data;
    return data;
}

//unfinished
static uint8 ifStatusChanged()
{
    uint16 data;
    data = getSensorData();
    return 1;
//    if(data == 0)
//    {
//        return 1;
//    }
//    else
//    {
//        return 0;
//    }
}

static uint8 getStatus()
{
    return Sensor.Status;
}

//unfinished
static void initSensor()
{

}


void Init_Sensor()
{
    Sensor.getData = getSensorData;
    Sensor.getStatus = getStatus;
    Sensor.ifStatusChanged = ifStatusChanged;
    Sensor.InitSensor = initSensor;
    
    Sensor.InitSensor();
}           

