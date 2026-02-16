# -*- coding: utf-8 -*-


import numpy as np
from keras_transformer import get_model, decode
np.random.seed(0)

# drive.mount('/content/drive')
#Corpus yoreme
with open("/content/drive/MyDrive/Colab Notebooks/Corpus/Yoreme.txt",mode="r",encoding="utf-8") as f_yor:
    yor = f_yor.read()
#Corpus español
with open("/content/drive/MyDrive/Colab Notebooks/Corpus/Español.txt",mode="r",encoding="utf-8") as f_esp:
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
#print(target_tokens[0])

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

#Se asignan direcciones
source_token_dict = build_token_dict(source_tokens)
target_token_dict = build_token_dict(target_tokens)
target_token_dict_inv = {v:k for k,v in target_token_dict.items()}

print(source_token_dict)
print(target_token_dict)
print(target_token_dict_inv)

# Agregar start, end y pad a cada frase del set de entrenamiento
encoder_tokens = [['<START>'] + tokens + ['<END>'] for tokens in source_tokens]
decoder_tokens = [['<START>'] + tokens + ['<END>'] for tokens in target_tokens]
output_tokens = [tokens + ['<END>'] for tokens in target_tokens]

#Determinar las longitudes maximas de las secuencidas de los tokens de entrada  y de salida
source_max_len = max(map(len, encoder_tokens))
target_max_len = max(map(len, decoder_tokens))

#Rellenar los tokens con PAD para tener la misma longitud
encoder_tokens = [tokens + ['<PAD>']*(source_max_len-len(tokens)) for tokens in encoder_tokens]
decoder_tokens = [tokens + ['<PAD>']*(target_max_len-len(tokens)) for tokens in decoder_tokens]
output_tokens = [tokens + ['<PAD>']*(target_max_len-len(tokens)) for tokens in output_tokens ]

#Se obtinenen una serie de listas que contienen los indices numéricos de los tokens según su corpus
encoder_input = [list(map(lambda x: source_token_dict[x], tokens)) for tokens in encoder_tokens]
decoder_input = [list(map(lambda x: target_token_dict[x], tokens)) for tokens in decoder_tokens]
output_decoded = [list(map(lambda x: [target_token_dict[x]], tokens)) for tokens in output_tokens]

# Crear la red transformer
model = get_model(
    token_num = max(len(source_token_dict),len(target_token_dict)),
    embed_dim = 32,
    encoder_num = 2,
    decoder_num = 2,
    head_num = 4,
    hidden_dim = 128,
    dropout_rate = 0.05,
    use_same_embed = False,
)

model.compile('adam', 'sparse_categorical_crossentropy')

#model.summary()

x = [np.array(encoder_input), np.array(decoder_input)]
y = np.array(output_decoded)

#descomentar lineas para entrenar el modelo
model.fit(x,y, epochs=50000, batch_size=32)
filename = '/content/drive/MyDrive/Colab Notebooks/esp-yor.keras'
model.save(filename)

#Ruta del modelo entrenado
model.load_weights(filename)

def translate(sentence):
  sentence_tokens = [tokens + ['<END>', '<PAD>'] for tokens in [sentence.split(' ')]]
  tr_input = [list(map(lambda x: source_token_dict[x], tokens)) for tokens in sentence_tokens][0]
  decoded = decode(
      model,
      tr_input,
      start_token = target_token_dict['<START>'],
      end_token = target_token_dict['<END>'],
      pad_token = target_token_dict['<PAD>']
  )

  print('Frase original: {}'.format(sentence))
  print('Traducción: {}'.format(' '.join(map(lambda x: target_token_dict_inv[x], decoded[1:-1]))))

translate("Adios")