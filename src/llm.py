from openai import OpenAI


client = OpenAI()

def Give_answer(message, model="gpt-3.5-turbo", temperature=1, max_tokens=1500, top_p=0.95, presence_penalty=0.6, frequency_penalty=0):
    response = client.chat.completions.create(
        model=model,
        messages=message,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
    )
    
    return response.choices[0].message.content