#include "common.h"

static void Deinit_All_GPIO()
{
    GPIO_DeInit(GPIOA);
    GPIO_DeInit(GPIOB);
    GPIO_DeInit(GPIOC);
    GPIO_DeInit(GPIOD);
    GPIO_DeInit(GPIOE);
    GPIO_DeInit(GPIOF);
    GPIO_DeInit(GPIOG);
}

static void Init_LED()
{
    GPIO_Init(LED1_PORT,LED1_BIT,GPIO_Mode_Out_PP_Low_Fast); 
    GPIO_Init(LED2_PORT,LED2_BIT,GPIO_Mode_Out_PP_Low_Fast);
    GPIO_Init(LED3_PORT,LED3_BIT,GPIO_Mode_Out_PP_Low_Fast); 
    GPIO_Init(LED4_PORT,LED4_BIT,GPIO_Mode_Out_PP_Low_Fast);
    GPIO_Init(LED5_PORT,LED5_BIT,GPIO_Mode_Out_PP_Low_Fast); 
    LED1_OFF;
    LED2_OFF;
    LED3_OFF;
    LED4_OFF;
    LED5_OFF;
}

static void Init_Delay()
{
    CLK_PeripheralClockConfig(CLK_Peripheral_TIM2, ENABLE);
    TIM2_DeInit();
    TIM2_TimeBaseInit(TIM2_Prescaler_16,TIM2_CounterMode_Up,0xFFFF);
    TIM2_Cmd(DISABLE);
    
    CLK_PeripheralClockConfig(CLK_Peripheral_TIM5, ENABLE);
    TIM5_DeInit();
    TIM5_TimeBaseInit(TIM5_Prescaler_16,TIM5_CounterMode_Up,0xFFFF);
    TIM5_Cmd(DISABLE);
}

static void Init_Time()
{
    CLK_PeripheralClockConfig(CLK_Peripheral_TIM3, ENABLE);
    TIM3_DeInit();
    TIM3_TimeBaseInit(TIM3_Prescaler_16,TIM3_CounterMode_Up,0xFFFF);
    TIM3_Cmd(DISABLE);
}


void Init_CLK()
{
    CLK_DeInit();
    CLK_SYSCLKSourceSwitchCmd(ENABLE);
    CLK_HSICmd(ENABLE);
    CLK_LSICmd(ENABLE);
    CLK_HSEConfig(CLK_HSE_OFF);
    CLK_LSEConfig(CLK_LSE_OFF);
    CLK_SYSCLKSourceConfig(CLK_SYSCLKSource_HSI);
    CLK_SYSCLKDivConfig(CLK_SYSCLKDiv_1);
    CLK_ClockSecuritySystemEnable();
    delay_100us;
}

void Init_GPIO()
{
    Deinit_All_GPIO();
    Init_LED();
    GPIO_Init(TEST1_PORT,TEST1_BIT,GPIO_Mode_Out_PP_Low_Fast); 
}

void All_PULL_UP()
{
    GPIO_Init(GPIOA,GPIO_Pin_3,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOA,GPIO_Pin_4,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOA,GPIO_Pin_5,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOA,GPIO_Pin_6,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOA,GPIO_Pin_7,GPIO_Mode_In_PU_No_IT); 
    
    GPIO_Init(GPIOB,GPIO_Pin_0,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOB,GPIO_Pin_1,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOB,GPIO_Pin_2,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOB,GPIO_Pin_3,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOB,GPIO_Pin_4,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOB,GPIO_Pin_5,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOB,GPIO_Pin_6,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOB,GPIO_Pin_7,GPIO_Mode_In_PU_No_IT); 
    
    GPIO_Init(GPIOC,GPIO_Pin_0,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOC,GPIO_Pin_1,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOC,GPIO_Pin_2,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOC,GPIO_Pin_3,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOC,GPIO_Pin_4,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOC,GPIO_Pin_5,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOC,GPIO_Pin_6,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOC,GPIO_Pin_7,GPIO_Mode_In_PU_No_IT); 
    
    GPIO_Init(GPIOD,GPIO_Pin_0,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOD,GPIO_Pin_1,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOD,GPIO_Pin_2,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOD,GPIO_Pin_3,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOD,GPIO_Pin_4,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOD,GPIO_Pin_5,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOD,GPIO_Pin_6,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOD,GPIO_Pin_7,GPIO_Mode_In_PU_No_IT); 
    
    GPIO_Init(GPIOE,GPIO_Pin_0,GPIO_Mode_In_PU_No_IT); 
    //GPIO_Init(GPIOE,GPIO_Pin_1,GPIO_Mode_In_PU_No_IT); 
    EN_SAMPLE_RESET;
    GPIO_Init(GPIOE,GPIO_Pin_2,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOE,GPIO_Pin_3,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOE,GPIO_Pin_4,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOE,GPIO_Pin_5,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOE,GPIO_Pin_6,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOE,GPIO_Pin_7,GPIO_Mode_In_PU_No_IT); 
    
    GPIO_Init(GPIOF,GPIO_Pin_0,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOF,GPIO_Pin_1,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOF,GPIO_Pin_4,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOF,GPIO_Pin_5,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOF,GPIO_Pin_6,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOF,GPIO_Pin_7,GPIO_Mode_In_PU_No_IT);
    
    GPIO_Init(GPIOG,GPIO_Pin_0,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOG,GPIO_Pin_1,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOG,GPIO_Pin_2,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOG,GPIO_Pin_3,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOG,GPIO_Pin_4,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOG,GPIO_Pin_5,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOG,GPIO_Pin_6,GPIO_Mode_In_PU_No_IT); 
    GPIO_Init(GPIOG,GPIO_Pin_7,GPIO_Mode_In_PU_No_IT); 
}

