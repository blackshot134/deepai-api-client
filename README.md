# 🤖 DeepAI Terminal Chat Client

A sleek, async terminal-based chat client for the [DeepAI](https://deepai.org) API.  
Features multi-turn conversations, image generation, session saving, and a colorized CLI experience.

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

---

## ✨ Features

- 💬 **Multi-turn chat** with DeepAI models
- 🖼️ **Image generation** via `/img` command
- 💾 **Automatic session saving** to DeepAI servers
- 🎨 **Colorized terminal output** (via `colorama`)
- ⚡ **Fully async** with `httpx`
- 🔧 **Configurable** via `config.py`
- 🧹 **History management** with `/clear`
- ⏳ **Animated "thinking" spinner**

---

## 📁 Project Structure
.
├── config.py # API keys, URLs, timeouts, and settings
├── deepai_client.py # Async DeepAI API client
├── main.py # CLI entry point
└── README.md

text

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/deepai-api-client.git
cd deepai-api-client
2. Create a virtual environment (recommended)
bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
3. Install dependencies
bash
pip install httpx colorama
4. Configure your API key
Edit config.py and set your DeepAI API key:

python
DEEPAI_API_KEY = "your-api-key-here"
🔑 Get a free API key at https://deepai.org/dashboard/profile

🎮 Usage
Run the client:

bash
python main.py
Special Commands
Command	Description
/exit or /quit	Exit the program
/clear	Clear conversation history
/img <prompt>	Generate an image (e.g. /img a cyberpunk cat)
/help	Show the help banner
Example Session
text
You: Hello, who are you?
DeepAI: I'm an AI assistant powered by DeepAI...

You: /img a futuristic city at sunset
Generating image...
Image: https://api.deepai.org/job-view-file/...

You: /clear
History cleared.
⚙️ Configuration Options (config.py)
Variable	Description	Default
DEEPAI_API_KEY	Your DeepAI API key	—
DEEPAI_CHAT_URL	Chat endpoint	https://api.deepai.org/hacking_is_a_serious_crime
DEEPAI_SAVE_URL	Session save endpoint	https://api.deepai.org/save_chat_session
DEEPAI_IMAGE_URL	Text-to-image endpoint	https://api.deepai.org/api/text2img
CHAT_STYLE	Chat style	"chat"
MODEL	Model name	"standard"
TIMEOUT_REQUEST	Request timeout (s)	60.0
TIMEOUT_CONNECT	Connect timeout (s)	15.0
TIMEOUT_SAVE	Save timeout (s)	10.0
MAX_HISTORY	Max messages kept in context	10
ENABLED_TOOLS	Enabled tools	["image_generator", "image_editor"]
SHOW_THINKING	Show spinner animation	True
USE_COLORS	Enable colored output	True
🔒 Security Notice
⚠️ Never commit your real API key to GitHub!

Instead, use environment variables:

python
import os
DEEPAI_API_KEY = os.getenv("DEEPAI_API_KEY", "your-default-key")
Or use a .env file with python-dotenv:

text
DEEPAI_API_KEY=your-key-here
And add .env to .gitignore.

📦 Requirements
Python 3.9+

httpx — async HTTP client

colorama — cross-platform colored terminal output

Install all at once:

bash
pip install httpx colorama
Or create a requirements.txt:

text
httpx>=0.27.0
colorama>=0.4.6
🤝 Contributing
Contributions, issues, and feature requests are welcome!
Feel free to check the issues page.

📜 License
This project is licensed under the MIT License — see the LICENSE file for details.

⭐ Show Your Support
If this project helped you, please give it a ⭐ on GitHub!

🙏 Acknowledgments
DeepAI for their API

httpx for the excellent async HTTP library

colorama for terminal colors

