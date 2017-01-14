#include "common.h"
Sensor_s Sensor;

//unfinished
void getSensorData()
{
    EN_SAMPLE_SET;
    /*delay_ms(200);
    ADC_SoftwareStartConv(ADC1);
    while(ADC_GetFlagStatus(ADC1,ADC_FLAG_EOC) != SET);  
    Sensor.Data.TMR = ADC_GetConversionValue(ADC1);*/
    Sensor.Data.reed = REED_GET;
    LED1_TOGGLE;
    EN_SAMPLE_RESET;
}

bool ifStatusChanged()
{
    bool changed_flag = FALSE;
    
    getSensorData();
    if((Sensor.Data.reed!=Sensor.Data.reed_memory)||
       (abs(Sensor.Data.TMR - Sensor.Data.TMR_memory) > 50))
    {
        changed_flag = TRUE;
    }
    Sensor.Data.reed_memory = Sensor.Data.reed;
    Sensor.Data.TMR_memory = Sensor.Data.TMR;
    changed_flag = TRUE;
    return changed_flag;
}

uint8 getStatus()
{
    return Sensor.Status;
}

void Deinit_UART()
{
    USART_DeInit(USART1);
    CLK_PeripheralClockConfig(CLK_Peripheral_USART1,DISABLE);
}

void Deinit_ADC()
{
    ADC_DeInit(ADC1);
    CLK_PeripheralClockConfig(CLK_Peripheral_ADC1, DISABLE);
}


void Deinit_TIMER()
{
    CLK_PeripheralClockConfig(CLK_Peripheral_TIM2, DISABLE);
    TIM2_DeInit();

    CLK_PeripheralClockConfig(CLK_Peripheral_TIM5, DISABLE);
    TIM5_DeInit();
    
    CLK_PeripheralClockConfig(CLK_Peripheral_TIM3, DISABLE);
    TIM3_DeInit();
}

void SystemSleep()
{
    LED1_OFF;
    LED2_OFF;
    Radio.setSleepState();
    Deinit_ADC();
    
    All_PULL_UP();
    CLK_LSICmd(DISABLE);
    while ((CLK->ICKCR & 0x04) != 0x00);
    sim();	
    halt();
}
void reboot()
{
    IWDG_WriteAccessCmd(IWDG_WriteAccess_Enable);
    IWDG_SetPrescaler(IWDG_Prescaler_4);
    IWDG_SetReload(1);
    IWDG_Enable();
    delay_1ms;delay_1ms;delay_1ms;
}
void SystemWake()
{
    Init_GPIO();
    Init_TIMER();
    Init_USART();
    Init_Radio();
    //Init_Sensor();
}



        

