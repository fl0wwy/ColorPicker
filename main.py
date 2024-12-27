from PIL import Image
import mouse
from pyperclip import copy
from screeninfo import get_monitors
from mss import mss
import os

# Getting monitors data
monitors = get_monitors()
print(f"Detected monitors: {len(monitors)}")
for monitor in monitors:
    print(f"Monitor: {monitor.name}, offset_x: {monitor.x}, offest_y: {monitor.y}, width: {monitor.width}, height: {monitor.height}")

def get_mouse_position():
    """Gets the mouse coordinates according to system setup
    and translates it using the top left corner of the actual setup as (0,0)

    Returns:
        tuple: Adjusted mouse position
    """
    min_x = min(monitor.x for monitor in monitors)  # smallest x-coordinate
    min_y = min(monitor.y for monitor in monitors)  # smallest y-coordinate    
    mouse_x, mouse_y = mouse.get_position()
    
    adjusted_x = mouse_x - min_x
    adjusted_y = mouse_y - min_y

    return adjusted_x, adjusted_y

def rgb_to_hex(rgb):
    """Translates RGB value to HEX value

    Args:
        rgb (tuple): RGB value

    Returns:
        str: HEX value
    """
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

def main():
    # Taking screenshot of the whole setup and storing it as a temporary file
    with mss() as sct:
        sc = sct.shot(mon=-1, output='temp.png')

    image = Image.open(sc)  
    # image.show()  

    sc_width, sc_height = image.size
    print(f'Setup dimensions: ({sc_width}, {sc_height})')

    mouse_position = get_mouse_position()

    color = rgb_to_hex(image.getpixel(mouse_position))    
      
    copy(color) 
    print(f'\nColor {color} at position {mouse_position} successfully copied to clipboard.')   

    # Deleting temporary image file
    if os.path.exists('temp.png'):
        os.remove('temp.png')


if __name__ == "__main__":
    mouse.wait()
    main()





