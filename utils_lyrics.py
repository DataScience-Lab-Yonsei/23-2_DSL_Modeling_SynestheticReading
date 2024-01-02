import pandas as pd
import string
string.punctuation
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')

# csv 형식의 노래 데이터
song_list=pd.read_csv('D:\spotify_millsongdata.csv')

# 영어 텍스트의 전처리 수행과 불용어 처리
def preprocess(text):
  text = text.lower()
  text="".join([i for i in text if i not in string.punctuation])
  text = re.sub(r'\d', '', text)
  text = re.sub(r'\n', ' ', text)
  text = re.sub(r'\s+', ' ', text)
  text = text.strip()
  return text


STOP_WORDS = set(stopwords.words('english'))

NOT_USED_STOP_WORDS = {'more', 'aren', "mightn't", 'doesn', 'isn', "didn't", 'wouldn', "won't", 'ain', 'couldn',
                       "shouldn't", "weren't", 'didn', "hadn't", 'needn', 'shouldn', 'mustn', "mustn't", "wasn't",
                       "couldn't", 'wasn', "hasn't", 'very', 'most', 'hadn', "wouldn't", "don't", "aren't", 'hasn',
                       "needn't", "haven't", 'nor', 'no', 'won', 'not', 'haven', "isn't", 'don', "doesn't"}

ADDITIONAL_STOP_WORDS = {"'s", "'re", "'m", "'ve", "'d", "'ll"}

STOP_WORDS = STOP_WORDS - NOT_USED_STOP_WORDS | ADDITIONAL_STOP_WORDS


# 불용어 제거
def remove_stop_words(text: str) -> str:
    text_without_stop_words = ' '.join([word for word in word_tokenize(text) if word not in STOP_WORDS])
    text_without_stop_words = re.sub(r'\s+\'\s+', ' ', text_without_stop_words)
    return text_without_stop_words

wordnet_lemmatizer = WordNetLemmatizer()

# 텍스트를 표제어로 변환
def lemmatize_text(text: str) -> str:
    return ' '.join([wordnet_lemmatizer.lemmatize(word) for word in word_tokenize(text)])

# 노래 가사에 대한 전처리 시행
def lyrics_preprocessing(song_list):
    song_list['clean_lyrics']=song_list['text'].apply(lambda x:preprocess(x))
    song_list['clean_lyrics']=song_list['clean_lyrics'].apply(lambda x:remove_stop_words(x))
    song_list['clean_lyrics']=song_list['clean_lyrics'].apply(lambda x:lemmatize_text(x))

    song_list=song_list[['artist','song','text','clean_lyrics']]

    return song_list