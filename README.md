mustached-pi-client
===================

This is the client application running on the **Raspberry Pi**.

Oh booting, it does:

* Check if its the first time I get booted
* * If it is, creates a new **machine code**
* Checks the internet connection and loops until connected
* Check if the house is configurated
* * If not, loops until connected and shows (in future will be *talks*) the machine code

Then, every **5** seconds it does:

* (HTTP) Check configuration of the ports
* (HTTP) If present, send last sensors data
* For each **sensor**
* * Set sensor port on the multiplexer
* * Collect sensor value
* * Prepare it for sending
* For each **output**
* * Check if the status has changed
* * * If yes, select the output port on the multiplexer
* * * If yes, send a pulse signal to change flip flop status
* **Loops** until shutdown

