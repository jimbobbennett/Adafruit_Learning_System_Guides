import board
import displayio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font

BACKGROUND_COLOR = 0xF76B1C
TEXT_COLOR = 0x000000
TITLE_STRING_1 = "Press A to take"
TITLE_STRING_2 = "a picture"
TAKING_PICTURE_STRING = "Taking picture..."
COUNTING_STRING = "Counting M&Ms..."
FOUND_STRING_START = "Found "
FOUND_STRING_END = " M&Ms"

SMALL_FONT_NAME = "/fonts/Arial-12.bdf"

class PyBadgeDisplay:
    def __init__(self, pixels):
        self._pixels = pixels

        # Set up the font
        self._small_font = bitmap_font.load_font(SMALL_FONT_NAME)
        self._small_font.load_glyphs("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890.&".encode('utf-8'))

        # Set up the display
        self._splash = displayio.Group(max_size=20)
        board.DISPLAY.show(self._splash)
        
        # Set the background
        rect = Rect(0, 0, 160, 120, fill=BACKGROUND_COLOR)
        self._splash.append(rect)

        # Set up some labels
        self._title_label_1 = None
        self._title_label_2 = None

        self.show_take_picture_message()

    def _replace_label_1(self, text:str):
        # Replace the top label with a new one

        # Remove the existing label
        if self._title_label_1 is not None:
            self._splash.remove(self._title_label_1)

        # Create a new label with the given text
        self._title_label_1 = Label(self._small_font, text=text)
        (x, y, w, h) = self._title_label_1.bounding_box
        self._title_label_1.x = (80 - w // 2)
        self._title_label_1.y = 35
        self._title_label_1.color = TEXT_COLOR

        # Add the label to the display
        self._splash.append(self._title_label_1)

    def _replace_label_2(self, text:str):
        # Replace the lower label with a new one

        # Remove the existing label
        if self._title_label_2 is not None:
            self._splash.remove(self._title_label_2)

        # Create a new label with the given text
        self._title_label_2 = Label(self._small_font, text=text)
        (x, y, w, h) = self._title_label_2.bounding_box
        self._title_label_2.x = (80 - w // 2)
        self._title_label_2.y = 40 + h
        self._title_label_2.color = TEXT_COLOR

        # Add the label to the display
        self._splash.append(self._title_label_2)

    def show_take_picture_message(self) -> None:
        self._replace_label_1(TITLE_STRING_1)
        self._replace_label_2(TITLE_STRING_2)
        self._pixels[4] = (0,255,0)

    def show_taking_picture_message(self) -> None:
        self._replace_label_1(TAKING_PICTURE_STRING)
        self._replace_label_2(" ")
        self._pixels[4] = (0,0,255)

    def show_counting_message(self) -> None:
        self._replace_label_1(COUNTING_STRING)
        self._replace_label_2(" ")
        self._pixels[4] = (50,50,50)

    def show_found_message(self, count:int) -> None:
        self._replace_label_1(FOUND_STRING_START + str(count) + FOUND_STRING_END)
        self._replace_label_2(" ")
        self._pixels[4] = (0,255,0)