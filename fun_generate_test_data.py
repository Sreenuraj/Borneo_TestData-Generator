import csv
import json
import os
import random
import string
import xml.etree.ElementTree as ET
from zipfile import ZipFile

def generate_test_data(
    formats=["csv", "json", "jsonl", "txt", "log", "xml", "html", "zip", "tsv"],
    rows=100,
    id_types=["Aadhar", "PAN", "VoterID", "Passport", "DrivingLicense"],
    files_per_format=1
):
    """
    Generate test data files with various ID types in multiple formats.
    
    Args:
        formats (list): List of output formats
        rows (int): Number of rows per file
        id_types (list): List of ID types to generate
        files_per_format (int): Number of files per format
    """
    
    def generate_aadhar():
        aadhar_number = "".join([str(random.randint(0, 9)) for _ in range(12)])
        return f"{aadhar_number[:4]}-{aadhar_number[4:8]}-{aadhar_number[8:]}"
    
    def generate_pan():
        return "".join(random.choices(string.ascii_uppercase, k=5)) + \
               "".join(random.choices(string.digits, k=4)) + \
               random.choice(string.ascii_uppercase)
    
    def generate_voter_id():
        return "".join(random.choices(string.ascii_uppercase, k=3)) + \
               "".join(random.choices(string.digits, k=7))
    
    def generate_passport():
        return random.choice(string.ascii_uppercase) + \
               "".join(random.choices(string.digits, k=7))
    
    def generate_driving_license():
        return "DL-" + "".join(random.choices(string.digits, k=13))

    id_generators = {
        "Aadhar": generate_aadhar,
        "PAN": generate_pan,
        "VoterID": generate_voter_id,
        "Passport": generate_passport,
        "DrivingLicense": generate_driving_license
    }

    def generate_mock_data():
        data = []
        generator_keys = list(id_generators.keys())
        for i in range(rows - 1):
            id_type = generator_keys[i % len(generator_keys)]
            id_value = id_generators[id_type]()
            data.append({"ID_Type": id_type, "ID_Value": id_value})
        return data

    def write_csv(data, filename, delimiter=','):
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["ID_Type", "ID_Value"], delimiter=delimiter)
            writer.writeheader()
            writer.writerows(data)

    def write_json(data, filename):
        with open(filename, "w") as file:
            json.dump({"IDs": data}, file, indent=4)

    def write_jsonl(data, filename):
        with open(filename, "w") as file:
            for entry in data:
                file.write(json.dumps(entry) + "\n")

    def write_txt(data, filename):
        with open(filename, "w") as file:
            for entry in data:
                file.write(f"{entry['ID_Type']}: {entry['ID_Value']}\n")

    def write_xml(data, filename):
        root = ET.Element("IDs")
        for entry in data:
            id_element = ET.SubElement(root, "ID", type=entry["ID_Type"])
            id_element.text = entry["ID_Value"]
        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)

    def write_html(data, filename):
        with open(filename, "w") as file:
            file.write("<html><body><table border='1'>\n")
            file.write("<tr><th>ID Type</th><th>ID Value</th></tr>\n")
            for entry in data:
                file.write(f"<tr><td>{entry['ID_Type']}</td><td>{entry['ID_Value']}</td></tr>\n")
            file.write("</table></body></html>")

    def write_zip(data, filename):
        with ZipFile(filename, "w") as zipf:
            temp_csv = "temp.csv"
            write_csv(data, temp_csv)
            zipf.write(temp_csv)
            os.remove(temp_csv)

    for fmt in formats:
        for file_number in range(1, files_per_format + 1):
            data = generate_mock_data()
            filename_suffix = f"_{file_number}" if files_per_format > 1 else ""
            
            if fmt == "csv":
                write_csv(data, f"test_data{filename_suffix}.csv")
            elif fmt == "json":
                write_json(data, f"test_data{filename_suffix}.json")
            elif fmt == "jsonl":
                write_jsonl(data, f"test_data{filename_suffix}.jsonl")
            elif fmt == "txt" or fmt == "log":
                write_txt(data, f"test_data{filename_suffix}.{fmt}")
            elif fmt == "xml":
                write_xml(data, f"test_data{filename_suffix}.xml")
            elif fmt == "html":
                write_html(data, f"test_data{filename_suffix}.html")
            elif fmt == "zip":
                write_zip(data, f"test_data{filename_suffix}.zip")
            elif fmt == "tsv":
                write_csv(data, f"test_data{filename_suffix}.tsv", delimiter='\t')
                
                
## Generate all formats with default settings
#generate_test_data()
#
# Generate specific formats with custom settings
#generate_test_data(
#    formats=["csv", "json"],
#    rows=50,
#    id_types=["Aadhar", "PAN"],
#    files_per_format=2
#)