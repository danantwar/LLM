import requests

def generateEmbeddings(content, AImodel):
  # API endpoint URL
  embeddingsurl = 'https://api.openai.com/v1/embeddings'
  headers = {
          #'Authorization': "Bearer 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",
          'Authorization': "Bearer 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",
          'Content-Type': 'application/json'
  }
  data =  {
      "input": content,
      "model": AImodel
    }
  
  response = requests.post(embeddingsurl, json=data, headers=headers)
  
  print(response.status_code)

  if response.status_code == 200:
      # Parse the JSON response
      response_json = response.json()
      
      # Extract the embeddings value from the response JSON
      content_embeddings = response_json["data"][0]["embedding"]  
      #print("Embeddings Value:", embeddings_value)
  else:
      content_embeddings = 'null'
      #print("Error:", response.status_code, response.text)

  return content_embeddings

#temp = generateEmbeddings("Fusion", "text-embedding-ada-002")
#print(temp)