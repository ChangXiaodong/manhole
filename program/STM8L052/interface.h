#ifndef __INTERFACE_H
#define __INTERFACE_H

#include "common.h"
#include "ProcessEvent.h"

struct Radio_interface
{
    /*!
    * \brief Initializes the radio
    *
    * \param [IN] events Structure containing the driver callback functions
    */
    void    (*Init)();
    /*!
    * Return current radio status
    *
    * \param status Radio status.[RF_IDLE, RF_RX_RUNNING, RF_TX_RUNNING]
    */
    RadioState_t ( *getState )( void );
    
    // \param [IN] modem Modem to be used [FSK_mode,LORA_mode]
    void    ( *setModem )( RadioModems_t modem );
    
    /*!
    * \brief Sets the channel frequency
    *
    * \param [IN] freq         Channel RF frequency
    */
    void    ( *setChannel )( uint32_t freq );
    
    /*!
    * \param [IN] modem      Radio modem to be used [LORA_mode,FSK_mode]
    * \param [IN] freq       Channel RF frequency
    * \param [IN] rssiThresh RSSI threshold
    *
    * \retval isFree         [true: Channel is free, false: Channel is not free]
    */
    bool    ( *isChannelFree )(int16_t rssiThresh );
    
    /*!
    * \brief Sets the reception parameters
    *
    * \param [IN] modem        Radio modem to be used [0: FSK, 1: LoRa]
    * \param [IN] bandwidth    Sets the bandwidth
    *                          FSK : >= 2600 and <= 250000 Hz
    *                          LoRa: [0: 125 kHz, 1: 250 kHz,
    *                                 2: 500 kHz, 3: Reserved] 
    * \param [IN] datarate     Sets the Datarate
    *                          FSK : 600..300000 bits/s
    *                          LoRa: [6: 64, 7: 128, 8: 256, 9: 512,
    *                                10: 1024, 11: 2048, 12: 4096  chips]
    * \param [IN] coderate     Sets the coding rate (LoRa only)
    *                          FSK : N/A ( set to 0 )
    *                          LoRa: [1: 4/5, 2: 4/6, 3: 4/7, 4: 4/8] 
    * \param [IN] preambleLen  Sets the Preamble length
    *                          FSK : Number of bytes 
    *                          LoRa: Length in symbols (the hardware adds 4 more symbols)
    * \param [IN] symbTimeout  Sets the RxSingle timeout value (LoRa only) 
    *                          FSK : N/A ( set to 0 ) 
    *                          LoRa: timeout in symbols
    * \param [IN] fixLen       Fixed length packets [0: variable, 1: fixed]
    * \param [IN] payloadLen   Sets payload length when fixed lenght is used
    * \param [IN] crcOn        Enables/Disables the CRC [0: OFF, 1: ON]
    * \param [IN] FreqHopOn    Enables disables the intra-packet frequency hopping
    *                          FSK : N/A ( set to 0 )
    *                          LoRa: [0: OFF, 1: ON]
    * \param [IN] HopPeriod    Number of symbols bewteen each hop
    *                          FSK : N/A ( set to 0 )
    *                          LoRa: Number of symbols
    * \param [IN] iqInverted   Inverts IQ signals (LoRa only)
    *                          FSK : N/A ( set to 0 )
    *                          LoRa: [0: not inverted, 1: inverted]
    * \param [IN] rxContinuous Sets the reception in continuous mode
    *                          [false: single mode, true: continuous mode]
    */
    void    ( *setRxConfig )( RadioModems_t modem, uint32_t bandwidth,
                             uint32_t datarate, uint8_t coderate,
                             uint16_t preambleLen,
                             uint16_t symbTimeout, bool fixLen,
                             uint8_t payloadLen,
                             bool crcOn, bool FreqHopOn, uint8_t HopPeriod,
                             bool iqInverted, bool rxContinuous,
                            uint32_t bandwidthAfc );
   
    
    /*!
    * \brief Sets the transmission parameters
    *
    * \param [IN] modem        Radio modem to be used [0: FSK, 1: LoRa] 
    * \param [IN] power        Sets the output power [dBm]
    * \param [IN] PA_enable    PA Select
    *                          TRUE: Enable
    *                          FALSE: DISABLE
    * \param [IN] bandwidth    Sets the bandwidth (LoRa only)
    *                          FSK : 0
    *                          LoRa: [0: 125 kHz, 1: 250 kHz,
    *                                 2: 500 kHz, 3: Reserved] 
    * \param [IN] datarate     Sets the Datarate
    *                          FSK : 600..300000 bits/s
    *                          LoRa: [6: 64, 7: 128, 8: 256, 9: 512,
    *                                10: 1024, 11: 2048, 12: 4096  chips]
    * \param [IN] coderate     Sets the coding rate (LoRa only)
    *                          FSK : N/A ( set to 0 )
    *                          LoRa: [1: 4/5, 2: 4/6, 3: 4/7, 4: 4/8] 
    * \param [IN] preambleLen  Sets the preamble length
    *                          FSK : Number of bytes 
    *                          LoRa: Length in symbols (the hardware adds 4 more symbols)
    * \param [IN] fixLen       Fixed length packets [0: variable, 1: fixed]
    * \param [IN] crcOn        Enables disables the CRC [0: OFF, 1: ON]
    * \param [IN] FreqHopOn    Enables disables the intra-packet frequency hopping
    *                          FSK : N/A ( set to 0 )
    *                          LoRa: [0: OFF, 1: ON]
    * \param [IN] HopPeriod    Number of symbols bewteen each hop
    *                          FSK : N/A ( set to 0 )
    *                          LoRa: Number of symbols
    * \param [IN] iqInverted   Inverts IQ signals (LoRa only)
    *                          FSK : N/A ( set to 0 )
    *                          LoRa: [0: not inverted, 1: inverted]
    * \param [IN] timeout      Transmission timeout [us]
    */
    void    ( *setTxConfig )( RadioModems_t modem, int8_t power, 
                             uint8_t PA_enable, 
                             uint32_t bandwidth, uint32_t datarate,
                             uint8_t coderate, uint16_t preambleLen,
                             bool fixLen, bool crcOn, bool FreqHopOn,
                             uint8_t HopPeriod, bool iqInverted, uint32_t timeout,
                               uint32_t fdev);
    
