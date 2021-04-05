# headmouse rpi pico project by Michał Banaś 


Headmouse is my "ode to laziness" :)

## "Rationale"

It's a project made from two thing: 

1) curiosity if simple gyroscope could be good enough to act as a computer mouse 
2) Laziness when I was coding, and didn't want to take my hands of the keyboard to grab a mouse

So I'm using vim, 'vimium' in browser and I use keyboard shortcuts extensively, but not everywhere - specially when browsing web- it's possible to use keyboard only....
.... and normal mouse is soooooo far.....

## Attempts:

Initial idea was to use accelerometer, however it has a limitation that the reading are based on gravity vector.

So I had a second attempt, where I have added a magnetometer to this setup, but the readings were too slow or too noisy.

Further reading showed that the data should be better if I would use DMP (Digital motion processor). I could do this, however I had only mpu6050 without a magnetometer, so I've decided  to ditch that as well.

I believe it's possible to get better results using gyro ,accell and magnet data combined. However I've decided to use gyroscope in this attempt. 

It's much simpler - trivial I would say. However, it works.



## Hardware 
Raspberry PI pico was used since I had it at home + mpu6050.

Pins used in this example are SCL: 15 , SDA : 14. Plus power, plus ground. Take a look at your MPU6050 pinout for more details. 

Any microcontroller could be used. I would go with esp32 next time since it's cheap, and it could be wireless then. 

I was thinking about adding UART BT module like HC-05. This modification would be simple, however I would have to find a way to provide power source, which is easy, but It would make the device bigger and heavier I guess. 


Casing is taken from some sweets - I think it was mentos :) 


## Installation 

### RPI part
Besides hardware, you need to upload micropython code to your rpi pico. 
Open Thony, and run "MPU6050_calibration" to obtain calibration data for your device.
**this step is important since every physical device has a little different Characteristics** 

### Desktop part 

Desktop part is just a simple python script. Download it, install dependencies and run it. 

```shell
 pip install -f requirements.txt 
```


### Config 
Additional config can be found in config.ini 

```ini
[APP]
filter = 5
sensitivity = 30

x-axis = x
y-axis = z
x-axis-modifier = 1.1
y-axis-modifier = -1
COM = 3
```

I think it is simple to understand what parameter is used for what. 
In my case I have changed ***x-axis-modifier*** to 1.1 - usually it should be 1 or -1, but I have pretty wide monitor, so I wanted something little different.

### HOTKEYS

But moving a cursor is not everything.  Like I said THe goal wos to keep you hand on keyboard So I have added global hot keys. You can add, edit them in main.py in desktop folder

```python
bindings = [
    [["control", "shift", "q"], None, quit],
    [["control", "shift", "a"], None, toggle_mouse_active],
    [["control", "shift", "z"], None, click],
    [["control", "shift", "x"], None, right_click],
    [["control", "shift", "3"], None, center],
    [["control", "shift", "1"], None, decrease_sensitivity],
    [["control", "shift", "2"], None, increase_sensitivity],
]
```


And thats basically it :) 

### ENJOY 

Here is a video of prototype in action: 



[![Alt text for your video](https://img.youtube.com/vi/Q5kQ7FVy0To/0.jpg)](https://www.youtube.com/watch?v=Q5kQ7FVy0To)









