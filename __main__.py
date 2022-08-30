import pathlib
import signal
import time
import random
from os import listdir
from threading import Event

import RPi.GPIO as GPIO
from PIL import Image
from inky.auto import auto

PHOTOS_DIRECTORY = '/opt/inky-photos'

PHOTO_CYCLE_PERIOD_SECS = 300

# Gpio pins for each button (from top to bottom)
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, C and D respectively
LABELS = ['A', 'B', 'C', 'D']

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# exit = Event()
# buttonA = Event()
button_pressed = Event()

def display_photo(display, photo_path: pathlib.Path) -> None:
    """
    test_function does blah blah blah.

    :param photo_path: Path to photo file we're processing
    """
    print("Displaying image")
    image = Image.open(photo_path)
    display.set_image(image)
    display.show()
    print("Display complete")


def handle_button(pin: int):
    """
    "handle_button" will be called every time a button is pressed
    It receives one argument: the associated input pin.
    :param pin:
    :return:
    """
    label = LABELS[BUTTONS.index(pin)]
    button_pressed.set()
    print("Button press detected on pin: {} label: {}".format(pin, label))


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        self.kill_now = True


if __name__ == '__main__':
    print("Running inky photo display")

    # Initialization
    display = auto()
    height = display.height
    width = display.width
    aspect_ratio = width / height

    # Loop throughout buttons and attach the "handle_button" function to each
    # We're watching the "FALLING" edge (transition from 3.3V to Ground) and
    # picking a generous bouncetime of 250ms to smooth out button presses.
    for pin in BUTTONS:
        GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)

    photo_files = listdir(PHOTOS_DIRECTORY)

    killer = GracefulKiller()
    last_photo_cycle = 0
    # Event loop
    while not killer.kill_now:
        timestamp = int(time.monotonic())
        if (timestamp - last_photo_cycle) > PHOTO_CYCLE_PERIOD_SECS or button_pressed.is_set():
            print("Cycling photo display")
            file = random.choice(photo_files)
            display_photo(display, pathlib.Path(PHOTOS_DIRECTORY + '/' + file))

            button_pressed.clear()
            last_photo_cycle = timestamp
        time.sleep(1)


# def main():
#     while not exit.is_set():
#         do_my_thing()
#         exit.wait(60)
#
#     print("All done!")
#     # perform any cleanup here
#
# def quit(signo, _frame):
#     print("Interrupted by %d, shutting down" % signo)
#     exit.set()
#
# if __name__ == '__main__':
#
#     import signal
#     for sig in ('TERM', 'HUP', 'INT'):
#         signal.signal(getattr(signal, 'SIG'+sig), quit);
#
#     main()
