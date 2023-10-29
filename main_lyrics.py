from utils_lyrics import lyrics_preprocessing

import torch
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer

song_list=pd.read_csv('D:\spotify_millsongdata.csv')
song_list=lyrics_preprocessing(song_list)

# 감정분석 모델 및 객체 설정
model_name = "j-hartmann/emotion-english-distilroberta-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
trainer = Trainer(model=model)

# 토큰화된 텍스트 데이터를 처리하고 모델에 입력으로 공급
class SimpleDataset:
    def __init__(self, tokenized_texts):
        self.tokenized_texts = tokenized_texts

    def __len__(self):
        return len(self.tokenized_texts["input_ids"])

    def __getitem__(self, idx):
        return {k: v[idx] for k, v in self.tokenized_texts.items()}


pred_texts = song_list.clean_lyrics.to_list()

def lyrics_emotion_classification(pred_texts):
    # Tokenize texts and create prediction data set
    tokenized_texts = tokenizer(pred_texts,truncation=True,padding=True)
    pred_dataset = SimpleDataset(tokenized_texts)

    # Run predictions
    predictions = trainer.predict(pred_dataset)

    # Transform predictions to labels
    preds = predictions.predictions.argmax(-1)
    labels = pd.Series(preds).map(model.config.id2label)
    scores = (np.exp(predictions[0])/np.exp(predictions[0]).sum(-1,keepdims=True)).max(1)

    # scores raw
    temp = (np.exp(predictions[0])/np.exp(predictions[0]).sum(-1,keepdims=True))

    # work in progress
    # container
    anger = []
    disgust = []
    fear = []
    joy = []
    neutral = []
    sadness = []
    surprise = []

    # extract scores (as many entries as exist in pred_texts)
    for i in range(len(pred_texts)):
        anger.append(temp[i][0])
        disgust.append(temp[i][1])
        fear.append(temp[i][2])
        joy.append(temp[i][3])
        neutral.append(temp[i][4])
        sadness.append(temp[i][5])
        surprise.append(temp[i][6])

    # Create DataFrame with texts, predictions, labels, and scores
    df = pd.DataFrame(list(zip(pred_texts,preds,labels,scores,  anger, disgust, fear, joy, neutral, sadness, surprise)),
                      columns=['text','pred','label','score', 'anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise'])

    song=pd.concat([song_list[['artist','song']],df],axis=1)

    return song