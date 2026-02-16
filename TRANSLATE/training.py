import numpy as np
from keras_transformer import get_model, decode
from config import config
import tokenizer

np.random.seed(0)

#Se asignan direcciones
source_token_dict = tokenizer.build_esp_token_dict()
target_token_dict = tokenizer.build_yor_token_dict()
target_token_dict_inv = {v:k for k,v in target_token_dict.items()}

# print(source_token_dict)
# print(target_token_dict)
# print(target_token_dict_inv)

# Agregar start, end y pad a cada frase del set de entrenamiento
encoder_tokens = [['<START>'] + tokens + ['<END>'] for tokens in tokenizer.source_tokens]
decoder_tokens = [['<START>'] + tokens + ['<END>'] for tokens in tokenizer.target_tokens]
output_tokens = [tokens + ['<END>'] for tokens in tokenizer.target_tokens]

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
model.fit(x,y, epochs=30, batch_size=32)
model.save(config.model_path())