"""
Local LLM backend.

This file provides the same interface as gemini_backend.py
but is intended for running local models such as:
- Ollama
- Llama
- Phi
- Qwen

Currently it is a placeholder.
"""


def generate_text(prompt: str):
    """
    Generate text using a local language model.
    """
    raise NotImplementedError(
        "Local text generation backend is not implemented yet."
    )


def generate_video_summary(contents):
    """
    Generate a video summary using a local multimodal model.
    """
    raise NotImplementedError(
        "Local video understanding backend is not implemented yet."
    )


# if __name__ == "__main__":
#     try:
#         generate_text("Hello")
#     except NotImplementedError as e:
#         print(e)