#!/usr/bin/env bash
# Hermes one-shot setup — clones, configures secrets, installs deps, and runs the bot.
set -e

cd ~/Desktop
if [ ! -d "automation-project-" ]; then
  git clone https://github.com/herohm0410-star/automation-project-.git
fi
cd automation-project-
git pull

if [ ! -f shared/config/secrets.py ]; then
  cp shared/config/secrets.example.py shared/config/secrets.py
fi

read -p "텔레그램 봇 토큰을 붙여넣으세요: " TG_TOKEN
read -p "OpenAI API 키를 붙여넣으세요: " OAI_KEY

python3 - "$TG_TOKEN" "$OAI_KEY" <<'EOF'
import re, sys
path = "shared/config/secrets.py"
tg, oai = sys.argv[1], sys.argv[2]
with open(path) as f:
    content = f.read()
content = re.sub(r'os\.environ\["TELEGRAM_BOT_TOKEN"\]\s*=\s*".*"', f'os.environ["TELEGRAM_BOT_TOKEN"] = "{tg}"', content)
content = re.sub(r'os\.environ\["OPENAI_API_KEY"\]\s*=\s*".*"', f'os.environ["OPENAI_API_KEY"] = "{oai}"', content)
with open(path, "w") as f:
    f.write(content)
print("키 저장 완료!")
EOF

pip3 install -r requirements.txt -q

echo ""
echo "설정 완료! Hermes 봇을 시작합니다. 텔레그램에서 봇과 대화해보세요."
echo "끄려면 이 창에서 Ctrl+C 를 누르세요."
echo ""
python3 -m hermes_bot.hermes_bot
