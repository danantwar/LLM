'''
import os
import openai
openai.organization = "org-i3FhQC7mPvA43Mv2XBt0gDS3"
openai.api_key = "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"
print(openai.Model.list())
'''

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import time
model = SentenceTransformer('BAAI/bge-small-en')
#model = SentenceTransformer('all-MiniLM-L6-v2')


def generateEmbedding(content):
    query_embeds = model.encode([content])
    return query_embeds

def start_encoding():
 content = "This is a test data for encoding it for embedding.This is a test data for encoding it for embedding.This is a test data for encoding it for embedding."
 start_time = time.time()
 result = generateEmbedding(content)
 end_time = time.time()
 # Calculate the execution time
 execution_time = end_time - start_time
 print(f"Execution Time: {execution_time:.6f} seconds") 
 #print(result)
 
start_encoding()