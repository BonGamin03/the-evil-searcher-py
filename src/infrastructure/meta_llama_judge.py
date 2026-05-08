from huggingface_hub import InferenceClient
from domain.i_judge import IJudge

class MetaLlamaJudge(IJudge):
    def __init__(self, hf_token: str):
         self.client = InferenceClient(
            model="meta-llama/Llama-3.1-8B-Instruct",
            token= hf_token 
        )

    def evaluate_context(self, query: str, context: str) -> str:
        system_prompt = (
            "Eres un evaluador estricto. Tu única tarea es analizar si el contexto dado es suficiente "
            "para responder adecuadamente la pregunta del usuario. "
            "DEBES RESPONDER ÚNICAMENTE CON UNA PALABRA: 'Sí' o 'No'. No añadas signos de puntuación ni texto extra."
        )
        
        user_prompt = f"Contexto:\n{context}\n\nPregunta: {query}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = self.client.chat_completion(
                messages,
                max_tokens=2,      
                temperature=0.01  #Highly deterministic to ensure a clear 'Sí' or 'No' answer
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {e}"