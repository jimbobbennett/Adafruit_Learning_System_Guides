import board
import busio
import neopixel
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi, adafruit_esp32spi_wifimanager
from pybadge_display import PyBadgeDisplay
from camera import Camera
from mandm_counter import MAndMCounter
from main_loop import MainLoop

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# ESP32 Setup
esp32_cs = DigitalInOut(board.D13)
esp32_ready = DigitalInOut(board.D11)
esp32_reset = DigitalInOut(board.D12)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

# Connect the WiFi managger
status_lights = neopixel.NeoPixel(board.NEOPIXEL, 5, brightness=0.2)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_lights)

print("Connecting to WiFi...")

wifi.connect()

print("Connected to WiFi!")

# Set up the display, camera, counter
display = PyBadgeDisplay(status_lights)
camera = Camera()
counter = MAndMCounter()

def take_picture_and_count_mandms():
    # Show a message
    display.show_taking_picture_message()

    # Take the picture
    buffer = camera.take_picture()

    # Show a counting message
    display.show_counting_message()

    # Count the M&Ms
    count = counter.count_mandms(buffer)

    # Show the count of M&Ms found
    display.show_found_message(count)

# Set up button polling loop
main_loop = MainLoop()
main_loop.on_button_a = take_picture_and_count_mandms

# Start the loop
main_loop.start_loop()
