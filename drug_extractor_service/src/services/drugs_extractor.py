from models.drugs_model import DrugExtractionOutput
from prompts.drug_extractor_prompts import extract_drug_prompt
from utils.llms_util import structured_model

def extract_drugs_from_text(input_text):
    output_class = DrugExtractionOutput
    user_prompt = extract_drug_prompt(input_text)
    result = structured_model(user_prompt, output_class)
    drugs_list = result.drugs_list
    return drugs_list