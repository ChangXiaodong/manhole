/**
  ******************************************************************************
  * @file    Project/STM8L15x_StdPeriph_Template/stm8l15x_it.c
  * @author  MCD Application Team
  * @version V1.6.1
  * @date    30-September-2014
  * @brief   Main Interrupt Service Routines.
  *          This file provides template for all peripherals interrupt service routine.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; COPYRIGHT 2014 STMicroelectronics</center></h2>
  *
  * Licensed under MCD-ST Liberty SW License Agreement V2, (the "License");
  * You may not use this file except in compliance with the License.
  * You may obtain a copy of the License at:
  *
  *        http://www.st.com/software_license_agreement_liberty_v2
  *
  * Unless required by applicable law or agreed to in writing, software 
  * distributed under the License is distributed on an "AS IS" BASIS, 
  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  * See the License for the specific language governing permissions and
  * limitations under the License.
  *
  ******************************************************************************
  */

/* Includes ------------------------------------------------------------------*/
#include "stm8l15x_it.h"
#include "common.h"
/** @addtogroup STM8L15x_StdPeriph_Template
  * @{
  */
void rxIrqCallback();
void txIrqCallback();
uint8 isCRCError();
uint8 getSNRValue();
int16_t getRSSIValue();
uint8 getPayloadSize();
void rxTimeoutIrqCalback();
/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/
const struct RadioCallback_inferface RadioIrqCallback= 
{
    rxIrqCallback,
    txIrqCallback,
    rxTimeoutIrqCalback,
};
/* Private function  -----------------------------------------------*/
void rxIrqCallback()
{
    SX1276WriteBuffer( REG_LR_IRQFLAGS, RFLR_IRQFLAGS_RXDONE );
    if(isCRCError())
    {
        RadioEvents.RxError(); 
        return;
    }
    
    SX1276.PacketInfo.SnrValue = getSNRValue();
    SX1276.PacketInfo.RssiValue = getRSSIValue();
    SX1276.PacketInfo.Size = getPayloadSize();
    SX1276ReadFifo(RxBuffer,SX1276.PacketInfo.Size);

    if( SX1276.Settings.LoRa.RxContinuous == FALSE )
    {
        SX1276.Settings.State = RF_IDLE;
    }

    if(!Link.ifValid(RxBuffer))
    {
        RadioEvents.Invalid();
        return;
    }
    
    TQStruct task;
    switch(RxBuffer[8])
    {
    case DATA_PACK:
        task.event = RECEIVE_DATA_PACKET;
        memcpy(task.data, RxBuffer, SX1276.PacketInfo.Size);
        OS.postTask(task);
        break;
        
    case DATA_ACK_PACK:
        LED1_OFF;
        Protocol.ack_received = 1;
        task.event = RECEIVE_DATAACK_PACKET;
        memcpy(task.data, RxBuffer, SX1276.PacketInfo.Size);
        OS.postTask(task);
        break;
    }
    
    RadioEvents.RxDone(RxBuffer);
}
void txIrqCallback()
{
    // Clear Irq
    SX1276WriteBuffer( REG_LR_IRQFLAGS, RFLR_IRQFLAGS_TXDONE );
    // Intentional fall through
    SX1276.Settings.State = RF_IDLE;
    RadioEvents.TxDone();
}
void rxTimeoutIrqCalback()
{

    SX1276WriteBuffer( REG_LR_IRQFLAGS, RFLR_IRQFLAGS_RXTIMEOUT );
    Protocol.resend_times++;
    Protocol.send_failed = 1;
    
}
/* Private functions prototypes---------------------------------------------------------*/
/* Public functions ----------------------------------------------------------*/
uint8 isCRCError()
{
    uint8 irqFlags = 0;
    irqFlags=SX1276ReadBuffer( REG_LR_IRQFLAGS ); 
    if((irqFlags & RFLR_IRQFLAGS_PAYLOADCRCERROR_MASK)==
       RFLR_IRQFLAGS_PAYLOADCRCERROR)
    {
        SX1276WriteBuffer(REG_LR_IRQFLAGS,
                          RFLR_IRQFLAGS_PAYLOADCRCERROR);
        if( SX1276.Settings.LoRa.RxContinuous == FALSE)
        {
            SX1276.Settings.State = RF_IDLE;
        }
        return 1;
    }
    else
    {
        return 0;
    }
}

