#include "common.h"

#define  OK     1
#define  ERROR  0
#define  TIME_OUT  5000

GPRS_s GPRS;
static void GPRS_Error()
{
    while(1)
    {
        LED1_ON;
        LED2_OFF;
        LED3_ON;
        delay_ms(300);
        LED1_OFF;
        LED2_ON;
        LED3_OFF;
        delay_ms(300);
    }
    
}

int fputc(int ch, FILE *f)
{
    USART_SendData(USART2, (uint8_t) ch);
    while (USART_GetFlagStatus(USART2, USART_FLAG_TC) == RESET);
    return ch;
}

uint8_t closeNet()
{
    uint16_t timeout = 0;
    memset( GPRS.receive, 0, ( size_t )GPRS_RX_BUFFER_SIZE );
    GPRS.receive_count = 0;
    printf("AT+SAPBR=0,1\r\n");
    while(GPRS.receive_count < 0x14)
    {
        timeout++;
        delay_1ms();
        if(timeout>TIME_OUT)
        {
            return ERROR;
        }
    }
    for(uint8_t i=GPRS.receive_count;i>0;i--)
    {
        if((GPRS.receive[i]   == '\r') && 
           (GPRS.receive[i+1] == '\n') && 
           (GPRS.receive[i+2] == 'O') && 
           (GPRS.receive[i+3] == 'K') && 
           (GPRS.receive[i+4] == '\r') && 
           (GPRS.receive[i+5] == '\n')
           )
        {
            return OK;
        }
    }
    return ERROR;
}

uint8_t openNet()
{
    uint16_t timeout = 0;
    memset( GPRS.receive, 0, ( size_t )GPRS_RX_BUFFER_SIZE );
    GPRS.receive_count = 0;
    printf("AT+SAPBR=1,1\r\n");
    while(GPRS.receive_count < 0x14)
    {
        timeout++;
        delay_1ms();
        if(timeout>TIME_OUT)
        {
            return ERROR;
        }
    }
    for(uint8_t i=GPRS.receive_count;i>0;i--)
    {
        if((GPRS.receive[i]   == '\r') && 
           (GPRS.receive[i+1] == '\n') && 
           (GPRS.receive[i+2] == 'O') && 
           (GPRS.receive[i+3] == 'K') && 
           (GPRS.receive[i+4] == '\r') && 
           (GPRS.receive[i+5] == '\n')
           )
        {
            return OK;
        }
    }
    for(uint8_t i=GPRS.receive_count;i>0;i--)
    {
        if((GPRS.receive[i]   == '\r') && 
           (GPRS.receive[i+1] == '\n') && 
           (GPRS.receive[i+2] == 'E') && 
           (GPRS.receive[i+3] == 'R') && 
           (GPRS.receive[i+4] == 'R') && 
           (GPRS.receive[i+5] == 'O') &&
           (GPRS.receive[i+6] == 'R') && 
           (GPRS.receive[i+7] == '\r') && 
           (GPRS.receive[i+8] == '\n')
           )
        {
           if(closeNet())
           {
              openNet();
           }
           else
           {
               GPRS_Error();
           }
            
        }
    }
    
    return ERROR;
}



uint8_t initHTTP()
{
    uint16_t timeout = 0;
    memset( GPRS.receive, 0, ( size_t )GPRS_RX_BUFFER_SIZE );
    GPRS.receive_count = 0;
    printf("AT+HTTPINIT\r\n");
    while(GPRS.receive_count < 0x13)
    {
        timeout++;
        delay_1ms();
        if(timeout>TIME_OUT)
        {
            return ERROR;
        }
    }
    for(uint8_t i=GPRS.receive_count;i>0;i--)
    {
        if((GPRS.receive[i]   == '\r') && 
           (GPRS.receive[i+1] == '\n') && 
           (GPRS.receive[i+2] == 'O') && 
           (GPRS.receive[i+3] == 'K') && 
           (GPRS.receive[i+4] == '\r') && 
           (GPRS.receive[i+5] == '\n')
           )
        {
            return OK;
        }
    }
    return ERROR;

}

