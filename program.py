#IMPORT REQUIRED LIBRARIES

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from charset_normalizer import detect
import nltk
nltk.download('all')
from nltk.tokenize import sent_tokenize


#DATA EXTRACTION

def extract_text(url):
  """
  Extract text from the given URL
  """
  extracted_text = []
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'lxml')

  title_tag = soup.find('h1', class_= 'entry-title')
  title = title_tag.text.strip()
  extracted_text.append(title + '.')

  main_content_div = soup.find('div', class_ = 'td-post-content tagdiv-type')

  def should_exclude(tag):
    if 'project snapshots' in tag.text.lower():
      return True

  for tag in main_content_div.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']):
    if should_exclude(tag):
      continue
    if tag.text.strip():
      extracted_text.append(tag.text.strip())

  content =  '\n'.join(extracted_text)
  return content

#LOAD THE STOPWORDS FROM ALL .txt FILES

def detect_encoding(file_path):
  """
  Find the encoding of a file
  """
  with open(file_path, 'rb') as f:
      result = detect(f.read())
  return result['encoding']

def load_stopwords(file_paths):
  """
  Load stopwords from all of the .txt files
  """

  stopwords = set()
  for filepath in file_paths:
    encoding = detect_encoding(filepath)
    with open(filepath, 'r', encoding=encoding) as file:
      stopwords.update(word.strip().lower() for word in file if word.strip())
  return stopwords


stopword_files = [
      "StopWords_Auditor.txt",
      "StopWords_Currencies.txt",
      "StopWords_DatesandNumbers.txt",
      "StopWords_Generic.txt",
      "StopWords_GenericLong.txt",
      "StopWords_Geographic.txt",
      "StopWords_Names.txt",
  ]

stopwords = load_stopwords( stopword_files)

#CREATE A DICTIONARY OF POSITIVE AND NEGATIVE WORDS

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

print(dict["positive"])

#VARIOUS FUNCTIONS FOR DATA ANALYSIS

def remove_stopwords(text):
  """
  Remove stopwords from the given text
  """

  words = text.split()
  filtered_words = [word for word in words if word.lower() not in stopwords]
  return ' '.join(filtered_words)

def tokeinize_words(text):
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


#PREPARE THE OUTPUT FILE WITH ALL REQUIRED VARIABLES

result = pd.read_excel('Input.xlsx')
result['Extracted_text'] = result['URL'].apply(extract_text)
result['Clean_Text'] = result["Extracted_text"].apply(remove_stopwords)
result['Tokens'] = result['Clean_Text'].apply(tokeinize_words)
result['POSITIVE SCORE'] = result['Tokens'].apply(compute_positive_score)
result['NEGATIVE SCORE'] = result['Tokens'].apply(compute_negative_score)
result['POLARITY SCORE'] = (result['POSITIVE SCORE'] - result['NEGATIVE SCORE']) / (result['POSITIVE SCORE'] + result['NEGATIVE SCORE'] + 0.000001)
result['WORD COUNT'] = result['Tokens'].apply(compute_word_count)
result['SUBJECTIVITY SCORE'] = (result['POSITIVE SCORE'] + result['NEGATIVE SCORE']) / (result['WORD COUNT'] + 0.000001)
result['NUM_SENTENCES'] = result['Clean_Text'].apply(count_sentences)
result['AVG SENTENCE LENGTH'] = round(result['WORD COUNT'] / result['NUM_SENTENCES'])
result['COMPLEX WORD COUNT'] = result['Tokens'].apply(compute_num_complex_words)
result['PERCENTAGE OF COMPLEX WORDS'] = result['COMPLEX WORD COUNT'] / result['WORD COUNT'] * 100
result['FOG INDEX'] = round(0.4 * (result['AVG SENTENCE LENGTH'] + result['PERCENTAGE OF COMPLEX WORDS']), 4)
result['AVG NUMBER OF WORDS PER SENTENCE'] = result['WORD COUNT'] / result['NUM_SENTENCES']
result['SYLLABLE PER WORD'] = result['Tokens'].apply(get_syllable_count_per_word)
result['PERSONAL PRONOUNS'] = result['Tokens'].apply(get_personal_pronouns)
result['AVG WORD LENGTH'] = result['Tokens'].apply(get_average_word_length)
result['SUBJECTIVITY SCORE'] = (result['POSITIVE SCORE'] + result['NEGATIVE SCORE']) / (result['WORD COUNT'] + 0.000001)
result['NUM_SENTENCES'] = result['Clean_Text'].apply(count_sentences)
result['AVG SENTENCE LENGTH'] = round(result['WORD COUNT'] / result['NUM_SENTENCES'])
result['COMPLEX WORD COUNT'] = result['Tokens'].apply(compute_num_complex_words)
result['PERCENTAGE OF COMPLEX WORDS'] = result['COMPLEX WORD COUNT'] / result['WORD COUNT'] * 100
result['FOG INDEX'] = round(0.4 * (result['AVG SENTENCE LENGTH'] + result['PERCENTAGE OF COMPLEX WORDS']), 4)
result['AVG NUMBER OF WORDS PER SENTENCE'] = result['WORD COUNT'] / result['NUM_SENTENCES']
result['SYLLABLE PER WORD'] = result['Tokens'].apply(get_syllable_count_per_word)
result['PERSONAL PRONOUNS'] = result['Tokens'].apply(get_personal_pronouns)
result['AVG WORD LENGTH'] = result['Tokens'].apply(get_average_word_length)
result = result.drop(['Extracted_text', 'Clean_Text', 'Tokens', 'NUM_SENTENCES'], axis=1)
result.to_excel('Output.xlsx', index=False)
