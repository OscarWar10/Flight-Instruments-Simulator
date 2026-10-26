**Language:** 🇺🇸 English | [🇪🇸 Español](README.md) 

# Real-Time Flight Parameter Monitoring Simulator

This project was developed as part of my Bachelor´s Degree Final Project in Computer Engineering.

The main objective of the project is to design and implement a real-time flight parameter monitoring simulator that integrates embedded systems, electronic sensors, wireless communication and graphical visualization applications.

The system consists of a physical aircraft model equipped with an **ESP32 Microcontroller**, an **Inertial Measurement Unit** IMU, a **Potentiometer** and a **Joystick**. Communication between ESP32 and IMU takes place via I²C protocol. The ESP32 collects and processes sensor and control input data, transmitting the information wirelessly via Wi-Fi using the UDP protocol to two independent applications:

- **MATLAB/Simulink (Flight Instruments Simulator)**: A flight instrumentation interface displaying six primary flight instruments. Airspeed Indicator, Attitude Indicator, Altimeter, Heading Indicator, Vertical Speed Indicator and Turn Coordinator.
- **Python/PyQt (Flight Controls Simulator)**: A graphical interface inspired by the Airbus ECAM Flight Controls (F/CTL) page, providing real-time visualization of the aircraft control surfaces. Ailerons, Elevators, Rudder and Spoilers.

The aircraft model is manually manipulated to simulate changes in orientation or attitude, while the potentiometer and joystick provide additional inputs for airspeed and control surface movement among others.

The project demonstrates the integration between hardware and software to acquire, process, transmit and visualize flight-related parameters in real time.

***Technologies Used:***
- *Microcontroller: ESP32-WROOM-32 38 pin layout.*
- *Sensors: Pololu AltIMU-10 v5 (accelerometer, gyroscope, magnetometer and barometer), Potentiometer and PS2 Joystick.*
- *Programming languages: Arduino, Python and MATLAB.*
- *Communication Protocols: I²C and UDP.*
- *Signal processing: Complementary Filtering, Magnetometer Hard-Iron Calibration, Tilt Compensation.*
