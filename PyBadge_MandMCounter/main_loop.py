import board
import time
from digitalio import DigitalInOut
from gamepadshift import GamePadShift

BUTTON_A = 2

class MainLoop:
    def __init__(self):
        self.on_button_a = None

        # Set up the game pad
        self._pad = GamePadShift(DigitalInOut(board.BUTTON_CLOCK),
                                 DigitalInOut(board.BUTTON_OUT),
                                 DigitalInOut(board.BUTTON_LATCH))
    
    def _check_buttons(self, buttons):
        # Check if button A was pressed
        if buttons == BUTTON_A:
            self.on_button_a()

    def start_loop(self):
        # Get the buttons that are pressed
        # Check
        current_buttons = self._pad.get_pressed()
        buttons = current_buttons
        last_read = 0

        # Start a loop
        while True:
            # Only check the buttons every 1/10 a second to avoid
            # reading a longer press as a double press
            if (last_read + 0.1) < time.monotonic():
                buttons = self._pad.get_pressed()
                last_read = time.monotonic()
            
            # If the buttons change, check the button pressed
            if current_buttons != buttons:
                self._check_buttons(buttons)
            
            current_buttons = buttons