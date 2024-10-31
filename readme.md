# Bertha Control

<!-- ![Architecture](https://github.com/user-attachments/assets/63b942b8-87cf-4601-a6a3-457d5935232a)
_Architecture Preview_ -->

## Quickstart

1. Check requirements.txt for required python libraries and install those.
2. Upload the Arduino firmware/code to the correct Arduinos. Node 1 goes to the stepper motors controlling the planar movement, Node 2 goes to the servo motor controlling the screwing motion.
3. Set the Arduino ports in main.py to the correct COM port. You can see which COM port which Arduino is using in the Arduino IDE. Make sure that the COM ports are defined by the same logic as in step 2. 
3. Run main.py. This should execute the full forward and backward sequences. Between each sequence press ENTER to move to the next sequence. It is possible to adjust which sequences are exectued by changing the boolean value of forward, backward, etc in main.py in the function definition of main().

## Additional points

- The Arduino will automatically home the arms everytime the firmware is uploaded and/or the main.py file is run.


## Created by
- Joran Blom
- Django Fakkeldij
- Caspar Hendriksen
- Bèr Kaelen
- Joris Lugtenburg
- Felix Schuring

*This code is the intellectual property of the authors. Unauthorized copying, distribution, or modification of this code, via any medium, is strictly prohibited. Use of this code is permitted only with explicit authorization from the authors or under an appropriate open-source license where indicated. If you have questions regarding usage or licensing, please contact the authors directly.

