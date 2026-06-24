# Week 4: Motor Control Firmware (Aido Rover)

This repository contains the closed-loop velocity controller for the Aido Rover wheel motor, implemented on an ESP32-S3.

## Project Structure
* `src/main.cpp`: Contains the PI controller logic, the software-simulated first-order DC motor plant, and UART telemetry output.
* `platformio.ini`: PlatformIO configuration file (Environment: ESP32-S3 DevKitC-1, Framework: Arduino, Baud rate: 115200).

## How to Flash and Run
1. Install **Visual Studio Code** and the **PlatformIO IDE** extension.
2. Open this `wk4-motor-control` folder in VS Code.
3. Connect your ESP32-S3 development board to your computer via USB.
4. Click the **Upload** (→) button in the bottom PlatformIO toolbar to compile and flash the firmware.
5. Click the **Serial Monitor** (plug icon) in the bottom toolbar to view the telemetry data (Time, Target Velocity, Actual Velocity).