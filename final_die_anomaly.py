import json
import cv2
import os
import numpy as np
import csv

# importing the json file
json_file = "input_1.json"

# Storing the inputs
with open (json_file) as f:
    data = json.load(f)
    dieWidth = data['die']['width']
    dieHeight = data['die']['height']
    streetWidth = data['street_width']
    careAreas = data['care_areas']
    exclusionZones = data.get('exclusion_zones')
    
'''
print(dieWidth)    
print(dieHeight)
print(streetWidth)
print(careAreas)
'''

# Take the wafer images and process it

image_directory = "C:\\Users\\91978\\Desktop\\ANOMALY\\images_1"

defects = []

images = []
subResult = 0
i = 0

# Iterate over the files in the image directory
for filename in os.listdir(image_directory):
    if filename.endswith('.png') and filename.startswith('wafer_image_'):
        
        #img = cv2.imread()
        # Extract the frame index from the file name
        frameIndex = int(filename.split('_')[-1].split('.')[0])
        
        #print(frameIndex)
        
        # Load the image
        image_path = os.path.join(image_directory, filename)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        # Cropping the images since we are concerned only about the care areas
        image = image[0:800, 0:600]
        
        # Calculate the dimensions of the image
        dimensions = image.shape
 
        # height, width
        imageHeight = image.shape[0]
        imageWidth = image.shape[1]
        
        # No. of image frames per die
        n = (dieHeight * dieWidth) // (imageHeight * imageWidth)
        
        images.append(image)
        
        if len(images) == 5:
            subResult = np.zeros_like(images[0]) # Initialize the subtraction result
            
            for i in range(1, len(images)):
                subResult -= cv2.subtract(images[i], images[i-1])
                
            coords = np.argwhere(subResult > 0)
            for coord in coords:
                defects.append((frameIndex, coord[1], coord[0]))
                
            images.pop(0) # Remove the oldest image from the list

defectPoints = []
# Print the defect information
for defect in defects:
    dieIndex, x, y = defect
    #print("{0}, {1}, {2}".format(dieIndex, x, y))
    
    defectPoints.append((dieIndex, x, y))
    
with open("defect.csv","a+") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(defectPoints)
    
    


        
        
