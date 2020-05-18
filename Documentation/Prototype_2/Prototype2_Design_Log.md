# **Prototype 2: Integrated System**

## **Goals**
1. End up with a platform to test mechanical aspects of the design, along with electronics and software.
2. Use this to figure out how to build the final, versatile system.

___________________
## **Frame Spin Mechanism**
For this design, I decided to go with a spur gear based system with a gear ratio of 1:2.

<img src="https://i.imgur.com/jhwZIHT.png">

> **Components:**
> * 17HS2408 stepper motor
> * DRV8225

According to the motor's datasheet, it spins with a total of 200 **full** steps per revolution.

Therefore, to rotate the frame 1 degree,

$$\frac{\text{Full Steps}}{\text{Degree}} = \frac{360\ \text{Degrees}}{\text{Steps Per Revolution}} \cdot \text{Gear Ratio}$$

And thus:
$$\frac{\text{Full Steps}}{\text{Degree}} = \frac{360}{200}\cdot\underbrace{\frac{1}{2}}_{\text{Gear Ratio}} = 0.9$$

I will be using TI's **DRV8825** stepper driver, which can support up to $\frac{1}{32}$ microsteps (per step) and therefore, this mechanical + electrical configuration can support a maximum resolution of:
$$\text{Maximum Resolution} = 0.028125 \frac{\text{degrees}}{\text{(micro)step}}$$

<img src="https://i.imgur.com/B6FxcrJ.png">

I wanted the design to allow me to adjust the distance between the gears, so I could try to aim for the perfect pitch distance, so I added elongated holes for the motor.

<img src="https://i.imgur.com/Po4X8gz.png">

I also wanted to test out a clamping method for the motor's gear, I usually dislike set-screw methods *(especially with 3D-printed parts)* so I went for a clamp-like design, found in some couplings and expensive machined parts.

If it comes to it, in the worst case scenario, I will glue the gear to the motor with some epoxy and call it a day.
_________________

## **Spool and Thread-Path Mechanism**

_________________

## **Weavehead Mechanism**

> **Components:**
> * Unbranded 12V DC motor with an *unknown* gear ratio

_________________

## **Microcontroller and Peripherals**

> **Components:**
> * *Arduino Mega* clone
> * RAMPS1.6 board
> * Unbranded 12V, 15A PSU (scary stuff) 