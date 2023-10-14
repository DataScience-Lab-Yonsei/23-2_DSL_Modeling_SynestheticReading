# 23-2_DSL_Modeling_Synesthetic_Reading
---
## 주제
- 동화 줄거리, 컨셉에 맞는 책 표지 이미지 제작
- 해당 줄거리, 컨셉에 맞는 음악 추천
## Team DSL 남승우 권수연 유현동 임세민
---
# Overview
[발표자료](https://github.com/smnii13/SynestheticReading_TeamD/blob/main/Team_DSL_%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C.pdf)
## 1. Overall Pipeline

![image](https://github.com/smnii13/SynestheticReading_TeamD/assets/121654185/1e7df008-7b88-46a0-81ce-db2ea6a28d75)


## 2. Model
### Story to Cover Image 
![image](https://github.com/smnii13/SynestheticReading_TeamD/assets/121654185/17dbfb15-8197-4e1b-977c-ff9fce18942f)
  
  
  Text summarization & promt generation
- Bart-Large-CNN 모델 활용 Sector 별 줄거리 요약, 임베딩 생성
- 요약된 줄거리 취합해 전체 요약 문장, 임베딩 생성
- 전체 요약 문장 - Sector 벼로 줄거리 임베딩 간 유사도 분석
- 가장 높은 유사도를 가진 줄거리를 prompt로 선정


![image](https://github.com/smnii13/SynestheticReading_TeamD/assets/121654185/b79553f9-2c8d-4cd8-8ace-8cd809c7c7fb)

![image](https://github.com/smnii13/SynestheticReading_TeamD/assets/121654185/39ba8622-d04d-4aa1-84eb-10ff21576c72)
  
    
  
  Diffusion
- 생성된 프롬트 기반으로 여러 Diffusion model 활용해 줄거리에 맞는 책 표지 이미지 생성

### Story to Music
  
![image](https://github.com/smnii13/SynestheticReading_TeamD/assets/121654185/2fa8b421-4ebe-4cbc-a1fb-548b74ba4a0d)

  
  Emotion Classification
- Ekman's 6 basic feelings: anger, disgust, fear, joy, sadness, surprise + neural 기반으로 동화 및 노래 가사 감정 분석하고자 함
- RoBERTa 활용 Spotify MillSong data 의 가사 / Section fairy tales 의 section story text 감정 분류, emotion vector 생성
- Story emotion vector vs Music emotion vector 유클리디안 거리 기반으로 유사도 측정





## 3. Dataset
- Section-Fairy tales
  - 287 row / 안데르슨, 이솝 우화 등 다양한 동화의 전문 text data
  - 챕터 별로 분류되어 있어 이미지 생성 단계에서는 합쳐서, 감정 분석 시에는 개별로 사용
- Spotify-Milsong data
  - 56870 row / 가수, 곡명, 가사, 링크로 분류되어 있음


# Result
## 1. Final Output
![image](https://github.com/smnii13/SynestheticReading_TeamD/assets/121654185/5713c03e-4e04-40ba-9c6e-9a8bb13563c9)

![image](https://github.com/smnii13/SynestheticReading_TeamD/assets/121654185/1d813e2a-b28c-4d50-be88-fa5bfb1747a2)


## 2. Limitations and Future works
Book to Cover Image...
- 책 표지에 글자가 삽입되는 경우, 무작위로 나열된 알파벳이 삽입되었던 경우가 많고, 알파벡조차 왜곡된 형태를 가지고 있었음.
- 책 표지에 인물이 등장하는 경우, 생성 모델 특성상 손가락이 6개가 있는 등 인물의 신테가 왜곡된 경우가 있었음.

  
Book to Music...
- Section 별로 측정된 감정의 평균을 감정 지표로 사용했기 때문에 Section 마다 변화하는 감정선을 고려하지 못함.
- 가사를 분석하여 동화와 매칭하다보니 노래 자체의 분위기는 고려하지 못한 경우가 존재함.


# End-to-End
(optional, 가능하다면 코드를 다시 실행해볼 수 있도록 코드 블럭을 활용하여 완성해주시면 좋을 것 같습니다.)
(ex)

```ruby
python run.py --config configs.txt
```

# File description
- main (실제 구동하는 파일)
  - ```main.py```  
- model (모델 내부 구조 파일)
  - ```encoder.py```
  - ```decoder.py```
- data (사용한 데이터 or 데이터 생성 파일)
(예시입니다! 각 팀의 프로젝트 파일 구조에 따라 자유롭게 완성해주세요)
