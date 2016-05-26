#include "stm8l15x_flash.h"
void setPHYAddress(uint16 address);
uint16_t getPHYAddress();
uint16 test_address;
#define EEPROM_START  0x0010FE
#define PHY_ADDRESS   0x0002

int main( void )
{
  setPHYAddress(PHY_ADDRESS);
  test_address = getPHYAddress();
  while(1);
}

void setPHYAddress(uint16 address)
{
    FLASH_Unlock(FLASH_MemType_Data);
    FLASH_ProgramByte(EEPROM_START,address>>8);
    FLASH_ProgramByte(EEPROM_START+1,address);
    FLASH_Lock(FLASH_MemType_Data);
}
uint16_t getPHYAddress()
{
    uint16 address = 0;
    address =  FLASH_ReadByte(EEPROM_START)<<8;
    address |= FLASH_ReadByte(EEPROM_START+1);
    return address;
}
