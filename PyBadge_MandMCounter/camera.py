import busio
import board
import gc
import adafruit_vc0706

READ_SIZE = 32
BAUD_RATE = 115200

class Camera:
    def __init__(self):
        # Set up the camera
        uart = busio.UART(board.TX, board.RX, baudrate=BAUD_RATE, timeout=0.25)
        self._vc0706 = adafruit_vc0706.VC0706(uart)
        self._vc0706.baudrate = BAUD_RATE
        self._vc0706.image_size = adafruit_vc0706.IMAGE_SIZE_320x240
    
    def take_picture(self) -> bytearray:
        print("Taking picture")

        # Take a picture
        self._vc0706.take_picture()

        print("Converting to byte array")

        # Convert the picture to a byte array
        frame_length = self._vc0706.frame_length
        buffer = bytearray(frame_length)
        index = 0

        copy_buffer = bytearray(READ_SIZE)

        while frame_length > 0:
            # Compute how much data is left to read as the lesser of remaining bytes
            # or the copy buffer size (32 bytes at a time).  Buffer size MUST be
            # a multiple of 4 and under 100.  Stick with 32!
            to_read = min(frame_length, READ_SIZE)

            if to_read < READ_SIZE:
                copy_buffer = bytearray(to_read)

            # Read picture data into the copy buffer.
            if self._vc0706.read_picture_into(copy_buffer) == 0:
                raise RuntimeError("Failed to read picture frame data!")

            for b in copy_buffer:
                buffer[index] = b
                index = index + 1

            frame_length -= READ_SIZE
            gc.collect()
        
        return buffer