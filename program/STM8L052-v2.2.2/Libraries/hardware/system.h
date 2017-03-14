#ifndef __SYSTEM_H
#define __SYSTEM_H

#define EEPROM_START  0x0010FE

typedef struct 
{
    void (*set)();
    void (*reset)();
    uint8 (*get)();
    uint8_t  pin;
    GPIO_TypeDef*  port;
}Gpio_t;

#define LED1_PORT GPIOA
#define LED1_BIT  GPIO_Pin_3
#define LED2_PORT GPIOA
#define LED2_BIT  GPIO_Pin_4
#define LED3_PORT GPIOA
#define LED3_BIT  GPIO_Pin_5
#define LED4_PORT GPIOA
#define LED4_BIT  GPIO_Pin_6
#define LED5_PORT GPIOA
#define LED5_BIT  GPIO_Pin_7

#define LED1_OFF     GPIO_SetBits(LED1_PORT,LED1_BIT);
#define LED1_ON      GPIO_ResetBits(LED1_PORT,LED1_BIT);
#define LED1_TOGGLE  GPIO_ToggleBits(LED1_PORT,LED1_BIT);
#define LED2_OFF     GPIO_SetBits(LED2_PORT,LED2_BIT);
#define LED2_ON      GPIO_ResetBits(LED2_PORT,LED2_BIT);
#define LED2_TOGGLE  GPIO_ToggleBits(LED2_PORT,LED2_BIT);
#define LED3_OFF     GPIO_SetBits(LED3_PORT,LED3_BIT);
#define LED3_ON      GPIO_ResetBits(LED3_PORT,LED3_BIT);
#define LED3_TOGGLE  GPIO_ToggleBits(LED3_PORT,LED3_BIT);
#define LED4_OFF     GPIO_SetBits(LED4_PORT,LED4_BIT);
#define LED4_ON      GPIO_ResetBits(LED4_PORT,LED4_BIT);
#define LED4_TOGGLE  GPIO_ToggleBits(LED4_PORT,LED4_BIT);
#define LED5_OFF     GPIO_SetBits(LED5_PORT,LED5_BIT);
#define LED5_ON      GPIO_ResetBits(LED5_PORT,LED5_BIT);
#define LED5_TOGGLE  GPIO_ToggleBits(LED5_PORT,LED5_BIT);

#define TEST1_PORT GPIOE
#define TEST1_BIT  GPIO_Pin_1
#define TEST1_HIGH    GPIO_SetBits(TEST1_PORT,TEST1_BIT);
#define TEST1_LOW      GPIO_ResetBits(TEST1_PORT,TEST1_BIT);
#define TEST1_TOGGLE  GPIO_ToggleBits(TEST1_PORT,TEST1_BIT);

#define  RF_REST_L	SX1276.Reset.reset()
#define  RF_REST_H	SX1276.Reset.set()
#define  RF_CE_L        SX1276.NSS.reset() 
#define  RF_CE_H        SX1276.NSS.set()  
#define  RF_CKL_L       SX1276.SCK.reset()    
#define  RF_CKL_H       SX1276.SCK.set()     
#define  RF_SDI_L       SX1276.MOSI.reset()
#define  RF_SDI_H       SX1276.MOSI.set()
#define  RF_SDO_DATA    SX1276.MISO.get()
#define RF_TX      SX1276.RxTx.reset()
#define RF_RX      SX1276.RxTx.set()

#define REED_PORT GPIOA
#define REED_BIT  GPIO_Pin_2
#define REED_GET  GPIO_ReadInputDataBit(REED_PORT,REED_BIT)

#define EN_SAMPLE_PORT   GPIOE
#define EN_SAMPLE_BIT    GPIO_Pin_1
#define EN_SAMPLE_SET    GPIO_SetBits(EN_SAMPLE_PORT,EN_SAMPLE_BIT);
#define EN_SAMPLE_RESET  GPIO_ResetBits(EN_SAMPLE_PORT,EN_SAMPLE_BIT);

extern void Init_System();
extern void UART_Send_Data(uint8 data);
extern uint16_t getPHYAddress();
extern void Init_Sensor();
extern void Init_GPIO();
extern void Init_TIMER();
extern void Init_USART1();
extern void Init_USART2();
void WIFI_Send_Data(uint8 data);
void power_on();
u8 UART_Receive_Data();

extern void All_PULL_UP();
#endif
