import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")

        self.coordinates = []
        self.intersection = []
        self.perpendicular = []

        self.load_button = tk.Button(root, text="Select Image", command=self.load_image)
        self.load_button.pack()

        # Create a "Binarize Image" button
        self.binarize_button = tk.Button(root, text="Process Image", command=self.binarize_image)
        self.binarize_button.pack()
        


        # Create Labels to display the selected image and binary image side by side
        self.image_label = tk.Label(root)
        self.image_label.pack(side="left")

        self.binary_image_label = tk.Label(root)
        self.binary_image_label.pack(side="left")


        self.get_coordinates_button = tk.Button(root, text="Get Coordinates", command=self.get_coordinates)
        self.get_coordinates_button.pack()

        self.get_coordinates_button = tk.Button(root, text="Get perpendicular", command=self.get_perpendicular)
        self.get_coordinates_button.pack()

        self.get_coordinates_button = tk.Button(root, text="Get Intersection", command=self.intersection_coordinates)
        self.get_coordinates_button.pack()

        self.image = None
        
        # Create a text widget to display the angle
        self.text_widget = tk.Text(root, wrap=tk.WORD)
        self.text_widget.pack()

        # Initialize the angle variable
        self.cobb = 0  # You can initialize it to any default value
        self.slope = []
        # Update the text widget with the initial angle
        self.update_text_widget()

        # You can have a button or a function that updates the angle
        self.update_button = tk.Button(root, text="Update Angle", command=self.calculate_angle)
        self.update_button.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if file_path:
            self.image = cv2.imread(file_path)
            self.display_image(self.image, self.image_label)
            self.coordinates = []  # Reset the coordinates

    def display_image(self, image, label):
        # Calculate the scaling factor to fit the image within the window
        # Calculate the scaling factor to fit the image within the fixed width
        width = image.shape[1]//2 # Set a fixed width for the displayed image
        scaling_factor = width / image.shape[1]
        self.new_width = width
        
        self.new_height = int(image.shape[0] * scaling_factor)

        new_width = self.new_width
        new_height = self.new_height


        # Resize the image and display it
        resized_image = cv2.resize(image, (new_width, new_height))
        resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        resized_image = Image.fromarray(resized_image)
        resized_image = ImageTk.PhotoImage(image=resized_image)
        label.config(image=resized_image)
        label.image = resized_image

        # self.canvas = tk.Canvas(self.root, width=new_width, height=new_height)
        # self.canvas.create_image(0, 0, image=resized_image, anchor='nw')
        # self.canvas.pack(side="left")

    # Link the scrollbar to the canvas
        # self.vertical_scrollbar.config(command=self.canvas.yview)

    def binarize_image(self):
        if hasattr(self, 'image'):
            # Convert the image to grayscale
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            
            # Apply binary thresholding (adjust the threshold value as needed)
            _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
            binary = 255 - binary_image
            output_of_curve = np.zeros(self.image.shape,dtype='uint8')
            first_occurrences = []

            # Iterate through each row
            for i,row in enumerate(binary):
                indices = np.argwhere(row == 255) # Find indices where '1' occurs in the row

                if len(indices) > 0:

                    col = indices[0]  # Get the column index of the first '1'
                    first_occurrences.append((col[0], i))
                    
            c = np.array(first_occurrences)
            # c_approx = c[:-1:20]
            self.curve = c
            for col,row in c:   #c_approx:
                # print(col,row)
                # cv2.circle(output_of_curve, (col, row), 2, (0, 0, 255), -1)  # Draw a red point (2-pixel radius)
                cv2.circle(output_of_curve, (col, row), 2, (0, 0, 255), -1)  # Draw a red point (2-pixel radius)
            # cv2.imwrite('contoured_image_of.png', image)


            color = (255, 0, 0)
            thickness = 2
            t = c[0]
            b = c[-1]
            # cv2.line(self.image, t, b, color, thickness)
            cv2.line(output_of_curve, t, b, color, thickness)

            apex = c[:,0].argmin()
            # cv2.circle(image, c[apex], 10, (0,255 , 0), -3)  # Red dot
            cv2.circle(output_of_curve, c[apex], 10, (0,255 , 0), -3)  # Red dot
            self.processed_image = output_of_curve


            self.display_image(output_of_curve, self.binary_image_label)


    def intersection_coordinates(self):
        # Register a mouse click event handler to capture the coordinates
        self.binary_image_label.bind("<Button-1>", self.capture_intersection)

    def capture_intersection(self, event):
        x, y = event.x, event.y
        self.intersection.append((x, y))

        if len(self.intersection) == 1:
            print("Coordinates of Point 1:", self.intersection[0])

            self.angle()

    def angle(self):
        p1 = self.coordinates[1]
        p2 = self.coordinates[3]
        p3 = self.intersection[0]

        p1 = self.coordinates[1]

        p2 = self.coordinates[3]
       
        p3 = self.intersection[0]
        p3 = tuple(v*2 for v in p3)
        self.intersection[0] = p3

        p1_2 = self.coordinates[0]

        p2_2 = self.coordinates[2]


        image = self.processed_image.copy()
        cv2.circle(image, p3,2, (0, 255, 0), 10)  # Green 

        cv2.circle(image, p1,2, (0, 255, 0), 10)  # Green 
        cv2.circle(image, p1_2, 2, (0, 255, 0), 10)  # Green 
        cv2.circle(image, p2,2, (0, 255, 0), 10)  # Green 
        cv2.circle(image, p2_2, 2, (0, 255, 0), 10)  # Green 



        self.draw_perpendicular(image,p1_2,p1)

        self.draw_perpendicular(image,p2,p2_2)

        self.draw_perpendicular_sec(image,self.perpendicular[1],self.slope[0])
        self.draw_perpendicular_sec(image,self.perpendicular[0],self.slope[1])

        self.display_image(image, self.binary_image_label)
        # Calculate direction vectors of the two lines
        vec1 = np.array([p3[0] - p1[0], p3[1] - p1[1]])
        vec2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])

        # Calculate the dot product of the two vectors
        dot_product = np.dot(vec1, vec2)

        # Calculate the magnitudes of the vectors
        magnitude_vec1 = np.linalg.norm(vec1)
        magnitude_vec2 = np.linalg.norm(vec2)

        # Calculate the cosine of the angle between the lines
        cosine_theta = dot_product / (magnitude_vec1 * magnitude_vec2)

        # Calculate the angle in radians
        angle_radians = np.arccos(cosine_theta)

        # Convert the angle from radians to degrees
        angle_degrees = np.degrees(angle_radians)
        self.cobb = 180 - angle_degrees
        print(f"Angle between lines at p3: {angle_degrees} degrees")


    def get_coordinates(self):
        # Register a mouse click event handler to capture the coordinates
        self.binary_image_label.bind("<Button-1>", self.capture_coordinates)

    def capture_coordinates(self, event):
        x, y = event.x, event.y
        self.coordinates.append((x, y))

        if len(self.coordinates) == 4:
            print("Coordinates of Point 1:", self.coordinates[0])
            print("Coordinates of Point 2:", self.coordinates[1])

            print("Coordinates of Point 1:", self.coordinates[2])
            print("Coordinates of Point 2:", self.coordinates[3])
            
            # Perform any further processing or action based on the coordinates
            # self.draw_line_between_points()
            
            self.draw_points()
            # self.draw_perpendicular()

    def get_perpendicular(self):
        # Register a mouse click event handler to capture the coordinates
        self.binary_image_label.bind("<Button-1>", self.capture_perpendicular)


    def draw_perpendicular_sec(self,image,point,slopes):
        x1,y1 = point

        slope = 1/slopes
        intercept = y1 - slope * x1
        x_top = int(-intercept / slope)

        y_top = 0
        height, width = 1200,1600
        # Bottom edge (y=height)
        x_bottom = int((height - intercept) / slope)
        y_bottom = height

        # Left edge (x=0)
        x_left = 0
        y_left = int(intercept)

        # Right edge (x=width)
        x_right = width
        y_right = int(slope * width + intercept)

        # Draw the line on the image
        cv2.line(image, (x_top, y_top), (x_bottom, y_bottom), (255, 255, 0), 2)  # Red line

    def capture_perpendicular(self, event):
        x, y = event.x, event.y
        self.perpendicular.append((x, y))

        if len(self.perpendicular) == 2:
            print("Coordinates of Point 1:", self.perpendicular[0])
            print("Coordinates of Point 2:", self.perpendicular[1])

            per1 = self.perpendicular[1]
            per1 = tuple(v*2 for v in per1)
            self.perpendicular[1] = per1

            per2 = self.perpendicular[0]
            per2 = tuple(v*2 for v in per2)
            self.perpendicular[0] = per2

            image_with_line = self.processed_image.copy()
            cv2.circle(image_with_line, per1,2, (0, 255, 0), 10)  # Green 
            cv2.circle(image_with_line, per2, 2, (0, 255, 0), 10)  # Green 


            self.draw_perpendicular_sec(image_with_line,per1,self.slope[0])
            self.draw_perpendicular_sec(image_with_line,per2,self.slope[1])

            # self.draw_perpendicular(image_with_line,point1,point2)

            # self.draw_perpendicular(image_with_line,point3,point4)

            self.coordinates[1] = self.perpendicular[0]
            self.coordinates[3] = self.perpendicular[1]
            self.display_image(image_with_line, self.binary_image_label)
            
            # cv2.line(image, (x_left, y_left), (x_right, y_right), (255,0, 0), 2)  # Red line   


        


    def draw_points(self):
        point1 = self.coordinates[0]
        point1 = tuple(v*2 for v in point1)
        self.coordinates[0] = point1

        point2 = self.coordinates[1]
        point2 = tuple(v*2 for v in point2)
        self.coordinates[1] = point2

        point3 = self.coordinates[2]
        point3 = tuple(v*2 for v in point3)
        self.coordinates[2] = point3

        point4 = self.coordinates[3]
        point4 = tuple(v*2 for v in point4)
        self.coordinates[3] = point4

        image_with_line = self.processed_image.copy()
        cv2.circle(image_with_line, point1,2, (0, 255, 0), 10)  # Green 
        cv2.circle(image_with_line, point2, 2, (0, 255, 0), 10)  # Green 



        cv2.circle(image_with_line, point3,2, (0, 255, 0), 10)  # Green 
        cv2.circle(image_with_line, point4, 2, (0, 255, 0), 10)  # Green 

        self.draw_perpendicular(image_with_line,point1,point2)

        self.draw_perpendicular(image_with_line,point3,point4)


        
        # Display the updated image with the line
        self.display_image(image_with_line, self.binary_image_label)

    def draw_perpendicular(self,image,point1,point2):
        x1, y1 = point1
        x2, y2 = point2

        # Calculate the slope and intercept of the line passing through the points
        slope = (y2 - y1) / (x2 - x1)
        self.slope.append( slope)
        intercept = y1 - slope * x1

        # Get image dimensions
        height, width = 1200,1600#self.new_height,self.new_width

        # Calculate intersection points with image edges
        # Top edge (y=0)
        x_top = int(-intercept / slope)
        y_top = 0

        # Bottom edge (y=height)
        x_bottom = int((height - intercept) / slope)
        y_bottom = height

        # Left edge (x=0)
        x_left = 0
        y_left = int(intercept)

        # Right edge (x=width)
        x_right = width
        y_right = int(slope * width + intercept)

        # Draw the line on the image
        cv2.line(image, (x_top, y_top), (x_bottom, y_bottom), (255, 0, 0), 2)  # Red line
        cv2.line(image, (x_left, y_left), (x_right, y_right), (255,0, 0), 2)  # Red line   
        # self.draw_line(ind)
    

    def draw_line(self,ind):
    # Example: Draw a line between the two captured points
        point1 = self.curve[ind[0]]
        # point1 = tuple(v*2 for v in point1)
        point2 = self.curve[ind[1]]
        # point2 = tuple(v*2 for v in point2)
        # Draw a line on the image (image is assumed to be a copy to avoid modifying the original)
        image_with_line = self.processed_image.copy()
        cv2.line(image_with_line, point1, point2, (0, 255, 0), 2)  # Green line
        print(point1,point2)
        # Display the updated image with the line
        self.display_image(image_with_line, self.binary_image_label)




    def draw_line_between_points(self):
        # Example: Draw a line between the two captured points
        point1 = self.coordinates[0]
        point1 = tuple(v*2 for v in point1)
        point2 = self.coordinates[1]
        point2 = tuple(v*2 for v in point2)
        print(point1,point2)
        # Draw a line on the image (image is assumed to be a copy to avoid modifying the original)
        image_with_line = self.processed_image.copy()
        cv2.line(image_with_line, point1, point2, (0, 255, 0), 2)  # Green line

        # Display the updated image with the line
        self.display_image(image_with_line, self.binary_image_label)


    def calculate_angle(self):
        # Perform your calculations to update the angle variable (self.A)
        # For example, let's increment it by 10 degrees
        

        # Update the text widget with the new angle
        self.update_text_widget()

    def update_text_widget(self):
        # Clear the existing text in the widget
        self.text_widget.delete("1.0", "end")

        # Insert the updated angle into the text widget
        self.text_widget.insert("1.0", f"Angle: {self.cobb} degrees")




if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.geometry("1600x1200")  # Set an initial window size
    
    root.mainloop()
