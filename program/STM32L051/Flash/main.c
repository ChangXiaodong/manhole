#include "stm32l051xx.h"
#include "stm32l0xx.h"
#include "stm32l0xx_hal_def.h"
#include "stm32l0xx_hal_flash.h"

FLASH_ProcessTypeDef ProcFlash;

#define FLASH_ADDRESS  0x08080100
#define PHY_ADDRESS   0x00001111
uint32_t flash_test = 0;

int main(void)
{
    SystemInit();
    flash_test = 123;
    HAL_FLASH_Unlock();
    HAL_FLASH_Program(FLASH_TYPEPROGRAMDATA_WORD,FLASH_ADDRESS,PHY_ADDRESS);
    HAL_FLASH_Lock();
    flash_test = FLASH_ReadByte(FLASH_ADDRESS);
    
    for (;;)
    {
        __ASM("nop");
    }
}

void SystemInit (void)
{    
    /*!< Set MSION bit */
    RCC->CR |= (uint32_t)0x00000100U;
    
    /*!< Reset SW[1:0], HPRE[3:0], PPRE1[2:0], PPRE2[2:0], MCOSEL[2:0] and MCOPRE[2:0] bits */
    RCC->CFGR &= (uint32_t) 0x88FF400CU;
    
    /*!< Reset HSION, HSIDIVEN, HSEON, CSSON and PLLON bits */
    RCC->CR &= (uint32_t)0xFEF6FFF6U;
    
    /*!< Reset HSI48ON  bit */
    RCC->CRRCR &= (uint32_t)0xFFFFFFFEU;
    
    /*!< Reset HSEBYP bit */
    RCC->CR &= (uint32_t)0xFFFBFFFFU;
    
    /*!< Reset PLLSRC, PLLMUL[3:0] and PLLDIV[1:0] bits */
    RCC->CFGR &= (uint32_t)0xFF02FFFFU;
    
    /*!< Disable all interrupts */
    RCC->CIER = 0x00000000U;
    
    /* Configure the Vector Table location add offset address ------------------*/
#ifdef VECT_TAB_SRAM
    SCB->VTOR = SRAM_BASE | 0x00U; /* Vector Table Relocation in Internal SRAM */
#else
    SCB->VTOR = FLASH_BASE | 0x00U; /* Vector Table Relocation in Internal FLASH */
#endif
}

static void FLASH_SetErrorCode(void)
{  
    if(__HAL_FLASH_GET_FLAG(FLASH_FLAG_WRPERR))
    { 
        ProcFlash.ErrorCode |= HAL_FLASH_ERROR_WRP;
    }
    if(__HAL_FLASH_GET_FLAG(FLASH_FLAG_PGAERR))
    { 
        ProcFlash.ErrorCode |= HAL_FLASH_ERROR_PGA;
    }
    if(__HAL_FLASH_GET_FLAG(FLASH_FLAG_SIZERR))
    { 
        ProcFlash.ErrorCode |= HAL_FLASH_ERROR_SIZE;
    }
    if(__HAL_FLASH_GET_FLAG(FLASH_FLAG_OPTVERR))
    { 
        /* WARNING : On the first cut of STM32L031xx and STM32L041xx devices,
        *           (RefID = 0x1000) the FLASH_FLAG_OPTVERR bit was not behaving
        *           as expected. If the user run an application using the first
        *           cut of the STM32L031xx device or the first cut of the STM32L041xx
        *           device, this error should be ignored. The revId of the device
        *           can be retrieved via the HAL_GetREVID() function.
        *
        */
        ProcFlash.ErrorCode |= HAL_FLASH_ERROR_OPTV;
    }
    if(__HAL_FLASH_GET_FLAG(FLASH_FLAG_RDERR))
    { 
        ProcFlash.ErrorCode |= HAL_FLASH_ERROR_RD;
    }
    if(__HAL_FLASH_GET_FLAG(FLASH_FLAG_FWWERR))
    { 
        ProcFlash.ErrorCode |= HAL_FLASH_ERROR_FWWERR;
    }
    if(__HAL_FLASH_GET_FLAG(FLASH_FLAG_NOTZEROERR))
    { 
        ProcFlash.ErrorCode |= HAL_FLASH_ERROR_NOTZERO;
    }
    
    /* Errors are now stored, clear errors flags */
    
    __HAL_FLASH_CLEAR_FLAG(FLASH_FLAG_WRPERR | FLASH_FLAG_PGAERR | FLASH_FLAG_SIZERR |
                           FLASH_FLAG_OPTVERR | FLASH_FLAG_RDERR | FLASH_FLAG_FWWERR | 
                               FLASH_FLAG_NOTZEROERR);
} 

