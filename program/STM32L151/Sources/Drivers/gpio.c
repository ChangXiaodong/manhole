#include "common.h"

static void Init_LED()
{
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Pin = LED1_BIT;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT; 
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_40MHz;	
    GPIO_Init(LED_PORT, &GPIO_InitStructure);
    
    GPIO_InitStructure.GPIO_Pin = LED2_BIT;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT; 
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_40MHz;	
    GPIO_Init(LED_PORT, &GPIO_InitStructure);
    
    GPIO_InitStructure.GPIO_Pin = LED3_BIT;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT; 
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_40MHz;	
    GPIO_Init(LED_PORT, &GPIO_InitStructure);
    
    LED1_OFF;
    LED2_OFF;
    LED3_OFF;
}

static void Init_GSM()
{
#ifdef GPRS_EN
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Pin = GSM_RST_BIT;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_40MHz;
    GPIO_Init(GSM_RST_PORT, &GPIO_InitStructure);
    GSM_RST_L;
    
    GPIO_InitStructure.GPIO_Pin = GSM_PW_BIT|GSM_ON_BIT;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_40MHz;
    GPIO_Init(GSM_PW_PORT, &GPIO_InitStructure);
    GSM_ON_L;
    
    GSM_PW_H;
    GPIO_InitStructure.GPIO_Pin = GSM_STATUS_BIT;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_40MHz;
    GPIO_Init(GSM_STATUS_PORT, &GPIO_InitStructure);
    

#endif
}

void Init_XBEE_GPIO()
{
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Pin = XBEE_RST_BIT|XBEE_SLEEP_BIT;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT; 
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_40MHz;	
    GPIO_Init(XBEE_RST_PORT, &GPIO_InitStructure);
    XBEE_RST_H;
    XBEE_SLEEP_L;
}

void Init_LORA_SPI()
{
    EXTI_InitTypeDef   EXTI_InitStructure;
    NVIC_InitTypeDef   NVIC_InitStructure;
    GPIO_InitTypeDef GPIO_InitStruct;
    
    GPIO_InitStruct.GPIO_Pin = RF_REST_BIT|RF_CE_BIT|RF_CKL_BIT|RF_SDI_BIT;
    GPIO_InitStruct.GPIO_Mode = GPIO_Mode_OUT;
    GPIO_InitStruct.GPIO_Speed = GPIO_Speed_10MHz;
    GPIO_InitStruct.GPIO_OType = GPIO_OType_PP;
    GPIO_InitStruct.GPIO_PuPd = GPIO_PuPd_NOPULL;
    GPIO_Init(RF_SPI_PORT, &GPIO_InitStruct);
    
    GPIO_InitStruct.GPIO_Pin = RF_SDO_BIT;
    GPIO_InitStruct.GPIO_Mode = GPIO_Mode_IN;
    GPIO_InitStruct.GPIO_PuPd = GPIO_PuPd_NOPULL;
    GPIO_Init(RF_SPI_PORT, &GPIO_InitStruct);
    
    GPIO_InitStruct.GPIO_Pin = RF_DIO0_BIT;
    GPIO_InitStruct.GPIO_Mode = GPIO_Mode_IN;
    GPIO_InitStruct.GPIO_PuPd = GPIO_PuPd_NOPULL;
    GPIO_Init(RF_DIO0_PORT, &GPIO_InitStruct);
    
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_SYSCFG, ENABLE);
    SYSCFG_EXTILineConfig(EXTI_PortSourceGPIOB, EXTI_PinSource3);
    
    EXTI_InitStructure.EXTI_Line = EXTI_Line3;
    EXTI_InitStructure.EXTI_Mode = EXTI_Mode_Interrupt;
    EXTI_InitStructure.EXTI_Trigger = EXTI_Trigger_Rising;  
    EXTI_InitStructure.EXTI_LineCmd = ENABLE;
    EXTI_Init(&EXTI_InitStructure);
    
    NVIC_InitStructure.NVIC_IRQChannel = EXTI3_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
    NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
    NVIC_Init(&NVIC_InitStructure);
    
    
    
    GPIO_InitStruct.GPIO_Pin = RF_DIO1_BIT;
    GPIO_InitStruct.GPIO_Mode = GPIO_Mode_IN;
    GPIO_InitStruct.GPIO_PuPd = GPIO_PuPd_NOPULL;
    GPIO_Init(RF_DIO1_PORT, &GPIO_InitStruct);
    SYSCFG_EXTILineConfig(EXTI_PortSourceGPIOB, EXTI_PinSource4);
    
    EXTI_InitStructure.EXTI_Line = EXTI_Line4;
    EXTI_InitStructure.EXTI_Mode = EXTI_Mode_Interrupt;
    EXTI_InitStructure.EXTI_Trigger = EXTI_Trigger_Rising;  
    EXTI_InitStructure.EXTI_LineCmd = ENABLE;
    EXTI_Init(&EXTI_InitStructure);
    
    NVIC_InitStructure.NVIC_IRQChannel = EXTI4_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
    NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
    NVIC_Init(&NVIC_InitStructure);
    
    
    RF_CKL_L;
    RF_CE_H;
    RF_SDI_H;

}

void Init_GPIO()
{
    RCC_AHBPeriphClockCmd(RCC_AHBPeriph_GPIOA|RCC_AHBPeriph_GPIOB,ENABLE);
    
    GPIO_DeInit(GPIOA);
    GPIO_DeInit(GPIOB);
    Init_LED();
    Init_GSM();
    
}

void Init_Finished()
{
    LED1_ON;
    LED2_ON;
    LED3_ON;
    delay_ms(100);
    LED1_OFF;
    LED2_OFF;
    LED3_OFF;
    delay_ms(100);
    LED1_ON;
    LED2_ON;
    LED3_ON;
    delay_ms(100);
    LED1_OFF;
    LED2_OFF;
    LED3_OFF;
    delay_ms(100);
    LED1_ON;
    LED2_ON;
    LED3_ON;
    delay_ms(100);
    LED1_OFF;
    LED2_OFF;
    LED3_OFF;
}