uint8 getSNRValue()
{
     return SX1276ReadBuffer(REG_LR_PKTSNRVALUE);
}

int16_t getRSSIValue()
{
    int8_t snr = 0;
    if(SX1276.PacketInfo.SnrValue & 0x80) // The SNR sign bit is 1
    {
        // Invert and divide by 4
        snr = ((~SX1276.PacketInfo.SnrValue 
                + 1) & 0xFF ) >> 2;
        snr = -snr;
    }
    else
    {
        // Divide by 4
        snr = (SX1276.PacketInfo.SnrValue & 
               0xFF ) >> 2;
    }
    int16_t rssi = SX1276ReadBuffer(REG_LR_PKTRSSIVALUE);
    if( snr < 0)
    {
        if(SX1276.Settings.Channel>RF_MID_BAND_THRESH)
        {
            return RSSI_OFFSET_HF + rssi + ( rssi >> 4 ) + snr;
        }
        else
        {
            return RSSI_OFFSET_LF + rssi + ( rssi >> 4 ) + snr;
        }
    }
    else
    {    
        if( SX1276.Settings.Channel > RF_MID_BAND_THRESH )
        {
            return RSSI_OFFSET_HF + rssi + ( rssi >> 4 );
        }
        else
        {
            return RSSI_OFFSET_LF + rssi + ( rssi >> 4 );
        }
    }
}

uint8 getPayloadSize()
{
    return SX1276ReadBuffer( REG_LR_RXNBBYTES );
}

#ifdef _COSMIC_
/**
  * @brief Dummy interrupt routine
  * @par Parameters:
  * None
  * @retval 
  * None
*/
INTERRUPT_HANDLER(NonHandledInterrupt,0)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}
#endif

/**
  * @brief TRAP interrupt routine
  * @par Parameters:
  * None
  * @retval 
  * None
*/
INTERRUPT_HANDLER_TRAP(TRAP_IRQHandler)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}
/**
  * @brief FLASH Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(FLASH_IRQHandler,1)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}
/**
  * @brief DMA1 channel0 and channel1 Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(DMA1_CHANNEL0_1_IRQHandler,2)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}
/**
  * @brief DMA1 channel2 and channel3 Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(DMA1_CHANNEL2_3_IRQHandler,3)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}
/**
  * @brief RTC / CSS_LSE Interrupt routine.
  * @param  None
  * @retval None
  */
uint8 send_t[]={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20};
uint16 time = 0;
INTERRUPT_HANDLER(RTC_CSSLSE_IRQHandler,4)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
    RTC_WakeUpCmd(DISABLE);
    
        
    TQStruct task;
    //task.event = COLLECT_DATA;
    //OS.postTask(task);
    
    RTC_ClearITPendingBit(RTC_IT_WUT);
    RTC_SetWakeUpCounter(80);
    RTC_WakeUpCmd(ENABLE);
    TEST1_TOGGLE;
    
    
    MpuGetData();
    UART_Send_Data(0x7D);
    UART_Send_Data(0x7E);
    UART_Send_Data(accelStruct.accelX>>8);
    UART_Send_Data(accelStruct.accelX);
    UART_Send_Data(accelStruct.accelY>>8);
    UART_Send_Data(accelStruct.accelY);
    UART_Send_Data(accelStruct.accelZ>>8);
    UART_Send_Data(accelStruct.accelZ);
    UART_Send_Data(gyroStruct.gyroX>>8);
    UART_Send_Data(gyroStruct.gyroX);
    UART_Send_Data(gyroStruct.gyroY>>8);
    UART_Send_Data(gyroStruct.gyroY);
    UART_Send_Data(gyroStruct.gyroZ>>8);
    UART_Send_Data(gyroStruct.gyroZ);
    
    time = GET_TIME3;
    RESET_TIME3;
    //SystemWake();
    //LED2_TOGGLE;
    //delay_ms(50);
    //getSensorData();
    //SystemSleep();
}
/**
  * @brief External IT PORTE/F and PVD Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(EXTIE_F_PVD_IRQHandler,5)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}

/**
  * @brief External IT PORTB / PORTG Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(EXTIB_G_IRQHandler,6)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}

/**
  * @brief External IT PORTD /PORTH Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(EXTID_H_IRQHandler,7)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}

/**
  * @brief External IT PIN0 Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(EXTI0_IRQHandler,8)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}

/**
  * @brief External IT PIN1 Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(EXTI1_IRQHandler,9)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
    if ((GPIO_ReadInputData(SX1276.DIO0.port) & SX1276.DIO0.pin) == 
    SX1276.DIO0.pin)
    {
        switch( SX1276.Settings.State )
        {
        case RF_RX_RUNNING:
            RadioIrqCallback.rxCallback();
            break;
        case RF_TX_RUNNING:
            RadioIrqCallback.txCallback();
            break;
        }
    }
    EXTI_ClearITPendingBit(EXTI_IT_Pin1);
}

/**
  * @brief External IT PIN2 Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(EXTI2_IRQHandler,10)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}

/**
  * @brief External IT PIN3 Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(EXTI3_IRQHandler,11)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}

/**
  * @brief External IT PIN4 Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(EXTI4_IRQHandler,12)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
    if ((GPIO_ReadInputData(SX1276.DIO1.port) & SX1276.DIO1.pin) == 
    SX1276.DIO1.pin)
    {
        RadioIrqCallback.timeoutCallback();
    }
    EXTI_ClearITPendingBit(EXTI_IT_Pin4);
}

/**
  * @brief External IT PIN5 Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(EXTI5_IRQHandler,13)
{
    /* In order to detect unexpected events during development,
    it is recommended to set a breakpoint on the following instruction.
    */
}

