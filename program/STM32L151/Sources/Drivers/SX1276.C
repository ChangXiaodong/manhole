#include "common.h"

SX1276_t SX1276;
uint8_t RxBuffer[RX_BUFFER_SIZE];
States_t State = LOWPOWER;

void	PA_TXD_OUT(void)
{
    //RF_TXC_H;
}
void	PA_RXD_OUT(void)
{
    //RF_TXC_L;
}
void	PA_SEELP_OUT(void)
{
    //RF_TXC_L;
}

void SX1276Reset( void )
{
    RF_REST_H;	
    delay_ms(20);
    RF_REST_L;	
    delay_ms(20);
    RF_REST_H;	
    
}

void RF_SPI_MasterIO(uint8_t out)
{
    uint8_t i;
    for (i=0;i<8;i++)
    {   
        if ((out & 0x80)== 0x80)			/* check if MSB is high */
            RF_SDI_H;
        else
            RF_SDI_L;							/* if not, set to low */
        
        RF_CKL_H;						  /* toggle clock high */
        out = (out << 1);					/* shift 1 place for next bit */
        RF_CKL_L;							/* toggle clock low */
    }
}

uint8_t RF_SPI_READ_BYTE()
{	 
    
    uint8_t j;
    uint8_t i;
    j=0;
    for (i = 0; i < 8; i++)
    {	 
        RF_CKL_H; 
        j = (j << 1);						 // shift 1 place to the left or shift in 0 //
        if(RF_SDO_DATA)							 // check to see if bit is high //
            j = j | 0x01; 					   // if high, make bit high //
        // toggle clock high // 
        RF_CKL_L; 							 // toggle clock low //  
    }
    return j;								// toggle clock low //
}

void SX1276WriteBuffer( uint8_t addr, uint8_t buffer)
{ 
    RF_CE_L; 
    RF_SPI_MasterIO( addr | 0x80 );
    RF_SPI_MasterIO( buffer);
    RF_CE_H;
}

uint8_t SX1276ReadBuffer( uint8_t addr)
{
    uint8_t i;
    RF_CE_L; 
    RF_SPI_MasterIO( addr & 0x7F );
    i = RF_SPI_READ_BYTE();
    RF_CE_H; 
    return i; 
}

uint8_t SX1276LoRaSetOpMode( RFMode_SET opMode )
{
    uint8_t opModePrev;
    if(opMode == receive_single)
    {
        SX1276.Settings.State = RF_RX_RUNNING;
    }
    else
    {
        SX1276.Settings.State = opMode;
    }
    if( opMode == RFLR_OPMODE_TRANSMITTER )
    {
        RF_TX;
    }
    else
    {
        RF_RX;
    }
//    SX1276WriteBuffer( REG_OPMODE, ( SX1276ReadBuffer( REG_OPMODE ) & RF_OPMODE_MASK ) | opMode );
    
    opModePrev=SX1276ReadBuffer(REG_LR_OPMODE);
    opModePrev &=0xf8;
    opModePrev |= (uint8_t)opMode;
    SX1276WriteBuffer( REG_LR_OPMODE, opModePrev);
    return opModePrev;
    
}

void SX1276LoRaFsk( RadioModems_t opMode )
{
    uint8_t opModePrev;
    opModePrev=SX1276ReadBuffer(REG_LR_OPMODE);
    opModePrev &=0x7F;
    opModePrev |= (uint8_t)opMode;
    SX1276WriteBuffer( REG_LR_OPMODE, opModePrev);		
    
}

void SX1276LoRaSetRFFrequency(uint8_t FrequencyADD )
{
//    SX1276WriteBuffer( REG_LR_FRFMSB, Frequency[0]);
//    SX1276WriteBuffer( REG_LR_FRFMID, Frequency[1]);
//    SX1276WriteBuffer( REG_LR_FRFLSB, Frequency[2]);
}

void SX1276LoRa_CAL_OMM(void)
{
    uint8_t opModePrev;
    opModePrev=SX1276ReadBuffer(0x31);
    opModePrev &=0x7f;
    SX1276WriteBuffer(0x31,opModePrev);
}

void SX1276LoRaSetRFPower (void)
{
    
    SX1276WriteBuffer( REG_LR_PADAC, 0x87);
    
    SX1276WriteBuffer( REG_LR_PACONFIG, 0X8F);
}

void SX1276LoRaSetNbTrigPeaks( uint8_t value )
{
    uint8_t RECVER_DAT;
    RECVER_DAT = SX1276ReadBuffer( 0x31);
    RECVER_DAT = ( RECVER_DAT & 0xF8 ) | value;
    SX1276WriteBuffer( 0x31, RECVER_DAT );
}

void SX1276LoRaSetSpreadingFactor( uint8_t factor )
{
    uint8_t RECVER_DAT;
    
    SX1276LoRaSetNbTrigPeaks( 3 );
    
    RECVER_DAT=SX1276ReadBuffer( REG_LR_MODEMCONFIG2);	  
    RECVER_DAT = ( RECVER_DAT & RFLR_MODEMCONFIG2_SF_MASK ) | ( factor << 4 );
    SX1276WriteBuffer( REG_LR_MODEMCONFIG2, RECVER_DAT );	 
}



void SX1276LoRaSetErrorCoding( uint8_t value )
{	
    uint8_t RECVER_DAT;
    RECVER_DAT=SX1276ReadBuffer( REG_LR_MODEMCONFIG1);
    RECVER_DAT = ( RECVER_DAT & RFLR_MODEMCONFIG1_CODINGRATE_MASK ) | ( value << 1 );
    SX1276WriteBuffer( REG_LR_MODEMCONFIG1, RECVER_DAT); 
}

void SX1276LoRaSetPacketCrcOn( bool enable )
{	
    uint8_t RECVER_DAT;
    RECVER_DAT= SX1276ReadBuffer( REG_LR_MODEMCONFIG2);
    RECVER_DAT = ( RECVER_DAT & RFLR_MODEMCONFIG2_RXPAYLOADCRC_MASK ) | ( enable << 2 );
    SX1276WriteBuffer( REG_LR_MODEMCONFIG2, RECVER_DAT );
}

void SX1276LoRaSetSignalBandwidth( uint8_t bw )
{
    uint8_t RECVER_DAT;
    RECVER_DAT=SX1276ReadBuffer( REG_LR_MODEMCONFIG1);
    RECVER_DAT = ( RECVER_DAT & RFLR_MODEMCONFIG1_BW_MASK ) | ( bw << 4 );
    SX1276WriteBuffer( REG_LR_MODEMCONFIG1, RECVER_DAT );
    
}

