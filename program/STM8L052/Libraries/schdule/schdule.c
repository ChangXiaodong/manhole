#include "common.h"
Sensor_s Sensor;

//unfinished
void getSensorData()
{
    EN_SAMPLE_SET;
    delay_ms(150);
    ADC_SoftwareStartConv(ADC1);
    while(ADC_GetFlagStatus(ADC1,ADC_FLAG_EOC) != SET);  
    Sensor.Data.TMR = ADC_GetConversionValue(ADC1);
    Sensor.Data.reed = REED_GET;
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
    
    return changed_flag;
}

uint8 getStatus()
{
    return Sensor.Status;
}

static void Deinit_UART()
{
    CLK_PeripheralClockConfig(CLK_Peripheral_USART1,DISABLE);
    USART_DeInit(USART1);
}

static void Deinit_ADC()
{
    CLK_PeripheralClockConfig(CLK_Peripheral_ADC1, DISABLE);
    ADC_DeInit(ADC1);
}

static void Deinit_GPIO()
{
    GPIO_Init(GPIOA,GPIO_Pin_All,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOB,GPIO_Pin_All,GPIO_Mode_In_PU_No_IT);
    GPIO_Init(GPIOC,GPIO_Pin_All,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOD,GPIO_Pin_All,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOE,GPIO_Pin_All,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOF,GPIO_Pin_All,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOG,GPIO_Pin_All,GPIO_Mode_In_PU_No_IT); 
    
    GPIO_Init(LED1_PORT,LED1_BIT,GPIO_Mode_Out_PP_Low_Fast); 
    GPIO_Init(LED2_PORT,LED2_BIT,GPIO_Mode_Out_PP_Low_Fast);
    LED1_OFF;
    LED2_OFF;
}

static void Deinit_TIMER()
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
    Radio.setSleepState();
    Deinit_UART();
    Deinit_ADC();
    Deinit_GPIO();
    Deinit_TIMER();
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
    Init_Sensor();
}



        

