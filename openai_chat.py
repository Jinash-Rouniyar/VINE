from openai import OpenAI
import tiktoken
import os

def num_tokens_from_messages(messages, model='gpt-3.5-turbo'):
  """Returns the number of tokens used by a list of messages.
  Copied with minor changes from: https://platform.openai.com/docs/guides/chat/managing-tokens """
  try:
      encoding = tiktoken.encoding_for_model(model)
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens
  except Exception:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
      #See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
      

class OpenAiManager:
    
    def __init__(self):
        self.chat_history = [] # Stores the entire conversation
        try:
            self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        except TypeError:
            exit("Ooops! You forgot to set OPENAI_API_KEY in your environment!")

    # Asks a question with no chat history
    def chat(self, prompt=""):
        if not prompt:
            print("Didn't receive input!")
            return

        # Check that the prompt is under the token context limit
        chat_question = [{"role": "user", "content": prompt}]
        if num_tokens_from_messages(chat_question) > 8000:
            print("The length of this chat question is too large for the GPT model")
            return

        print("[yellow]\nAsking ChatGPT a question...")
        try:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "generate a story of 150 words proper ending where you will generate a story according to the genere that I will provide--{prompt}. Also give the output in 5 different short paragraphs in a senseable way that make the story feel smooth with realizing a paragraph break. Strictly limit the story to max 150 words in total"},
                    {"role": "user", "content": f"Genre: {prompt}"}
                ]
            )
            # Assuming 'completion' is the object that contains the generated text
            print(completion.choices[0].text)  # Adjust according to the actual structure of 'completion'
        except Exception as e:
            print(f"An error occurred: {e}")

    # Asks a question that includes the full conversation history
    def generate_story(self, prompt=""):

        chat_question = [{"role": "user", "content": prompt}]
        if num_tokens_from_messages(chat_question) > 8000:
            print("The length of this chat question is too large for the GPT model")
            return

        print("Asking ChatGPT a question...")
        completion = self.client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=chat_question
        )

        # Process the answer
        openai_answer = completion.choices[0].message.content
        print(f"{openai_answer}\n")
        return openai_answer
   