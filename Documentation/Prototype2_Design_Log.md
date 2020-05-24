# **Prototype 2: Integrated System**

## **Goals**
1. End up with a platform to test mechanical aspects of the design, along with electronics and software.
2. Use this to figure out how to build the final, versatile system.

## **Assembly CAD:**

<div align="center"><img src="https://i.imgur.com/9sV4vfC.png"></div>

___________________
## **Frame Spin Mechanism**
For this design, I decided to go with a spur gear based system with a gear ratio of 1:2.

<div align="center"><img src="https://i.imgur.com/jhwZIHT.png"></div>

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

<div align="center"><img height="200" src="https://i.imgur.com/B6FxcrJ.png"></div>

I wanted the design to allow me to adjust the distance between the gears, so I could try to aim for the perfect pitch distance, so I added elongated holes for the motor.

<div align="center"><img height="200" src="https://i.imgur.com/Po4X8gz.png"></div>

I also wanted to test out a clamping method for the motor's gear, I usually dislike set-screw methods *(especially with 3D-printed parts)* so I went for a clamp-like design, found in some couplings and expensive machined parts.

If it comes to it, in the worst case scenario, I will glue the gear to the motor with some epoxy and call it a day.

I decided to go with the conclusion of the previous prototype and go with a design based off of angled nails, again at $20\deg$.\
This helps prevent overlapping and knotting of the thread on the nails, as the thread slides down the nail as the mechanism rotates, freeing up space on the top of the nails for fresh weaves.


Here's a section view of the design, with the angled nails visible:

<div align="center"><img align="center" height="200" width="auto" src="https://i.imgur.com/pYhP8Nu.png"></div>
<div align="center"><img align="center" height="300" width="auto" src="https://i.imgur.com/YKD8PTx.png"></div>


_________________
## **Weavehead Mechanism**

> **Components:**
> * Unbranded 12V DC motor with an *unknown* gear ratio, rated for 62RPM.

I liked the design of the weavehead from prototype #1, it wasn't pretty but it looked promising.

I've added a support for the motor and moutned the cam on the shaft, played with the tolerances based on the previous prototype.

<div align="center"><img height="300" width="auto" src="https://i.imgur.com/wYpwgwt.png"></div>

Here's a cross-section of the weavehead:

<div align="center"><img height="250" width="auto" src="https://i.imgur.com/nc7wcFg.png"></div>

And a top view of the cam and follower:

<div align="center"><img height="250" width="auto" src="https://i.imgur.com/mzVR2WJ.png"></div>

Note that the blue and red parts are supposed to be touching, and the springs are absent from the assembly, but the general idea is sufficiently explained with the image.
_________________

## **Body, Spool and Thread-Path Control**
I decided to mostly go with what I had for the previous prototype.

To improve my control over the tension of the thread, I decided to add a mobile roller that I could move to obscure the path to the needle, thus increasing the tension on the spool.

This was incorporated to the "body" part of the mechanism.

<div align="center"><img height="300" width="auto" src="https://i.imgur.com/7yKcw0i.png"></div>
<div align="center"><img height="330" width="auto" src="https://i.imgur.com/H9xKd1I.png"></div>

I intend to check if a constant-force spring would improve the stability of the system by pulling back on the threads.\
If this feature would be required, I will implement it within the parts that hold the spools, to make it fit every spool.

_________________

## **Microcontroller and Peripherals**

> **Components:**
> * *Arduino Mega* clone
> * RAMPS1.6 board
> * Unbranded 12V, 15A PSU (scary stuff) 


The choice of PSU for the project was based on the idea that I would like to expand and add a "drill jig" that could drill holes for the nails, to be used in the (hopefully) final version of the machine, saving me the trouble of drilling hundreds of holes at a 20 degree angle.

The project's code currently exports the motion to g-code, at this stage it's not even tested, but the general idea for development purposes is to debug with a serial connection to the arduino, sending g-code from the computer.

Eventually, I will have sufficient confidence in the g-code exporter from my script, and I will be able to run the machine without having a computer connected to it.