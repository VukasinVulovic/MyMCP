import requests
from dotenv import load_dotenv
import json
import re
load_dotenv()

import os

def queryModel(prompt: str):
    res = requests.post(os.getenv("MODEL_COMPLETIONS_ENDPOINT", "http://localhost:1111/chat/completions"), json={
        "model": os.getenv("SELECTED_MODEL", "gemma-3-12b-it-q4_0.gguf"),
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    if res.status_code != 200:
        raise Exception(res.text)

    return res.json()["choices"][0]["message"]["content"]

def parseModelResponseJSON(model_output: str):
    return json.loads(
        re.search(r'\[.*\]', model_output, re.S) \
        .group(0) \
        .replace('\\n', '').replace('\n', '')
    )