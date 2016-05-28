#ifndef __COMMON_H__
#define __COMMON_H__

#define FLASH_ADDRESS  0x08080100

typedef __INT8_T_TYPE__   int8;
typedef __UINT8_T_TYPE__ uint8;
typedef __INT16_T_TYPE__   int16;
typedef __UINT16_T_TYPE__ uint16;
typedef __INT32_T_TYPE__   int32;
typedef __UINT32_T_TYPE__ uint32;


#define bool  uint8
#define FALSE 0
#define TRUE  1

#include <math.h>
#include <string.h>
#include <stdlib.h>
#include "stm32l0xx_hal.h"
#include "stm32l0xx.h"
#include "stm32l0xx_it.h"
#include "usart.h"
#include "gpio.h"
#include "system.h"
#include "delay.h"
#include "SX1276.H"
#include "sx1276Regs-LoRa.h"
#include "interface.h"
#include "mac.h"
#include "schdule.h"
#include "ProcessEvent.h"

#define DISABLE_INTERRUPTS __disable_irq();
#define ENABLE_INTERRUPTS  __enable_irq(); 




#endif
