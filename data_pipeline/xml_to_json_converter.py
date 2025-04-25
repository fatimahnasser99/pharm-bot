import xml.etree.ElementTree as ET
import json
import os
import sys
import random

def xml_to_dict(element):
    """
    Recursively converts an XML element and its children into a dictionary.
    """
    result = {}
    if element.text and element.text.strip():
        result["text"] = element.text.strip()
    for key, value in element.attrib.items():
        result[key] = value
    for child in element:
        child_result = xml_to_dict(child)
        if child.tag not in result:
            result[child.tag] = child_result
        else:
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(child_result)
    return result

def extract_drug_interactions(drug):
    """
    Extracts up to 100 random drug interactions in the specified format.
    """
    interactions = []
    current_drug_name = drug.get("name", "this drug")
    if isinstance(current_drug_name, dict):
        current_drug_name = current_drug_name.get("text", "this drug")
    if "drug-interactions" in drug and isinstance(drug["drug-interactions"], dict):
        drug_interactions = drug["drug-interactions"].get("drug-interaction", [])
        if isinstance(drug_interactions, list):
            # Randomly sample up to 100 interactions
            sampled_interactions = random.sample(drug_interactions, min(len(drug_interactions), 100))
            for interaction in sampled_interactions:
                second_drug_name = interaction.get("name", "unknown drug")
                if isinstance(second_drug_name, dict):
                    second_drug_name = second_drug_name.get("text", "unknown drug")
                description = interaction.get("description", {}).get("text", "no description available")
                interactions.append(f"{current_drug_name} interaction with {second_drug_name} is: {description}")
        elif isinstance(drug_interactions, dict):
            second_drug_name = drug_interactions.get("name", "unknown drug")
            if isinstance(second_drug_name, dict):
                second_drug_name = second_drug_name.get("text", "unknown drug")
            description = drug_interactions.get("description", {}).get("text", "no description available")
            interactions.append(f"{current_drug_name} interaction with {second_drug_name} is: {description}")
    return interactions

def convert_xml_to_json(xml_file, output_dir):
    """
    Converts an XML file to individual JSON files containing up to 100 random drug interactions for each drug.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # Remove namespace from tags
    for elem in root.iter():
        elem.tag = elem.tag.split('}')[-1]
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process up to 100 drugs and write their interactions to JSON files
    for i, child in enumerate(root.findall('drug')):
        if i >= 100:  # Limit to 100 drugs
            break
        drug_data = xml_to_dict(child)
        interactions = extract_drug_interactions(drug_data)
        if interactions:
            # Safely extract the drug name as a string
            drug_name = drug_data.get("name", "unknown_drug")
            if isinstance(drug_name, dict):
                drug_name = drug_name.get("text", "unknown_drug")
            drug_name = drug_name.replace(" ", "_")
            
            json_file = os.path.join(output_dir, f"{drug_name}_interactions.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(interactions, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python xml_to_json_converter.py /path/to/input.xml /path/to/output_directory")
        sys.exit(1)

    # Get input file and output directory paths from command-line arguments
    xml_file = sys.argv[1]
    output_dir = sys.argv[2]

    # Validate input file
    if not os.path.isfile(xml_file):
        print(f"Error: The file '{xml_file}' does not exist.")
        sys.exit(1)

    # Convert XML to JSON
    convert_xml_to_json(xml_file, output_dir)
    print(f"XML file '{xml_file}' has been processed. JSON files are saved in '{output_dir}'.")