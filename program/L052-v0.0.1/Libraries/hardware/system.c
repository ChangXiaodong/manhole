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
    LED1_OFF;
    LED2_OFF;
    
    GPIO_Init(GPIOA,GPIO_Pin_2,GPIO_Mode_Out_PP_Low_Fast);
}

static void Init_Delay()
{
    CLK_PeripheralClockConfig(CLK_Peripheral_TIM2, ENABLE);
    TIM2_DeInit();
    TIM2_TimeBaseInit(TIM2_Prescaler_1,TIM2_CounterMode_Up,0xFFFF);
    TIM2_Cmd(DISABLE);
}

static void Init_Time()
{
    CLK_PeripheralClockConfig(CLK_Peripheral_TIM3, ENABLE);
    TIM3_DeInit();
    TIM3_TimeBaseInit(TIM3_Prescaler_1,TIM3_CounterMode_Up,0xFFFF);
    TIM3_Cmd(DISABLE);
}


static void Init_CLK()
{
    CLK_DeInit();
    CLK_SYSCLKSourceSwitchCmd(ENABLE);
    CLK_HSICmd(ENABLE);
    CLK_LSICmd(ENABLE);
    CLK_HSEConfig(CLK_HSE_OFF);
    CLK_LSEConfig(CLK_LSE_OFF);
    CLK_SYSCLKSourceConfig(CLK_SYSCLKSource_HSI);
    CLK_SYSCLKDivConfig(CLK_SYSCLKDiv_16);
    CLK_ClockSecuritySystemEnable();
    delay_100us;
}

static void Init_GPIO()
{
    Deinit_All_GPIO();
    Init_LED();
}

static void Init_TIMER()
{
    Init_Delay();  //TIMER2
    Init_Time();   //TIMER3
}

static void Init_USART()
{
    CLK_PeripheralClockConfig(CLK_Peripheral_USART1,ENABLE);
    
    USART_DeInit(USART1);
    GPIO_ExternalPullUpConfig(GPIOC,GPIO_Pin_2|GPIO_Pin_3,ENABLE);
    USART_Init(USART1,
               9600,
               USART_WordLength_8b,
               USART_StopBits_1,
               USART_Parity_No,
               (USART_Mode_TypeDef)(USART_Mode_Tx|USART_Mode_Rx));
    
    //USART_ITConfig(USART1, USART_IT_RXNE, ENABLE);
    USART_Cmd(USART1,ENABLE);
}

static void Init_EXIT()
{
    GPIO_Init(GPIOD, GPIO_Pin_5, GPIO_Mode_In_FL_IT);
    EXTI_SetPinSensitivity(EXTI_Pin_5,EXTI_Trigger_Rising);
}

static void Init_RTC()
{
    CLK_RTCClockConfig(CLK_RTCCLKSource_LSI, CLK_RTCCLKDiv_1);
    while (CLK_GetFlagStatus(CLK_FLAG_LSIRDY) == RESET);
    
    CLK_PeripheralClockConfig(CLK_Peripheral_RTC, ENABLE);
    RTC_WakeUpClockConfig(RTC_WakeUpClock_RTCCLK_Div8);
    RTC_ITConfig(RTC_IT_WUT, ENABLE);
    RTC_SetWakeUpCounter(6000);
    RTC_WakeUpCmd(ENABLE);
}

void UART_Send_Data(uint8 data)
{
    USART_SendData8(USART1,data);
    while (USART_GetFlagStatus(USART1, USART_FLAG_TC) == RESET);
}

void Init_System()
{
    Init_CLK();
    Init_GPIO();
    Init_TIMER();
    Init_USART();
    Init_EXIT();
    Init_RTC();
    Init_Radio();
}