void SX1276LoRaSetImplicitHeaderOn( bool enable )
{
    uint8_t RECVER_DAT;
    RECVER_DAT=SX1276ReadBuffer( REG_LR_MODEMCONFIG1 );
    RECVER_DAT = ( RECVER_DAT & RFLR_MODEMCONFIG1_IMPLICITHEADER_MASK ) | ( enable );
    SX1276WriteBuffer( REG_LR_MODEMCONFIG1, RECVER_DAT );
}

void SX1276LoRaSetSymbTimeout( uint16_t value )
{
    uint8_t RECVER_DAT[2];
    RECVER_DAT[0]=SX1276ReadBuffer( REG_LR_MODEMCONFIG2 );
    RECVER_DAT[1]=SX1276ReadBuffer( REG_LR_SYMBTIMEOUTLSB );
    
    RECVER_DAT[0] = ( RECVER_DAT[0] & RFLR_MODEMCONFIG2_SYMBTIMEOUTMSB_MASK ) | ( ( value >> 8 ) & ~RFLR_MODEMCONFIG2_SYMBTIMEOUTMSB_MASK );
    RECVER_DAT[1] = value & 0xFF;
    SX1276WriteBuffer( REG_LR_MODEMCONFIG2, RECVER_DAT[0]);
    SX1276WriteBuffer( REG_LR_SYMBTIMEOUTLSB, RECVER_DAT[1]);
}

void SX1276LoRaSetPayloadLength( uint8_t value )
{
    
    SX1276WriteBuffer( REG_LR_PAYLOADLENGTH, value );
} 

void SX1276LoRaSetPreamLength( uint16_t value )
{
    uint8_t a[2];
    a[0]=(value&0xff00)>>8;
    a[1]=value&0xff;
    
    SX1276WriteBuffer( REG_LR_PREAMBLEMSB, a[0] );  
    SX1276WriteBuffer( REG_LR_PREAMBLELSB, a[1] );
}

void SX1276LoRaSetMobileNode( bool enable )
{	 
    uint8_t RECVER_DAT;
    RECVER_DAT=SX1276ReadBuffer( REG_LR_MODEMCONFIG3 );
    RECVER_DAT = ( RECVER_DAT & RFLR_MODEMCONFIG3_MOBILE_NODE_MASK ) | ( enable << 3 );
    SX1276WriteBuffer( REG_LR_MODEMCONFIG3, RECVER_DAT );
}

void SX1276SetChannel( uint32_t freq )
{
    SX1276.Settings.Channel = freq;
    freq = ( uint32_t )( ( double )freq / ( double )FREQ_STEP );
    SX1276WriteBuffer( REG_LR_FRFMSB, ( uint8_t )( ( freq >> 16 ) & 0xFF ) );
    SX1276WriteBuffer( REG_LR_FRFMID, ( uint8_t )( ( freq >> 8 ) & 0xFF ) );
    SX1276WriteBuffer( REG_LR_FRFLSB, ( uint8_t )( freq & 0xFF ) );
}

static void RxChainCalibration( void )
{
    uint8_t regPaConfigInitVal;
    double initialFreq;
    // Service settings
    #define REG_IMAGECAL                                0x3B
    #define RF_IMAGECAL_IMAGECAL_MASK                   0xBF
    #define RF_IMAGECAL_IMAGECAL_START                  0x40
    #define RF_IMAGECAL_IMAGECAL_RUNNING                0x20
    
    // Save context
    regPaConfigInitVal = SX1276ReadBuffer( REG_LR_PACONFIG );
    initialFreq = ( double )( ( ( uint32_t )SX1276ReadBuffer( REG_LR_FRFMSB ) << 16 ) |
                              ( ( uint32_t )SX1276ReadBuffer( REG_LR_FRFMID ) << 8 ) |
                              ( ( uint32_t )SX1276ReadBuffer( REG_LR_FRFLSB ) ) ) * ( double )FREQ_STEP;

    // Cut the PA just in case, RFO output, power = -1 dBm
    SX1276WriteBuffer( REG_LR_PACONFIG, 0x00 );

    // Launch Rx chain calibration for LF band
    SX1276WriteBuffer( REG_IMAGECAL, ( SX1276ReadBuffer( REG_IMAGECAL ) & RF_IMAGECAL_IMAGECAL_MASK ) | RF_IMAGECAL_IMAGECAL_START );
    while( ( SX1276ReadBuffer( REG_IMAGECAL ) & RF_IMAGECAL_IMAGECAL_RUNNING ) == RF_IMAGECAL_IMAGECAL_RUNNING )
    {
    }

    // Sets a Frequency in HF band
    SX1276SetChannel( 868000000 );

    // Launch Rx chain calibration for HF band 
    SX1276WriteBuffer( REG_IMAGECAL, ( SX1276ReadBuffer( REG_IMAGECAL ) & RF_IMAGECAL_IMAGECAL_MASK ) | RF_IMAGECAL_IMAGECAL_START );
    while( ( SX1276ReadBuffer( REG_IMAGECAL ) & RF_IMAGECAL_IMAGECAL_RUNNING ) == RF_IMAGECAL_IMAGECAL_RUNNING )
    {
    }

    // Restore context
    SX1276WriteBuffer( REG_LR_PACONFIG, regPaConfigInitVal );
    SX1276SetChannel((uint32_t)initialFreq );
}

void SX1276LORA_INT(void)
{
//    SX1276Reset();
//    SX1276LoRaSetOpMode(Sleep_mode);  //设置睡眠模式
//    SX1276LoRaFsk(MODEM_LORA);		   // 设置扩频模式
//    SX1276LoRaSetOpMode(Stdby_mode);  // 设置为普通模式
//    SX1276WriteBuffer( REG_LR_DIOMAPPING1,GPIO_VARE_1);
//    SX1276WriteBuffer( REG_LR_DIOMAPPING2,GPIO_VARE_2);
//    SX1276LoRaSetRFFrequency(0);
//    SX1276LoRaSetRFPower();
//    SX1276LoRaSetSpreadingFactor(SpreadingFactor);			 // 扩频因子设置
//    SX1276LoRaSetErrorCoding(2);				//有效数据比
//    SX1276LoRaSetPacketCrcOn( TRUE);			 //CRC 校验打开
//    SX1276LoRaSetSignalBandwidth( Bw_Frequency );			//设置扩频带宽
//    SX1276LoRaSetImplicitHeaderOn( FALSE);		 //同步头是显性模式
//    SX1276LoRaSetPayloadLength( 0xff);
//    SX1276LoRaSetSymbTimeout( 0x3FF );
//    SX1276LoRaSetMobileNode(TRUE ); 			// 低数据的优化
//    RF_RECEIVE();
    
}

