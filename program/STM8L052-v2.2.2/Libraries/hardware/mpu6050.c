#include "mpu6050.h"

struct ACCELSTRUCT accelStruct = {0,0,0};
struct GYROSTRUCT	gyroStruct = {0,0,0};
u8 acc_scale = 0;
u8 gyo_scale = 0;
u8 acc_fchoice = 0;
u8 acc_dlpf = 0;
u8 gyo_fchoice = 0;
u8 gyo_dlpf = 0;


//IO��������
#define MPU_SDA_IN()  MPU_SDA_PORT->DDR &= (uint8_t)(~(MPU_SDA_BIT))
#define MPU_SDA_OUT() MPU_SDA_PORT->DDR |= MPU_SDA_BIT

//IO��������	 
#define MPU_READ_SDA   ((BitStatus)(MPU_SDA_PORT->IDR & (uint8_t)MPU_SDA_BIT))


/**************************MPU5883 IIC��������*********************************/

static void MPU5883IOInit(void)
{
    GPIO_Init(MPU_SDA_PORT,MPU_SDA_BIT,GPIO_Mode_Out_PP_High_Fast); 
    GPIO_Init(MPU_SCL_PORT,MPU_SCL_BIT,GPIO_Mode_Out_PP_High_Fast); 
}

//����IIC��ʼ�ź�
inline void ComStart(void)
{
    MPU_SDA_OUT();     //sda�����
    MPU_SDA_HIGH;	  	  
    MPU_SCL_HIGH;
    delay_1us;
    MPU_SDA_LOW;//START:when CLK is high,DATA change form high to low 
    delay_1us;
    MPU_SCL_LOW;//ǯסI2C���ߣ�׼�����ͻ��������
}
//����IICֹͣ�ź�
inline void ComStop(void)
{
    MPU_SDA_OUT();//sda�����
    MPU_SDA_LOW;//STOP:when CLK is high DATA change form low to high
    MPU_SCL_HIGH;
    delay_1us;
    MPU_SDA_HIGH;//����I2C���߽����ź�
    delay_1us;		
}
//�ȴ�ACK,Ϊ1������ACK Ϊ0�����ȵ���ACK
static u8 ComWaitAck(void)
{
    u8 waitTime = 0;
    MPU_SDA_OUT();//sda�����
    MPU_SDA_HIGH;
    delay_1us;
    MPU_SDA_IN();      //SDA����Ϊ����
    MPU_SCL_HIGH;
    delay_1us;
    while(MPU_READ_SDA)
    {
        waitTime++;
        delay_1us;
        if(waitTime > MPU_ACK_WAIT_TIME)
        {
            ComStop();
            return 1;
        }
    }
    MPU_SCL_LOW;
    return 0;
    
}


static void ComSendNoAck(void)
{
    MPU_SCL_LOW;
    MPU_SDA_OUT();
    MPU_SDA_HIGH;
    delay_1us;
    MPU_SCL_HIGH;
    delay_1us;
    MPU_SCL_LOW;
    delay_1us;
}
//����0 д���յ�ACK ����1д��δ�յ�ACK
static u8 ComSendByte(u8 byte)
{
    u8 t;   
    MPU_SDA_OUT(); 	
    for(t=0;t<8;t++)
    {              
        if((byte&0x80)>>7)
        {
            MPU_SDA_HIGH;
        }
        else
        {
            MPU_SDA_LOW;
        }
        byte<<=1; 	   
        MPU_SCL_HIGH;
        delay_1us; 
        MPU_SCL_LOW;
        delay_1us;
    }
    return ComWaitAck();
}

static void ComReadByte(u8* byte)
{
    u8 i,receive=0;
    MPU_SDA_IN();//SDA����Ϊ����
    for(i=0;i<8;i++ )
    {
        receive <<= 1;
        MPU_SCL_HIGH; 
        delay_1us;
        if(MPU_READ_SDA)receive++;
        MPU_SCL_LOW; 
        delay_1us;
    }					  
    *byte = receive;
}

/**************************MPU5883 IIC��������*********************************/


