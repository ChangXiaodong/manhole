#include "common.h"

void EXTI2_3_IRQHandler(void)
{

  HAL_GPIO_EXTI_IRQHandler(RF_DIO0_BIT);

}

void EXTI4_15_IRQHandler(void)
{

  HAL_GPIO_EXTI_IRQHandler(RF_DIO1_BIT);

}

/**
* @brief This function handles Non maskable interrupt.
*/
void NMI_Handler(void)
{
}

/**
* @brief This function handles Hard fault interrupt.
*/
void HardFault_Handler(void)
{
  while (1)
  {
  }
}

/**
* @brief This function handles System service call via SWI instruction.
*/
void SVC_Handler(void)
{
}

/**
* @brief This function handles Pendable request for system service.
*/
void PendSV_Handler(void)
{
}

/**
* @brief This function handles System tick timer.
*/
void SysTick_Handler(void)
{
  HAL_IncTick();
  HAL_SYSTICK_IRQHandler();
}

