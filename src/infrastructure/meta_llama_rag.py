from huggingface_hub import InferenceClient
from domain.i_rag import IRAG

class MetaLLamaRAG(IRAG):
    def __init__(self):
         self.client = InferenceClient(
            model="meta-llama/Llama-3.1-8B-Instruct",
            token="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" 
        )

    def generate_response(self, query: str, context: str) -> str:
        # Construimos el prompt uniendo el contexto recuperado y la pregunta del usuario
        prompt = f"Usando el siguiente contexto, responde la pregunta breve y claramente.\n\nContexto:\n{context}\n\nPregunta: {query}"
        
        # Llama 3.1 Instruct usa formato de chat (roles)
        messages = [{"role": "user", "content": query}, {"role" : "system", "content": f"Responde la pregunta del usuario usando el siguiente contexto como referencia para generar la respuesta : {context} "}]
        
        try:
            # Hacemos la request a la API de Hugging Face
            response = self.client.chat_completion(
                messages,
                max_tokens=300,  # Límite de la respuesta
                temperature=0.5  # Baja temperatura para respuestas más precisas y ceñidas al contexto
            )
            # Extraemos el texto generado de la respuesta
            return response.choices[0].message.content
        except Exception as e:
            return f"Hubo un error al conectar con el modelo: {e}"