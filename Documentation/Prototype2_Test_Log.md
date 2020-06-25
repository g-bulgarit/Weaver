# **Weaver:** Prototype 2 Test Log


# First Testing Phase Summary
## **Issues:**

> ## "Jamming":
> **Description:**
> 
> During first test runs, the weave-mechanism would create 'loops' or 'knots', preventing the frame from rotating.
> 
> **Cause:**
> 
> The weave is somewhat directional, as for now, the weave algorithm looks something like the following:
> 
> * Move to target nail
> * Rotate the frame a little bit to **side #1**
> * Retract nail to **outside** position
> * Rotate the frame to **side #2** of the nail
> * Push the needle back to the **inside** position
> 
> The problem with this algorithm is that once a loop has been made, the frame simply can not rotate back towards side #1, as there is currently a thread blocking it.
> 
> Trying to move towards side #1 anyway results in the motor getting stuck and skipping steps, which leads to even more chaos until the system is finally shut down.
> 
> **Workaround:**
> 
> To keep testing the system without finding a proper solution to this problem (which may just be a redesign of the entire weave mechanism), I forced the code to output gcode moves that make the frame rotate in one direction only (between nails).
> 
> This way, there is no jamming and the system can keep weaving.
> 
> 
> **Solution:**
> * Considering a redesign of the weave mechanism or thread feed mechanism.
> 
_______________________________

> ## Skipping Steps on Frame Rotation:
> **Description:**
> 
> Sometimes, as the frame rotates, it does not reach the intended nail, sometimes missing by a small amount or by a big amount.
> 
> This, in turn, leads to incorrect weaves.
> 
> 
> **Possible Causes:**
> 1. **Irregular torques** acting on the motor:\
> While playing with the system by hand, I noticed that there is a substantial increase in the torque required to spin the frame, whenever more "new" thread had to be pulled in from the spool.\
> This happens because the motor needs to work harder to resist the frictional forces in the way of the thread (friction with the eye of the needle, friction with the mechanical parts touching the thread...)
> 
> **Suggested Solutions:**
> 1. A **redesign** of the thread path, minimizing contact with plastic parts, or replacing the contact points with PTFE tubing for a smoother pull on the thread.
> 
> 2. Moving the frame more slowly, allowing the motor to excert more torque on the thread without skipping steps.
> 3. Considering moving to a motor that is rated for higher torque if all else fails.

# Modifications after the First Testing Phase
1. I swapped out the gears in order to achieve a **1:4 ratio** instead of the 1:2 ratio I had before.\
   This appears to have somewhat helped.

> Switching to a larger gear ratio without changing the original design means that I had to settle for a lower tooth module, which means that the teeth of the gears are smaller, and therefore more suspectible to wear and breakage.

2. A new "thread path" guide part was printed, it is lined with PTFE tubing and it seems to somewhat reduce the friction in the thread's path to the needle.