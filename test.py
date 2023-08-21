import openai
openai.organization = "org-i3FhQC7mPvA43Mv2XBt0gDS3"
openai.api_key = "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"
# list models
models = openai.Model.list()

# print the first model's id
#print(models.data[0].id)

# create a chat completion
chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "who is MS Dhoni"}])

# print the chat completion
print(chat_completion.choices[0].message.content)
