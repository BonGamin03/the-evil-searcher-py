from huggingface_hub import InferenceClient
from domain.i_rag import IRAG

class MetaLLamaRAG(IRAG):
    def __init__(self, hf_token: str):
         
         self.client = InferenceClient(
            model="meta-llama/Llama-3.1-8B-Instruct",
            token= hf_token
        )

    def generate_response(self, query: str, context: str) -> str:

        prompt = f"Usando el siguiente contexto, responde la pregunta breve y claramente.\n\nContexto:\n{context}\n\nPregunta: {query}"
        
        messages = [{"role": "user", "content": query}, {"role" : "system", "content": f"Responde la pregunta del usuario usando el siguiente contexto como referencia para generar la respuesta : {context} "}]
        
        try:

            response = self.client.chat_completion(
                messages,
                max_tokens=300,  
                temperature=0.3 #Midly creative to allow for more natural responses while still being relevant to the context
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Hubo un error al conectar con el modelo: {e}"