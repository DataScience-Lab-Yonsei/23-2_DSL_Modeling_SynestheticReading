import os
import pandas as pd
import numpy as np
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 주어진 디렉토리에서 파일을 검색하고 파일 목록을 딕셔너리로 생성(Searching) & 주어진 파일 경로에서 데이터를 가져옴(Importing)
def Searching():
    PATH = 'C:\Users\suyea\Downloads\section-stories-20231015T151746Z-001\section-stories'
    Key_value_dict =  dict()
    Folder_list = os.listdir(PATH)
    for Folder in Folder_list:
        if '.' in Folder:
            pass
        else:
            Key_value_dict[f'\n\n - File list of {Folder}\n'] = 'Dummy'

            for File in os.listdir(PATH + '/' + Folder):
                Key_value_dict[File.split('.')[0]] = PATH + '/' +Folder + '/' + File

    for key in Key_value_dict.keys():
        print(key)
    return Key_value_dict

def Importing(PATH):
    Data = pd.read_csv(PATH, encoding = 'utf-8-sig')
    return Data

#  Transformers 및 Sentence Transformers 라이브러리를 사용하여 동화에서 관련성 높은 요약 출력
def making_summary(title):
    # Load the data using your Importing function
    Dict = Searching()
    data = Importing(Dict[title])

    # Initialize the summarizer
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Load the SentenceTransformer model
    sentence_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    articles = data['text']
    total_article = ''
    article_list = []

    for article in articles:
        # Generate a summary for each article
        summary = summarizer(article, max_length=100, min_length=30, do_sample=False)[0]
        total_article += summary['summary_text']
        article_list.append(title + ' Script : ' + summary['summary_text'])

    # Encode the summaries and total article for similarity
    sentence_embedding = sentence_model.encode(article_list)
    whole_embedding = sentence_model.encode(total_article)

    # Calculate the cosine similarity
    sim_list = cosine_similarity(whole_embedding.reshape(1, 384), sentence_embedding)
    sorted_indices = np.argsort(sim_list[0])[::-1]
    top_index = sorted_indices[0]
    best = article_list[top_index]

    print(f'\nBest for "{title}": {best}')

    return best