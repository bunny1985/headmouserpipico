import utime, machine, sys, struct

#

timer = machine.Timer()


def to_short(somebytes):
    if type(somebytes) == int:
        return somebytes
    return struct.unpack('>h', somebytes)[0]


def blink_with_frequency(frequency=1, pin=25):
    global timer
    led = machine.Pin(pin, machine.Pin.OUT)
    timer.deinit()
    timer.init(freq=frequency, mode=machine.Timer.PERIODIC, callback=lambda timer: led.toggle())
    return timer


timer = blink_with_frequency(1, 25);


class HeadMouseDataProducer:
    i2c_bus = 1

    device_address = 0x68
    # The offsets are different for each device and should be changed
    # accordingly using a calibration procedure!!!!!
    x_accel_offset = 3229
    y_accel_offset = -1139
    z_accel_offset = 1636
    x_gyro_offset = 110
    y_gyro_offset = 24
    z_gyro_offset = 26
    enable_debug_output = False
    mpu = None

    def __init__(self):
        from MPU6050RPI import MPU6050
        self.mpu = MPU6050(self.i2c_bus, self.device_address, self.x_accel_offset, self.y_accel_offset,
                           self.z_accel_offset, self.x_gyro_offset, self.y_gyro_offset, self.z_gyro_offset,
                           self.enable_debug_output)
        self.mpu.dmp_initialize()
        self.mpu.set_DMP_enabled(True)
        # just to make sure
        self.mpu.set_x_gyro_offset(int(self.x_gyro_offset))
        self.mpu.set_y_gyro_offset(int(self.y_gyro_offset))
        self.mpu.set_z_gyro_offset(int(self.z_gyro_offset))
        self.mpu.set_x_accel_offset(int(self.x_accel_offset))
        self.mpu.set_y_accel_offset(int(self.y_accel_offset))
        self.mpu.set_z_accel_offset(int(self.z_accel_offset))

    def start(self):
        while True:
            data = self.mpu.get_rotation()

            print(">>>G-X:{:.2f},\tG-y:{:.2f},\tZ-X:{:.2f}".format(to_short(data[0]), to_short(data[1]),
                                                                   to_short(data[2])))


is_started = False


def start():
    global is_started, timer;
    if not is_started:
        try:
            head_mouse = HeadMouseDataProducer()
            is_started = True;
            head_mouse.start()
            timer = blink_with_frequency(1, 25);
        except Exception as e:
            timer = blink_with_frequency(10, 25);
            is_started = False
            raise e
            utime.sleep(2)

            sys.exit()


import i2cscan

start()
