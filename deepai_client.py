import json
import uuid
import httpx
from config import (
    DEEPAI_API_KEY,
    DEEPAI_CHAT_URL,
    DEEPAI_SAVE_URL,
    DEEPAI_IMAGE_URL,
    CHAT_STYLE,
    MODEL,
    TIMEOUT_REQUEST,
    TIMEOUT_CONNECT,
    TIMEOUT_SAVE,
    MAX_HISTORY,
    ENABLED_TOOLS,
)


class DeepAIClient:
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(TIMEOUT_REQUEST, connect=TIMEOUT_CONNECT),
            limits=httpx.Limits(
                max_keepalive_connections=10,
                max_connections=20,
            ),
        )
        self.session_uuid = str(uuid.uuid4())
        self.history = []

    async def _save_session(self, chat_history: list, title: str = "") -> bool:
        try:
            resp = await self.client.post(
                DEEPAI_SAVE_URL,
                data={
                    "uuid": self.session_uuid,
                    "title": title,
                    "chat_style": CHAT_STYLE,
                    "messages": json.dumps(chat_history, ensure_ascii=False),
                },
                headers={"api-key": DEEPAI_API_KEY},
                timeout=TIMEOUT_SAVE,
            )
            return resp.status_code == 200
        except Exception:
            return False

    async def _chat_request(self, chat_history: list) -> tuple[bool, str]:
        try:
            resp = await self.client.post(
                DEEPAI_CHAT_URL,
                files={
                    "chat_style": (None, CHAT_STYLE),
                    "chatHistory": (None, json.dumps(chat_history, ensure_ascii=False)),
                    "model": (None, MODEL),
                    "session_uuid": (None, self.session_uuid),
                    "sensitivity_request_id": (None, str(uuid.uuid4())),
                    "hacker_is_stinky": (None, "very_stinky"),
                    "enabled_tools": (None, json.dumps(ENABLED_TOOLS)),
                },
                headers={"api-key": DEEPAI_API_KEY},
                timeout=TIMEOUT_REQUEST,
            )

            if resp.status_code == 200:
                text = resp.text.strip()
                if text:
                    return True, text
                return False, "No response received"
            return False, f"Server error: {resp.status_code}"

        except httpx.ReadTimeout:
            return False, "Request timed out, please try again"
        except httpx.ConnectError:
            return False, "Failed to connect to server"
        except Exception as e:
            return False, f"Error: {str(e)[:150]}"

    async def chat(self, question: str) -> str:
        self.history.append({"role": "user", "content": question})
        chat_history = self.history[-MAX_HISTORY:]
        await self._save_session(chat_history, title=question[:50])

        success, response = await self._chat_request(chat_history)

        if success:
            self.history.append({"role": "assistant", "content": response})
            return response

        self.history.pop()
        return response

    async def generate_image(self, prompt: str) -> str:
        try:
            resp = await self.client.post(
                DEEPAI_IMAGE_URL,
                data={"text": prompt},
                headers={"api-key": DEEPAI_API_KEY},
                timeout=TIMEOUT_REQUEST,
            )
            if resp.status_code == 200:
                data = resp.json()
                return data.get("output_url", "") or "No image URL received"
            return f"Error: {resp.status_code}"
        except Exception as e:
            return f"Error: {str(e)[:100]}"

    def clear_history(self):
        self.history = []
        self.session_uuid = str(uuid.uuid4())

    async def close(self):
        try:
            await self.client.aclose()
        except Exception:
            pass