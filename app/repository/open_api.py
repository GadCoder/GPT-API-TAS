from openai import OpenAI
from app.repository.llm import qa_chain
from app.core.config import settings
from app.repository.get_info_from_context import get_info_from_context


def get_response_from_context(prompt: str, secret_key: str) -> str:
    if secret_key != settings.SECRET_KEY:
        raise RuntimeError("Invalid secret key")
    try:
        context = get_context_from_query(prompt, secret_key)
        result = qa_chain({"query": prompt})
        return result["result"]
    except Exception as e:
        raise RuntimeError(e)


def get_response_from_openai(prompt: str, secret_key: str):
    if secret_key != settings.SECRET_KEY:
        raise RuntimeError("Invalid secret key")
    context_from_query = get_context_from_query(prompt)
    print(f"Context from query: {context_from_query}")
    if not context_from_query:
        return "No pude entender el contexto a tu pregunta. Por favor, vuelve a intentarlo. Me ayudaría mucho si me indicas qué tipo de información deseas (Noticias, Profesores, Trámites, etc.)"
    info_results = get_info_from_context(context=context_from_query)
    if not info_results:
        return "No pude encontrar información relacionada a tu pregunta. Por favor, vuelve a intentarlo"
    prompt = (
        f"{info_results}\n\n"
        "Based on the above, answer the following question. "
        "If the answer relies on specific information, include its corresponding URL:\n"
        f"{prompt}"
    )
    client = OpenAI()
    model: str = "gpt-3.5-turbo"

    # Make the request to OpenAI
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,  # Limite de palabras
    )

    response = completion.choices[0].message.content.strip()
    return response


def get_context_from_query(prompt: str, model: str = "gpt-3.5-turbo"):
    client = OpenAI()
    allowed_responses = ["News", "Teacher", "Tramites", "invalidQuery"]

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You must interpret the user's request and respond with only one of these four words (News, Teacher, Tramites, invalidQuery). You cannot respond with any other word. Ensure that the response pertains only to the user's query and does not address questions about any other person. If the user's query is unclear or does not match any of the categories, respond with 'invalidQuery'",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=10,  # Limite de palabras
    )

    # Validate and process the response
    context = completion.choices[0].message.content.strip()
    print(context)

    if context in allowed_responses:
        values = {
            "News": "news",
            "Teacher": "teachers",
            "Tramites": "mat",
            "invalidQuery": None,
        }
        return values[context]
    return None
