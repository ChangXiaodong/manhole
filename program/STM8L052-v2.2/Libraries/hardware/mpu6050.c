#include "mpu6050.h"

struct ACCELSTRUCT accelStruct = {0,0,0};
struct GYROSTRUCT	gyroStruct = {0,0,0};


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
//�ȴ�ACK,Ϊ1������ACK Ϊ0����ȵ���ACK
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

//static void ComSendAck(void)
//{
//	MPU_SCL_LOW;
//	MPU_SDA_OUT();
//    MPU_SDA_LOW;
//	delay_us(2);
//    MPU_SCL_HIGH;
//    delay_us(5);
//    MPU_SCL_LOW;
//    delay_us(5);
//}

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

/*
*��ʼ��������0����ʧ�� ����1����ɹ�
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


//��ȡ��Ӧ�Ĳ�������
void MpuGetData(void)
{
    //s16 temp = 0;
    accelStruct.accelX =  MpuReadTwoByte(MPU6050_RA_ACCEL_XOUT_H) + accelStruct.accx_offset;
    accelStruct.accelY =  MpuReadTwoByte(MPU6050_RA_ACCEL_YOUT_H) + accelStruct.accy_offset;
    accelStruct.accelZ =  MpuReadTwoByte(MPU6050_RA_ACCEL_ZOUT_H) + accelStruct.accz_offset;
    gyroStruct.gyroX =   MpuReadTwoByte(MPU6050_RA_GYRO_XOUT_H) + gyroStruct.gyox_offset;
    gyroStruct.gyroY =  MpuReadTwoByte(MPU6050_RA_GYRO_YOUT_H) + gyroStruct.gyoy_offset;
    gyroStruct.gyroZ =  MpuReadTwoByte(MPU6050_RA_GYRO_ZOUT_H) + gyroStruct.gyoz_offset;
    //temp = MpuReadTwoByte(MPU6050_RA_TEMP_OUT_H); 
}

//u8 MPU_Set_Rate(u16 rate)
//{
//        u8 data;
//        if(rate>1000)rate=1000;
//        if(rate<4)rate=4;
//        data=1000/rate-1;
//        data=MPUWriteReg(MPU_SAMPLE_RATE_REG,data);        //�������ֵ�ͨ�˲���
//        return MPU_Set_LPF(rate/2);        //�Զ�����LPFΪ�����ʵ�һ��
//}

void MPU_set_offset(u16 zero)
{
    accelStruct.accelX =  MpuReadTwoByte(MPU6050_RA_ACCEL_XOUT_H);
    accelStruct.accelY =  MpuReadTwoByte(MPU6050_RA_ACCEL_YOUT_H);
    accelStruct.accelZ =  MpuReadTwoByte(MPU6050_RA_ACCEL_ZOUT_H);
    gyroStruct.gyroX =   MpuReadTwoByte(MPU6050_RA_GYRO_XOUT_H);
    gyroStruct.gyroY =  MpuReadTwoByte(MPU6050_RA_GYRO_YOUT_H);
    gyroStruct.gyroZ =  MpuReadTwoByte(MPU6050_RA_GYRO_ZOUT_H);
    
    accelStruct.accx_offset = zero - accelStruct.accelX;
    accelStruct.accy_offset = zero - accelStruct.accelY;
    accelStruct.accz_offset = zero - accelStruct.accelZ;
    gyroStruct.gyox_offset = zero - gyroStruct.gyroX;
    gyroStruct.gyoy_offset = zero - gyroStruct.gyroY;
    gyroStruct.gyoz_offset = zero - gyroStruct.gyroZ;
    
}
