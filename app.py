import chainlit as cl
from src.llm import Give_answer
from src.prompt import system_instruction
from src.utils import query_collection,add_text_to_collection



messages =[
    {"role": "system", "content" : system_instruction}
]


@cl.on_chat_start
async def on_chat_start():
    
    files =None

    while(files == None):
        files = await cl.AskFileMessage(
            content="Please upload a PDF file to begin !!!",
            accept=["application/pdf"],
            max_size_mb=20,
            timeout=180,
        ).send()

    file = files[0]

    msg = cl.Message(
        content=f"processing `{file.name}`...",
        disable_feedback=True
    )
    await msg.send()

    response = add_text_to_collection(file.path)

    await cl.Message(
        content=response
    ).send()



@cl.on_message
async def main(message: cl.Message):
    try:
        queried_texts = query_collection(query_text=message.content, n=5)
        
     
        queried_string = ' '.join(queried_texts)
        queried_string += f" question: {message.content}"
        
       
        messages.append({"role": "user", "content": queried_string})


        response = Give_answer(messages)
        messages.append({"role": "assistant", "content": response})

        await cl.Message(
            content=response,
        ).send()
    except Exception as e:
        error_message = f"An error occurred: {e}"
        await cl.Message(
            content=error_message,
        ).send()


