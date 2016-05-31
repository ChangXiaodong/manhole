/**
  ******************************************************************************
  * File Name          : gpio.h
  * Description        : This file contains all the functions prototypes for 
  *                      the gpio  
  ******************************************************************************
  *
  * COPYRIGHT(c) 2016 STMicroelectronics
  *
  * Redistribution and use in source and binary forms, with or without modification,
  * are permitted provided that the following conditions are met:
  *   1. Redistributions of source code must retain the above copyright notice,
  *      this list of conditions and the following disclaimer.
  *   2. Redistributions in binary form must reproduce the above copyright notice,
  *      this list of conditions and the following disclaimer in the documentation
  *      and/or other materials provided with the distribution.
  *   3. Neither the name of STMicroelectronics nor the names of its contributors
  *      may be used to endorse or promote products derived from this software
  *      without specific prior written permission.
  *
  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
  * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
  * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
  * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
  * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
  * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
  * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
  *
  ******************************************************************************
  */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __gpio_H
#define __gpio_H
#ifdef __cplusplus
 extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32l0xx_hal.h"
#include "common.h"
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */


#define GPIO_SetBits(port,pin)              HAL_GPIO_WritePin(port,pin,GPIO_PIN_SET)
#define GPIO_ResetBits(port,pin)            HAL_GPIO_WritePin(port,pin,GPIO_PIN_RESET)
#define GPIO_ToggleBits(port,pin)           HAL_GPIO_TogglePin(port,pin)    
#define GPIO_ReadInputDataBit(port,pin)     HAL_GPIO_ReadPin(port,pin)
     
#define LED_PORT     GPIOB
#define LED1_PORT    GPIOB
#define LED1_BIT     GPIO_PIN_0
#define LED1_OFF     GPIO_SetBits(LED1_PORT,LED1_BIT)
#define LED1_ON      GPIO_ResetBits(LED1_PORT,LED1_BIT)
#define LED1_TOGGLE  GPIO_ToggleBits(LED1_PORT,LED1_BIT)
     
#define LED2_PORT    GPIOB
#define LED2_BIT     GPIO_PIN_1
#define LED2_OFF     GPIO_SetBits(LED2_PORT,LED2_BIT)
#define LED2_ON      GPIO_ResetBits(LED2_PORT,LED2_BIT)
#define LED2_TOGGLE  GPIO_ToggleBits(LED2_PORT,LED2_BIT)
     
#define LED3_PORT      GPIOB
#define LED3_BIT       GPIO_PIN_2
#define LED3_OFF       GPIO_SetBits(LED3_PORT,LED3_BIT)
#define LED3_ON        GPIO_ResetBits(LED3_PORT,LED3_BIT)
#define LED3_TOGGLE    GPIO_ToggleBits(LED3_PORT,LED3_BIT)

#define RF_SPI_PORT    GPIOA     
#define RF_REST_PORT   GPIOA
#define RF_REST_BIT    GPIO_PIN_15
#define RF_REST_H      GPIO_SetBits(RF_REST_PORT,RF_REST_BIT)
#define RF_REST_L      GPIO_ResetBits(RF_REST_PORT,RF_REST_BIT)
     
#define RF_CE_PORT     GPIOA
#define RF_CE_BIT      GPIO_PIN_4
#define RF_CE_H        GPIO_SetBits(RF_CE_PORT,RF_CE_BIT)
#define RF_CE_L        GPIO_ResetBits(RF_CE_PORT,RF_CE_BIT)

#define RF_CKL_PORT    GPIOA
#define RF_CKL_BIT     GPIO_PIN_5
#define RF_CKL_H       GPIO_SetBits(RF_CKL_PORT,RF_CKL_BIT)
#define RF_CKL_L       GPIO_ResetBits(RF_CKL_PORT,RF_CKL_BIT)

#define RF_SDO_PORT    GPIOA
#define RF_SDO_BIT     GPIO_PIN_6
#define RF_SDO_DATA    GPIO_ReadInputDataBit(RF_SDO_PORT,RF_SDO_BIT)

#define RF_SDI_PORT    GPIOA
#define RF_SDI_BIT     GPIO_PIN_7
#define RF_SDI_H       GPIO_SetBits(RF_SDI_PORT,RF_SDI_BIT)
#define RF_SDI_L       GPIO_ResetBits(RF_SDI_PORT,RF_SDI_BIT)

#define RF_TX    
#define RF_RX     
     
#define RF_DIO0_PORT    GPIOB
#define RF_DIO0_BIT     GPIO_PIN_3

#define RF_DIO1_PORT    GPIOB
#define RF_DIO1_BIT     GPIO_PIN_4

#define GSM_RST_PORT    GPIOA
#define GSM_RST_BIT     GPIO_PIN_0
#define GSM_RST_H       GPIO_SetBits(GSM_RST_PORT,GSM_RST_BIT)
#define GSM_RST_L       GPIO_ResetBits(GSM_RST_PORT,GSM_RST_BIT)

#define GSM_PW_PORT    GPIOB
#define GSM_PW_BIT     GPIO_PIN_8
#define GSM_PW_H       GPIO_SetBits(GSM_PW_PORT,GSM_PW_BIT)
#define GSM_PW_L       GPIO_ResetBits(GSM_PW_PORT,GSM_PW_BIT)

#define GSM_ON_PORT    GPIOB
#define GSM_ON_BIT     GPIO_PIN_9
#define GSM_ON_H       GPIO_SetBits(GSM_ON_PORT,GSM_ON_BIT)
#define GSM_ON_L       GPIO_ResetBits(GSM_ON_PORT,GSM_ON_BIT)

#define GSM_STATUS_PORT  GPIOB
#define GSM_STATUS_BIT   GPIO_PIN_9
#define GSM_STATUS       GPIO_ReadInputDataBit(GSM_STATUS_PORT,GSM_STATUS_BIT)
     
#define XBEE_RST_PORT    GPIOA
#define XBEE_RST_BIT     GPIO_PIN_8
#define XBEE_RST_H       GPIO_SetBits(XBEE_RST_PORT,XBEE_RST_BIT)
#define XBEE_RST_L       GPIO_ResetBits(XBEE_RST_PORT,XBEE_RST_BIT)

#define XBEE_SLEEP_PORT    GPIOA
#define XBEE_SLEEP_BIT     GPIO_PIN_12
#define XBEE_SLEEP_H       GPIO_SetBits(XBEE_SLEEP_PORT,XBEE_SLEEP_BIT)
#define XBEE_SLEEP_L       GPIO_ResetBits(XBEE_SLEEP_PORT,XBEE_SLEEP_BIT)

     
/* USER CODE END Private defines */

void Init_GPIO(void);
extern void Init_XBEE_GPIO();
/* USER CODE BEGIN Prototypes */

/* USER CODE END Prototypes */

#ifdef __cplusplus
}
#endif
#endif /*__ pinoutConfig_H */

/**
  * @}
  */

/**
  * @}
  */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
