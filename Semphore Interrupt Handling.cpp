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

/////////////////Code Block 1
#include <vxWorks.h>
#include <intLib.h>
#include <taskLib.h>
#include <stdio.h>
#include <stdint.h>

// Memory-mapped FIFO register addresses (update with actual addresses)
#define UART_FIFO_BASE_ADDR   0xFF000000
#define UART_FIFO_DATA_REG    (UART_FIFO_BASE_ADDR + 0x30)  // FIFO data register
#define UART_FIFO_STATUS_REG  (UART_FIFO_BASE_ADDR + 0x34)  // FIFO status register
#define UART_FIFO_EMPTY_FLAG  (1 << 0)  // Bit indicating FIFO is empty

// Shared flag between ISR and main function
volatile bool uartInterruptFlag = false;

// ISR triggered by the UART interrupt
void uartIsr(void) {
    // Set the flag to indicate data is available
    uartInterruptFlag = true;

    // Optionally clear the interrupt in hardware (if required)
    // Example:
    // #define UART_INTERRUPT_ACK_REG (UART_FIFO_BASE_ADDR + 0x3C)
    // volatile uint32_t *interruptAckReg = reinterpret_cast<uint32_t *>(UART_INTERRUPT_ACK_REG);
    // *interruptAckReg = 1;  // Acknowledge the interrupt
}

// Function to process all available FIFO data
void processFifoData() {
    // Pointers to FIFO status and data registers
    volatile uint32_t *fifoStatusReg = reinterpret_cast<uint32_t *>(UART_FIFO_STATUS_REG);
    volatile uint32_t *fifoDataReg = reinterpret_cast<uint32_t *>(UART_FIFO_DATA_REG);

    // Read and process all data while the FIFO is not empty
    while (!(*fifoStatusReg & UART_FIFO_EMPTY_FLAG)) {
        uint32_t data = *fifoDataReg;  // Read the next message
        printf("Received FIFO data: 0x%X\n", data);  // Handle the message (example processing)
    }
}

// Function to perform other ongoing application work
void performMainWork() {
    // Simulate ongoing work
    printf("Main application is running...\n");
    taskDelay(100);  // Sleep for a short period to simulate work
}

int main() {
    // Register the ISR (replace UART_IRQ_NUM with your UART IRQ number)
    int irqNumber = UART_IRQ_NUM;
    if (intConnect(INUM_TO_IVEC(irqNumber), (VOIDFUNCPTR)uartIsr, 0) != OK) {
        printf("Failed to connect UART ISR\n");
        return -1;
    }

    // Enable the interrupt
    intEnable(irqNumber);

    while (true) {
        // Perform other main application logic
        performMainWork();

        // Check the flag set by the ISR
        if (uartInterruptFlag) {
            // Clear the flag
            uartInterruptFlag = false;

            // Process all available FIFO data
            processFifoData();
        }
    }

    return 0;
}

