
from openai import OpenAI
from app.repository.llm import  qa_chain

def get_response_from_context(prompt: str )->str:
    try:
        context = get_context_from_query(prompt)
        result=qa_chain({"query":prompt})
        return result["result"]
    except Exception as e:
        raise RuntimeError(e)
        


def get_response_from_openai(prompt: str):
    client = OpenAI()
    model: str = "gpt-3.5-turbo"

        # Make the request to OpenAI
    completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt},
            ],
            max_tokens=60  # Limite de palabras
        )

    response = completion.choices[0].message.content.strip()

   # if response in allowed_responses:
    return response


def get_context_from_query(prompt: str, ):
    client = OpenAI()
    # allowed_responses = ["moneyReceived", "moneyGiven", "moneyBalance", "invalidQuery"]
    model: str = "gpt-3.5-turbo"
        # Make the request to OpenAI
    completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Tu funcion es detectar el contexto de la pregunta. El contexto puede ser una de estas 3 opciones: noticias, tramites y profesores. Solo debes retornar una palabra indicando el contexto, esa palabra debe ser una de las 3 opciones dadas. Si no es posible identificar el contexto, debes retornar la palabra none"},
                {"role": "user", "content": prompt},
            ],
            max_tokens=10  # Limite de palabras
        )

        # Validate and process the response
    response = completion.choices[0].message.content.strip()

   # if response in allowed_responses:
    return response