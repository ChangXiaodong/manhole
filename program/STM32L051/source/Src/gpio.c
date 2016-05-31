
#include "common.h"

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
    GSM_RST_H;
    
    GPIO_InitStruct.Pin = GSM_PW_BIT|GSM_ON_BIT;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(GSM_PW_PORT, &GPIO_InitStruct);
    GSM_ON_L;
    GSM_PW_H;
    
    GPIO_InitStruct.Pin = GSM_STATUS_BIT;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLDOWN;
    HAL_GPIO_Init(GSM_STATUS_PORT, &GPIO_InitStruct);
}

void Init_XBEE_GPIO()
{
    GPIO_InitTypeDef GPIO_InitStruct;
    GPIO_InitStruct.Pin = XBEE_RST_BIT|XBEE_SLEEP_BIT;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(XBEE_RST_PORT, &GPIO_InitStruct);
    XBEE_RST_H;
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
  Init_GSM();

  
}
