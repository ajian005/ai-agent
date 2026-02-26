# Hardware Engineer Skills

The Hardware Engineer designs, develops, and tests computer hardware components, such as circuit boards, processors, and memory devices. In the context of AI, this often overlaps with AI accelerators.

## Role Definition
Focuses on digital logic design, PCB design, embedded systems, and hardware acceleration (FPGA/ASIC).

## Skills & Tools

### 1. Digital Logic Design
Designing the logic of chips.

- **Tool: Verilog / VHDL**
  - *Description*: Hardware Description Languages (HDL).
  - *Practice*: Design logic gates, flip-flops, and state machines.
  - *Agent Prompt*: "Write a Verilog module for a 4-bit counter."

- **Tool: Simulation & Verification**
  - *Description*: Testing the logic before fabrication.
  - *Practice*: Use testbenches to verify timing and functionality.
  - *Agent Prompt*: "Write a testbench to verify the counter module."

### 2. PCB Design
Designing circuit boards.

- **Tool: Altium Designer / KiCad**
  - *Description*: PCB design software.
  - *Practice*: Schematic capture, layout, and routing.
  - *Agent Prompt*: "Explain the best practices for routing high-speed differential pairs."

- **Tool: Signal Integrity**
  - *Description*: Ensuring signals are transmitted without distortion.
  - *Practice*: Analyze impedance matching and crosstalk.
  - *Agent Prompt*: "How to minimize crosstalk in a multi-layer PCB?"

### 3. Embedded Systems
Programming close to the metal.

- **Tool: C / Assembly**
  - *Description*: Low-level programming languages.
  - *Practice*: Write drivers for sensors and peripherals.
  - *Agent Prompt*: "Write a C function to configure the I2C peripheral on an STM32 microcontroller."

- **Tool: Microcontrollers (MCU)**
  - *Description*: ARM Cortex-M, ESP32, Arduino.
  - *Practice*: Interface with hardware and manage power.
  - *Agent Prompt*: "Design a system to read a temperature sensor and send data via UART."

### 4. AI Hardware Acceleration
Specialized hardware for AI.

- **Tool: FPGA (Field-Programmable Gate Array)**
  - *Description*: Reconfigurable hardware.
  - *Practice*: Implement custom accelerators for neural networks.
  - *Agent Prompt*: "Explain the advantages of using FPGAs for low-latency inference."

- **Tool: ASIC Design Flow**
  - *Description*: Application-Specific Integrated Circuit.
  - *Practice*: Understanding the flow from RTL to GDSII (Synthesis, Place & Route).
  - *Agent Prompt*: "Outline the steps in the digital ASIC design flow."
