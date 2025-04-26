# XML to JSON Converter

This script converts an XML file containing drug information into individual JSON files. Each JSON file contains up to 100 random drug interactions for a specific drug.

## Features

- Converts XML data into JSON format.
- Extracts up to 100 random drug interactions for each drug.
- Saves the interactions in separate JSON files, named after the drug.

## Requirements

The script requires the following Python packages:

- `python-dotenv`
- `xmltodict`

Install the dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Usage

Run the script from the command line with the following syntax:

```bash
python xml_to_json_converter.py /path/to/input.xml /path/to/output_directory
```

### Arguments

1. `/path/to/input.xml`: Path to the input XML file containing drug data.
2. `/path/to/output_directory`: Path to the directory where the JSON files will be saved.

### Example

```bash
python xml_to_json_converter.py drugs.xml output/
```

This will process the `drugs.xml` file and save the JSON files in the `output/` directory.

## Notes

- The script processes up to 100 drugs from the XML file.
- Each drug's interactions are saved in a separate JSON file named `<drug_name>_interactions.json`.
- If the drug name contains spaces, they are replaced with underscores in the file name.

## Error Handling

- If the input XML file does not exist, the script will display an error message and exit.
- If the output directory does not exist, it will be created automatically.
