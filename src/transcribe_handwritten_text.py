from src.openai_client import openai_client


def transcribe_handwritten_text(base64_img: str):
    GPT_MODEL = "gpt-4-turbo-2024-04-09"
    response = openai_client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {
                "role": "user",
                "content": 'Transcribe the handwriting in this image, only output the handwritten text.',
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_img}"
                        }
                    },
                ],
            }
        ],
    )

    return response.choices[0].message.content
