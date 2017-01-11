#ifndef __GPIO_H
#define __GPIO_H

#define LED_PORT     GPIOB
#define LED1_PORT    GPIOB
#define LED1_BIT     GPIO_Pin_0
#define LED1_OFF     GPIO_SetBits(LED1_PORT,LED1_BIT)
#define LED1_ON      GPIO_ResetBits(LED1_PORT,LED1_BIT)
#define LED1_TOGGLE  GPIO_ToggleBits(LED1_PORT,LED1_BIT)
     
#define LED2_PORT    GPIOB
#define LED2_BIT     GPIO_Pin_1
#define LED2_OFF     GPIO_SetBits(LED2_PORT,LED2_BIT)
#define LED2_ON      GPIO_ResetBits(LED2_PORT,LED2_BIT)
#define LED2_TOGGLE  GPIO_ToggleBits(LED2_PORT,LED2_BIT)

#define LED3_PORT      GPIOB
#define LED3_BIT       GPIO_Pin_2
#define LED3_OFF       GPIO_SetBits(LED3_PORT,LED3_BIT)
#define LED3_ON        GPIO_ResetBits(LED3_PORT,LED3_BIT)
#define LED3_TOGGLE    GPIO_ToggleBits(LED3_PORT,LED3_BIT)

#define GSM_RST_PORT    GPIOA
#define GSM_RST_BIT     GPIO_Pin_0
#define GSM_RST_H       GPIO_SetBits(GSM_RST_PORT,GSM_RST_BIT)
#define GSM_RST_L       GPIO_ResetBits(GSM_RST_PORT,GSM_RST_BIT)

#define GSM_PW_PORT    GPIOB
#define GSM_PW_BIT     GPIO_Pin_8
#define GSM_PW_H       GPIO_SetBits(GSM_PW_PORT,GSM_PW_BIT)
#define GSM_PW_L       GPIO_ResetBits(GSM_PW_PORT,GSM_PW_BIT)

#define GSM_ON_PORT    GPIOB
#define GSM_ON_BIT     GPIO_Pin_9
#define GSM_ON_H       GPIO_SetBits(GSM_ON_PORT,GSM_ON_BIT)
#define GSM_ON_L       GPIO_ResetBits(GSM_ON_PORT,GSM_ON_BIT)

#define GSM_STATUS_PORT  GPIOC
#define GSM_STATUS_BIT   GPIO_Pin_13
#define GSM_STATUS       GPIO_ReadInputDataBit(GSM_STATUS_PORT,GSM_STATUS_BIT)

#define XBEE_RST_PORT    GPIOA
#define XBEE_RST_BIT     GPIO_Pin_8
#define XBEE_RST_H       GPIO_SetBits(XBEE_RST_PORT,XBEE_RST_BIT)
#define XBEE_RST_L       GPIO_ResetBits(XBEE_RST_PORT,XBEE_RST_BIT)

#define XBEE_SLEEP_PORT    GPIOA
#define XBEE_SLEEP_BIT     GPIO_Pin_12
#define XBEE_SLEEP_H       GPIO_SetBits(XBEE_SLEEP_PORT,XBEE_SLEEP_BIT)
#define XBEE_SLEEP_L       GPIO_ResetBits(XBEE_SLEEP_PORT,XBEE_SLEEP_BIT)

#define RF_SPI_PORT    GPIOA     
#define RF_REST_PORT   GPIOA
#define RF_REST_BIT    GPIO_Pin_15
#define RF_REST_H      GPIO_SetBits(RF_REST_PORT,RF_REST_BIT)
#define RF_REST_L      GPIO_ResetBits(RF_REST_PORT,RF_REST_BIT)
     
#define RF_CE_PORT     GPIOA
#define RF_CE_BIT      GPIO_Pin_4
#define RF_CE_H        GPIO_SetBits(RF_CE_PORT,RF_CE_BIT)
#define RF_CE_L        GPIO_ResetBits(RF_CE_PORT,RF_CE_BIT)

#define RF_CKL_PORT    GPIOA
#define RF_CKL_BIT     GPIO_Pin_5
#define RF_CKL_H       GPIO_SetBits(RF_CKL_PORT,RF_CKL_BIT)
#define RF_CKL_L       GPIO_ResetBits(RF_CKL_PORT,RF_CKL_BIT)

#define RF_SDO_PORT    GPIOA
#define RF_SDO_BIT     GPIO_Pin_6
#define RF_SDO_DATA    GPIO_ReadInputDataBit(RF_SDO_PORT,RF_SDO_BIT)

#define RF_SDI_PORT    GPIOA
#define RF_SDI_BIT     GPIO_Pin_7
#define RF_SDI_H       GPIO_SetBits(RF_SDI_PORT,RF_SDI_BIT)
#define RF_SDI_L       GPIO_ResetBits(RF_SDI_PORT,RF_SDI_BIT)

#define RF_TX    
#define RF_RX     
     
#define RF_DIO0_PORT    GPIOB
#define RF_DIO0_BIT     GPIO_Pin_3

#define RF_DIO1_PORT    GPIOB
#define RF_DIO1_BIT     GPIO_Pin_4

#define ENABLE_DIO0     EXTI->PR|=EXTI_PR_PR3;EXTI->IMR |= EXTI_IMR_MR3
#define DISABLE_DIO0    EXTI->PR|=EXTI_PR_PR3;EXTI->IMR &= ~EXTI_IMR_MR3

#define ENABLE_DIO1     EXTI->PR|=EXTI_PR_PR4;EXTI->IMR |= EXTI_IMR_MR4
#define DISABLE_DIO1    EXTI->PR|=EXTI_PR_PR4;EXTI->IMR &= ~EXTI_IMR_MR4

extern void Init_GPIO();
extern void Init_XBEE_GPIO();
extern void Init_Finished();
#endif