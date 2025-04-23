from utils.llms_util import structured_model
from utils.db_utils import get_vector_db
from models.drugs_model import DrugExtractionOutput
from detect_drug_interaction_serivce.src.prompts.drug_interaction_detection_prompts import detect_drug_interaction_prompt


def detect_drugs_interaction_from_text(input_text):
    output_class = DrugExtractionOutput
    vector_db = get_vector_db("drugs_collection")
    user_prompt = detect_drug_interaction_prompt(input_text)
    result = structured_model(user_prompt, vector_db, output_class)
    drugs_list = result.drugs_list
    return drugs_list