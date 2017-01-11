#ifndef __COMMON_H
#define __COMMON_H

#define FLASH_ADDRESS  0x08080100

#define bool  uint8_t
#define FALSE 0
#define TRUE  1

#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "stm32l1xx.h"
#include "stm32l1xx_it.h"
#include "delay.h"
#include "gpio.h"
#include "SX1276.H"
#include "sx1276Regs-LoRa.h"
#include "mac.h"
#include "schdule.h"
#include "ProcessEvent.h"
#include "xbee.h"
#include "gsm.h"
#include "interface.h"
#include "uart.h"

#define DISABLE_INTERRUPTS __disable_irq();
#define ENABLE_INTERRUPTS  __enable_irq(); 

#endif