void FUN_RF_SENDPACKET(uint8_t *RF_TRAN_P,uint8_t LEN)
{
//    uint8_t ASM_i;
//    uint8_t ASM_ADD=0;
//    
//    PA_TXD_OUT();
//    
//    SX1276LoRaSetOpMode( Stdby_mode );
//    SX1276WriteBuffer( REG_LR_HOPPERIOD, 0 );	//不做频率跳变
//    
//    SX1276WriteBuffer(REG_LR_IRQFLAGSMASK,IRQN_TXD_Value);	//打开发送中断
//    
//    SX1276WriteBuffer( REG_LR_PAYLOADLENGTH, LEN+2);	 //最大数据包
//    
//    SX1276WriteBuffer( REG_LR_FIFOTXBASEADDR, 0);
//    
//    SX1276WriteBuffer( REG_LR_FIFOADDRPTR, 0 );
//    RF_CE_L;
//    RF_SPI_MasterIO( 0x80 );
//    
////    RF_SPI_MasterIO( Network_ID_H );
//    for( ASM_i = 0; ASM_i < LEN; ASM_i++ )
//    {
//        RF_SPI_MasterIO( *RF_TRAN_P );
//        ASM_ADD +=*RF_TRAN_P;
//        RF_TRAN_P++;
//        if(RF_TRAN_P==TX_RF_DATAEND)
//        {
//            RF_TRAN_P  =TX_RF_DATAIN;
//        }
//    }
//    RF_SPI_MasterIO( ASM_ADD );
//    
//    RF_CE_H;
//    
//    SX1276WriteBuffer(REG_LR_DIOMAPPING1,0x40);
//    
//    SX1276WriteBuffer(REG_LR_DIOMAPPING2,0x00);
//    
//    SX1276LoRaSetOpMode( Transmitter_mode );
    
}

void RF_RECEIVE (void)
{
    
    SX1276LoRaSetOpMode( Stdby_mode );
    SX1276WriteBuffer(REG_LR_IRQFLAGSMASK,IRQN_RXD_Value);  
    SX1276WriteBuffer( REG_LR_DIOMAPPING1, 0X00 );
    SX1276WriteBuffer( REG_LR_DIOMAPPING2, 0X00 );	
    SX1276LoRaSetOpMode( Receiver_mode );
    PA_RXD_OUT();
}

static void SX1276SetModem( RadioModems_t modem )
{
    if( SX1276.Settings.Modem == modem )
    {
        return;
    }
    SX1276.Settings.Modem = modem;
    SX1276LoRaSetOpMode(Sleep_mode);
    SX1276LoRaFsk(MODEM_LORA);
    SX1276LoRaSetOpMode(Stdby_mode);
    SX1276WriteBuffer( REG_LR_DIOMAPPING1,GPIO_VARE_1);
    SX1276WriteBuffer( REG_LR_DIOMAPPING2,GPIO_VARE_2);
}

void Set_SCK()
{
    GPIO_SetBits(SX1276.SCK.port, SX1276.SCK.pin);
}
void Reset_SCK()
{
    GPIO_ResetBits(SX1276.SCK.port, SX1276.SCK.pin);
}
void Set_MISO()
{
    GPIO_SetBits(SX1276.MISO.port, SX1276.MISO.pin);
}
void Reset_MISO()
{
    GPIO_ResetBits(SX1276.MISO.port, SX1276.MISO.pin);
}
uint8_t Get_MISO()
{
    return GPIO_ReadInputDataBit(SX1276.MISO.port,SX1276.MISO.pin);
}
void Set_MOSI()
{
    GPIO_SetBits(SX1276.MOSI.port, SX1276.MOSI.pin);
}
void Reset_MOSI()
{
    GPIO_ResetBits(SX1276.MOSI.port, SX1276.MOSI.pin);
}
void Set_NSS()
{
    GPIO_SetBits(SX1276.NSS.port, SX1276.NSS.pin);
}
void Reset_NSS()
{
    GPIO_ResetBits(SX1276.NSS.port, SX1276.NSS.pin);
}
void Set_Reset()
{
    GPIO_SetBits(SX1276.Reset.port, SX1276.Reset.pin);
}
void Reset_Reset()
{
    GPIO_ResetBits(SX1276.Reset.port, SX1276.Reset.pin);
}

void Set_RxTx()
{
    GPIO_SetBits(SX1276.RxTx.port, SX1276.RxTx.pin);
}
void Reset_RxTx()
{
    GPIO_ResetBits(SX1276.RxTx.port, SX1276.RxTx.pin);
}



static void clearSettings()
{
    SX1276.Settings.Modem = MODEM_FSK;
    SX1276.Settings.State = RF_SLEEP;
    SX1276.Settings.Channel = 0;
    SX1276.Settings.sta_cmd = 0;
    SX1276.Settings.Address = 0;
    SX1276.Settings.LoRa.Bandwidth = 0;
    SX1276.Settings.LoRa.Coderate = 0;
    SX1276.Settings.LoRa.CrcOn = FALSE;
    SX1276.Settings.LoRa.Datarate = 0;
    SX1276.Settings.LoRa.FixLen = FALSE;
    SX1276.Settings.LoRa.FreqHopOn = FALSE;
    SX1276.Settings.LoRa.HopPeriod = 0;
    SX1276.Settings.LoRa.IqInverted = FALSE;
    SX1276.Settings.LoRa.LowDatarateOptimize = FALSE;
    SX1276.Settings.LoRa.PayloadLen = 0;
    SX1276.Settings.LoRa.Power = 0;
    SX1276.Settings.LoRa.PreambleLen = 0;
    SX1276.Settings.LoRa.RxContinuous = FALSE;
    SX1276.Settings.LoRa.TxTimeout = 0;
}

void  SX1276Init()
{
    Init_LORA_SPI();
    clearSettings();
    SX1276Reset();
    RxChainCalibration();
    SX1276SetModem( MODEM_LORA ); 
    SX1276.Settings.State = RF_IDLE;

}

