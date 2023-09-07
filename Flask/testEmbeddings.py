
import requests


#def generateEmbeddings(content)
# API endpoint URL
embeddingsurl = 'https://api.openai.com/v1/embeddings'
headers = {
        'Authorization': "Bearer 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",
        'Content-Type': 'application/json'
}
data =  {
    "input": "The food was delicious and the waiter...",
    "model": "gpt-3.5-turbo"
  }


response = requests.post(embeddingsurl, json=data, headers=headers)

#content_embeddings = response.text

print(response.text)
