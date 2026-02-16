from config import config

with open(config.corpus_yor_path(),mode="r",encoding="utf-8") as f_yor:
    yor = f_yor.read()
#Corpus español
with open(config.corpus_esp_path(),mode="r",encoding="utf-8") as f_esp:
    esp = f_esp.read()

    
sentences_yor = yor.split("\n")
sentences_esp = esp.split("\n")

source_tokens = []
for sentence in sentences_esp:
  source_tokens.append(sentence.split(' '))
#print(source_tokens[0])

target_tokens = []
for sentence in sentences_yor:
  target_tokens.append(sentence.split(' '))

def build_esp_token_dict():
    return build_token_dict(source_tokens)

def build_yor_token_dict():
    return build_token_dict(target_tokens)

#Se dividen los tokens en frases especiales
def build_token_dict(token_list):
  token_dict = {
     '<PAD>': 0,
      '<START>': 1,
      '<END>': 2
  }
  for tokens in token_list:
    for token in tokens:
      if token not in token_dict:
        token_dict[token] = len(token_dict)
  return token_dict