int16_t SX1276ReadRssi()
{
    int16_t rssi = 0;

    if( SX1276.Settings.Channel > RF_MID_BAND_THRESH )
    {
        rssi = RSSI_OFFSET_HF + SX1276ReadBuffer( REG_LR_RSSIVALUE );
    }
    else
    {
        rssi = RSSI_OFFSET_LF + SX1276ReadBuffer( REG_LR_RSSIVALUE );
    }
    return rssi;
}

bool SX1276IsChannelFree(int16_t rssiThresh )
{
    int16_t rssi = 0;
    RadioModems_t modem = MODEM_LORA;
    
    SX1276SetModem( modem );

    SX1276SetChannel( SX1276.Settings.Channel );
    
    SX1276LoRaSetOpMode(Receiver_mode);

    delay_1ms();
    
    rssi = SX1276ReadRssi();
    
    SX1276LoRaSetOpMode(Sleep_mode);
    
    if( rssi > rssiThresh )
    {
        return FALSE;
    }
    return TRUE;
}

RadioState_t SX1276GetState( void )
{
    return SX1276.Settings.State;
}

void SX1276SetRxConfig( RadioModems_t modem, uint32_t bandwidth,
                         uint32_t datarate, uint8_t coderate,
                         uint16_t preambleLen,
                         uint16_t symbTimeout, bool fixLen,
                         uint8_t payloadLen,
                         bool crcOn, bool freqHopOn, uint8_t hopPeriod,
                         bool iqInverted, bool rxContinuous )
{
    SX1276SetModem( modem );

    if( bandwidth > 2 )
    {
        // Fatal error: When using LoRa modem only bandwidths 125, 250 and 500 kHz are supported
        while( 1 );
    }
    bandwidth += 7;
    SX1276.Settings.LoRa.Bandwidth = bandwidth;
    SX1276.Settings.LoRa.Datarate = datarate;
    SX1276.Settings.LoRa.Coderate = coderate;
    SX1276.Settings.LoRa.FixLen = fixLen;
    SX1276.Settings.LoRa.PayloadLen = payloadLen;
    SX1276.Settings.LoRa.CrcOn = crcOn;
    SX1276.Settings.LoRa.FreqHopOn = freqHopOn;
    SX1276.Settings.LoRa.HopPeriod = hopPeriod;
    SX1276.Settings.LoRa.IqInverted = iqInverted;
    SX1276.Settings.LoRa.RxContinuous = rxContinuous;

    if( datarate > 12 )
    {
        datarate = 12;
    }
    else if( datarate < 6 )
    {
        datarate = 6;
    }

    if( ( ( bandwidth == 7 ) && ( ( datarate == 11 ) || ( datarate == 12 ) ) ) ||
        ( ( bandwidth == 8 ) && ( datarate == 12 ) ) )
    {
        SX1276.Settings.LoRa.LowDatarateOptimize = 0x01;
    }
    else
    {
        SX1276.Settings.LoRa.LowDatarateOptimize = 0x00;
    }

    SX1276WriteBuffer( REG_LR_MODEMCONFIG1, 
                 ( SX1276ReadBuffer( REG_LR_MODEMCONFIG1 ) &
                   RFLR_MODEMCONFIG1_BW_MASK &
                   RFLR_MODEMCONFIG1_CODINGRATE_MASK &
                   RFLR_MODEMCONFIG1_IMPLICITHEADER_MASK ) |
                   ( bandwidth << 4 ) | ( coderate << 1 ) | 
                   fixLen );
                
    SX1276WriteBuffer( REG_LR_MODEMCONFIG2,
                 ( SX1276ReadBuffer( REG_LR_MODEMCONFIG2 ) &
                   RFLR_MODEMCONFIG2_SF_MASK &
                   RFLR_MODEMCONFIG2_RXPAYLOADCRC_MASK &
                   RFLR_MODEMCONFIG2_SYMBTIMEOUTMSB_MASK ) |
                   ( datarate << 4 ) | ( crcOn << 2 ) |
                   ( ( symbTimeout >> 8 ) & ~RFLR_MODEMCONFIG2_SYMBTIMEOUTMSB_MASK ) );

    SX1276WriteBuffer( REG_LR_MODEMCONFIG3, 
                 ( SX1276ReadBuffer( REG_LR_MODEMCONFIG3 ) &
                   RFLR_MODEMCONFIG3_LOWDATARATEOPTIMIZE_MASK ) |
                   ( SX1276.Settings.LoRa.LowDatarateOptimize << 3 ) );

    SX1276WriteBuffer( REG_LR_SYMBTIMEOUTLSB, ( uint8_t )( symbTimeout & 0xFF ) );
    
    SX1276WriteBuffer( REG_LR_PREAMBLEMSB, ( uint8_t )( ( preambleLen >> 8 ) & 0xFF ) );
    SX1276WriteBuffer( REG_LR_PREAMBLELSB, ( uint8_t )( preambleLen & 0xFF ) );

    if( fixLen == 1 )
    {
        SX1276WriteBuffer( REG_LR_PAYLOADLENGTH, payloadLen );
    }

    if( SX1276.Settings.LoRa.FreqHopOn == TRUE )
    {
        SX1276WriteBuffer( REG_LR_PLLHOP, ( SX1276ReadBuffer( REG_LR_PLLHOP ) & RFLR_PLLHOP_FASTHOP_MASK ) | RFLR_PLLHOP_FASTHOP_ON );
        SX1276WriteBuffer( REG_LR_HOPPERIOD, SX1276.Settings.LoRa.HopPeriod );
    }

    if( ( bandwidth == 9 ) && ( RF_MID_BAND_THRESH ) )
    {
        // ERRATA 2.1 - Sensitivity Optimization with a 500 kHz Bandwidth 
        SX1276WriteBuffer( REG_LR_TEST36, 0x02 );
        SX1276WriteBuffer( REG_LR_TEST3A, 0x64 );
    }
    else if( bandwidth == 9 )
    {
        // ERRATA 2.1 - Sensitivity Optimization with a 500 kHz Bandwidth
        SX1276WriteBuffer( REG_LR_TEST36, 0x02 );
        SX1276WriteBuffer( REG_LR_TEST3A, 0x7F );
    }
    else
    {
        // ERRATA 2.1 - Sensitivity Optimization with a 500 kHz Bandwidth
        SX1276WriteBuffer( REG_LR_TEST36, 0x03 );
    }
    
    if( datarate == 6 )
    {
        SX1276WriteBuffer( REG_LR_DETECTOPTIMIZE, 
                     ( SX1276ReadBuffer( REG_LR_DETECTOPTIMIZE ) &
                       RFLR_DETECTIONOPTIMIZE_MASK ) |
                       RFLR_DETECTIONOPTIMIZE_SF6 );
        SX1276WriteBuffer( REG_LR_DETECTIONTHRESHOLD, 
                     RFLR_DETECTIONTHRESH_SF6 );
    }
    else
    {
        SX1276WriteBuffer( REG_LR_DETECTOPTIMIZE,
                     ( SX1276ReadBuffer( REG_LR_DETECTOPTIMIZE ) &
                     RFLR_DETECTIONOPTIMIZE_MASK ) |
                     RFLR_DETECTIONOPTIMIZE_SF7_TO_SF12 );
        SX1276WriteBuffer( REG_LR_DETECTIONTHRESHOLD, 
                     RFLR_DETECTIONTHRESH_SF7_TO_SF12 );
    }
}

