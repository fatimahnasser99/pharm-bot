def detect_drug_interaction_prompt(input_text):
    prompt = f"""
    You are a clinical pharmacist and pharmacology expert.
    For a given 2 drugs, your task is to:
    - determine whether there is a clinically significant interaction between them.
    - If there is an interaction, provide the type of interaction and a brief description of the interaction. 

    Given these two drugs:  {input_text}
    
  """
    return prompt

