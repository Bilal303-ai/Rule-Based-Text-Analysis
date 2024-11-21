#IMPORT REQUIRED LIBRARIES

import requests
from bs4 import BeautifulSoup
import pandas as pd
from charset_normalizer import detect
import nltk
nltk.download('all')
from nltk.tokenize import sent_tokenize
import gradio as gr



def detect_encoding(file_path):
  """
  Find the encoding of a file
  """
  with open(file_path, 'rb') as f:
      result = detect(f.read())
  return result['encoding']

def load_stopwords(file_paths):
  """
  Load stopwords from stopwords-en.txt file
  """

  stopwords = set()
  for filepath in file_paths:
    encoding = detect_encoding(filepath)
    with open(filepath, 'r', encoding=encoding) as file:
      stopwords.update(word.strip().lower() for word in file if word.strip())
  return stopwords


stopword_files = [
  'stopwords-en.txt'
  ]

stopwords = load_stopwords(stopword_files)


def create_dict(positive_words_filepath, negative_words_filepath):
  """
  Create a dictionary of positive and negative words
  """

  dict = {}
  positive_words_set = set()
  negative_words_set = set()
  encoding_of_pos_file = detect_encoding( positive_words_filepath)
  encoding_of_neg_file = detect_encoding( negative_words_filepath)
  with open(positive_words_filepath, 'r', encoding=encoding_of_pos_file) as pos_file:
    positive_words_set.update(word.strip().lower() for word in pos_file if word.lower() not in stopwords)

  with open(negative_words_filepath, 'r', encoding=encoding_of_neg_file) as neg_file:
    negative_words_set.update(word.strip().lower() for word in neg_file if word.lower() not in stopwords)

  dict["positive"] = positive_words_set
  dict["negative"] = negative_words_set
  return dict

dict = create_dict("positive-words.txt", "negative-words.txt")


#VARIOUS FUNCTIONS FOR DATA ANALYSIS

def remove_stopwords(text):
  """
  Remove stopwords from the given text
  """

  words = text.split()
  filtered_words = [word for word in words if word.lower() not in stopwords]
  return ' '.join(filtered_words)

def tokenize_words(text):
  """
  Tokenize the given text
  """

  tokens = nltk.word_tokenize(text)
  return tokens



def count_sentences(text):
  """
  Calculate the number of sentences in the text
  """
  sentences = sent_tokenize(text)
  return len(sentences)

def compute_positive_score(tokens):
  """
  Compute the positive score
  """
  words = [token for token in tokens if token.isalpha()]
  positive_score = 0
  for word in words:
    if word.lower() in dict["positive"]:
      positive_score += 1
  return positive_score

def compute_negative_score(tokens):
  """
  Compute the negative score
  """
  words = [token for token in tokens if token.isalpha()]
  negative_score = 0
  for word in words:
    if word.lower() in dict["negative"]:
      negative_score -= 1
  negative_score = -1 * negative_score
  return negative_score

def compute_word_count(tokens):
  """
  Compute the word count
  """
  words = [token for token in tokens if token.isalpha()]
  return len(words)

def compute_num_complex_words(tokens):
  """
  Compute the number of complex words
  """
  complex_word_count = 0
  words = [token for token in tokens if token.isalpha()]
  for word in words:
    if word.endswith('es') or word.endswith('ed'):
      word = word[0: -2]
      vowels = 'aeiou'
      count = 0
      for char in word:
        if char.lower() in vowels:
          count += 1
      if count > 2:
        complex_word_count += 1

    else:
      vowels = 'aeiou'
      count = 0
      for char in word:
        if char.lower() in vowels:
          count += 1
      if count > 2:
        complex_word_count += 1
  return complex_word_count

def get_syllable_count_per_word(tokens):
  """
  Compute the average syllable count per word
  """
  syllable_count = []
  words = [token for token in tokens if token.isalpha()]
  for word in words:
    if word.endswith('es') or word.endswith('ed'):
      word = word[0: -2]
      vowels = 'aeiou'
      count = 0
      for char in word:
        if char.lower() in vowels:
          count += 1

      syllable_count.append(count)

    else:
      vowels = 'aeiou'
      count = 0
      for char in word:
        if char.lower() in vowels:
          count += 1

      syllable_count.append(count)

  return round(sum(syllable_count) / len(syllable_count))

def get_personal_pronouns(tokens):
  """
  Find the count of personal pronouns
  """
  words = [token for token in tokens if token.isalpha()]
  personal_pronouns = ['i', 'we', 'my', 'ours', 'us']

  count = 0
  for word in words:
    if word.lower() in personal_pronouns:
      count += 1
  return count

def get_average_word_length(tokens):
  """
  Compute the average word length
  """
  total_length = 0
  words = [token for token in tokens if token.isalpha()]
  for word in words:
    total_length += len(word)
  average_word_length = total_length / len(words)
  return round(average_word_length)




def analyze(input_text):
  clean_text = remove_stopwords(input_text)
  tokens = tokeinize_words(clean_text)
  word_count = compute_word_count(tokens)
  sentence_count = (count_sentences(clean_text))
  average_sentence_length = round(word_count / sentence_count)
  complex_word_count = compute_num_complex_words(tokens)
  percentage_of_complex_words = round((Complex_word_count / word_count) * 100, 2)
  average_word_length = round(get_average_word_length(tokens))
  positive_score = compute_positive_score(tokens)
  negative_score = compute_negative_score(tokens)
  polarity_score = round((positive_score - negative_score) / (positive_score - negative_score + 0.000001), 2)
  subjectivity_score = round((positive_score + negative_score) / (word_count + 0.000001), 2)
  fog_index = round(0.4 * (average_sentence_length + percentage_of_complex_words), 2)
  return word_count, sentence_count, average_sentence_length, complex_word_count, percentage_of_complex_words, average_word_length, positive_score, negative_score, subjectivity_score, fog_index

gradio_app = gr.Interface(
  analyze,
  inputs = gr.Textbox(label='Text'),
  outputs = [gr.Textbox(label='Num of words'), gr.Textbox(label='Number of Sentences'), gr.Textbox(label='Average sentence length'), gr.Textbox(label='Num of complex words'), gr.Textbox(label='Percentage of complex words'),  gr.Textbox(label='Average word length'), gr.Textbox(label='Positive score'), gr.Textbox(label='Negative score'), gr.Textbox(label='Subjectivity score'), gr.Textbox(label='Fog index')],
  title="Text Analysis",
)

if __name__ == "__main__":
    gradio_app.launch(debug=True)
