print('Loading configurations...')

import os
import torch

from transformers import (AlbertConfig, AlbertTokenizer, AlbertForQuestionAnswering)

MODEL_CLASSES = {'albert': (AlbertConfig, AlbertForQuestionAnswering, AlbertTokenizer)}
SPIECE_UNDERLINE = "▁"

def _truncate_seq_pair(tokens_a, tokens_b, max_length):
   """Truncates a sequence pair in place to the maximum length."""
   # This is a simple heuristic which will always truncate the longer sequence
   # one token at a time. This makes more sense than truncating an equal percent
   # of tokens from each, since if one sequence is very short then each token
   # that's truncated likely contains more information than a longer sequence.

   while True:
      total_length = len(tokens_a) + len(tokens_b)
      if total_length <= max_length:
         break
      if len(tokens_a) > len(tokens_b):
         tokens_a.pop()
      else:
         tokens_b.pop()

class QuestionAnswering(object):
   def __init__(self, config_file, weight_file, tokenizer_file):
      self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
      self.config_class, self.model_class, self.tokenizer_class = MODEL_CLASSES['albert']
      self.config = self.config_class.from_json_file(config_file)
      self.model = self.model_class(self.config)
      self.model.load_state_dict(torch.load(weight_file, map_location=self.device))
      self.tokenizer = self.tokenizer_class(tokenizer_file)

   def to_list(self, tensor):
      return tensor.detach().cpu().tolist()

   def get_answer(self, question, passage):
      self.model.eval()
      with torch.no_grad():
         inputs, attention_mask, tokens = self.convert_examples_to_features(question, passage)
         start_logit, end_logit = self.model(inputs)
         start_idx, end_idx = torch.argmax(start_logit), torch.argmax(end_logit)
         answer = self.convert_tokens_to_string(tokens[start_idx : end_idx + 1])
      return answer

   def convert_tokens_to_string(self, tokens):
      out_string = "".join(tokens).replace(SPIECE_UNDERLINE, " ").strip()
      return out_string
      
   def convert_examples_to_features(self, question, passage, max_seq_length = 384):
      question_tokens = self.tokenizer.tokenize(question)
      context_tokens = self.tokenizer.tokenize(passage)
      _truncate_seq_pair(context_tokens, question_tokens, max_seq_length - 3)

      tokens = []
      tokens.append(self.tokenizer.cls_token)
      for token in question_tokens:
         tokens.append(token)
      tokens.append(self.tokenizer.sep_token)
      for token in context_tokens:
         tokens.append(token)
      tokens.append(self.tokenizer.sep_token)

      input_ids = self.tokenizer.convert_tokens_to_ids(tokens)
      input_mask = [1] * len(input_ids)

      return torch.tensor(input_ids).unsqueeze(0), input_mask, tokens
      #return input_ids, input_mask, tokens

model_dir = './model'
config_file = model_dir + '/config.json'
weight_file = model_dir + '/pytorch_model.bin'
tokenizer_file = model_dir + '/spiece.model'
albert_qa = QuestionAnswering(config_file, weight_file, tokenizer_file)
print('Ready')
