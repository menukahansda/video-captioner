import json
from src.captioning.llm_client import generate_json
from src.captioning.prompts import CAPTION_GENERATION_PROMPT

def generate_captions(summary: dict, styles: list[str]):
    prompt = CAPTION_GENERATION_PROMPT.format(
        summary=summary,
        styles=", ".join(styles),
    )
    captions = generate_json(prompt=prompt)

    return {k: v for k, v in captions.items() if k in styles}
    

# if __name__ == "__main__":
#     sample_summary = {
#         "main_subject": "A person walking",
#         "actions": "walking along a tree-lined street",
#         "location": "urban street with trees",
#         "objects": "vehicles, trees",
#         "scene_changes": "single continuous scene",
#         "story": "no clear narrative, a walk through the street",
#     }
#     captions = generate_captions(sample_summary, ["formal", "sarcastic", "humorous_tech", "humorous_non_tech"])
#     print(json.dumps(captions, indent=4))