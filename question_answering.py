import os
import torch

from transformers import (
AlbertConfig,
AlbertTokenizer,
AlbertForQuestionAnswering
)

MODEL_CLASSES = {
   'albert': (AlbertConfig, AlbertForQuestionAnswering, AlbertTokenizer),
}

SPIECE_UNDERLINE = "▁"

class QuestionAnswering(object):
   def __init__(self, config_file, weight_file, tokenizer_file, model_type):
      self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
      self.config_class, self.model_class, self.tokenizer_class = MODEL_CLASSES[model_type]
      self.config = self.config_class.from_json_file(config_file)
      self.model = self.model_class(self.config)
      self.model.load_state_dict(torch.load(weight_file, map_location=self.device))
      self.tokenizer = self.tokenizer_class(tokenizer_file)
      self.model_type = model_type

   def to_list(self, tensor):
      return tensor.detach().cpu().tolist()

   def get_answer(self, question, passage):
      self.model.eval()
      with torch.no_grad():
         inputs, attention_mask, tokens = self.convert_examples_to_features(question, passage)
         if self.model_type == 'albert':
            start_logit, end_logit = self.model(inputs)
            start_idx, end_idx = torch.argmax(start_logit), torch.argmax(end_logit)
            answer = self.albert_convert_tokens_to_string(tokens[start_idx : end_idx + 1])
      return answer

   

   def albert_convert_tokens_to_string(self, tokens):
      """Converts a sequence of tokens (strings for sub-words) in a single string."""
      out_string = "".join(tokens).replace(SPIECE_UNDERLINE, " ").strip()
      return out_string
      
   

   def convert_examples_to_features(self, question, passage, max_seq_length = 384,
         zero_pad=False, include_CLS_token=True, include_SEP_token=True):

      tokens_a = self.tokenizer.tokenize(question)
      tokens_b = self.tokenizer.tokenize(passage)
      if len(tokens_a) > max_seq_length - 2:
          tokens_a = tokens_a[0: 0(max_seq_length - 2)]

      tokens = []
      if include_CLS_token:
         tokens.append(self.tokenizer.cls_token)
      for token in tokens_a:
         tokens.append(token)
      if include_SEP_token:
         tokens.append(self.tokenizer.sep_token)
      for token in tokens_b:
         tokens.append(token)

      input_ids = self.tokenizer.convert_tokens_to_ids(tokens)
      input_mask = [1] * len(input_ids)

      if zero_pad:
         while len(input_ids) < max_seq_length:
            input_ids.append(0)
            input_mask.append(0)

      return torch.tensor(input_ids).unsqueeze(0), input_mask, tokens

model_dir = './model'
config_file = model_dir + '/config.json'
weight_file = model_dir + '/pytorch_model.bin'
tokenizer_file = model_dir + '/spiece.model'
print('Loading albert model...')
albert_qa = QuestionAnswering(config_file, weight_file, tokenizer_file, 'albert')

print('Enter passage:')
passage = input()
print('Enter question:')
question = input()
print('Answer:')
ans = albert_qa.get_answer(question, passage)
print(ans)
