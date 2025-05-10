# Elevator Control System

This repository contains VHDL code for a comprehensive Elevator Control System. The system is modularized into various VHDL modules, each serving a specific functionality.
![elevator](https://github.com/SuzyAdel/Elevator-Control-System/assets/128175020/08c6e36d-9467-4e1a-82fa-e9eeeda1cbbc)

## Table of Contents
- [Purpose](#purpose)
@@ -22,6 +23,8 @@ The Elevator Control System is designed to address the complex task of managing

### Key Features:

![control](https://github.com/SuzyAdel/Elevator-Control-System/assets/128175020/49bb0f62-99fa-42e3-9797-c3e8caa462b9)

1. **Floor Control:** The system efficiently manages requests from various floors, prioritizing based on a First Come First Serve (FCFS) approach.

2. **Display System:** The 7-segment floor display provides clear information about the current floor and enhances user experience.
@@ -49,6 +52,9 @@ Traditional elevator control systems often lack flexibility and extensibility, m
### Up Counter 4-bit (up_counter_4_bit)
- Behavioral VHDL implementation of a 4-bit up counter.
- The counter increments on each rising clock edge, with optional clearing on a dedicated signal.
- 
  ![counter](https://github.com/SuzyAdel/Elevator-Control-System/assets/128175020/f9f86375-d0ad-4558-93bb-1b7b2a35edec)

- **Ports:**
  - `CLK`: Input clock signal.
  - `CLR`: Input clear signal.
@@ -58,6 +64,9 @@ Traditional elevator control systems often lack flexibility and extensibility, m
### Encoder 16-to-4 (enc_16_4)
- Behavioral VHDL module for encoding a 16-bit input into a 4-bit output.
- The encoding logic is based on specific conditions for each bit.
- 
  ![enc](https://github.com/SuzyAdel/Elevator-Control-System/assets/128175020/d803c5ff-206c-4382-b842-bf9d25c9a812)

- **Ports:**
  - `enc_in`: Input 16-bit vector to be encoded.
  - `enable`: Input signal enabling the encoding.
@@ -76,20 +85,31 @@ Traditional elevator control systems often lack flexibility and extensibility, m
### Floor Display (FloorDisplay)
- Behavioral VHDL module for a 7-segment display representing floor numbers from 0 to 15.
- It includes an optional binary-to-BCD converter for enhanced functionality.

![display](https://github.com/SuzyAdel/Elevator-Control-System/assets/128175020/d981a09f-35fa-4f25-bf01-4b78a64c1412)


- **Ports:**
  - `FLOOR`: Input binary representation of the floor number (0 to 15).
  - `SEG1`: Output for DISPLAY1.
  - `SEG2`: Output for DISPLAY2.

### Binary to BCD Converter (binary_to_bcd_converter)
- Behavioral VHDL module for converting a 4-bit binary input to two 4-bit BCD outputs.

![BCD-7](https://github.com/SuzyAdel/Elevator-Control-System/assets/128175020/1992ea78-5120-4b23-84fd-b5937a33a6ea)


- **Ports:**
  - `binary_in`: Input 4-bit binary vector.
  - `bcd0`: Output lower 4 bits of BCD.
  - `bcd1`: Output higher 4 bits of BCD.

### Clock Divider (clock_divider)
- Behavioral VHDL module for dividing the input clock frequency by a configurable factor.

![clockdiv](https://github.com/SuzyAdel/Elevator-Control-System/assets/128175020/0515a969-4108-4d0e-a695-1cc33d1f2d9d)

- **Ports:**
  - `clk`: Input clock signal.
  - `clk_out`: Output divided clock signal.
@@ -100,6 +120,9 @@ Traditional elevator control systems often lack flexibility and extensibility, m
### Elevator Control (Elevator_Control)
- Behavioral VHDL module for an elevator control system integrating multiple modules.
- Implements a state machine for elevator operation, floor requests, and door control.

![asm](https://github.com/SuzyAdel/Elevator-Control-System/assets/128175020/7a12fe06-8664-4199-af65-be5423fb7662)

- **Ports:**
  - `CLK`: Input clock signal.
  - `Keypad`: Input vector representing the keypad.
@@ -113,17 +136,4 @@ Traditional elevator control systems often lack flexibility and extensibility, m
  - `Display1`: Output 7-segment display for floor representation.
  - `Display2`: Output 7-segment display for floor representation.

  
![BCD-dec](https://github.com/SuzyAdel/Elevator-Control-System/assets/128175020/131fe869-34a4-4cb8-84b0-14059c4a3720)
