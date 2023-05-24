# MagicCube
This is a program used to identify and solve the Rubik's Cube.

## Background
The purpose of this project itself is to understand and learn the process of program development, and at the same time learn the corresponding programming and engineering knowledge.

The goal of this program is to collect real-world Rubik's Cube information and reproduce it in the program based on this information, then restore it and visualize the process.

## Platform
Windows

## Install
Clone this repository to local.

```
$ git clone https://github.com/2820207922/MagicCube.git
```

Run the following code to install dependencies. It is recommended to use Conda to create a virtual environment before.

```
$ pip install -r requirements
```

## Usage
Find the file ```visualization.py``` and run it. Wait for a while, you will see the following screen.

![image](example/e1.png)

Click the button on the far right. you will see 

![image](example/e2.png)

Aim the Rubik's Cube at the camera, and press the space to complete a capture.

![image](example/e3.png)

If you find that the color is not accurate when capturing, press c to enter the correction mode, and then correct in turn.

![image](example/e4.png)

Then capture 6 faces in turn, make sure each face is correct.

![image](example/e5.png)

Press the enter key to automatically complete the homing of each surface.

![image](example/e6.png)

Press esc to exit, after completing the above steps you will find that your Rubik's Cube has been copied. Clicking the play button will start the restore.

![image](example/e7.png)
![image](example/e8.png)
![image](example/e9.png)

Finally, your Rubik's Cube will be solved. You can check more functions in the image below.

![image](example/e10.png)
![image](example/e11.png)