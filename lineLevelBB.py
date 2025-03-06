import xml.etree.ElementTree as ET

def extract_line_bounding_boxes(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    line_boxes = []

    # Iterate through all handwritten lines
    for line in root.findall(".//handwritten-part/line"):
        line_text = line.attrib.get("text", "")
        line_id = line.attrib.get("id", "")
        bbox = None

        # Extract bounding box coordinates from `lower-contour` and `upper-contour`
        lower_contour = line.find("lower-contour")
        upper_contour = line.find("upper-contour")

        contour_points = []
        if lower_contour is not None:
            contour_points += [(int(pt.attrib.get("x")), int(pt.attrib.get("y"))) for pt in lower_contour.findall("point")]
        if upper_contour is not None:
            contour_points += [(int(pt.attrib.get("x")), int(pt.attrib.get("y"))) for pt in upper_contour.findall("point")]

        # Compute bounding box if points exist
        if contour_points:
            x_min = min(pt[0] for pt in contour_points)
            x_max = max(pt[0] for pt in contour_points)
            y_min = min(pt[1] for pt in contour_points)
            y_max = max(pt[1] for pt in contour_points)

            bbox = (x_min, y_min, x_max - x_min, y_max - y_min)  # (x, y, width, height)

        line_boxes.append({
            "line_id": line_id,
            "line_text": line_text,
            "bounding_box": bbox
        })

    return line_boxes

# Example usage
xml_file_path = "path/to/your/file.xml"  # Replace with your XML file path
line_bounding_boxes = extract_line_bounding_boxes(xml_file_path)

# Print extracted line bounding boxes
for line_info in line_bounding_boxes:
    print(f"Line ID: {line_info['line_id']}, Text: {line_info['line_text']}, Bounding Box: {line_info['bounding_box']}")

# Count the total number of extracted lines
print(f"\nTotal number of extracted line bounding boxes: {len(line_bounding_boxes)}")
