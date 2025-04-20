# Data Pipeline Instructions

## Step 1: Convert XML to JSON
Before proceeding, ensure you have the XML data files ready. Run the script `xml_to_json_converter.py` to convert the XML files into JSON format. This step is necessary for preparing the data for further processing.

```bash
python xml_to_json_converter.py /path/to/input.xml /path/to/output_directory
```

## Step 2: Create Database with Embeddings
Once the JSON files are generated, use the script `create_database.py` to create a database with embeddings. This step involves processing the JSON data and generating embeddings for efficient querying.

```bash
python create_database.py
```

Follow these steps in order to ensure the data pipeline is set up correctly.
