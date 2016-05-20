#ifndef __SX1276_H
#define __SX1276_H

/* Radio Config ---------------------------------------------------------*/
#if defined( USE_BAND_433 )
#define RF_FREQUENCY                                434000000 // Hz
#elif defined( USE_BAND_470 )
#define RF_FREQUENCY                                470000000 // Hz
#elif defined( USE_BAND_868 )
#define RF_FREQUENCY                                868000000 // Hz
#elif defined( USE_BAND_915 )
#define RF_FREQUENCY                                915000000 // Hz
#else
    #error "Please define a frequency band in the compiler options."
#endif

#define TX_OUTPUT_POWER_20dBm                       20        // dBm
#define LORA_ENABLE_PA                              TRUE
#define LORA_BANDWIDTH_125k                         0         // [0: 125 kHz,
                                                              //  1: 250 kHz,
                                                              //  2: 500 kHz,
                                                              //  3: Reserved]
#define LORA_SPREADING_FACTOR_12                    12         // [SF7..SF12]
#define LORA_CODINGRATE_48                          4         // [1: 4/5,
                                                              //  2: 4/6,
                                                              //  3: 4/7,
                                                              //  4: 4/8]
#define LORA_PREAMBLE_LENGTH_8                      8         // Same for Tx and Rx
#define LORA_SYMBOL_TIMEOUT_5                         5         // Symbols
#define LORA_FIX_LENGTH_PAYLOAD_FALSE               FALSE
#define LORA_IQ_INVERSION_FLASE                     FALSE
#define LORA_CRC_ON                                 TRUE
#define LORA_CRC_OFF                                FALSE
#define LORA_HOP_OFF                                0
#define LORA_HOP_PERIOD_0                           0
#define LORA_TIMEOUT_0                              0
#define LORA_CONTINUOUS_MODE                        TRUE
#define LORA_SINGLE_MODE                            FLASE

/* Radio Config End---------------------------------------------------------*/

#define RF_MID_BAND_THRESH                          525000000
#define XTAL_FREQ                                   32000000
#define FREQ_STEP                                   61.03515625

#define RX_BUFFER_SIZE                              20
#define RX_TIMEOUT_VALUE 1000000
/*!
 * Constant values need to compute the RSSI value
 */
#define RSSI_OFFSET_LF                              -164
#define RSSI_OFFSET_HF                              -157

/*!
SX1276 Internal registers Address
*/
#define REG_LR_FIFO                                 0x00 
// Common settings
#define REG_LR_OPMODE                               0x01 
#define REG_LR_BANDSETTING                          0x04
#define REG_LR_FRFMSB                               0x06 
#define REG_LR_FRFMID                               0x07
#define REG_LR_FRFLSB                               0x08 
// Tx settings
#define REG_LR_PACONFIG                             0x09 
#define REG_LR_PARAMP                               0x0A 
#define REG_LR_OCP                                  0x0B 
// Rx settings
#define REG_LR_LNA                                  0x0C 
// LoRa registers
#define REG_LR_FIFOADDRPTR                          0x0D 
#define REG_LR_FIFOTXBASEADDR                       0x0E 
#define REG_LR_FIFORXBASEADDR                       0x0F 
#define REG_LR_FIFORXCURRENTADDR                    0x10 
#define REG_LR_IRQFLAGSMASK                         0x11 
#define REG_LR_IRQFLAGS                             0x12 
#define REG_LR_NBRXBYTES                            0x13 
#define REG_LR_RXHEADERCNTVALUEMSB                  0x14 
#define REG_LR_RXHEADERCNTVALUELSB                  0x15 
#define REG_LR_RXPACKETCNTVALUEMSB                  0x16 
#define REG_LR_RXPACKETCNTVALUELSB                  0x17 
#define REG_LR_MODEMSTAT                            0x18 
#define REG_LR_PKTSNRVALUE                          0x19 
#define REG_LR_PKTRSSIVALUE                         0x1A 
#define REG_LR_RSSIVALUE                            0x1B 
#define REG_LR_HOPCHANNEL                           0x1C 
#define REG_LR_MODEMCONFIG1                         0x1D 
#define REG_LR_MODEMCONFIG2                         0x1E 
#define REG_LR_SYMBTIMEOUTLSB                       0x1F 
#define REG_LR_PREAMBLEMSB                          0x20 
#define REG_LR_PREAMBLELSB                          0x21 
#define REG_LR_PAYLOADLENGTH                        0x22 
#define REG_LR_PAYLOADMAXLENGTH                     0x23 
#define REG_LR_HOPPERIOD                            0x24 
#define REG_LR_FIFORXBYTEADDR                       0x25
#define REG_LR_MODEMCONFIG3                         0x26
// end of documented register in datasheet
// I/O settings
#define REG_LR_DIOMAPPING1                          0x40
#define REG_LR_DIOMAPPING2                          0x41
// Version
#define REG_LR_VERSION                              0x42
// Additional settings
#define REG_LR_PLLHOP                               0x44
#define REG_LR_TCXO                                 0x4B
#define REG_LR_PADAC                                0x4D
#define REG_LR_FORMERTEMP                           0x5B
#define REG_LR_BITRATEFRAC                          0x5D
#define REG_LR_AGCREF                               0x61
#define REG_LR_AGCTHRESH1                           0x62
#define REG_LR_AGCTHRESH2                           0x63
#define REG_LR_AGCTHRESH3                           0x64


