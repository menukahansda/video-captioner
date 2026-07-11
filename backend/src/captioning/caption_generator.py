import json
from src.captioning.llm_client import generate_text
from src.captioning.prompts import CAPTION_GENERATION_PROMPT

def generate_captions(summary: str):
    prompt = CAPTION_GENERATION_PROMPT.format(summary=summary)
    response = generate_text(prompt)
    if response.startswith("```"):
        response = response.strip("`")
        response = response.replace("json\n", "", 1).strip()
    try:
        captions = json.loads(response)
        return captions
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON from Gemini: {response[:200]}")
    

# if __name__ == "__main__":
#     sample_summary = """
#     A person walks through a tree-lined street while vehicles pass by.
#     The weather is pleasant and the surroundings are calm.
#     """
#     captions = generate_captions(sample_summary)
#     print(json.dumps(captions, indent=4))