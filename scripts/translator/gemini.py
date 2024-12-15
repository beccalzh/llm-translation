import os
import sys
from dotenv import load_dotenv
load_dotenv()
import argparse
from pathlib import Path
import google.generativeai as genai
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.insert(0, project_path)
from intercept import get_pofile_from_path

def get_prompt(text_in:str) -> str:
    return f'''
            Translate the following Python documentation into Traditional Chinese. 
            Ensure that the translation is accurate and uses appropriate technical terminology. 
            The output must be in Traditional Chinese. 
            Pay careful attention to context, idiomatic expressions, and any specialized vocabulary related to Python programming. 
            Maintain the structure and format of the original documentation as much as possible to ensure clarity and usability for readers. 
            Here is the text to translate: {text_in}.
            '''

def translate_text(text_in:str) -> str:
    genai.configure(api_key=os.getenv('GEMINI_API'))
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(get_prompt(text_in))
    return response.text

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