uint8_t SX1276GetPaSelect( uint32_t channel )
{
    if( channel > RF_MID_BAND_THRESH )
    {
        return RFLR_PACONFIG_PASELECT_PABOOST;
    }
    else
    {
        return RFLR_PACONFIG_PASELECT_RFO;
    }
}

void SX1276SetPower(int8_t power,uint8_t PA_enable)
{
    uint8_t paConfig = 0;
    uint8_t paDac = 0;
    
    paConfig = SX1276ReadBuffer( REG_LR_PACONFIG );
    paDac = SX1276ReadBuffer( REG_LR_PADAC );
    paConfig = ( paConfig & RFLR_PACONFIG_PASELECT_MASK );   
    paConfig = ( paConfig & RFLR_PACONFIG_MAX_POWER_MASK ) | 0x70;
    if(PA_enable)
    {
        paConfig |= 0x80;        
    }
    
    if( ( paConfig & RFLR_PACONFIG_PASELECT_PABOOST ) == RFLR_PACONFIG_PASELECT_PABOOST )
    {
        if( power > 17 )
        {
            paDac = ( paDac & RFLR_PADAC_20DBM_MASK ) | RFLR_PADAC_20DBM_ON;
        }
        else
        {
            paDac = ( paDac & RFLR_PADAC_20DBM_MASK ) | RFLR_PADAC_20DBM_OFF;
        }
        if( ( paDac & RFLR_PADAC_20DBM_ON ) == RFLR_PADAC_20DBM_ON )
        {
            if( power < 5 )
            {
                power = 5;
            }
            if( power > 20 )
            {
                power = 20;
            }
            paConfig = ( paConfig & RFLR_PACONFIG_OUTPUTPOWER_MASK ) | ( uint8_t )( ( uint16_t )( power - 5 ) & 0x0F );
        }
        else
        {
            if( power < 2 )
            {
                power = 2;
            }
            if( power > 17 )
            {
                power = 17;
            }
            paConfig = ( paConfig & RFLR_PACONFIG_OUTPUTPOWER_MASK ) | ( uint8_t )( ( uint16_t )( power - 2 ) & 0x0F );
        }
    }
    else
    {
        if( power < -1 )
        {
            power = -1;
        }
        if( power > 14 )
        {
            power = 14;
        }
        paConfig = ( paConfig & RFLR_PACONFIG_OUTPUTPOWER_MASK ) | ( uint8_t )( ( uint16_t )( power + 1 ) & 0x0F );
    }
    SX1276WriteBuffer( REG_LR_PACONFIG, paConfig );
    SX1276WriteBuffer( REG_LR_PADAC, paDac );
    SX1276.Settings.LoRa.Power = power;
}


void SX1276SetTxConfig( RadioModems_t modem, int8_t power, uint8_t PA_enable, 
                        uint32_t bandwidth, uint32_t datarate,
                        uint8_t coderate, uint16_t preambleLen,
                        bool fixLen, bool crcOn, bool freqHopOn, 
                        uint8_t hopPeriod, bool iqInverted, uint32_t timeout )
{


    SX1276SetModem( modem );
    SX1276SetPower( power,PA_enable);   
    
    if( bandwidth > 2 )
    {
        // Fatal error: When using LoRa modem only bandwidths 125, 250 and 500 kHz are supported
        while( 1 );
    }
    bandwidth += 7;
    SX1276.Settings.LoRa.Bandwidth = bandwidth;
    SX1276.Settings.LoRa.Datarate = datarate;
    SX1276.Settings.LoRa.Coderate = coderate;
    SX1276.Settings.LoRa.PreambleLen = preambleLen;
    SX1276.Settings.LoRa.FixLen = fixLen;
    SX1276.Settings.LoRa.FreqHopOn = freqHopOn;
    SX1276.Settings.LoRa.HopPeriod = hopPeriod;
    SX1276.Settings.LoRa.CrcOn = crcOn;
    SX1276.Settings.LoRa.IqInverted = iqInverted;
    SX1276.Settings.LoRa.TxTimeout = timeout;

    if( datarate > 12 )
    {
        datarate = 12;
    }
    else if( datarate < 6 )
    {
        datarate = 6;
    }
    if( (( bandwidth == 7 ) && (( datarate == 11 )||( datarate == 12 ))) ||
        (( bandwidth == 8 ) && (datarate == 12)))
    {
        SX1276.Settings.LoRa.LowDatarateOptimize = 0x01;
    }
    else
    {
        SX1276.Settings.LoRa.LowDatarateOptimize = 0x00;
    }

    if( SX1276.Settings.LoRa.FreqHopOn == TRUE )
    {
        SX1276WriteBuffer( REG_LR_PLLHOP, ( SX1276ReadBuffer( REG_LR_PLLHOP ) & RFLR_PLLHOP_FASTHOP_MASK ) | RFLR_PLLHOP_FASTHOP_ON );
        SX1276WriteBuffer( REG_LR_HOPPERIOD, SX1276.Settings.LoRa.HopPeriod );
    }

    SX1276WriteBuffer( REG_LR_MODEMCONFIG1, 
                 ( SX1276ReadBuffer( REG_LR_MODEMCONFIG1 ) &
                   RFLR_MODEMCONFIG1_BW_MASK &
                   RFLR_MODEMCONFIG1_CODINGRATE_MASK &
                   RFLR_MODEMCONFIG1_IMPLICITHEADER_MASK ) |
                   ( bandwidth << 4 ) | ( coderate << 1 ) | 
                   fixLen );
    
    SX1276WriteBuffer( REG_LR_MODEMCONFIG2,
                 ( SX1276ReadBuffer( REG_LR_MODEMCONFIG2 ) &
                   RFLR_MODEMCONFIG2_SF_MASK &
                   RFLR_MODEMCONFIG2_RXPAYLOADCRC_MASK ) |
                   ( datarate << 4 ) | ( crcOn << 2 ) );

    SX1276WriteBuffer( REG_LR_MODEMCONFIG3, 
                 ( SX1276ReadBuffer( REG_LR_MODEMCONFIG3 ) &
                   RFLR_MODEMCONFIG3_LOWDATARATEOPTIMIZE_MASK ) |
                   ( SX1276.Settings.LoRa.LowDatarateOptimize << 3 ) );

    SX1276WriteBuffer( REG_LR_PREAMBLEMSB, ( preambleLen >> 8 ) & 0x00FF );
    SX1276WriteBuffer( REG_LR_PREAMBLELSB, preambleLen & 0xFF );
    
    if( datarate == 6 )
    {
        SX1276WriteBuffer( REG_LR_DETECTOPTIMIZE, 
                     ( SX1276ReadBuffer( REG_LR_DETECTOPTIMIZE ) &
                       RFLR_DETECTIONOPTIMIZE_MASK ) |
                       RFLR_DETECTIONOPTIMIZE_SF6 );
        SX1276WriteBuffer( REG_LR_DETECTIONTHRESHOLD, 
                     RFLR_DETECTIONTHRESH_SF6 );
    }
    else
    {
        SX1276WriteBuffer( REG_LR_DETECTOPTIMIZE,
                     ( SX1276ReadBuffer( REG_LR_DETECTOPTIMIZE ) &
                     RFLR_DETECTIONOPTIMIZE_MASK ) |
                     RFLR_DETECTIONOPTIMIZE_SF7_TO_SF12 );
        SX1276WriteBuffer( REG_LR_DETECTIONTHRESHOLD, 
                     RFLR_DETECTIONTHRESH_SF7_TO_SF12 );
    }
    
}

