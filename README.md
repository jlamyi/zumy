# zumy
Zumy is a small robot running linux using Pololu's Zumo robot chassis. This source code are algorithms based on zumy driver codes: https://github.com/andrewjchen/zumy

## Getting Started
* [Ground Station Setup](GroundStationSetup.md)
* Zumy Setup
    * Chassis: http://www.pololu.com/docs/pdf/0J54/zumo_chassis.pdf
    * [Zumy Electronics Stack](ElectronicsSetup.md): in progress
    * [Robot Bringup From Image](RobotBringupFromImage.md)


## Architecture Diagram
https://wiki.eecs.berkeley.edu/biomimetics/Main/Zumy?action=download&upname=zumy_architecture.pdf

## For Maintainers
* [ODROID Imaging and Setup](RobotCodeSetup.md): For image maintainers
* [ODROID Image Saving](odroid_image_saving.md): Saving master images

## Run

cd ~/zumy/python

Gradient ascend algorithm:

python GAscent_beta.py

Gradient descend algorithm:

One to one descent

python GDscent.py

One to multiple descent

python GDscent_multiBot.py

## Reference 

https://github.com/andrewjchen/zumy





