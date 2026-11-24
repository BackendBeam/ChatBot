from urllib import response
import time
import dotenv
import os
import tiktoken
from openai import OpenAI
from transformers import AutoTokenizer
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
                                    messages=self.messages,
                                    stream = True)
        # response_text = response.choices[0].message.content
        # self.messages.append({
        #                     'role':'assistant',
        #                     'content': response_text
        #                 })
        # self.input_tokens += response.usage.prompt_tokens
        # self.output_tokens += response.usage.completion_tokens
        # self.total_tokens += response.usage.total_tokens

        response_text = ''
        for chunk in response:
            if chunk.choices:
                delta = chunk.choices[0].delta.content
                if delta:
                    print(delta, end='', flush=True)
                    response_text += delta
                    time.sleep(0.05)  # Adjust the sleep time as needed for a smoother streaming effect
            if chunk.usage:
                self.input_tokens += chunk.usage.prompt_tokens
                self.output_tokens += chunk.usage.completion_tokens
                self.total_tokens += chunk.usage.total_tokens

        print()  # Print a newline after the response is complete
        self.messages.append({
                            'role':'assistant',
                            'content': response_text
                        })    
        return response_text


    def chat(self):
        #encoding = tiktoken.get_encoding('cl100k_base')
        encoding = AutoTokenizer.from_pretrained("gpt2")
        #encoding = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
        while True:
            user_input = input('Ask something(type "q" to terminate):').strip().lower()
            
            if user_input == 'q':
                print('Good luck')
                break

            token_count = len(encoding.encode(user_input))
            print(f'Your input has {token_count} tokens.')
            
            if token_count > 10:
                print(f'Your input is too long. It has {token_count} tokens, but the limit is 10 tokens. Try a shorter one, please.')
                continue

            if self.total_tokens > 1000:
                print(f'You have exceeded the total token limit. You have used {self.total_tokens} tokens. Please start a new session.')
                break
            self.bot(user_input)
            

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