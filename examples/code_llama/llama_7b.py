from llama_cpp import Llama
import ray
from ray import serve
from fastapi import FastAPI

app = FastAPI()

@serve.deployment(num_replicas=2, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
@serve.ingress(app)
class GenerateCode:
    def __init__(self):
        self.model = Llama(model_path="../ggml-model-q8_0.gguf" )
    
    @app.post("/")    
    def generate(self, text:str) -> str:
        model_output = self.model(text, max_tokens=512)
        return model_output["choices"][0]["text"]

gen_code_app = GenerateCode.bind()