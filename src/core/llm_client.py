import requests
from . import config

class LLMClient:
    @staticmethod
    def fetch_models():
        """Fetch available models from Ollama API"""
        try:
            response = requests.get(config.OLLAMA_URL + "tags")
            if response.status_code == 200:
                response_tmp = response.json()
                model_list = [model['name'] for model in response_tmp['models']]
                return [model for model in model_list if "embed" not in model]
            else:
                raise Exception(f"Failed to fetch models: {response.status_code}")
        except Exception as e:
            raise Exception(f"Error fetching models: {str(e)}")

    @staticmethod
    def generate_stream(model, prompt):
        """Generate streaming response from the LLM"""
        try:
            response = requests.post(
                config.OLLAMA_URL + "generate",
                json={"model": model, "prompt": prompt, "keep_alive": "5m", "stream": True},
                stream=True
            )
            
            if response.status_code == 200:
                if response == "":
                    raise Exception(f"No response from the model")
                else:
                    return response
            else:
                raise Exception(f"LLM request failed: {response.status_code}")
        except Exception as e:
            raise Exception(f"Error in LLM request: {str(e)}") 