//��MPUд��һ���ֽ�����,ʧ�ܷ���1 �ɹ�����0
u8 MPUWriteReg(u8 regValue,u8 setValue)
{
    u8 res;
    ComStart();                 	//��ʼ�ź�
    res = ComSendByte(MPU_ADDR);    //�����豸��ַ+д�ź�
    if(res)
    {
        return res;
    }
    res = ComSendByte(regValue);    //�ڲ��Ĵ�����ַ
    if(res)
    {
        return res;
    }
    res = ComSendByte(setValue);    //�ڲ��Ĵ�������
    if(res)
    {
        return res;
    }
    ComStop();                   	//����ֹͣ�ź�
    return res;
}

//**************************************
//��I2C�豸��ȡһ���ֽ����� ����ֵ ��ȡ�ɹ���ʧ��
//**************************************
u8 MPUReadReg(u8 regAddr,u8* readValue)
{
    u8 res;
    ComStart();                 		//��ʼ�ź�
    res = ComSendByte(MPU_ADDR);    	//�����豸��ַ+д�ź�
    if(res)
    {
        return res;
    }
    res = ComSendByte(regAddr);     	//���ʹ洢��Ԫ��ַ����0��ʼ	
    if(res)
    {
        return res;
    }
    ComStart();                 		//��ʼ�ź�
    res = ComSendByte(MPU_ADDR+1);  	//�����豸��ַ+���ź�
    if(res)
    {
        return res;
    }
    ComReadByte(readValue);     		//�����Ĵ�������
    ComSendNoAck();               		//���ͷ�Ӧ���ź�
    ComStop();                  		//ֹͣ�ź�
    return res;
}

//MPU��ȡ�����ֽڵ�����
s16 MpuReadTwoByte(u8 addr)
{
    u8 H,L;

    MPUReadReg(addr,&H);
    MPUReadReg(addr+1,&L);
    return (s16)((((u16)H)<<8)+L);   //�ϳ�����
}

s16 MpuReadTwoByteSPI(u8 addr)
{
    u8 H,L;
    SPI_ReadRegByte(addr,&H);
    SPI_ReadRegByte(addr+1,&L);

    return (s16)((((u16)H)<<8)+L);   //�ϳ�����
}

/*
*��ʼ��������0����ʧ�� ����1�����ɹ�
**/
u8 Init_MPU6050(void)
{
    u8 result;
    u8 id = 0;
    MPU5883IOInit();
    delay_1ms;
    result = MPUReadReg(MPU6050_RA_WHO_AM_I,&id);
    if(result)
    {
        while(1)
        {
            LED1_ON;
            LED2_ON;
            LED3_ON;
            LED4_ON;
            LED5_ON;
            delay_ms(500);
            LED1_OFF;
            LED2_OFF;
            LED3_OFF;
            LED4_OFF;
            LED5_OFF;
            delay_ms(500);
        }
    }	//IIC���ߴ���
    else 
    {
        id &= 0x7e;//��ȥ���λ���λ
        id>>= 1;
        if(id != 0x34) return 1;	//��ȡ����оƬID����
    }
//    //��ʼ���ɹ������ò���
    MPUWriteReg(MPU6050_RA_PWR_MGMT_1,0x01);			// �˳�˯��ģʽ����ȡ��ʱ��Ϊ����X�ᡣ
    MPUWriteReg(MPU6050_RA_SMPLRT_DIV,0x01);			// ȡ��ʱ��4��Ƶ��1k/4��ȡ����Ϊ25Hz��
    MPUWriteReg(MPU6050_RA_CONFIG,7);				    // �رյ�ͨ�˲���
    MPUWriteReg(MPU6050_RA_GYRO_CONFIG,3<<3);			// �������̣�2000dps
    MPUWriteReg(MPU6050_RA_ACCEL_CONFIG,2<<3);			// ���ٶȼ����̣�8g��
    MPUWriteReg(MPU6050_RA_INT_PIN_CFG,0x32);					// �ж��ź�Ϊ�ߵ�ƽ�����������ֱ���ж�ȡ��������ʧ��ֱͨ����I2C��
    MPUWriteReg(MPU6050_RA_INT_ENABLE,0x01);					// ʹ�á�����׼���á��жϡ�
    MPUWriteReg(MPU6050_RA_USER_CTRL,0x00);					// ��ʹ�ø���I2C��
    return 0;

}


