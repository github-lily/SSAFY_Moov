# views.py

import os
import openai
from django.conf import settings
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

# OPENAI_API_KEY = settings.OPENAI_API_KEY
openai.api_key = settings.OPENAI_API_KEY

User = get_user_model()

# 대화 히스토리 유지를 위한 딕셔너리
CHAT_HISTORY = {}

# 기본 설정
PRE_PROMPT = """
# 역할 
- 한국어로 이야기한다.
- 너는 경력 30년차 국제 공인 영어 실력 분류사다.
- 지금부터 간단한 질의응답을 통해 사용자의 영어 실력을 평가하고 5단계로 분류한다.
- 레벨은 총 5단계 : Beginner/Elementary/Intermediate/Upper-Intermediate/Advanced
- 질문은 5개만 할 수 있다
- 평가가 끝나면 "당신의 영어 레벨은 []입니다." 형식에 맞게 답변한다.
"""



# OPEN AI API 호출
def get_completion(messages):
    try :
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",  # 원하는 모델 지정
            messages=messages,
        )
        response_message = completion.choices[0].message.content
        return response_message
    # 일반 예외 처리
    except Exception as e  :
        print(f"Open API Error : {e}")
        raise e     # 필요시 예외를 다시 던짐



@csrf_exempt
@api_view(['POST'])
def stream_chat(request) :
    print(request.user) 
    if request.method == 'POST' :
        try :
            data = JSONParser().parse(request)
            print(f"Received data: {data}")  # 요청 데이터 디버깅
        except Exception as e:
            print(f"JSON Parse Error: {e}")
            return JsonResponse({'response': 'Invalid JSON format.'}, status=400)

        user_id = data.get('user_id', 'default')
        prompt = data.get('prompt', None)
        clear = data.get('clear', False)
        
        # 대화 초기화(히스토리까지)
        if clear:
            CHAT_HISTORY.pop(user_id, None)
            return JsonResponse({'response': '대화가 초기화되었습니다.'})
    

        # 요청이 빈 값일 경우
        if not prompt :
            return JsonResponse({'response' : '유효한 입력이 필요합니다.'}, status=400)
        


        if user_id not in CHAT_HISTORY:
            CHAT_HISTORY[user_id] = [{"role": "system", "content": PRE_PROMPT}]

        CHAT_HISTORY[user_id].append({"role": "user", "content": prompt})

        try:
            response_message = get_completion(CHAT_HISTORY[user_id])
            CHAT_HISTORY[user_id].append({"role": "assistant", "content": response_message})
            print(response_message)


            # 레벨 정보가 포함되어 있는지 검사
            level_list = ['Beginner','Elementary','Intermediate','Upper-Intermediate','Advanced']
            for level in level_list:
                if level in response_message:
                    user = User.objects.get(pk=request.user.id)
                    print(request.user)
                    user.level = level
                    user.save()
                    print(f"User {user_id}'s level updated to: {level}")
            

        except Exception as e:
            # print(f"OpenAI API Error: {e}")
            print(e)
            return JsonResponse({'response': 'OpenAI API 요청 중 문제가 발생했습니다.'}, status=500)

        return JsonResponse({'response': response_message})