uint32_t SX1276GetTimeOnAir( RadioModems_t modem, uint8_t pktLen )
{
    uint32_t airTime = 0;
    double bw = 0.0;
    // REMARK: When using LoRa modem only bandwidths 125, 250 and 500 kHz are supported
    switch( SX1276.Settings.LoRa.Bandwidth )
    {
    //case 0: // 7.8 kHz
    //    bw = 78e2;
    //    break;
    //case 1: // 10.4 kHz
    //    bw = 104e2;
    //    break;
    //case 2: // 15.6 kHz
    //    bw = 156e2;
    //    break;
    //case 3: // 20.8 kHz
    //    bw = 208e2;
    //    break;
    //case 4: // 31.2 kHz
    //    bw = 312e2;
    //    break;
    //case 5: // 41.4 kHz
    //    bw = 414e2;
    //    break;
    //case 6: // 62.5 kHz
    //    bw = 625e2;
    //    break;
    case 7: // 125 kHz
        bw = 125e3;
        break;
    case 8: // 250 kHz
        bw = 250e3;
        break;
    case 9: // 500 kHz
        bw = 500e3;
        break;
    }

    // Symbol rate : time for one symbol (secs)
    double rs = bw / ( 1 << SX1276.Settings.LoRa.Datarate );
    double ts = 1 / rs;
    // time of preamble
    double tPreamble = ( SX1276.Settings.LoRa.PreambleLen + 4.25 ) * ts;
    // Symbol length of payload and time
    double tmp = ceil( ( 8 * pktLen - 4 * SX1276.Settings.LoRa.Datarate +
                         28 + 16 * SX1276.Settings.LoRa.CrcOn -
                         ( SX1276.Settings.LoRa.FixLen ? 20 : 0 ) ) /
                         ( double )( 4 * SX1276.Settings.LoRa.Datarate -
                         ( ( SX1276.Settings.LoRa.LowDatarateOptimize > 0 ) ? 8 : 0 ) ) ) *
                         ( SX1276.Settings.LoRa.Coderate + 4 );
    double nPayload = 8 + ( ( tmp > 0 ) ? tmp : 0 );
    double tPayload = nPayload * ts;
    // Time on air 
    double tOnAir = tPreamble + tPayload;
    // return us secs
    airTime = (uint32_t)floor( tOnAir * 1e6 + 0.999 );
        

    return airTime;
}

void SX1276WriteFifo( uint8_t *buffer, uint8_t size )
{
    uint8_t i=0;
    for(i=0;i<size;i++)
    {
        SX1276WriteBuffer(0, *buffer++);
    }
}

void SX1276ReadFifo( uint8_t *buffer, uint8_t size )
{
    uint8_t i=0;
    for(i=0;i<size;i++)
    {
         *buffer++ = SX1276ReadBuffer(0);
    }
}

void SX1276SetTx( uint32_t timeout )
{
    if( SX1276.Settings.LoRa.FreqHopOn == TRUE )
    {
        SX1276WriteBuffer( REG_LR_IRQFLAGSMASK, RFLR_IRQFLAGS_RXTIMEOUT |
                                          RFLR_IRQFLAGS_RXDONE |
                                          RFLR_IRQFLAGS_PAYLOADCRCERROR |
                                          RFLR_IRQFLAGS_VALIDHEADER |
                                          //RFLR_IRQFLAGS_TXDONE |
                                          RFLR_IRQFLAGS_CADDONE |
                                          //RFLR_IRQFLAGS_FHSSCHANGEDCHANNEL |
                                          RFLR_IRQFLAGS_CADDETECTED );
                                      
        // DIO0=TxDone, DIO2=FhssChangeChannel
        SX1276WriteBuffer( REG_LR_DIOMAPPING1, ( SX1276ReadBuffer( REG_LR_DIOMAPPING1 ) & RFLR_DIOMAPPING1_DIO0_MASK & RFLR_DIOMAPPING1_DIO2_MASK ) | RFLR_DIOMAPPING1_DIO0_01 | RFLR_DIOMAPPING1_DIO2_00 );
    }
    else
    {
        SX1276WriteBuffer( REG_LR_IRQFLAGSMASK, RFLR_IRQFLAGS_RXTIMEOUT |
                                          RFLR_IRQFLAGS_RXDONE |
                                          RFLR_IRQFLAGS_PAYLOADCRCERROR |
                                          RFLR_IRQFLAGS_VALIDHEADER |
                                          //RFLR_IRQFLAGS_TXDONE |
                                          RFLR_IRQFLAGS_CADDONE |
                                          RFLR_IRQFLAGS_FHSSCHANGEDCHANNEL |
                                          RFLR_IRQFLAGS_CADDETECTED );

        // DIO0=TxDone
        SX1276WriteBuffer( REG_LR_DIOMAPPING1, ( SX1276ReadBuffer( REG_LR_DIOMAPPING1 ) & RFLR_DIOMAPPING1_DIO0_MASK ) | RFLR_DIOMAPPING1_DIO0_01 );
    }
    SX1276LoRaSetOpMode(Transmitter_mode);
}

