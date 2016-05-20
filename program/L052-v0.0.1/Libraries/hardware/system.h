#ifndef __SYSTEM_H
#define __SYSTEM_H

typedef struct 
{
    void (*set)();
    void (*reset)();
    uint8 (*get)();
    uint8_t  pin;
    GPIO_TypeDef*  port;
}Gpio_t;

#define LED1_PORT GPIOE
#define LED1_BIT  GPIO_Pin_0
#define LED2_PORT GPIOE
#define LED2_BIT  GPIO_Pin_1

#define LED1_OFF     GPIO_SetBits(LED1_PORT,LED1_BIT);
#define LED1_ON      GPIO_ResetBits(LED1_PORT,LED1_BIT);
#define LED1_TOGGLE  GPIO_ToggleBits(LED1_PORT,LED1_BIT);
#define LED2_OFF     GPIO_SetBits(LED2_PORT,LED2_BIT);
#define LED2_ON      GPIO_ResetBits(LED2_PORT,LED2_BIT);
#define LED2_TOGGLE  GPIO_ToggleBits(LED2_PORT,LED2_BIT);

#define  RF_REST_L	SX1276.Reset.reset()
#define  RF_REST_H	SX1276.Reset.set()

#define  RF_CE_L        SX1276.NSS.reset() 
#define  RF_CE_H        SX1276.NSS.set()  

#define  RF_CKL_L       SX1276.SCK.reset()    
#define  RF_CKL_H       SX1276.SCK.set()     

#define  RF_SDI_L       SX1276.MOSI.reset()
#define  RF_SDI_H       SX1276.MOSI.set()

#define  RF_SDO_DATA    SX1276.MISO.get()


#define RF_TX      GPIO_ResetBits(GPIOA,GPIO_Pin_2);
#define RF_RX      GPIO_SetBits(GPIOA,GPIO_Pin_2);
//#define  RF_REST_PORT   GPIOD
//#define  RF_REST_BIT    GPIO_Pin_4
//#define  RF_REST_L	GPIO_ResetBits (GPIOD, GPIO_Pin_4)
//#define  RF_REST_H	GPIO_SetBits   (GPIOD, GPIO_Pin_4)
//
//#define  RF_CE_PORT     GPIOB
//#define  RF_CE_BIT      GPIO_Pin_2
//#define  RF_CE_L        GPIO_ResetBits (GPIOB, GPIO_Pin_2)     
//#define  RF_CE_H        GPIO_SetBits   (GPIOB, GPIO_Pin_2)     
//
//#define  RF_CKL_PORT    GPIOB
//#define  RF_CKL_BIT     GPIO_Pin_5
//#define  RF_CKL_L       GPIO_ResetBits (GPIOB, GPIO_Pin_5)     
//#define  RF_CKL_H       GPIO_SetBits   (GPIOB, GPIO_Pin_5)     
//
//#define  RF_SDI_PORT    GPIOB
//#define  RF_SDI_BIT     GPIO_Pin_3
//#define  RF_SDI_L       GPIO_ResetBits (GPIOB, GPIO_Pin_3)     
//#define  RF_SDI_H       GPIO_SetBits   (GPIOB, GPIO_Pin_3)     
//
//#define  RF_SDO_PORT    GPIOB
//#define  RF_SDO_BIT     GPIO_Pin_4
//#define  RF_SDO_DATA    GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_4)

extern void Init_System();
extern void UART_Send_Data(uint8 data);
#endif
