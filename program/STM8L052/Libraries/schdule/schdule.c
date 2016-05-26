#include "common.h"
Sensor_s Sensor;

//unfinished
SensorData_s getSensorData()
{
    EN_SAMPLE_SET;
    delay_ms(150);
    ADC_SoftwareStartConv(ADC1);
    while(ADC_GetFlagStatus(ADC1,ADC_FLAG_EOC) != SET);  
    Sensor.Data.TMR = ADC_GetConversionValue(ADC1);
    Sensor.Data.reed = REED_GET;
    EN_SAMPLE_RESET;
    return Sensor.Data;
}

bool ifStatusChanged()
{
    SensorData_s data;
    bool changed_flag = FALSE;
    
    data = getSensorData();
    if((data.reed!=data.reed_memory)||
       (abs(data.TMR - data.TMR_memory) > 100))
    {
        changed_flag = TRUE;
    }
    data.reed_memory = data.reed;
    data.TMR_memory = data.TMR;
    
    return changed_flag;
}

uint8 getStatus()
{
    return Sensor.Status;
}

        