void SX1276Send( uint8_t *buffer, uint8_t size )
{
    uint32_t txTimeout = 0;
    RadioEvents.TxBefore();
    if( SX1276.Settings.LoRa.IqInverted == TRUE )
    {
        SX1276WriteBuffer( REG_LR_INVERTIQ, ( ( SX1276ReadBuffer( REG_LR_INVERTIQ ) & RFLR_INVERTIQ_TX_MASK & RFLR_INVERTIQ_RX_MASK ) | RFLR_INVERTIQ_RX_OFF | RFLR_INVERTIQ_TX_ON ) );
        SX1276WriteBuffer( REG_LR_INVERTIQ2, RFLR_INVERTIQ2_ON );
    }
    else
    {
        SX1276WriteBuffer( REG_LR_INVERTIQ, ( ( SX1276ReadBuffer( REG_LR_INVERTIQ ) & RFLR_INVERTIQ_TX_MASK & RFLR_INVERTIQ_RX_MASK ) | RFLR_INVERTIQ_RX_OFF | RFLR_INVERTIQ_TX_OFF ) );
        SX1276WriteBuffer( REG_LR_INVERTIQ2, RFLR_INVERTIQ2_OFF );
    }      

    SX1276.PacketInfo.Size = size;

    // Initializes the payload size
    SX1276WriteBuffer( REG_LR_PAYLOADLENGTH, size );

    // Full buffer used for Tx            
    SX1276WriteBuffer( REG_LR_FIFOTXBASEADDR, 0 );
    SX1276WriteBuffer( REG_LR_FIFOADDRPTR, 0 );

    // FIFO operations can not take place in Sleep mode
    if( ( SX1276ReadBuffer( REG_LR_OPMODE ) & ~RFLR_OPMODE_MASK ) == RFLR_OPMODE_SLEEP )
    {
        SX1276LoRaSetOpMode(Stdby_mode);
        delay_1ms();
    }
    // Write payload buffer
    SX1276WriteFifo( buffer, size );
    txTimeout = SX1276.Settings.LoRa.TxTimeout;

    SX1276SetTx( txTimeout );
}

void SX1276SetSleep( void )
{
    SX1276LoRaSetOpMode( Stdby_mode );
    SX1276WriteBuffer(REG_LR_IRQFLAGSMASK,  IRQN_SEELP_Value);  //打开发送中断
    SX1276WriteBuffer( REG_LR_DIOMAPPING1, 0X00 );
    SX1276WriteBuffer( REG_LR_DIOMAPPING2, 0X00 );	
    SX1276LoRaSetOpMode(Sleep_mode);
}

void SX1276SetStby( void )
{
    SX1276LoRaSetOpMode( Stdby_mode );
}

static void LoRa_err()
{
    
    LED1_OFF;
    LED2_OFF;
    LED3_OFF;
    while(1)
    {
        LED1_TOGGLE;
        LED2_TOGGLE;
        LED3_TOGGLE;
        delay_ms(500);
    }
}
 
static uint8_t ifSX1276Correct()
{
    uint8_t check = 0;
    if(LORA_RECEIVE_MODE == LORA_CONTINUOUS_MODE)
    {
        check = SX1276LoRaSetOpMode(Receiver_mode);
    }
    else
    {
        check = SX1276LoRaSetOpMode(receive_single);
    }
    if(check!=SX1276ReadBuffer(REG_LR_OPMODE))
    {
        return 0;
    }
    return 1;
}
void SX1276SetRx( uint32_t timeout )
{
    bool rxContinuous = FALSE;

    if( SX1276.Settings.LoRa.IqInverted == TRUE )
    {
        SX1276WriteBuffer( REG_LR_INVERTIQ, ( ( SX1276ReadBuffer( REG_LR_INVERTIQ ) & RFLR_INVERTIQ_TX_MASK & RFLR_INVERTIQ_RX_MASK ) | RFLR_INVERTIQ_RX_ON | RFLR_INVERTIQ_TX_OFF ) );
        SX1276WriteBuffer( REG_LR_INVERTIQ2, RFLR_INVERTIQ2_ON );
    }
    else
    {
        SX1276WriteBuffer( REG_LR_INVERTIQ, ( ( SX1276ReadBuffer( REG_LR_INVERTIQ ) & RFLR_INVERTIQ_TX_MASK & RFLR_INVERTIQ_RX_MASK ) | RFLR_INVERTIQ_RX_OFF | RFLR_INVERTIQ_TX_OFF ) );
        SX1276WriteBuffer( REG_LR_INVERTIQ2, RFLR_INVERTIQ2_OFF );
    }         

    rxContinuous = SX1276.Settings.LoRa.RxContinuous;
    
    if( SX1276.Settings.LoRa.FreqHopOn == TRUE )
    {
        SX1276WriteBuffer( REG_LR_IRQFLAGSMASK, //RFLR_IRQFLAGS_RXTIMEOUT |
                                          //RFLR_IRQFLAGS_RXDONE |
                                          //RFLR_IRQFLAGS_PAYLOADCRCERROR |
                                          RFLR_IRQFLAGS_VALIDHEADER |
                                          RFLR_IRQFLAGS_TXDONE |
                                          RFLR_IRQFLAGS_CADDONE |
                                          //RFLR_IRQFLAGS_FHSSCHANGEDCHANNEL |
                                          RFLR_IRQFLAGS_CADDETECTED );
                                      
        // DIO0=RxDone, DIO2=FhssChangeChannel
        SX1276WriteBuffer( REG_LR_DIOMAPPING1, ( SX1276ReadBuffer( REG_LR_DIOMAPPING1 ) & RFLR_DIOMAPPING1_DIO0_MASK & RFLR_DIOMAPPING1_DIO2_MASK  ) | RFLR_DIOMAPPING1_DIO0_00 | RFLR_DIOMAPPING1_DIO2_00 );
    }
    else
    {
        SX1276WriteBuffer( REG_LR_IRQFLAGSMASK, //RFLR_IRQFLAGS_RXTIMEOUT |
                                          //RFLR_IRQFLAGS_RXDONE |
                                          //RFLR_IRQFLAGS_PAYLOADCRCERROR |
                                          RFLR_IRQFLAGS_VALIDHEADER |
                                          RFLR_IRQFLAGS_TXDONE |
                                          RFLR_IRQFLAGS_CADDONE |
                                          RFLR_IRQFLAGS_FHSSCHANGEDCHANNEL |
                                          RFLR_IRQFLAGS_CADDETECTED );
                                      
        // DIO0=RxDone
        SX1276WriteBuffer( REG_LR_DIOMAPPING1, ( SX1276ReadBuffer( REG_LR_DIOMAPPING1 ) & RFLR_DIOMAPPING1_DIO0_MASK ) | RFLR_DIOMAPPING1_DIO0_00 );
    }
    SX1276WriteBuffer( REG_LR_FIFORXBASEADDR, 0 );
    SX1276WriteBuffer( REG_LR_FIFOADDRPTR, 0 );
        
    

    SX1276.Settings.State = RF_RX_RUNNING;
    if( rxContinuous == FALSE )
    {
        SX1276WriteBuffer(REG_LR_MODEMCONFIG2,
                         (SX1276ReadBuffer(REG_LR_MODEMCONFIG2)&0xFC) | 
                         (timeout >> 8));
        SX1276WriteBuffer(REG_LR_SYMBTIMEOUTLSB,timeout);
    }

    if( rxContinuous == TRUE )
    {
        SX1276LoRaSetOpMode(Receiver_mode);
    }
    else
    {
        SX1276LoRaSetOpMode(receive_single);
    }

    
}