    /*!
    * \brief Computes the packet time on air in us for the given payload
    *
    * \Remark Can only be called once SetRxConfig or SetTxConfig have been called
    *
    * \param [IN] modem      Radio modem to be used [0: FSK, 1: LoRa]
    * \param [IN] pktLen     Packet payload length
    *
    * \retval airTime        Computed airTime (us) for the given packet payload length
    */    
    uint32_t  ( *getTimeOnAir )( RadioModems_t modem, uint8_t pktLen );
    
    /*!
    * \brief Sends the buffer of size. Prepares the packet to be sent and sets
    *        the radio in transmission
    *
    * \param [IN]: buffer     Buffer pointer
    * \param [IN]: size       Buffer size
    */
    void    ( *Send )( uint8_t *buffer, uint8_t size );
    /*!
     * \brief Sets the radio in sleep mode
     */
    void    ( *setSleepState )( void );
     /*!
     * \brief Sets the radio in standby mode
     */
    void    ( *steStandbyState )( void );
    /*!
    * \brief Sets the radio in reception mode for the given time
    * \param [IN] timeout Reception timeout [us]
    *                     [0: continuous, others timeout]
    */
    void    ( *setRxState )( uint32_t timeout );
    /*!
    * \brief Start a Channel Activity Detection
    */
    void    ( *StartCad )( void );
    /*!
    * \brief Reads the current RSSI value
    *
    * \retval rssiValue Current RSSI value in [dBm]
    */
    int16_t ( *getRssi )();
    
    /*!
    * brief Return current radio send status
    *
    * \return 1: sending 0:sending finished
    */
    uint8_t ( *sendNotDone )( void );
    
    /*!
    * brief Scaning the channel and choose a optimal channel basaed on rssi and snr
    *
    * \return the number of the optimal channel
    */
    uint8_t ( *getOptiamlChannel )( void );
    /*!
    * brief write and read reg
    *
    * \return 1:correct 0:error
    */
    uint8 (*ifCorrect)(void);
    void  (*Error)();
};

/*!
 * \brief Radio driver callback functions
 */
struct RadioEvents_inferface
{
    /*!
     * \brief  Tx Done callback prototype.
     */
    void    ( *TxDone )( void );
    /*!
     * \brief  Before Tx callback prototype.
     */
    void    ( *TxBefore )( void );
    /*!
     * \brief  Tx Timeout callback prototype.
     */
    void    ( *TxTimeout )( void );
    /*!
     * \brief Rx Done callback prototype.
     *
     * \param [IN] payload Received buffer pointer
     */
    void    ( *RxDone )( uint8_t *payload);
    /*!
     * \brief  Rx Timeout callback prototype.
     */
    void    ( *RxTimeout )( void );
    /*!
     * \brief Rx Error callback prototype.
     */
    void    ( *RxError )( void );
    /*!
     * \brief  FHSS Change Channel callback prototype.
     *
     * \param [IN] currentChannel   Index number of the current channel
     */
    void ( *FhssChangeChannel )( uint8_t currentChannel );

    /*!
     * \brief CAD Done callback prototype.
     *
     * \param [IN] channelDetected    Channel Activity detected during the CAD
     */
    void ( *CadDone ) ( bool channelActivityDetected );
    /*!
     * \brief Invalid packet Error callback prototype.
     */
    void ( *Invalid )( void );
    /*!
     * \brief On resend failed Error callback prototype.
     */
    void ( *ResendFailed )( void );
};

struct RadioCallback_inferface
{
    void (*rxCallback)();
    void (*txCallback)();
    void (*timeoutCallback)();
};

struct TaskQuene_inferface
{
    uint8 (*executeTask)();
    uint8 (*postTask)(TQStruct task);
    uint8 (*isEmpty)();
    void (*initTQ)();
};

struct Link_interface
{
    void (*sendData)();
    //void (*sendDataACK)(uint8* data);
    void (*receiveDataACK)(uint8* data);
    uint8 (*ifValid)(uint8* data);
};


#endif