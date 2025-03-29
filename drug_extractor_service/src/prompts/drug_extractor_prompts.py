def extract_drug_prompt(input_text):
    prompt = f"""
    You are a pharmacist and expert in drug nomenclature.

    Your task is to extract a **clean list of drug names only** from the provided text. 
    Exclude dosage forms, strengths, quantities, and packaging info.

    If no drug is detected, return an empty list.

    Input:
    {input_text}
  """
    return prompt

