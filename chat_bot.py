import dotenv
import os
from openai import OpenAI
dotenv.load_dotenv()


llm = OpenAI(
    api_key=os.getenv('GROQ_API_KEY'),
    base_url='https://api.groq.com/openai/v1'
)

messages = []

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