HAL_StatusTypeDef FLASH_WaitForLastOperation(uint32_t Timeout)
{
    /* Wait for the FLASH operation to complete by polling on BUSY flag to be reset.
    Even if the FLASH operation fails, the BUSY flag will be reset and an error
    flag will be set */
    
    uint32_t tickstart = HAL_GetTick();   
    
    while(__HAL_FLASH_GET_FLAG(FLASH_FLAG_BSY) != RESET) 
    { 
        if(Timeout != HAL_MAX_DELAY)
        {
            if((Timeout == 0U)||((HAL_GetTick() - tickstart ) > Timeout))
            {
                return HAL_TIMEOUT;
            }
        } 
    }
    
    /* Check FLASH End of Operation flag  */
    if (__HAL_FLASH_GET_FLAG(FLASH_FLAG_EOP))
    {
        /* Clear FLASH End of Operation pending bit */
        __HAL_FLASH_CLEAR_FLAG(FLASH_FLAG_EOP);
    }
    
    
    if((__HAL_FLASH_GET_FLAG(FLASH_FLAG_WRPERR) != RESET) || (__HAL_FLASH_GET_FLAG(FLASH_FLAG_PGAERR)  != RESET) || \
        (__HAL_FLASH_GET_FLAG(FLASH_FLAG_SIZERR) != RESET) || (__HAL_FLASH_GET_FLAG(FLASH_FLAG_OPTVERR) != RESET) || \
            (__HAL_FLASH_GET_FLAG(FLASH_FLAG_RDERR)  != RESET) || (__HAL_FLASH_GET_FLAG(FLASH_FLAG_FWWERR)  != RESET) || \
                (__HAL_FLASH_GET_FLAG(FLASH_FLAG_NOTZEROERR) != RESET))
    {
        /* Save the error code */
        
        /* WARNING : On the first cut of STM32L031xx and STM32L041xx devices,
        *           (RefID = 0x1000) the FLASH_FLAG_OPTVERR bit was not behaving
        *           as expected. If the user run an application using the first
        *           cut of the STM32L031xx device or the first cut of the STM32L041xx
        *           device, this error should be ignored. The revId of the device
        *           can be retrieved via the HAL_GetREVID() function.
        *
        */
        FLASH_SetErrorCode();
        return HAL_ERROR;
    }
    
    /* There is no error flag set */
    return HAL_OK;  
}

HAL_StatusTypeDef HAL_FLASH_Program(uint32_t TypeProgram, uint32_t Address, uint32_t Data)
{
    HAL_StatusTypeDef status = HAL_ERROR;
    
    /* Process Locked */
    __HAL_LOCK(&ProcFlash);
    
    /* Check the parameters */
    assert_param(IS_FLASH_TYPEPROGRAM(TypeProgram));
    
    /* Wait for last operation to be completed */
    status = FLASH_WaitForLastOperation(FLASH_TIMEOUT_VALUE);
    
    if(status == HAL_OK)
    {
        /* Program word (32-bit) at a specified address */
        *(__IO uint32_t*)Address = (uint32_t) Data;
        
        /* Wait for last operation to be completed */
        status = FLASH_WaitForLastOperation(FLASH_TIMEOUT_VALUE);
    }
    
    /* Process Unlocked */
    __HAL_UNLOCK(&ProcFlash);
    
    return status;  
}

HAL_StatusTypeDef HAL_FLASH_Unlock(void)  
{
    if((FLASH->PECR & FLASH_PECR_PRGLOCK) != RESET)
    {
        /* Unlocking FLASH_PECR register access */
        if((FLASH->PECR & FLASH_PECR_PELOCK) != RESET)
        {  
            FLASH->PEKEYR = FLASH_PEKEY1;
            FLASH->PEKEYR = FLASH_PEKEY2;
        }
        
        /* Unlocking the program memory access */
        FLASH->PRGKEYR = FLASH_PRGKEY1;
        FLASH->PRGKEYR = FLASH_PRGKEY2;  
    }
    else
    {
        return HAL_ERROR;
    }
    
    return HAL_OK; 
}

HAL_StatusTypeDef HAL_FLASH_Lock(void)
{
    /* Set the PRGLOCK Bit to lock the program memory access */
    SET_BIT(FLASH->PECR, FLASH_PECR_PRGLOCK);
    
    return HAL_OK;
}

uint32_t FLASH_ReadByte(uint32_t Address)
{
    return(*(__IO uint32_t*) (uint32_t)Address);
}

void assert_failed(uint8_t* file, uint32_t line)
{
}

