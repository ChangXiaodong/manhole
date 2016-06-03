#include "common.h"

uint8_t isCRCError();
uint8_t getSNRValue();
int16_t getRSSIValue();
uint8_t getPayloadSize();
uint8_t xbee_receive_count = 0;

static void rxIrqCallback()
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
    }
    
    RadioEvents.RxDone(RxBuffer);
}

static void txIrqCallback()
{
    // Clear Irq
    SX1276WriteBuffer( REG_LR_IRQFLAGS, RFLR_IRQFLAGS_TXDONE );
    // Intentional fall through
    SX1276.Settings.State = RF_IDLE;
    RadioEvents.TxDone();
}

uint8_t getSNRValue()
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

uint8_t getPayloadSize()
{
    return SX1276ReadBuffer( REG_LR_RXNBBYTES );
}

uint8_t isCRCError()
{
    uint8_t irqFlags = 0;
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


void EXTI3_IRQHandler(void)
{
    if(EXTI_GetITStatus(EXTI_Line3) != RESET)
    {
        switch( SX1276.Settings.State )
        {
        case RF_RX_RUNNING:
            rxIrqCallback();
            break;
        case RF_TX_RUNNING:
            txIrqCallback();
            break;
        }
        EXTI_ClearITPendingBit(EXTI_Line3);
    }
}

void EXTI4_IRQHandler(void)
{
  if(EXTI_GetITStatus(EXTI_Line4) != RESET)
  {
    EXTI_ClearITPendingBit(EXTI_Line4);
  }
}

void USART1_IRQHandler(void)
{
    uint8_t xbee_receive_buf = 0;
    if(USART_GetITStatus(USART1, USART_IT_RXNE) != RESET)
    {
        USART_ClearITPendingBit(USART1,USART_IT_RXNE);
        xbee_receive_buf = (uint8_t)USART_ReceiveData(USART1);
        if(xbee_receive_buf == 0x7E)
        {
            xbee_receive_count = 0;
            Xbee.values.ack = 1;
        }
        xbee_receive[xbee_receive_count++]=xbee_receive_buf;
        if(xbee_receive_count == 11)
        {
            xbee_receive_count = 0;
        }
    }
}

void USART2_IRQHandler(void)
{
    uint8_t gprs_receive_buf = 0;
    if(USART_GetITStatus(USART2, USART_IT_RXNE) != RESET)
    {
        USART_ClearITPendingBit(USART2,USART_IT_RXNE);
        gprs_receive_buf = (uint8_t)USART_ReceiveData(USART2);
        GPRS.receive[GPRS.receive_count++] = gprs_receive_buf;
        if(GPRS.receive_count == GPRS_RX_BUFFER_SIZE)
        {
            GPRS.receive_count = 0;
        }
    }
}

/**
  * @brief  This function handles NMI exception.
  * @param  None
  * @retval None
  */
void NMI_Handler(void)
{
}

/**
  * @brief  This function handles Hard Fault exception.
  * @param  None
  * @retval None
  */
void HardFault_Handler(void)
{
  /* Go to infinite loop when Hard Fault exception occurs */
  while (1)
  {
  }
}

/**
  * @brief  This function handles Memory Manage exception.
  * @param  None
  * @retval None
  */
void MemManage_Handler(void)
{
  /* Go to infinite loop when Memory Manage exception occurs */
  while (1)
  {
  }
}

/**
  * @brief  This function handles Bus Fault exception.
  * @param  None
  * @retval None
  */
void BusFault_Handler(void)
{
  /* Go to infinite loop when Bus Fault exception occurs */
  while (1)
  {
  }
}

/**
  * @brief  This function handles Usage Fault exception.
  * @param  None
  * @retval None
  */
void UsageFault_Handler(void)
{
  /* Go to infinite loop when Usage Fault exception occurs */
  while (1)
  {
  }
}

/**
  * @brief  This function handles SVCall exception.
  * @param  None
  * @retval None
  */
void SVC_Handler(void)
{
}

/**
  * @brief  This function handles Debug Monitor exception.
  * @param  None
  * @retval None
  */
void DebugMon_Handler(void)
{
}

/**
  * @brief  This function handles PendSVC exception.
  * @param  None
  * @retval None
  */
void PendSV_Handler(void)
{
}

/**
  * @brief  This function handles SysTick Handler.
  * @param  None
  * @retval None
  */
void SysTick_Handler(void)
{
}

/******************************************************************************/
/*                 STM32L1xx Peripherals Interrupt Handlers                   */
/*  Add here the Interrupt Handler for the used peripheral(s) (PPP), for the  */
/*  available peripheral interrupt handler's name please refer to the startup */
/*  file (startup_stm32l1xx_xx.s).                                            */
/******************************************************************************/

/**
  * @brief  This function handles PPP interrupt request.
  * @param  None
  * @retval None
  */
/*void PPP_IRQHandler(void)
{
}*/

/**
  * @}
  */ 


/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
