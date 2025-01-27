import argparse
import csv
import json
import os
import random
import string
import xml.etree.ElementTree as ET
from zipfile import ZipFile

# Helper function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Test Data File Generator")
    parser.add_argument(
        "--formats",
        type=str,
        default="all",
        help="Comma-separated list of file formats to generate (e.g., csv,json,zip). Default: all"
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=100,
        help="Number of rows to generate per file (default: 100)"
    )
    parser.add_argument(
        "--id-types",
        type=str,
        default="all",
        help="Comma-separated list of ID types to generate (e.g., Aadhar,PAN). Default: all"
    )
    parser.add_argument(
        "--files-per-format",
        type=int,
        default=1,
        help="Number of files to generate per format (default: 1)"
    )
    return parser.parse_args()

# Functions to generate random IDs in different formats
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

# Function to validate ID types
def validate_id_types(id_types, valid_id_types):
    if id_types == "all":
        return valid_id_types
    invalid_types = [id_type for id_type in id_types if id_type not in valid_id_types]
    if invalid_types:
        raise ValueError(f"Invalid ID types: {', '.join(invalid_types)}. Supported types are: {', '.join(valid_id_types)}.")
    return id_types

# Function to generate random ID data
def generate_mock_data(rows, id_types):
    id_generators = {
        "Aadhar": generate_aadhar,
        "PAN": generate_pan,
        "VoterID": generate_voter_id,
        "Passport": generate_passport,
        "DrivingLicense": generate_driving_license
    }

    selected_generators = {k: v for k, v in id_generators.items() if k in id_types}

    data = []
    generator_keys = list(selected_generators.keys())
    for i in range(rows -1):
        #id_type = random.choice(list(selected_generators.keys())) # Randomly select an ID type
        id_type = generator_keys[i % len(generator_keys)]  # Cycle through the keys sequentially
        id_value = selected_generators[id_type]()
        data.append({"ID_Type": id_type, "ID_Value": id_value})
    return data

# Function to write data to a CSV file
def write_csv(data, filename, delimiter=','):
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["ID_Type", "ID_Value"], delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)

# Function to write data to a JSON file
def write_json(data, filename):
    with open(filename, "w") as file:
        json.dump({"IDs": data}, file, indent=4)

# Function to write data to a JSONL file
def write_jsonl(data, filename):
    with open(filename, "w") as file:
        for entry in data:
            file.write(json.dumps(entry) + "\n")

# Function to write data to a TXT or LOG file
def write_txt(data, filename):
    with open(filename, "w") as file:
        for entry in data:
            file.write(f"{entry['ID_Type']}: {entry['ID_Value']}\n")

# Function to write data to an XML file
def write_xml(data, filename):
    root = ET.Element("IDs")
    for entry in data:
        id_element = ET.SubElement(root, "ID", type=entry["ID_Type"])
        id_element.text = entry["ID_Value"]

    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)

# Function to write data to an HTML file
def write_html(data, filename):
    with open(filename, "w") as file:
        file.write("<html><body><table border='1'>\n")
        file.write("<tr><th>ID Type</th><th>ID Value</th></tr>\n")
        for entry in data:
            file.write(f"<tr><td>{entry['ID_Type']}</td><td>{entry['ID_Value']}</td></tr>\n")
        file.write("</table></body></html>")

# Function to write data to a ZIP file
def write_zip(data, filename):
    with ZipFile(filename, "w") as zipf:
        temp_csv = "temp.csv"
        write_csv(data, temp_csv)
        zipf.write(temp_csv)
        os.remove(temp_csv)

# Main function to handle file generation
def main():
    args = parse_arguments()
    formats = args.formats.split(",") if args.formats != "all" else ["csv", "json", "jsonl", "txt", "log", "xml", "html", "zip", "tsv"]
    rows = args.rows
    id_types = args.id_types.split(",") if args.id_types != "all" else "all"
    files_per_format = args.files_per_format

    valid_id_types = ["Aadhar", "PAN", "VoterID", "Passport", "DrivingLicense"]
    id_types = validate_id_types(id_types, valid_id_types)

    for fmt in formats:
        for file_number in range(1, files_per_format + 1):
            data = generate_mock_data(rows, id_types)
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
            else:
                print(f"Unsupported format: {fmt}")

if __name__ == "__main__":
    main()
