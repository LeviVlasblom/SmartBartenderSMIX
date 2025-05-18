import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

def convert_pillow(image):
    #print('[DEBUG] convert_pillow')
    
    # Load the pizels into memory
    pixels = image.load()
    
    # For each pixel in the image
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            # If the pixel is white
            if pixels[i, j] == (255, 255, 255, 255):
                # Make it transparent
                pixels[i, j] = (255, 255, 255, 0)

    return image
    
def convert_numpy(image):
    #print('[DEBUG] convert_numpy')
    import numpy as np

    # convert pillow.Image to numpy.array
    array = np.array(image)  
    
    #mask = np.all(array == [255, 255, 255, 255], axis=-1)  # png without artefacts
    mask = np.all(array >= [230, 230, 230, 255], axis=-1)  # jpg with artefacts
    array[ mask ] = [255, 255, 255, 0]

    # convert numpy.array to pillow.Image
    image = Image.fromarray(array)
    
    return image

# --- main ---

width = 100
height = 100

filename = "/home/pi/Desktop/SB/SymbolsBtn/arrow.png"
#filename = "test/rgb.jpg"
image = Image.open(filename).convert("RGBA")

#image = convert_pillow(image)
image = convert_numpy(image)

# resize after changing color - because resize creates new artefacts
image = image.resize((width, height), Image.LANCZOS)

# Save the now transparent image:
image.save("new_image.png", format="png")

# Show it on the screen
root = tk.Tk()

canvas = tk.Canvas(root, bg="gray")
canvas.pack()

tk_image = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, image=tk_image, anchor="nw")

root.mainloop()