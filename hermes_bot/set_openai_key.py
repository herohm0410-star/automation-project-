"""Prompts for an OpenAI API key and writes it into shared/config/secrets.py.

Run from the repo root:
    python3 hermes_bot/set_openai_key.py
"""

import re
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "shared" / "config" / "secrets.py"

key = input("OpenAI 키를 붙여넣으세요: ").strip()

text = path.read_text()
text, n = re.subn(
    r'os\.environ\["OPENAI_API_KEY"\]\s*=\s*".*"',
    f'os.environ["OPENAI_API_KEY"] = "{key}"',
    text,
)
if n == 0:
    raise SystemExit("OPENAI_API_KEY line not found in secrets.py")

path.write_text(text)
print("저장 완료!")