void SX1276StartCad( void )
{      
      SX1276WriteBuffer( REG_LR_IRQFLAGSMASK, RFLR_IRQFLAGS_RXTIMEOUT |
                                  RFLR_IRQFLAGS_RXDONE |
                                  RFLR_IRQFLAGS_PAYLOADCRCERROR |
                                  RFLR_IRQFLAGS_VALIDHEADER |
                                  RFLR_IRQFLAGS_TXDONE |
                                  //RFLR_IRQFLAGS_CADDONE |
                                  RFLR_IRQFLAGS_FHSSCHANGEDCHANNEL // |
                                  //RFLR_IRQFLAGS_CADDETECTED 
                                  );
                                          
      // DIO3=CADDone
      SX1276WriteBuffer( REG_LR_DIOMAPPING1, ( SX1276ReadBuffer( REG_LR_DIOMAPPING1 ) & RFLR_DIOMAPPING1_DIO0_MASK ) | RFLR_DIOMAPPING1_DIO0_00 );
      
      SX1276LoRaSetOpMode( CAD_mode );
}

uint8_t SX1276SendingStatus()
{
    return Protocol.data_sending;
}

void onTxDone( void )
{
    //    Radio.Sleep();
    //    State = TX;
    Protocol.data_sending = 0;
}
void onTxBefore( void )
{
    Protocol.data_sending = 1;
    Protocol.ack_received = 0;
    Protocol.send_failed = 0;
}

void onRxDone( uint8_t *payload)
{
    //LED2_TOGGLE;
//    memcpy(Buffer, payload, SX1276.PacketInfo.Size);
//    memset( payload, 0, ( size_t )RX_BUFFER_SIZE );
}

void onTxTimeout( void )
{
    //    Radio.Sleep( );
    //    State = TX_TIMEOUT;
}

void onRxTimeout( void )
{
    //    Radio.Sleep( );
//    State = RX_TIMEOUT;
}

void onRxError( void )
{
//    Radio.Sleep( );
//    State = RX_ERROR;
}

void onChangeChannel(uint8_t currentChannel)
{
    
}

void onCadDone(bool channelActivityDetected)
{

}

void onInvalid()
{

}

void onResendFailed()
{
    Protocol.ack_received = 0;
    Protocol.data_sending = 0;
    Protocol.resend_times = 0;
    Protocol.send_failed = 0;
}

//unfinished
static uint8_t SX1276OptimalChannel()
{
    uint8_t channel = 0;
    
    return channel;
}

const struct RadioEvents_inferface RadioEvents = 
{
   onTxDone,
   onTxBefore,
   onTxTimeout,
   onRxDone,
   onRxTimeout,
   onRxError,
   onChangeChannel,
   onCadDone,
   onInvalid,
   onResendFailed,
};
const struct Radio_interface Radio =
{
    SX1276Init,
    SX1276GetState,
    SX1276SetModem,
    SX1276SetChannel,
    SX1276IsChannelFree,
    SX1276SetRxConfig,
    SX1276SetTxConfig,
    SX1276GetTimeOnAir,
    SX1276Send,
    SX1276SetSleep,
    SX1276SetStby, 
    SX1276SetRx,
    SX1276StartCad,
    SX1276ReadRssi,
    SX1276SendingStatus,
    SX1276OptimalChannel,
    ifSX1276Correct,
    LoRa_err,
};

void Init_Radio()
{
    Radio.Init();
    Radio.setChannel(RF_FREQUENCY);
    Radio.setTxConfig(MODEM_LORA,
                      TX_OUTPUT_POWER_20dBm, 
                      LORA_ENABLE_PA, 
                      LORA_BANDWIDTH_125k,
                      LORA_SPREADING_FACTOR_12, 
                      LORA_CODINGRATE_48,
                      LORA_PREAMBLE_LENGTH_8, 
                      LORA_FIX_LENGTH_PAYLOAD_FALSE,
                      LORA_CRC_ON, 
                      LORA_HOP_OFF, 
                      LORA_HOP_PERIOD_0, 
                      LORA_IQ_INVERSION_FLASE, 
                      TX_TIMEOUT_VALUE);
    
    Radio.setRxConfig(MODEM_LORA,
                      LORA_BANDWIDTH_125k, 
                      LORA_SPREADING_FACTOR_12,
                      LORA_CODINGRATE_48,
                      LORA_PREAMBLE_LENGTH_8,
                      LORA_SYMBOL_TIMEOUT_5,
                      LORA_FIX_LENGTH_PAYLOAD_FALSE,
                      0,
                      LORA_CRC_ON,
                      LORA_HOP_OFF, 
                      LORA_HOP_PERIOD_0, 
                      LORA_IQ_INVERSION_FLASE,
                      LORA_RECEIVE_MODE);
    Radio.setRxState(RX_TIMEOUT_VALUE);
    if(!ifSX1276Correct())
    {
        LoRa_err();
    }
    SX1276.Settings.Address = 0x00001111;
    //SX1276.Settings.Address = FLASH_ReadByte(FLASH_ADDRESS);
}