void MpuGetData(void)
{
  accelStruct.accelX = MpuReadTwoByteSPI(MPU6050_RA_ACCEL_XOUT_H) + accelStruct.accx_offset;
  accelStruct.accelY = MpuReadTwoByteSPI(MPU6050_RA_ACCEL_YOUT_H) + accelStruct.accy_offset;
  accelStruct.accelZ = MpuReadTwoByteSPI(MPU6050_RA_ACCEL_ZOUT_H) + accelStruct.accz_offset;
  gyroStruct.gyroX = MpuReadTwoByteSPI(MPU6050_RA_GYRO_XOUT_H) + gyroStruct.gyox_offset;
  gyroStruct.gyroY = MpuReadTwoByteSPI(MPU6050_RA_GYRO_YOUT_H) + gyroStruct.gyoy_offset;
  gyroStruct.gyroZ = MpuReadTwoByteSPI(MPU6050_RA_GYRO_ZOUT_H) + gyroStruct.gyoz_offset;
  
}


void MPU_set_offset(u16 zero)
{
    accelStruct.accelX =  MpuReadTwoByteSPI(MPU6050_RA_ACCEL_XOUT_H);
    accelStruct.accelY =  MpuReadTwoByteSPI(MPU6050_RA_ACCEL_YOUT_H);
    accelStruct.accelZ =  MpuReadTwoByteSPI(MPU6050_RA_ACCEL_ZOUT_H);
    gyroStruct.gyroX =   MpuReadTwoByteSPI(MPU6050_RA_GYRO_XOUT_H);
    gyroStruct.gyroY =  MpuReadTwoByteSPI(MPU6050_RA_GYRO_YOUT_H);
    gyroStruct.gyroZ =  MpuReadTwoByteSPI(MPU6050_RA_GYRO_ZOUT_H);
    
    accelStruct.accx_offset = zero - accelStruct.accelX;
    accelStruct.accy_offset = zero - accelStruct.accelY;
    accelStruct.accz_offset = zero - accelStruct.accelZ;
    gyroStruct.gyox_offset = zero - gyroStruct.gyroX;
    gyroStruct.gyoy_offset = zero - gyroStruct.gyroY;
    gyroStruct.gyoz_offset = zero - gyroStruct.gyroZ;
}

void SPI_6500_IOInit(void)
{
  GPIO_Init(SPI_CS_PORT,SPI_CS_BIT,GPIO_Mode_Out_PP_High_Fast);
  GPIO_Init(SPI_MISO_PORT,SPI_MISO_BIT,GPIO_Mode_In_FL_No_IT);
  GPIO_Init(SPI_MOSI_PORT,SPI_MOSI_BIT,GPIO_Mode_Out_PP_High_Fast);
  GPIO_Init(SPI_CLK_PORT,SPI_CLK_BIT,GPIO_Mode_Out_PP_Low_Fast);
}

void get_scale(u8 acc_config, u8 gyo_config)
{
    switch(acc_config>>3 & 0x03)
    {
        case 0:
            acc_scale = 2;
            break;
        case 1:
            acc_scale = 4;
            break;
        case 2:
            acc_scale = 8;
            break;
        case 3:
            acc_scale = 16;
            break;
    }
    switch(gyo_config>>3 & 0x03)
    {
        case 0:
            gyo_scale = 25;
            break;
        case 1:
            gyo_scale = 50;
            break;
        case 2:
            gyo_scale = 100;
            break;
        case 3:
            gyo_scale = 200;
            break;
    }
}

