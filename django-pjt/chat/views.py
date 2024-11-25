import os
import openai
from django.conf import settings
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

# OPENAI_API_KEY = settings.OPENAI_API_KEY
openai.api_key = settings.OPENAI_API_KEY

# 기본 설정
PRE_PROMPT = """
You are an English language assistant.
You are a nationally certified English proficiency evaluater.
Your job is to assess the user's English proficiency and categorize it into 5 levels
1. Beginner
2. Elementary
3. Intermediate
4. Upper-Intermediate
5. Advanced
Respond conversationally and provide feedback. 
Please write in korean.
you can ask them only five simple questions
"""



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