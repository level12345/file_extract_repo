///Flag with Polling (Non-Blocking)
//ISR Example
#include <vxWorks.h>

// Shared flag between ISR and main function
volatile bool uartInterruptFlag = false;

void uartIsr(void) {
    // Set the flag to indicate the interrupt occurred
    uartInterruptFlag = true;

    // Optionally clear the interrupt in the hardware
    // volatile uint32_t *uartStatusReg = reinterpret_cast<uint32_t *>(UART_BASE_ADDR + STATUS_OFFSET);
    // *uartStatusReg = INTERRUPT_CLEAR_FLAG;
}





// Main Function
#include <taskLib.h>

int main() {
    // Register the ISR
    setupUartInterrupt(UART_IRQ_NUM);

    while (true) {
        // Main application logic
        performMainWork();

        // Check the interrupt flag
        if (uartInterruptFlag) {
            uartInterruptFlag = false;  // Clear the flag

            // Read the UART register
            volatile uint32_t *uartRxReg = reinterpret_cast<uint32_t *>(UART_RX_REG);
            uint32_t data = *uartRxReg;

            // Process the data
            printf("Received UART data: 0x%X\n", data);
        }
    }

    return 0;
}

void performMainWork() {
    // Simulate some ongoing application work
    printf("Main application is running...\n");
    taskDelay(100);  // Sleep for a short period (optional)
}
//////////////////////////////////////////////////////////////////


Semaphore with Blocking


//ISR Example
#include <semLib.h>

// Shared semaphore for ISR to signal main function
SEM_ID uartSem;

void uartIsr(void) {
    // Signal the semaphore to wake the main function
    semGive(uartSem);

    // Optionally clear the interrupt in the hardware
    // volatile uint32_t *uartStatusReg = reinterpret_cast<uint32_t *>(UART_BASE_ADDR + STATUS_OFFSET);
    // *uartStatusReg = INTERRUPT_CLEAR_FLAG;
}

Main Function

#include <taskLib.h>
#include <semLib.h>

SEM_ID uartSem;  // Semaphore for UART interrupt

int main() {
    // Create the semaphore
    uartSem = semBCreate(SEM_Q_FIFO, SEM_EMPTY);
    if (uartSem == NULL) {
        printf("Failed to create semaphore\n");
        return -1;
    }

    // Register the ISR
    setupUartInterrupt(UART_IRQ_NUM);

    while (true) {
        // Perform ongoing application work
        performMainWork();

        // Try to take the semaphore (non-blocking)
        if (semTake(uartSem, NO_WAIT) == OK) {
            // Read the UART register
            volatile uint32_t *uartRxReg = reinterpret_cast<uint32_t *>(UART_RX_REG);
            uint32_t data = *uartRxReg;

            // Process the data
            printf("Received UART data: 0x%X\n", data);
        }
    }

    return 0;
}

void performMainWork() {
    // Simulate ongoing work
    printf("Main application is running...\n");
    taskDelay(100);  // Sleep for a short period (optional)
}
/////////////////////////////////////////////////

//Deferred Processing Task

///iSR Example
#include <semLib.h>

// Semaphore for interrupt signaling
SEM_ID uartSem;

void uartIsr(void) {
    // Signal the semaphore
    semGive(uartSem);
}

//Dedicated Task
void uartTask(void) {
    while (true) {
        // Wait for the ISR to signal
        if (semTake(uartSem, WAIT_FOREVER) == OK) {
            // Read the UART register
            volatile uint32_t *uartRxReg = reinterpret_cast<uint32_t *>(UART_RX_REG);
            uint32_t data = *uartRxReg;

            // Process the data
            printf("UART Task: Received data: 0x%X\n", data);
        }
    }
}


//Main Function
int main() {
    // Create the semaphore
    uartSem = semBCreate(SEM_Q_FIFO, SEM_EMPTY);

    // Register the ISR
    setupUartInterrupt(UART_IRQ_NUM);

    // Spawn the UART processing task
    taskSpawn("tUartTask", 100, 0, 4096, (FUNCPTR)uartTask, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

    while (true) {
        // Perform main application logic
        performMainWork();
    }

    return 0;
}


//Use semaphore


