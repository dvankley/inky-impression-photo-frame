# Adapted from https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/examples/inky_frame/image_gallery/image_gallery_sd.py
# Requires properly formatted files in the SD card's root directory
# Each file should be named $index.jpg, where $index is the file's index in the directory.
# This is done to avoid the overhead of listing all the files in the directory.

# An offline image gallery that switches between five jpg images
# on your SD card (copy them across by plugging your SD into a computer).
# If you want to use your own images they must be 600 x 448 pixels or smaller
# and saved as *non-progressive* jpgs

import random
import inky_helper
from pimoroni import ShiftRegister
from picographics import PicoGraphics, DISPLAY_INKY_FRAME
from machine import Pin, SPI
import jpegdec
import sdcard
import uos

SLEEP_MINUTES = 2
FILE_COUNT = 5

# Enable vsys hold so we don't go to sleep
# This variable and vsys setup are imported from inky_helper
inky_helper.hold_vsys_en_pin.value(True)

# set up the display
display = PicoGraphics(display=DISPLAY_INKY_FRAME)

# Inky Frame uses a shift register to read the buttons
SR_CLOCK = 8
SR_LATCH = 9
SR_OUT = 10

sr = ShiftRegister(SR_CLOCK, SR_LATCH, SR_OUT)

# set up the button LEDs
button_a_led = Pin(11, Pin.OUT)
button_b_led = Pin(12, Pin.OUT)
button_c_led = Pin(13, Pin.OUT)
button_d_led = Pin(14, Pin.OUT)
button_e_led = Pin(15, Pin.OUT)

# and the activity LED
activity_led = Pin(6, Pin.OUT)

# set up the SD card
sd_spi = SPI(0, sck=Pin(18, Pin.OUT), mosi=Pin(19, Pin.OUT), miso=Pin(16, Pin.OUT))
sd = sdcard.SDCard(sd_spi, Pin(22))
uos.mount(sd, "/sd")

# setup
activity_led.on()


def display_jpg(filename):
    # Create a new JPEG decoder for our PicoGraphics
    j = jpegdec.JPEG(display)

    # Open the JPEG file
    j.open_file(filename + ".jpg")

    # Decode the JPEG
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)

    # Display the result
    display.update()


def display_raw(filename):
    # Open the file
    open(filename + ".bin", "rb").readinto(display)

    # Display the result
    display.update()


# photo_files = listdir("/sd")
file_index = random.randrange(1, FILE_COUNT + 1)
file = "/sd/" + str(file_index)
display_raw(file)
# display_jpg(file)

activity_led.off()
inky_helper.sleep(SLEEP_MINUTES)
