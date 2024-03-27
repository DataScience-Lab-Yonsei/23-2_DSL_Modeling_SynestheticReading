from utils import making_summary

import torch
from diffusers import StableDiffusionPipeline

best = []

# 동화 목록 중 하나를 Title에 입력
title = 'Snow-man-story'

#  Transformers 및 Sentence Transformers 라이브러리를 사용하여 동화에서 관련성 높은 요약 출력
making_summary(title)

# stable diffusion 목록
Style_Dict = dict(
    Comic = 'ogkalu/Comic-Diffusion',
    Ghibli = 'nitrosocke/Ghibli-Diffusion',
    Cartoon = 'stabilityai/stable-diffusion-2-1',
    Dreamlike = 'dreamlike-art/dreamlike-diffusion-1.0',
    MoDi = 'nitrosocke/mo-di-diffusion',
    Inkpuck = 'Envvi/Inkpunk-Diffusion',
    Double_Exposure = 'joachimsallstrom/Double-Exposure-Diffusion'
)

# 파이프라인 호출 및 이미지 생성
for Style in Style_Dict.keys():
    model_id = Style_Dict[Style]
    pipeline = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype = torch.float16)
    pipe = pipeline.to('cuda')

    prompt = f'{Style} style book cover, Prompt : {best}'
    image = pipe(prompt).images[0]
    image.save(f'{Style}.jpg')
    del pipeline

