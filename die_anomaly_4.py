from PIL import Image
import json
import os
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


# Take the wafer images and process it

image_directory = "C:\\Users\\91978\\Desktop\\ANOMALY\\images_1"

colour_freq = {}

# Iterate over the files in the image directory
for filename in os.listdir(image_directory):
    if filename.endswith('.png') and filename.startswith('wafer_image_'):
        
        #img = cv2.imread()
        # Extracting the die index from the file name
        dieIndex = int(filename.split('_')[-1].split('.')[0])
        
        #print(frameIndex)
        
        # Load the image
        image_path = os.path.join(image_directory, filename)
        
        image = Image.open(image_path)
        image = image.convert('RGB')
        pixels = image.load()
        
        #setting care area coordinates
        x1 = careAreas[0]['top_left']['x']
        x2 = careAreas[0]['bottom_right']['x']
        y1 = careAreas[0]['bottom_right']['y']
        y2 = careAreas[0]['top_left']['y']

        # Cropping the images since we are concerned only about the care areas
        # Finding the colour that occurred the most times
        for y in range(y1, y2):
            for x in range(x1, x2):
                colour = pixels[x, y]
                if colour in colour_freq:
                    colour_freq[colour] += 1
                else:
                    colour_freq[colour] = 1

        colours = {} 
        
        # Background
        maxcol1 = max(colour_freq.values())
        for key in colour_freq:
            if colour_freq[key] == maxcol1:
                major_col1 = key
        colours[major_col1] = colour_freq.pop(major_col1)
    
        # White lines
        maxcol2 = max(colour_freq.values())
        for key in colour_freq:
            if colour_freq[key] == maxcol2:
                major_col2 = key
        colours[major_col2] = colour_freq.pop(major_col2)
    
        defectPoints = []
        defect_xy = []
    
        for y in range(y1, y2):
            for x in range(x1, x2):
                colour = pixels[x, y]
                if colour != major_col1 and colour != major_col2:
                    defectPoints.append((dieIndex, x, y))
        #print(defectPoints)

    # writing into file
    with open("defect_1.csv","a+") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(defectPoints)

