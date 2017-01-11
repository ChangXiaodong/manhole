#include "common.h"
u32 count = 0;
void main()
{

    disableInterrupts();
    Init_System();
    //SystemSleep();
    //enableInterrupts();
    while(1)
    {
    TEST1_HIGH;
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
    TEST1_LOW;
    count++;
    }

    while(1)
    {
        OS.executeTask(); 
    }
}