#define  GPIO_VARE_1                                 0X00
#define  GPIO_VARE_2                                 0X00
//#define  RFLR_MODEMCONFIG2_SF_MASK                   0x0f
#define RFLR_MODEMCONFIG1_CODINGRATE_MASK            0xF1 
#define RFLR_MODEMCONFIG2_RXPAYLOADCRC_MASK          0xFB 
#define RFLR_MODEMCONFIG1_BW_MASK                    0x0F 
#define RFLR_MODEMCONFIG1_IMPLICITHEADER_MASK        0xFE 
//#define RFLR_MODEMCONFIG2_SYMBTIMEOUTMSB_MASK        0xfc
#define RFLR_MODEMCONFIG3_MOBILE_NODE_MASK           0xF7 

#define TIME_OUT_INT                                 0x80 
#define PACKET_RECVER_INT                            0x40 
#define CRC_ERROR_INT                                0x20 
#define RECVER_HEAR_INT                              0x10 
#define FIFO_SEND_OVER                               0x08 
#define RFLR_IRQFLAGS_CAD                            0x04 
#define RFLR_IRQFLAGS_FHSS                           0x02 
#define RFLR_IRQFLAGS_CADD                           0x01 

#define IRQN_TXD_Value                               0xF7
#define IRQN_RXD_Value                               0x9F
#define IRQN_CAD_Value                               0xFA
#define IRQN_SEELP_Value                             0xFF

/*!
 * RegOpMode
 */
#define RFLR_OPMODE_LONGRANGEMODE_MASK              0x7F 
#define RFLR_OPMODE_LONGRANGEMODE_OFF               0x00 // Default
#define RFLR_OPMODE_LONGRANGEMODE_ON                0x80 

#define RFLR_OPMODE_ACCESSSHAREDREG_MASK            0xBF 
#define RFLR_OPMODE_ACCESSSHAREDREG_ENABLE          0x40 
#define RFLR_OPMODE_ACCESSSHAREDREG_DISABLE         0x00 // Default

#define RFLR_OPMODE_FREQMODE_ACCESS_MASK            0xF7
#define RFLR_OPMODE_FREQMODE_ACCESS_LF              0x08 // Default
#define RFLR_OPMODE_FREQMODE_ACCESS_HF              0x00 

#define RFLR_OPMODE_MASK                            0xF8 
#define RFLR_OPMODE_SLEEP                           0x00 
#define RFLR_OPMODE_STANDBY                         0x01 // Default
#define RFLR_OPMODE_SYNTHESIZER_TX                  0x02 
#define RFLR_OPMODE_TRANSMITTER                     0x03 
#define RFLR_OPMODE_SYNTHESIZER_RX                  0x04 
#define RFLR_OPMODE_RECEIVER                        0x05 
// LoRa specific modes
#define RFLR_OPMODE_RECEIVER_SINGLE                 0x06 
#define RFLR_OPMODE_CAD                             0x07 

