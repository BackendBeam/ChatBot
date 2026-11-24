from urllib import response

import dotenv
import os
from openai import OpenAI
dotenv.load_dotenv()


# llm = OpenAI(
#     api_key=os.getenv('GROQ_API_KEY'),
#     base_url='https://api.groq.com/openai/v1'
# )

# messages = [
#      {
#         'role':'system',
#         'content':'''You are a helpful assistant. Your name is GroqBot. 
#         You are a large language model trained by Groq. 
#         You are capable of answering questions and providing information on a wide range of topics. 
#         You are also able to provide code examples and explanations for programming-related questions. 
#         Introdue yourself as GroqBot. 
#         Always Give short and helpful answers. 
#         If you are unsure about an answer, say "I am not sure about that, but I can help you find more information."'''
#      }
# ]


# total_tokens = 0

class ChatBot:
    def __init__(self):
        self.llm = OpenAI(
            api_key=os.getenv('GROQ_API_KEY'),
            base_url='https://api.groq.com/openai/v1'
        )
        self.messages = [
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
        self.total_tokens = 0
        self.input_tokens = 0
        self.output_tokens = 0

    def bot(self, message):
        self.messages.append({
                            'role':'user',
                            'content': message
                        })
        response = self.llm.chat.completions.create(model='openai/gpt-oss-20b',
                                    messages=self.messages)
        response_text = response.choices[0].message.content
        self.messages.append({
                            'role':'assistant',
                            'content': response_text
                        })
        self.input_tokens += response.usage.prompt_tokens
        self.output_tokens += response.usage.completion_tokens
        self.total_tokens += response.usage.total_tokens
        return response_text


    def chat(self):
        while True:
            user_input = input('Ask something(type "q" to terminate):').strip().lower()
        
            if user_input == 'q':
                print('Good luck')
                break
            bot_answer = self.bot(user_input)
            print(bot_answer)

    def report(self):
        for message in self.messages:
            print(message)
            print(f"{message['role']}: {message['content']}")
        print(f'Input tokens: {self.input_tokens}')
        print(f'Output tokens: {self.output_tokens}')
        print(f'Consumed tokens: {self.total_tokens}')
        print(f'Cost: ${(self.input_tokens * 0.01 + self.output_tokens * 0.05)/1000000}')

def main():
    bot = ChatBot()
    bot.chat()
    bot.report()

if __name__ == '__main__':
    main()