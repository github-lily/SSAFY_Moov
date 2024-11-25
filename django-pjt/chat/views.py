# views.py

import os
import openai
from django.conf import settings
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.contrib.auth import get_user_model

# OPENAI_API_KEY = settings.OPENAI_API_KEY
openai.api_key = settings.OPENAI_API_KEY

user = get_user_model()
print(user)

# 기본 설정
PRE_PROMPT = """
# 역할 
- 너는 경력 30년차 국제 공인 영어 실력 분류사야. 
- 사용자의 영어 자기소개를 듣고 사용자의 레벨을 평가해
- 레벨은 총 5단계야 : Beginner/Elementary/Intermediate/Upper-Intermediate/Advanced
- 한국어로 답변해줘
"""

# - 지금부터 을 이용해 사용자의 영어 실력을 평가하고 5단계로 분류할거야.
# - 한국어로 답변해
# - 이전 답변을 기억해뒀다가 최종 평가에 반영해
# - 평가가 끝나면 "당신의 영어 레벨은 []입니다." 형식에 맞게 답변해


def recieve_response(prompt):
    full_prompt = f"{PRE_PROMPT}\n # 사용자 입력: {prompt}\n # 응답:"
    print(full_prompt)  # 디버깅 용도
    # stream = openai.chat.completions.create(
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",  # 원하는 모델 지정
        # stream=True,
        messages=[
            {
                "role": "user", 
                "content": full_prompt
            }
        ],
    )
    # 응답 메시지 추출
    # for chunk in stream:
    #     response_message = chunk.choices[0].delta.content or "", end=""
    #     print(chunk.choices[0].delta.content or "", end="")

    response_message = completion.choices[0].message.content
    print(response_message)
    return response_message

    


@csrf_exempt
@api_view(['POST'])
def stream_chat(request) :
    if request.method == 'POST' :
        data = JSONParser().parse(request)
        prompt = data.get('prompt', None)  # 사용자 입력
        
        # 요청이 빈 값일 경우
        if not prompt :
            return JsonResponse({'response' : '유효한 입력이 필요합니다.'}, status=400)
        
        # 올바른 요청일 경우 응답 생성
        response = recieve_response(prompt)
        return JsonResponse({'response' : response})