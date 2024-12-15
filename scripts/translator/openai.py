import os
import sys
from dotenv import load_dotenv
load_dotenv()
import argparse
from pathlib import Path
import requests
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.insert(0, project_path)
from intercept import get_pofile_from_path

def get_prompt(text_in:str) -> list:
    if text_in.strip() == '':
        raise ValueError('No translate targets.')
    return [
        {"role": "system", "content": "Translate the following Python documentation into Traditional Chinese."},
        {"role": "system", "content": "Ensure that the translation is accurate and uses appropriate technical terminology."},
        {"role": "system", "content": "The output must be in Traditional Chinese."},
        {"role": "system", "content": "Pay careful attention to context, idiomatic expressions, and any specialized vocabulary related to Python programming."},
        {"role": "system", "content": "Maintain the structure and format of the original documentation as much as possible to ensure clarity and usability for readers."},
        {"role": "user", "content": f"{text_in}"}
    ]

def translate_text(text_in: str) -> str:
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.getenv("OPENAI_API")}'
        },
        json={
            'model': 'gpt-3.5-turbo',
            'messages': get_prompt(text_in),
            'temperature': 0,
            'max_tokens': 4096
        }
    )
    response.raise_for_status() 
    result = response.json()
    return result['choices'][0]['message']['content']

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        help="the path of a po file",
    )
    parser.add_argument("-n", '--occurrence_number', type=int, default=1)
    args = parser.parse_args()
    path = Path(args.path).resolve()
    pofile = get_pofile_from_path(path)
    occurrence_number = args.occurrence_number

    for entry in pofile:
        if not any(path.stem in p and int(n) == occurrence_number for p, n in entry.occurrences):
            continue
        print(f'parsed: {entry.msgid}')
        print(f'translated: {translate_text(entry.msgid)}')
        break

