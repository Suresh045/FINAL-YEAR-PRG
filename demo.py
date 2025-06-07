from flask import Flask, jsonify
import pyautogui
from tkinter import *
from PIL import ImageGrab, ImageTk
import time

app = Flask(__name__)

class FreeCropScreenshot:
    def __init__(self):
        self.root = Tk()
        self.root.withdraw()  # Hide the main tkinter window

        # Initialize the coordinates for the selection box
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        # Start the cropping process
        self.capture_screen()

    def capture_screen(self):
        """Capture the screen and allow the user to crop freely."""
        # Give a few seconds for the user to prepare the screen
        print("You have 5 seconds to prepare your screen...")
        time.sleep(5)
        
        # Use pyautogui to capture the full screen
        print("Capturing the screen... Please click and drag to select the area.")
        screenshot = pyautogui.screenshot()

        # Store the screenshot as a global image
        self.image = screenshot
        self.show_crop_window(screenshot)

    def show_crop_window(self, screenshot):
        """Create a window to manually select the area to crop."""
        # Create a tkinter canvas to show the screenshot
        self.canvas = Canvas(self.root, width=screenshot.width, height=screenshot.height)
        self.canvas.pack()
        
        # Convert the screenshot to a format that tkinter can handle
        self.tk_image = ImageTk.PhotoImage(screenshot)
        self.canvas.create_image(0, 0, anchor=NW, image=self.tk_image)

        # Set up mouse events to track the drag
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Show the canvas
        self.root.deiconify()
        self.root.mainloop()

    def on_press(self, event):
        """Start the cropping area when the user clicks."""
        self.start_x = event.x
        self.start_y = event.y

        # Draw a rectangle starting from the initial click point
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_drag(self, event):
        """Update the size of the rectangle as the user drags."""
        self.end_x = event.x
        self.end_y = event.y

        # Update the coordinates of the rectangle being drawn
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_release(self, event):
        """Capture the cropped area once the user releases the mouse button."""
        self.end_x = event.x
        self.end_y = event.y

        # Get the coordinates of the crop area
        left = min(self.start_x, self.end_x)
        top = min(self.start_y, self.end_y)
        right = max(self.start_x, self.end_x)
        bottom = max(self.start_y, self.end_y)

        # Crop the image using Pillow
        cropped_image = self.image.crop((left, top, right, bottom))

        # Save and show the cropped image
        cropped_image.save("cropped_screenshot.png")
        cropped_image.show()
        
        # Close the tkinter window
        self.root.quit()

@app.route('/capture', methods=['POST'])
def capture():
    FreeCropScreenshot()
    return jsonify({"message": "Screenshot captured successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
