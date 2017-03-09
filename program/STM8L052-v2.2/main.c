#include "common.h"
u16 get_time = 0;
u8 spi_testH;
u8 spi_testL;
u16 spi_test;
u8 spi1_testH;
u8 spi1_testL;
u16 spi1_test;
void main()
{
    disableInterrupts();
    Init_System();
    
    //MPU_set_offset(0);
    power_on();
    //SystemSleep();
    enableInterrupts();
    
//    while(1)
//    {
//        if(UART_Receive_Data()==0x01)
//        {
//            //MPU_set_offset(0);
//            break;
//        }
//    }
    while(1)
    {
        RESET_TIME3;
        MpuGetData();
        get_time = GET_TIME3;
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
        UART_Send_Data(acc_scale);
        UART_Send_Data(gyo_scale);
    }
    
    while(1)
    {
        OS.executeTask(); 
    }
}

