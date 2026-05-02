from crewai import  LLM

class LLMConfig:
    def __init__(self):
        self.mistral_llm = self.init_llm("ollama/mistral")
        #self.llama3_1= self.init_llm("ollama/llama3.1")
        #self.llama3_2 = self.init_llm("ollama/llama3.2:1b")
        #self.embedder = self.init_embedder() # embeddings locaux pour la mémoire

    def init_llm(self,model_name):
        return LLM(
            model=model_name,               # format obligatoire : "ollama/nom_modele"
            base_url="http://localhost:11434",
            temperature=0.2,
            
        )
    
    def init_embedder(self):
        return {                   # embeddings locaux pour la mémoire
            "provider": "ollama",
            "config": {
                "model_name": "nomic-embed-text",
                "base_url": "http://localhost:11434"
            }
        }
