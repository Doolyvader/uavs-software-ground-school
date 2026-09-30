# Week 4 - Flight Controllers

## Skill Booster 3: Protocol Pro

### Drone Mission
Autonomous mapping and inspection quadcopter.

### Flight Controller
- CubePilot Cube Orange+
- Firmware: PX4

### Components
- Flight Controller: Cube Orange+
- GNSS + Compass: Here3
- Companion Computer: NVIDIA Jetson
- Camera: RGB USB camera
- RC Receiver: SBUS-compatible receiver
- 4 ESCs
- 4 Brushless Motors

### Planned Communication Links
- Here3 → Flight Controller: CAN / DroneCAN
- Jetson → Flight Controller: UART / MAVLink
- RC Receiver → Flight Controller: SBUS
- Camera → Jetson: USB
- Flight Controller → ESCs: Motor control outputs

### Next Step
Create a wiring diagram and verify that every selected component is electrically and logically compatible.

## Wiring Diagram

```mermaid
flowchart TD

    CAM[RGB USB Camera]
    JETSON[NVIDIA Jetson<br/>Computer Vision / Planning]

    GPS[Here3 GNSS + Compass]
    RX[RC Receiver]

    FC[Cube Orange+<br/>PX4 Flight Controller]

    ESC1[ESC 1]
    ESC2[ESC 2]
    ESC3[ESC 3]
    ESC4[ESC 4]

    M1[Motor 1]
    M2[Motor 2]
    M3[Motor 3]
    M4[Motor 4]

    BAT[LiPo Battery]
    PWR[Power Distribution / Regulators]

    CAM -->|USB| JETSON

    JETSON <-->|UART + MAVLink| FC

    GPS -->|CAN / DroneCAN| FC
    RX -->|SBUS| FC

    FC -->|PWM| ESC1
    FC -->|PWM| ESC2
    FC -->|PWM| ESC3
    FC -->|PWM| ESC4

    ESC1 --> M1
    ESC2 --> M2
    ESC3 --> M3
    ESC4 --> M4

    BAT --> PWR
    PWR --> FC
    PWR --> JETSON
    PWR --> ESC1
    PWR --> ESC2
    PWR --> ESC3
    PWR --> ESC4


    ## Compatibility Check

| Component | Connection | Protocol | Compatibility |
|---|---|---|---|
| Here3 GNSS + Compass | Cube Orange+ CAN port | DroneCAN | Compatible. Here3 supports DroneCAN and Cube Orange+ provides CAN interfaces. |
| NVIDIA Jetson | Cube Orange+ TELEM2 | UART + MAVLink | Compatible. PX4 commonly uses TELEM2 for companion-computer MAVLink communication. |
| RC Receiver | Cube Orange+ RCIN | SBUS | Compatible. Cube Orange+ supports S.Bus receiver input. |
| RGB Camera | Jetson USB | USB | Compatible, assuming the selected camera supports Linux/Jetson. |
| Cube Orange+ | ESCs | PWM motor outputs | Compatible. Cube Orange+ provides PWM outputs for motor/servo control. |

### Important Electrical Note

For the Jetson-to-flight-controller serial connection, voltage levels must be checked before direct UART wiring. PX4 documentation notes that Pixhawk serial interfaces use 3.3 V logic, while some companion computers may use different UART voltage levels. A USB-to-serial adapter or level shifter can be used if necessary.

The Jetson should also be powered from a dedicated regulator/BEC rather than directly from the flight controller peripheral power output.