typedef enum 
{
    Sleep_mode			= (uint8_t)0x00, 
    Stdby_mode			= (uint8_t)0x01, 
    TX_mode 			= (uint8_t)0x02,
    Transmitter_mode		= (uint8_t)0x03,
    RF_mode 			= (uint8_t)0x04,
    Receiver_mode		= (uint8_t)0x05,
    receive_single		= (uint8_t)0x06,
    CAD_mode			= (uint8_t)0x07,
} RFMode_SET;

typedef enum 
{
    MODEM_FSK               = (uint8_t)0x00, 
    MODEM_LORA              = (uint8_t)0x80, 
} RadioModems_t;

typedef enum
{
    RF_IDLE = Stdby_mode,
    RF_RX_RUNNING = Receiver_mode,
    RF_TX_RUNNING = Transmitter_mode,
    RF_SLEEP = Sleep_mode,
    RF_CAD = CAD_mode,
}RadioState_t;

typedef struct
{
    int8_t   Power;
    uint32_t Bandwidth;
    uint32_t Datarate;
    bool     LowDatarateOptimize;
    uint8_t  Coderate;
    uint16_t PreambleLen;
    bool     FixLen;
    uint8_t  PayloadLen;
    bool     CrcOn;
    bool     FreqHopOn;
    uint8_t  HopPeriod;
    bool     IqInverted;
    bool     RxContinuous;
    uint32_t TxTimeout;
}RadioLoRaSettings_t;

typedef struct
{
    int8_t  SnrValue;
    int16_t RssiValue;
    uint8_t Size;
}RadioLoRaPacketHandler_t;

typedef struct
{
    int8_t   Power;
    uint32_t Fdev;
    uint32_t Bandwidth;
    uint32_t BandwidthAfc;
    uint32_t Datarate;
    uint16_t PreambleLen;
    bool     FixLen;
    uint8_t  PayloadLen;
    bool     CrcOn;
    bool     IqInverted;
    bool     RxContinuous;
    uint32_t TxTimeout;
}RadioFskSettings_t;

typedef struct
{
    uint8_t  PreambleDetected;
    uint8_t  SyncWordDetected;
    int8_t   RssiValue;
    int32_t  AfcValue;
    uint8_t  RxGain;
    uint16_t Size;
    uint16_t NbBytes;
    uint8_t  FifoThresh;
    uint8_t  ChunkSize;
}RadioFskPacketHandler_t;

typedef struct
{
    RadioState_t             State;
    RadioModems_t            Modem;
    uint32_t                 Channel;
    RadioLoRaSettings_t      LoRa;
}RadioSettings_t;

typedef struct SX1276_s
{
    Gpio_t        Reset;
    Gpio_t        DIO0;
    Gpio_t        DIO1;
    Gpio_t        DIO2;
    Gpio_t        DIO3;
    Gpio_t        DIO4;
    Gpio_t        DIO5;
    Gpio_t        NSS;
    Gpio_t        MOSI;
    Gpio_t        MISO;
    Gpio_t        SCK;
    uint8_t       RxTx;
    RadioSettings_t Settings;
    RadioLoRaPacketHandler_t PacketInfo;
}SX1276_t;

typedef enum
{
    LOWPOWER,
    RX,
    RX_TIMEOUT,
    RX_ERROR,
    TX,
    TX_TIMEOUT,
}States_t;

typedef struct
{
    RadioModems_t Modem;
    uint8_t       Addr;
    uint8_t       Value;
}RadioRegisters_t;

extern const struct Radio_interface Radio;
extern States_t State;
extern SX1276_t SX1276;
extern const struct RadioEvents_inferface RadioEvents;
extern uint8_t RxBuffer[RX_BUFFER_SIZE];
extern uint8 data_sending;


void    SX1276WriteBuffer( uint8_t addr, uint8_t buffer);
uint8_t SX1276ReadBuffer( uint8_t addr);
void SX1276ReadFifo( uint8_t *buffer, uint8_t size );
void Init_Radio();
#endif

