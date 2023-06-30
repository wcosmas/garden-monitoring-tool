import os
import xml.etree.ElementTree as ET
from PIL import Image

# Step 1: Read XML annotation files
annotations_dir = './data'
output_dir = './dataset'
class_label_mapping = {'maize': 'maize', 'cassava': 'cassava', 'grass': 'grass',
                       'sugarcane': 'sugarcane'}  # Define your class label mapping

# Create output directories for each class
for class_label in class_label_mapping.values():
    class_output_dir = os.path.join(output_dir, class_label)
    os.makedirs(class_output_dir, exist_ok=True)

for xml_file in os.listdir(annotations_dir):
    if not xml_file.endswith('.xml'):
        continue

    # Step 2: Parse XML annotations
    tree = ET.parse(os.path.join(annotations_dir, xml_file))
    root = tree.getroot()

    image_path = root.find('filename').text  # Image filename
    bounding_boxes = root.findall(
        './/object/bndbox')  # Bounding box coordinates
    class_labels = root.findall('.//object/name')  # Class labels

    # Step 3: Load the image
    image = Image.open(os.path.join(annotations_dir, image_path))

    for bbox, label in zip(bounding_boxes, class_labels):
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)

        class_label = label.text.lower()

        if class_label in class_label_mapping:
            class_folder = class_label_mapping[class_label]
        else:
            class_folder = 'unknown'

        # Step 4: Crop and save the image in the respective class folder
        cropped_image = image.crop((xmin, ymin, xmax, ymax))

        class_output_dir = os.path.join(output_dir, class_folder)
        os.makedirs(class_output_dir, exist_ok=True)
        if os.path.splitext(xml_file)[0] is not None:
            print(os.path.splitext(xml_file)[0])
            image_filename = os.path.splitext(xml_file)[0] + '.jpg'
            output_path = os.path.join(class_output_dir, image_filename)

            cropped_image.save(output_path)
