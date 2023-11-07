import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")

        self.coordinates = []

        # Create a button to open a file dialog for image selection
        self.load_button = tk.Button(root, text="Select Image", command=self.load_image)
        self.load_button.pack()

        # Create a Label to display the selected image
        self.image_label = tk.Label(root)
        self.image_label.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if file_path:
            self.image = cv2.imread(file_path)
            self.display_image(self.image)
            self.coordinates = []  # Reset the coordinates

    def display_image(self, image):
        # Calculate the scaling factor to fit the image within the window
        width, height = self.root.winfo_width(), self.root.winfo_height()
        scaling_factor = min(width / image.shape[1], height / image.shape[0])
        new_width = int(image.shape[1] * scaling_factor)
        new_height = int(image.shape[0] * scaling_factor)

        # Resize the image and display it
        resized_image = cv2.resize(image, (new_width, new_height))
        resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        resized_image = Image.fromarray(resized_image)
        resized_image = ImageTk.PhotoImage(image=resized_image)

        self.image_label.config(image=resized_image)
        self.image_label.image = resized_image

    def get_coordinates(self, event):
        x, y = event.x, event.y
        self.coordinates.append((x, y))
        
        # Check if we have collected 2 points
        if len(self.coordinates) == 2:
            print("Coordinates of Point 1:", self.coordinates[0])
            print("Coordinates of Point 2:", self.coordinates[1])
            
            # You can perform your image processing using self.image here
            # Example: cropped_image = self.image[y1:y2, x1:x2]

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.geometry("800x600")  # Set an initial window size
    root.mainloop()