uint8_t setCID()
{
    uint16_t timeout = 0;
    memset( GPRS.receive, 0, ( size_t )GPRS_RX_BUFFER_SIZE );
    GPRS.receive_count = 0;
    printf("AT+HTTPPARA=\"CID\",\"1\"\r\n");
    while(GPRS.receive_count < 0x1D)
    {
        timeout++;
        delay_1ms();
        if(timeout>TIME_OUT)
        {
            return ERROR;
        }
    }
    for(uint8_t i=GPRS.receive_count;i>0;i--)
    {
        if((GPRS.receive[i]   == '\r') && 
           (GPRS.receive[i+1] == '\n') && 
           (GPRS.receive[i+2] == 'O') && 
           (GPRS.receive[i+3] == 'K') && 
           (GPRS.receive[i+4] == '\r') && 
           (GPRS.receive[i+5] == '\n')
           )
        {
            return OK;
        }
    }
    return ERROR;
}

uint8_t setURL(uint32_t address,uint8_t data_type, uint16_t data)
{
    uint16_t timeout = 0;
    memset( GPRS.receive, 0, ( size_t )GPRS_RX_BUFFER_SIZE );
    GPRS.receive_count = 0;
    printf("AT+HTTPPARA=\"URL\",");
    printf("http://www.xiaoxiami.space/info/manhole-post/");
    printf("?address=%d&data_type=%d&data=%d\r\n",address,data_type,data);
    while(GPRS.receive_count < 0x66)
    {
        timeout++;
        delay_1ms();
        if(timeout>TIME_OUT)
        {
            return ERROR;
        }
    }
    for(uint8_t i=GPRS.receive_count;i>50;i--)
    {
        if((GPRS.receive[i]   == '\r') && 
           (GPRS.receive[i+1] == '\n') && 
           (GPRS.receive[i+2] == 'O') && 
           (GPRS.receive[i+3] == 'K') && 
           (GPRS.receive[i+4] == '\r') && 
           (GPRS.receive[i+5] == '\n')
           )
        {
            return OK;
        }
    }
    return ERROR;
}

uint8_t getRequest()
{
    uint16_t timeout = 0;
    memset( GPRS.receive, 0, ( size_t )GPRS_RX_BUFFER_SIZE );
    GPRS.receive_count = 0;
    printf("AT+HTTPACTION=0\r\n");
    while(GPRS.receive_count < 0x30)
    {
        timeout++;
        delay_1ms();
        if(timeout>5000)
        {
            return ERROR;
        }
    }
    for(uint8_t i=30;i<50;i++)
    {
        if((GPRS.receive[i]   == 'H') && 
           (GPRS.receive[i+1] == 'T') && 
           (GPRS.receive[i+2] == 'T') && 
           (GPRS.receive[i+3] == 'P') && 
           (GPRS.receive[i+4] == 'A') && 
           (GPRS.receive[i+5] == 'C') && 
           (GPRS.receive[i+6] == 'T') && 
           (GPRS.receive[i+7] == 'I') && 
           (GPRS.receive[i+8] == 'O') && 
           (GPRS.receive[i+9] == 'N') && 
           (GPRS.receive[i+10]== ':') && 
           (GPRS.receive[i+11]== '0') && 
           (GPRS.receive[i+12]== ',') && 
           (GPRS.receive[i+13]== '2') && 
           (GPRS.receive[i+14]== '0') && 
           (GPRS.receive[i+15]== '0') && 
           (GPRS.receive[i+16]== ',')
           )
        {
            return OK;
        }
    }
    return ERROR;
    
}



uint8_t softControl()
{
    memset( GPRS.receive, 0, ( size_t )GPRS_RX_BUFFER_SIZE );
    GPRS.receive_count = 0;
    printf("AT+IFC=1,1\n");
    return 0;
}

void GSMPowerOn_OFF()
{
//    DISABLE_DIO0;
//    DISABLE_DIO1;
    GSM_ON_H;
    delay_s(2);
    GSM_ON_L;
    
    delay_s(30);
    if(!openNet())
    {
        GPRS_Error();
    }
    delay_ms(100);
    if(!initHTTP())
    {
        GPRS_Error();
    }
    delay_ms(100);
    if(!setCID())
    {
        GPRS_Error();
    }
//    ENABLE_DIO0;
//    ENABLE_DIO1;
}

static void GPRS_Send(uint32_t address,uint8_t data_type, uint16_t data)
{
    setURL(address,data_type,data);
    delay_s(2);
    getRequest();
    delay_s(4);
    
}

void Init_GPRS()
{
    GPRS.PowerOn = GSMPowerOn_OFF;
    GPRS.Send = GPRS_Send;
}