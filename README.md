# Test Data File Generator Script

## **User Story**

### **Title:**
As a Software Development Engineer in Test (SDET), I want to create a script that generates test data files in various specified formats, so that I can validate systems that process these files with realistic mock data.

### **Description:**
The script should generate files in a given list of formats. Each file should contain text data, including strings that match the formats of Indian Government IDs such as Aadhar numbers, PAN card numbers, Voter ID numbers, Passport numbers, and Driving License numbers. The script must support file generation for formats including:

`csv`, `json`, `zip`, ~~`orc`~~, `jsonl`, `txt`, `log`, `tsv`, `html`, `xml`, ~~`ts`~~, ~~`java`~~.

> **Note:**
> - **`orc`**: Apache ORC is not natively supported in Python without external libraries like `pyorc`, currently for this exercise we are using only "built-in libraries".
> - **`ts`**: TypeScript files are not relevant as they do not serve as a data storage format for test data.
> - **`java`**: Java source files are not typically used for storing test data and are therefore excluded.
> - **Decision**: Skip `orc`, `ts`, and `java` as they are either infeasible without external dependencies or irrelevant for the current use case.

---

## **Acceptance Criteria**

### **Functional Requirements**

1. **File Format Support**:
   - The script should support the following file formats:
     - `csv`, `json`, `zip`, `jsonl`, `txt`, `log`, `tsv`, `html`, `xml`.
   - Files must be named with the appropriate extensions (e.g., `test_data.csv`, `test_data.json`).

2. **ID Generation**:
   - The script should generate mock IDs in the following formats:
     - **Aadhar Number**: 12-digit numeric (e.g., `1234-5678-9012`).
     - **PAN Card Number**: Alphanumeric, 10 characters, format: `AAAAA9999A`.
     - **Voter ID Number**: Alphanumeric, 10 characters, format: `AAA9999999`.
     - **Passport Number**: Alphanumeric, 8 characters, format: `A9999999` or `AA999999`.
     - **Driving License Number**: Alphanumeric, format (e.g., `DL-0420150149646`).

3. **Data Content**:
   - Each file must contain multiple rows of mock data with the following fields:
     - ID Type (e.g., Aadhar, PAN, etc.)
     - ID Value (randomly generated mock ID)

4. **File Content Format**:
   - **CSV/TSV**: Tabular data with headers (e.g., `ID_Type,ID_Value`).
   - **JSON**: Structured JSON objects (e.g., `{ "IDs": [{ "type": "Aadhar", "value": "123456789012" }] }`).
   - **JSONL**: Line-separated JSON objects.
   - **TXT/LOG**: Plain text data.
   - **HTML/XML**: Markup with valid formatting (e.g., `<id type="Aadhar">123456789012</id>`).
   - **ZIP**: A compressed archive containing one or more data files.

5. **Command-Line Input**:
   - The script should accept the list of formats as a command-line argument or configuration file.

---

## **How to Use**

### **Prerequisites**
- Python 3.7 or higher.
- Required libraries: `random`, `csv`, `json`, `zipfile`, and others as needed.

### **Running the Script**

1. Run the script with defaults:
   ```bash
   python generate_test_data.py
   ```
   - This will generate files in all format with 100 rows of data

2. Run the script with desired file formats:
   ```bash
   python generate_test_data.py --formats csv,json,zip --rows 100 --id-types Aadhar,PAN --files-per-format 3
   ```
   - `--formats`: Comma-separated list of file formats to generate (default: all).
   - `--rows`: Number of data entries per file (default: 100).
   - `--id-types`: Comma-separated list of ID types to include (default: all).
   - `--files-per-format` : Number of file per format (default: 1)

### **Output**
- Generated files will be saved in the script's directory with appropriate extensions.

---

## **Example Output**

### **CSV File (test_data.csv):**
```
ID_Type,ID_Value
Aadhar,123456789012
PAN,ABCDE1234F
VoterID,ABC1234567
Passport,A1234567
DrivingLicense,DL-0420150149646
```

### **JSON File (test_data.json):**
```json
{
  "IDs": [
    { "type": "Aadhar", "value": "123456789012" },
    { "type": "PAN", "value": "ABCDE1234F" },
    { "type": "VoterID", "value": "ABC1234567" },
    { "type": "Passport", "value": "A1234567" },
    { "type": "DrivingLicense", "value": "DL-0420150149646" }
  ]
}
```