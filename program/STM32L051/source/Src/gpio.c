
#include "common.h"

static void Init_LORA()
{
    GPIO_InitTypeDef GPIO_InitStruct;
    GPIO_InitStruct.Pin = RF_REST_BIT|RF_CE_BIT|RF_CKL_BIT|RF_SDI_BIT;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(RF_SPI_PORT, &GPIO_InitStruct);
    GPIO_InitStruct.Pin = RF_SDO_BIT;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(RF_SPI_PORT, &GPIO_InitStruct);
    
    GPIO_InitStruct.Pin = RF_DIO0_BIT;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(RF_DIO0_PORT, &GPIO_InitStruct);
    HAL_NVIC_SetPriority(EXTI2_3_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(EXTI2_3_IRQn);
    
    GPIO_InitStruct.Pin = RF_DIO1_BIT;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(RF_DIO1_PORT, &GPIO_InitStruct);
    HAL_NVIC_SetPriority(EXTI4_15_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(EXTI4_15_IRQn);
}

static void Init_LED()
{
    GPIO_InitTypeDef GPIO_InitStruct;
    GPIO_InitStruct.Pin = LED1_BIT|LED2_BIT|LED3_BIT;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(LED_PORT, &GPIO_InitStruct);
    
    LED1_OFF;
    LED2_OFF;
    LED3_OFF;
}

static void Init_GSM()
{
    GPIO_InitTypeDef GPIO_InitStruct;
    GPIO_InitStruct.Pin = GSM_RST_BIT;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(GSM_RST_PORT, &GPIO_InitStruct);
    GSM_RST_L;
    
    GPIO_InitStruct.Pin = GSM_PW_BIT|GSM_ON_BIT;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(GSM_PW_PORT, &GPIO_InitStruct);
    GSM_ON_L;
    GSM_PW_L;
    
    GPIO_InitStruct.Pin = GSM_STATUS_BIT;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLDOWN;
    HAL_GPIO_Init(GSM_STATUS_PORT, &GPIO_InitStruct);
}

static void Init_XBEE()
{
    GPIO_InitTypeDef GPIO_InitStruct;
    GPIO_InitStruct.Pin = XBEE_RST_BIT|XBEE_SLEEP_BIT;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(XBEE_RST_PORT, &GPIO_InitStruct);
    XBEE_RST_L;
    XBEE_SLEEP_L;
}
void Init_GPIO(void)
{



  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();
  
  Init_LED();
  Init_LORA();
  Init_GSM();
  Init_XBEE();
  
}
