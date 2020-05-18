# Prototype 2: Electronics

## Frame Spin Mechanism
For this design, I decided to go with a spur gear based system with a gear ratio of 1:2.

<img src="https://i.imgur.com/jhwZIHT.png">

According to the motor's datasheet, there is a total of 200 **full** steps per revolution.

Therefore, to rotate the frame 1 degree,

$$\frac{\text{Full Step}}{\text{Degree}} = \frac{360\ \text{Degrees}}{\text{Steps Per Revolution}} \cdot \text{Gear Ratio}$$

And thus:
$$\frac{\text{Full Step}}{\text{Degree}} = \frac{360}{200}\cdot\frac{1}{2} = 0.9$$

I will be using TI's **DRV8825** stepper driver, which can support up to $\frac{1}{32}$ microsteps (per step) and therefore, this mechanical + electrical configuration can support a maximum resolution of:
$$\text{Maximum Resolution} = 0.028125 \frac{\text{degrees}}{\text{(micro)step}}$$

