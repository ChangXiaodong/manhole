#include "common.h"
uint8 isCRCError();
uint8 getSNRValue();
int16_t getRSSIValue();
uint8 getPayloadSize();
uint8 xbee_receive_count = 0;
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


#if (XBEE_UART_RX_ENABLE)
void HAL_UART_RxCpltCallback(UART_HandleTypeDef* UartHandle)
{
    if(UartHandle->Instance==USART1){
        if(xbee_receive_buf == 0x7E)
        {
            xbee_receive_count = 0;
            Xbee.values.ack = 1;
        }
        xbee_receive[xbee_receive_count]=xbee_receive_buf;
        HAL_UART_Receive_IT(&huart1,&xbee_receive_buf,1);
        xbee_receive_count++;
        if(xbee_receive_count == 11)
        {
            xbee_receive_count = 0;
        }
    }
}
#endif

static void txIrqCallback()
{
    // Clear Irq
    SX1276WriteBuffer( REG_LR_IRQFLAGS, RFLR_IRQFLAGS_TXDONE );
    // Intentional fall through
    SX1276.Settings.State = RF_IDLE;
    RadioEvents.TxDone();
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

void EXTI2_3_IRQHandler(void)
{
    HAL_GPIO_EXTI_IRQHandler(RF_DIO0_BIT);
    
    switch( SX1276.Settings.State )
    {
    case RF_RX_RUNNING:
        rxIrqCallback();
        break;
    case RF_TX_RUNNING:
        txIrqCallback();
        break;
    }
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

/**
* @brief This function handles USART1 global interrupt / USART1 wake-up interrupt through EXTI line 25.
*/
void USART1_IRQHandler(void)
{
  /* USER CODE BEGIN USART1_IRQn 0 */

  /* USER CODE END USART1_IRQn 0 */
  HAL_UART_IRQHandler(&huart1);
  /* USER CODE BEGIN USART1_IRQn 1 */

  /* USER CODE END USART1_IRQn 1 */
}