/**
  * @brief External IT PIN6 Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(EXTI6_IRQHandler,14)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */

}

/**
  * @brief External IT PIN7 Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(EXTI7_IRQHandler,15)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}
/**
  * @brief LCD /AES Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(LCD_AES_IRQHandler,16)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}
/**
  * @brief CLK switch/CSS/TIM1 break Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(SWITCH_CSS_BREAK_DAC_IRQHandler,17)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}

/**
  * @brief ADC1/Comparator Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(ADC1_COMP_IRQHandler,18)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}

/**
  * @brief TIM2 Update/Overflow/Trigger/Break /USART2 TX Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(TIM2_UPD_OVF_TRG_BRK_USART2_TX_IRQHandler,19)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}

/**
  * @brief Timer2 Capture/Compare / USART2 RX Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(TIM2_CC_USART2_RX_IRQHandler,20)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}


/**
  * @brief Timer3 Update/Overflow/Trigger/Break Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(TIM3_UPD_OVF_TRG_BRK_USART3_TX_IRQHandler,21)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}
/**
  * @brief Timer3 Capture/Compare /USART3 RX Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(TIM3_CC_USART3_RX_IRQHandler,22)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}
/**
  * @brief TIM1 Update/Overflow/Trigger/Commutation Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(TIM1_UPD_OVF_TRG_COM_IRQHandler,23)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}
/**
  * @brief TIM1 Capture/Compare Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(TIM1_CC_IRQHandler,24)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}

/**
  * @brief TIM4 Update/Overflow/Trigger Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(TIM4_UPD_OVF_TRG_IRQHandler,25)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}
/**
  * @brief SPI1 Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(SPI1_IRQHandler,26)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */		
}

/**
  * @brief USART1 TX / TIM5 Update/Overflow/Trigger/Break Interrupt  routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(USART1_TX_TIM5_UPD_OVF_TRG_BRK_IRQHandler,27)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}

/**
  * @brief USART1 RX / Timer5 Capture/Compare Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(USART1_RX_TIM5_CC_IRQHandler,28)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
    USART_ClearFlag(USART1,USART_FLAG_PE);
    
    if(USART_GetFlagStatus(USART1,USART_FLAG_RXNE))
    {

    }
}

/**
  * @brief I2C1 / SPI2 Interrupt routine.
  * @param  None
  * @retval None
  */
INTERRUPT_HANDLER(I2C1_SPI2_IRQHandler,29)
{
    /* In order to detect unexpected events during development,
       it is recommended to set a breakpoint on the following instruction.
    */
}
/**
  * @}
  */ 

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/