import httpx
from app.core.config import settings

class LLMClient:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = settings.GROQ_MODEL

    async def generate_completion(self, prompt: str) -> str:
        if not self.api_key or "YOUR_GROQ" in self.api_key:
            return "[Error: Groq API Key belum dikonfigurasi di .env]"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Anda adalah asisten pelaporan anonim."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                if response.status_code == 401:
                    return f"[Error: Groq API Key Tidak Valid (401). Cek .env Anda]"

                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[Error in sanitization: {str(e)}]"

llm_client = LLMClient()