void Init_TIMER()
{
    Init_Delay();  //TIMER2  TIMER5
    Init_Time();   //TIMER3
}

void Init_USART()
{
    CLK_PeripheralClockConfig(CLK_Peripheral_USART1,ENABLE);
    
    USART_DeInit(USART1);
    GPIO_ExternalPullUpConfig(GPIOC,GPIO_Pin_2|GPIO_Pin_3,ENABLE);
    USART_Init(USART1,
               115200,
               USART_WordLength_8b,
               USART_StopBits_1,
               USART_Parity_No,
               (USART_Mode_TypeDef)(USART_Mode_Tx|USART_Mode_Rx));
    
    USART_ITConfig(USART1, USART_IT_RXNE, ENABLE);
    USART_Cmd(USART1,ENABLE);
}

void Init_RTC()
{
    CLK_RTCClockConfig(CLK_RTCCLKSource_LSI, CLK_RTCCLKDiv_1);
    while (CLK_GetFlagStatus(CLK_FLAG_LSIRDY) == RESET);
    
    CLK_PeripheralClockConfig(CLK_Peripheral_RTC, ENABLE);
    RTC_WakeUpClockConfig(RTC_WakeUpClock_RTCCLK_Div2);
    RTC_ITConfig(RTC_IT_WUT, ENABLE);
    RTC_SetWakeUpCounter(1);
    RTC_WakeUpCmd(ENABLE);
}

void UART_Send_Data(uint8 data)
{
    USART_SendData8(USART1,data);
    while (USART_GetFlagStatus(USART1, USART_FLAG_TC) == RESET);
}

u8 UART_Receive_Data()
{
    while (USART_GetFlagStatus(USART1, USART_FLAG_RXNE) == RESET);
    return USART_ReceiveData8(USART1);
}

void setPHYAddress(uint16 address)
{
    FLASH_Unlock(FLASH_MemType_Data);
    FLASH_ProgramByte(EEPROM_START,address>>8);
    FLASH_ProgramByte(EEPROM_START+1,address);
    FLASH_Lock(FLASH_MemType_Data);
}

uint16_t getPHYAddress()
{
    uint16 address = 0;
    address =  FLASH_ReadByte(EEPROM_START)<<8;
    address |= FLASH_ReadByte(EEPROM_START+1);
    return address;
}

static void Init_ADC()
{
    CLK_PeripheralClockConfig(CLK_Peripheral_ADC1, ENABLE);
    ADC_DeInit(ADC1);
    ADC_Init(ADC1,
             ADC_ConversionMode_Single,
             ADC_Resolution_12Bit,
             ADC_Prescaler_1);
    ADC_ChannelCmd(ADC1,ADC_Channel_0,ENABLE);
    ADC_Cmd(ADC1,ENABLE);
    ADC_SoftwareStartConv(ADC1);
    while(ADC_GetFlagStatus(ADC1,ADC_FLAG_EOC)!=SET);  
    ADC_GetConversionValue(ADC1);
}       
//unfinished
static void initSensor()
{
    //GPIO_Init(REED_PORT,REED_BIT,GPIO_Mode_In_FL_No_IT); 
    GPIO_Init(EN_SAMPLE_PORT,EN_SAMPLE_BIT,GPIO_Mode_Out_PP_Low_Fast); 
    //Init_ADC();
}


void Init_Sensor()
{
    Sensor.getStatus = getStatus;
    Sensor.ifStatusChanged = ifStatusChanged;
    Sensor.InitSensor = initSensor;
    
    //Sensor.InitSensor();
}   

void Init_System()
{
    Init_CLK();
    Init_TIMER();
    Init_GPIO();
    delay_ms(1000);

    //Init_MPU6050();
    Init_MPU6500_SPI();
    Init_USART();
    //Init_RTC();
    //Init_Radio();
    //Init_Sensor();
}

void power_on()
{
    LED1_ON;
    delay_ms_T5(100);
    LED1_OFF;
    LED2_ON;
    delay_ms_T5(100);
    LED2_OFF;
    LED3_ON;
    delay_ms_T5(100);
    LED3_OFF;
    LED4_ON;
    delay_ms_T5(100);
    LED4_OFF;
    LED5_ON;
    delay_ms_T5(100);
    LED5_OFF;
    
}