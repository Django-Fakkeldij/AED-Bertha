# Bertha Control

## Quickstart

1. Check requirements.txt for required python libraries and install those.

   ```bash
   pip install -r requirements.txt
   ```

2. Upload the Arduino firmware/code to the correct Arduinos. Node 1 goes to the stepper motors controlling the planar movement, Node 2 goes to the servo motor controlling the screwing motion. **(You can skip this step if the firmware has been flashed previously!)**
   - Please note that **most** libraries used in the firmware(s) are installable from the Arduino IDE. However, we use a custom Servo library, which can be found and installed from `clients\libraries\ServoTimer2.zip`
3. Set the Arduino ports in main.py to the correct COM port. You can see which COM port which Arduino is using in the Arduino IDE. Make sure that the COM ports are defined by the same logic as in step 2.
4. Run main.py. This should execute the full forward and backward sequences. Between each sequence press ENTER to move to the next sequence. It is possible to adjust which sequences are exectued by changing the boolean value of forward, backward, etc in main.py in the function definition of main().

   ```bash
   python main.py
   ```

## Additional points

- The Arduino will automatically home the arms everytime the firmware is uploaded and/or the main.py file is run.

## Created by

- Joran Blom
- Django Fakkeldij
- Caspar Hendriksen
- Bèr Kaelen
- Joris Lugtenburg
- Felix Schuring

\*This code is the intellectual property of the authors. Unauthorized copying, distribution, or modification of this code, via any medium, is strictly prohibited. Use of this code is permitted only with explicit authorization from the authors or under an appropriate open-source license where indicated. If you have questions regarding usage or licensing, please contact the authors directly.
