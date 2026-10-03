import httpx

from app.llm.base import LLMProvider


class OllamaProvider(LLMProvider):

    def __init__(
        self,
        model: str = "qwen3:8b",
        base_url: str = "http://localhost:11434",
    ):
        self.model = model
        self.base_url = base_url

    def generate(self, prompt: str) -> str:

        response = httpx.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "think": False,
                "options": {"temperature": 0.4},
            },
            timeout=120.0,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"].strip()
