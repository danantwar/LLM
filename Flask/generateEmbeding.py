from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
model = SentenceTransformer('BAAI/bge-small-en')

def generateEmbedding(content):
    query_embeds = model.encode([content])
    return query_embeds

def generatetokens(content):
    # Tokenize the input string
    #print("content is :", content)
    tokens =model.tokenizer.convert_ids_to_tokens(model.tokenize([content]).get('input_ids').flatten().tolist())
    numberoftokens=len(tokens)
    print("aLL tOKEN:", tokens)
    tokens =tokens[1:numberoftokens-1]
    
    # Define the token limit
    token_limit = 150
    # Initialize variables to keep track of chunks and the current chunk
    chunks = []
    current_chunk = []
    substrings =[]
    current_substring = []
    start_idx = 0
    end_idx = token_limit
    
    # Iterate through the tokens
    for token in tokens:
        current_chunk.append(token)
        # if current_substring ==[] and token.startswith ('##'):
        #     print("curent token is", tokens[start_idx+1])
        #     print("previous token is", tokens[start_idx])
        #     tokens[start_idx+1] = tokens[start_idx] + tokens[start_idx+1]
        # If the current chunk exceeds the token limit, start a new chunk
        if len(current_chunk) >= token_limit:
            chunks.append(" ".join(current_chunk))
            substring_tokens = tokens[start_idx:end_idx]
            current_substring.append(model.tokenizer.convert_tokens_to_string(substring_tokens))
            substrings.append(" ".join(current_substring))        
            current_chunk = []
            current_substring = []
            start_idx = end_idx
            end_idx = end_idx + token_limit
            
    # Add the last chunk, if any
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        substring_tokens = tokens[start_idx:numberoftokens-1]
        current_substring.append(model.tokenizer.convert_tokens_to_string(substring_tokens))     
        substrings.append(" ".join(current_substring)) 
        
    return substrings

input_string = """VPN-NA - Application-Server onprem-vpn liogn issue ...
BMC Helix Intelligent Automation Initiated Incident VPN-NA - Application-Server onprem-vpn login issue ...BMC Helix Intelligent Automation Initiated Incident VPN-NA - Application-Server onprem-vpn login issue ...BMC Helix Intelligent Automation Initiated Incident VPN-NA - Application-Server onprem-vpn login issue ...BMC Helix Intelligent Automation Initiated Incident VPN-NA - Application-Server onprem-vpn login issue ...BMC Helix Intelligent Automation Initiated Incident VPN-NA - Application-Server onprem-vpn login issue ...,
None"""

substrings=generatetokens(input_string)
#print(substrings)
for i, substring in enumerate(substrings):
     print(f"Substring {i + 1}:", substring)
    # query_embeds = model.encode(substring)
     #query_embeds = model.encode(chunks)
     #print("Shape of encoded chunks:", query_embeds.shape)
    # print(query_embeds)
