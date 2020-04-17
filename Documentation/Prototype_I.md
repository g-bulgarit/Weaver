# Weaver - First Mechanical Prototype
> **Date:** 17/4/2020

## **Goals**
1. Check if the project is feasible from a mechanical standpoint.
2. Have a platform for experimenting and writing microcontroller code on.

## **Design**

<img src="https://i.imgur.com/SV727YN.png">

The current design for the prototype consists of three elements:

1. The **weave-head**:\
   I decided to go for a needle-like object moving on a linear track, with springs pushing it to the default position and an eccentric cam pushing it into the engaged position.
   For this prototype I opted to avoid electronics, but there is room for a motor for this mechanism for future experiments.

2. The **spindle**:\
    I used a roll of cotton thread that I had lying around, I suspended it on ball bearing rollers so that it spins freely.

3. The **frame**:\
    I printed the frame (although the plan is to make it out of wood for the larger models), it has a ball bearing in the center for almost friction-free rotation, and I chose to only house 50 nails in it in order to keep the same distance between the nails as in the larger design.

## **Build**

<img src="https://i.imgur.com/QuZSaJz.jpg">

    This is a slanted view of the build, with all the parts somewhat visible.

<img src="https://i.imgur.com/v8zmrCv.jpg">

    Bottom-up view of the weave-head mechanism, with the sewing needle in the center and some nails.


<img src="https://i.imgur.com/CqtZWcF.jpg">

    The spindle and the weave-head roller engaging in some thread action together.


<img src="https://i.imgur.com/BoKUnad.jpg">

    A random side view.

## **What worked**
* **Most of the things!**\
    I was happy with how the spindle worked, with the frame and with the weave head in general.

## **What didn't work**
* **Weave-head spring:**\
    I took springs from random pens around the house and tried to use them, I ended up with uneven spring tension in the weaving mechanism which failed to bring the eccentric cam back to it's original relaxed position.

* **Tension:**\
    At some points (when the weave head retracts, or when the frame rotates more than 180 degrees), the thread loses it's tension and the wire droops down.

    It looks like a tensioning mechanism is required in order to keep the thread from going loose and messing up the weave.

## **Steps going forward**
* Design tensioning mechanism for the spool.
* Add electronics;
  * Motor to spin the frame,
  * Motor to operate the weave-head mechanism