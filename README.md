**Idioma:** 🇪🇸 Español | [🇺🇸 English](README_EN.md)

# Simulador para Monitorización en Tiempo Real de Parámetros de Vuelo.

Este proyecto se desarrolló como parte de mi TFG del Grado en Ingeniería de Computadores.

El objetivo principal del proyecto es diseñar e implementar un simulador que permita monitorizar parámetros de vuelo en tiempo real mediante la integración de sistemas embebidos, sensores, comunicación inalámbrica y visualización gráfica mediante aplicaciones.

El sistema consiste en una maqueta de avión equipada con un **Microcontrolador ESP32**, una **Unidad de Medida Inercial** IMU, un **Potenciómetro** y un **Joystick**. La comunicación entre la ESP32 y la IMU se lleva a cabo mediante el estándar/protocolo I²C. La ESP32 adquiere y procesa los datos de los sensores, transmite la información de forma inalámbrica vía Wi-Fi usando el protocolo UDP a dos aplicaciones independientes:

- **MATLAB/Simulink**: Aplicación en la que se muestran los seis instrumentos de vuelo principales (Six Pack). Airspeed Indicator, Attitude Indicator, Altimeter, Heading Indicator, Vertical Speed Indicator and Turn Coordinator.
- **Python/PyQt**: Interfaz gráfica en inspirada en la página Flight Controls (F/CTL) del sistema ECAM de Airbus, donde se muestran en tiempo real las superficies de control. Ailerons, Elevators, Rudder y Spoilers.

El propósito de la maqueta es que se realizan movimientos sobre ella para simular cambios en la orientación o la actitud. La manipulación del potenciómetro y el joystick aportan entradas para la velocidad y el movimiento de las superficies de control entre otras cosas.

El proyecto demuestra la integración entre hardware y software para adquirir, procesar, transmitir y visualizar parámetros de vuelo en tiempo real.
***Tecnologías Usadas:***
- *Microcontrolador: ESP32-WROOM-32 38 pines.*
- *Sensores: Pololu AltIMU-10 v5 (acelerómetro, giroscopio, magnetómetro y barómetro), Potenciómetro y Joystick PS2*
- *Lenguajes de programación: Arduino, Python y MATLAB.*
- *Protocolos de comunicación: I²C y UDP.*
- *Procesamiento de señales: Filtro complementario, Calibración Hard-Iron sobre el magnetómetro, compoensación por inclinación.*
