import dotenv
import os
from openai import OpenAI
dotenv.load_dotenv()


llm = OpenAI(
    api_key=os.getenv('GROQ_API_KEY'),
    base_url='https://api.groq.com/openai/v1'
)

messages = [
     {
        'role':'system',
        'content':'''You are a helpful assistant. Your name is GroqBot. 
        You are a large language model trained by Groq. 
        You are capable of answering questions and providing information on a wide range of topics. 
        You are also able to provide code examples and explanations for programming-related questions. 
        Introdue yourself as GroqBot. 
        Always Give short and helpful answers. 
        If you are unsure about an answer, say "I am not sure about that, but I can help you find more information."'''
     }
]

def bot(message):
    messages.append({
                        'role':'user',
                        'content': message
                    })
    response = llm.chat.completions.create(model='openai/gpt-oss-20b',
                                messages=messages)
    response_text = response.choices[0].message.content
    messages.append({
                        'role':'assistant',
                        'content': response_text
                    })
    return response_text

def chat():
    while True:
           user_input = input('Ask something(type "q" to terminate):').strip().lower()
    
           if user_input == 'q':
               print('Good luck')
               break
           bot_answer = bot(user_input)
           print(bot_answer)

def main():
    chat()

if __name__ == '__main__':
    main()