void Init_MPU6500_SPI(void)
{
    u8 id = 0;
    SPI_6500_IOInit();
    delay_1ms;
    SPI_ReadRegByte(MPU6050_RA_WHO_AM_I,&id);
    if((id!=0x70)&&(id!=0x73))
    {
        while(1)
        {
            LED1_ON;
            LED2_ON;
            LED3_ON;
            LED4_ON;
            LED5_ON;
            delay_ms(500);
            LED1_OFF;
            LED2_OFF;
            LED3_OFF;
            LED4_OFF;
            LED5_OFF;
            delay_ms(500);
        }
    }	//IIC���ߴ���
    
    SPI_WriteRegByte(MPU6050_RA_PWR_MGMT_1,0x00);			
    delay_ms(100);                                            
    SPI_WriteRegByte(MPU6050_RA_SIGNAL_PATH_RESET,0x07);
    delay_ms(100);
    SPI_WriteRegByte(MPU6050_RA_SMPLRT_DIV,0x00);
    gyo_dlpf = 7;
    SPI_WriteRegByte(MPU6050_RA_CONFIG,gyo_dlpf);  
    gyo_scale = 3;
    gyo_fchoice = 1;
    
    SPI_WriteRegByte(MPU6050_RA_GYRO_CONFIG,(gyo_scale<<3) | gyo_fchoice);
    acc_scale = 2;
    acc_fchoice = 0;
    acc_dlpf = 0;
    SPI_WriteRegByte(MPU6050_RA_ACCEL_CONFIG,0x00 | (acc_scale)<<3);             //2G:0x00  4G:0x08  8G:0x10   16G:0x18
    SPI_WriteRegByte(MPU6050_RA_ACCEL_CONFIG2,acc_fchoice<<3|acc_dlpf);
    SPI_WriteRegByte(MPU6050_RA_INT_PIN_CFG,0x00/*0x32*/);					
    SPI_WriteRegByte(MPU6050_RA_INT_ENABLE,0x00/*0x01*/);					
    SPI_WriteRegByte(MPU6050_RA_USER_CTRL,0x11);	
}

/*
**
**
**
**
*/

void set_config(u8* data)
{
    u8 id = 0;
    
    if((data[0]>3)||(data[3]>3)||(data[1]>1)||(data[4]>3)||(data[2]>7)||(data[5]>7))
    {
        return;
    }
    acc_scale = data[0];
    acc_fchoice = data[1];
    acc_dlpf = data[2];
    gyo_scale = data[3];
    gyo_fchoice = data[4];
    gyo_dlpf = data[5];
    
    SPI_6500_IOInit();
    delay_1ms;
    SPI_ReadRegByte(MPU6050_RA_WHO_AM_I,&id);
    if((id!=0x70)&&(id!=0x73))
    {
        while(1)
        {
            LED1_ON;
            LED2_ON;
            LED3_ON;
            LED4_ON;
            LED5_ON;
            delay_ms(500);
            LED1_OFF;
            LED2_OFF;
            LED3_OFF;
            LED4_OFF;
            LED5_OFF;
            delay_ms(500);
        }
    }	//IIC���ߴ���
    
    SPI_WriteRegByte(MPU6050_RA_PWR_MGMT_1,0x00);			
    delay_ms(100);                                            
    SPI_WriteRegByte(MPU6050_RA_SIGNAL_PATH_RESET,0x07);
    delay_ms(100);
    SPI_WriteRegByte(MPU6050_RA_SMPLRT_DIV,0x00);
    SPI_WriteRegByte(MPU6050_RA_CONFIG,gyo_dlpf);  
    SPI_WriteRegByte(MPU6050_RA_GYRO_CONFIG,(gyo_scale<<3) | gyo_fchoice);
    SPI_WriteRegByte(MPU6050_RA_ACCEL_CONFIG,0x00 | (acc_scale)<<3);             //2G:0x00  4G:0x08  8G:0x10   16G:0x18
    SPI_WriteRegByte(MPU6050_RA_ACCEL_CONFIG2,acc_fchoice<<3|acc_dlpf);
    SPI_WriteRegByte(MPU6050_RA_INT_PIN_CFG,0x00/*0x32*/);					
    SPI_WriteRegByte(MPU6050_RA_INT_ENABLE,0x00/*0x01*/);					
    SPI_WriteRegByte(MPU6050_RA_USER_CTRL,0x11);	
}
