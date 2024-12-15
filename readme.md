## Project Directory Structure:

```plaintext
library/
├── builtins.po                # Contains translations for built-in functionality
scripts/
├── translator/
│   ├── .env                   # Environment variables for secure API usage
│   ├── gemini.py              # Script for handling translations via Gemini API
│   └── openai.py              # Script for handling translations via OpenAI API
└── intercept.py               # Script for intercepting and processing text inputs
requirements.txt               # Dependencies for the project
readme.md                      # Documentation for the project
.gitignore
```

## Set up
 
1. Configure the .env File:

Add your API keys to the .env file in the `scripts/translator/` directory. Example:

```plaintext
OPENAI_API=your_openai_api_key
GEMINI_API=your_gemini_api_key
```

2. Install Dependencies:

Use uv for dependency isolation and to install all necessary packages:

```bash
uv pip install -r requirements.txt
```

3.	Verify File Paths:
Ensure that the .po file paths provided in the `library/` directory match your intended usage.

## Sample .po File Format

Below is an example .po file structure:

```plaintext
#: ../../library/builtins.rst:9
msgid ""
"This module provides direct access to all 'built-in' identifiers of Python; "
"for example, ``builtins.open`` is the full name for the built-in function :"
"func:`open`."
```

## Usage

To process and translate a .po file, use the following command:

```bash
uv run intercept.py library/builtins.po -n 9
```

## Output Example

```plaintext
parsed: This module provides direct access to all 'built-in' identifiers of Python; for example, ``builtins.open`` is the full name for the built-in function :func:`open`. See :ref:`built-in-funcs` and :ref:`built-in-consts` for documentation.
translated: 這個模組提供直接存取 Python 所有「內建」識別項的功能；例如，`builtins.open` 是內建函式 :func:`open` 的完整名稱。請參閱 :ref:`built-in-funcs` 和 :ref:`built-in-consts` 了解更多文件說明。
```