import json
import time
from google import genai
from google.genai.types import HttpOptions, GenerateContentResponse

class GoogleLLMService:

    def __init__(self):
        with open("./.local/google_genai.json") as f:
            genai_info = json.loads(f.read())
        self.api_key = genai_info["api_key"]
        self.project = genai_info["GOOGLE_CLOUD_PROJECT"]
        self.model = "gemini-2.0-flash"
        self.log_folder = "./llm_service/logs"
        
    def send_prompt(self, prompt: str) -> str:

        client = genai.Client(
            http_options=HttpOptions(api_version="v1",),
            api_key=self.api_key
            )
        response = client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        self.log_prompt(prompt, response)
        return response.text
        

    def log_prompt(self, prompt: str, response: GenerateContentResponse):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        log_filename = f"{self.log_folder}/prompt_{timestamp}.log"
        with open(log_filename, "w") as log_file:
            log_file.write(f"Model: {self.model}\n\n")
            log_file.write(f"Prompt: {prompt}\n\n")
            log_file.write(f"Response: {response.text}\n\n")
            log_file.write(f"Usage metadata: {response.usage_metadata}")

    

if __name__ == "__main__":
    llm = GoogleLLMService()
    llm.send_prompt("Hi")
