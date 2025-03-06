import xml.etree.ElementTree as ET

def extract_word_bounding_boxes(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    word_boxes = []

    # Iterate through handwritten part
    for line in root.findall(".//handwritten-part/line"):
        line_text = line.attrib.get("text", "")
        for word in line.findall("word"):
            word_text = word.attrib.get("text", "")
            word_id = word.attrib.get("id", "")
            bbox = []

            # Extract bounding box coordinates
            for cmp in word.findall("cmp"):
                x = int(cmp.attrib.get("x", 0))
                y = int(cmp.attrib.get("y", 0))
                width = int(cmp.attrib.get("width", 0))
                height = int(cmp.attrib.get("height", 0))
                bbox.append((x, y, width, height))

            word_boxes.append({
                "word_id": word_id,
                "word_text": word_text,
                "bounding_boxes": bbox
            })

    return word_boxes

# Specify the path to the uploaded XML file
xml_file_path = "/mnt/data/p03-173.xml"

# Extract word bounding boxes
word_bounding_boxes = extract_word_bounding_boxes(xml_file_path)

# Print the extracted bounding boxes
for word_info in word_bounding_boxes[:10]:  # Display first 10 words for brevity
    print(f"Word ID: {word_info['word_id']}, Text: {word_info['word_text']}, Bounding Boxes: {word_info['bounding_boxes']}")
