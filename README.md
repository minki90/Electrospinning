# Electrospinning
control syringe pump, camera, linear stage, temperature controller

Made by Minki Lee during his Postdoc at the Osuji group of the University of Pennsylvania.

Python program to conduct electrospinning using syringe pump, high voltage generator, linear stage, temperature controller and camera.  

Through the GUI, you can set the postion, temprature, flow rate, voltage and experiment time.
with blank the set like below.
position = 0,0, temperature =25 degree celcius, flow rate=0 ul/min, voltage=0, experiment time = infinite.
This program can maintain stable taylor-cone during the spinning by PID contorl.

## Screenshot
![](gui.jpg)

## Hardware List
*High voltage power supply - PS364(stanford research systems) X2
*temperature controller - Omega platinum series(omega) X1
*syringe pump - PHD ULTRA(Harvard apparatus) X3
*linear stage - ESP301(Newport) X2
*camera - USB camera X1

## Support
If you have any questions feel free email or open an issue on github.


## Some details
* The code is written for Python 3.9
* Back light is needed to do the image processing of taylor-cone

