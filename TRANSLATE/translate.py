from tensorflow import keras
from keras_transformer import decode,get_custom_objects as get_transformer_objects
from config import config 
import tokenizer

custom_objects = get_transformer_objects()

model = keras.models.load_model(
    config.model_path(),
    custom_objects=custom_objects
)

#Se asignan direcciones
source_token_dict = tokenizer.build_esp_token_dict()
target_token_dict = tokenizer.build_yor_token_dict()
target_token_dict_inv = {v:k for k,v in target_token_dict.items()}

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

  translation = ' '.join(map(lambda x: target_token_dict_inv[x], decoded[1:-1]))  

  return translation
  