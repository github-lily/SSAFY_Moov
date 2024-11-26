<template>
   

      <!-- 홈으로 -->

      <div class="home sticky-top" @click="goToHome" >
        <h1 class=" moovtext ">MOOV</h1>
      </div>
      <div class="chat-box test-list">
        <!-- 메세지 창 -->
          <div v-for="(message, index) in messages" :key="index" class="message">
            <div v-if="message.role === 'user'" class="user-message">
              <p class="you fo">{{ username }}</p>
              <p class="yourcomment comment fo">{{ message.content }}</p>
            </div>
            <div v-else>
              <p class="moov ">MOOV</p>
              <p class="Englishcomment comment fo">{{ message.content }}</p>
            </div>
          </div>
          <!-- 입력 하는 곳-->
          <div class="input-box">
            
            <div class="input-container">
              <input
              v-model="prompt"
              type="text"
              @keyup.enter="sendMessage"
              placeholder="입력해주세요."
              />
              <button @click="sendMessage" class="send-button"><i class="fa-solid fa-paper-plane"></i></button>
              <button @click="clearMessages" class="clear-button"><i class="fa-solid fa-reply"></i></button>
            </div>
            
          </div>
        </div>
   
  
</template>

<script setup>
import { RouterLink } from 'vue-router';
import axios from "axios"
import { onMounted, ref } from 'vue';
import { useUserStore } from '@/stores/user';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';


const userStore = useUserStore()
const authStore = useAuthStore()
const username = ref('')
const user_id = ref('')
const router = useRouter()

// user정보 가져오기
onMounted(async () => {
  if (authStore.token) {
    try {
      const User = await userStore.getUser(); // 비동기 호출 대기
      username.value = User.username;
      user_id.value = User.pk;
      console.log(User.username, '님, 테스트 시작합니다.'); // username 출력
    } catch (error) {
      console.error('사용자 정보를 가져오는 데 실패했습니다:', error);
    }
  }
});


const goToHome = () => {
  router.push({name:'MovieView'})
} 


const prompt = ref("");
const messages = ref([]);
const user_level = ref("")
const level_list = ['Beginner','Elementary','Intermediate','Upper-Intermediate','Advanced']


// 메시지 주고받기
const sendMessage = async () => {
  if (!prompt.value.trim) return;

  messages.value.push({ role: "user", content: prompt.value });

  try {
    const config={
      url: "http://127.0.0.1:8000/chat/",
      method: 'post',
      headers: {
            Authorization: `Token ${authStore.token}`,
      },
      data: {
        user_id : user_id.value,
        prompt : prompt.value, // 사용자 입력      
      }
    }
    const response = await axios(config)
    // const response = await axios.post("http://127.0.0.1:8000/chat/", data={
    //   user_id : user_id.value,
    //   prompt : prompt.value, // 사용자 입력      
    // }, headers={
    //         Authorization: `Token ${authStore.token}`,
    //       });

    // 챗봇 응답
    const chatbotResponse = response.data.response;

    // 챗봇 응답 추가
    messages.value.push({ role: "assistant", content: chatbotResponse });

    // 응답에서 레벨 확인 및 저장
    
    level_list.forEach((level) => {
      if (chatbotResponse.includes(level)) {
        user_level.value = level;
        updateUserLevel(level); // 사용자 레벨 정보 업데이트 함수 호출
      }
    });


  } catch (error) {
    console.error("Error sending message:", error);
    messages.value.push({
      role: "assistant",
      content: "죄송합니다. 요청 처리 중 문제가 발생했습니다. 잠시후 다시 시도해주세요.",
    });
  }

  prompt.value = ""; // 입력 필드 초기화
};


// 메시지 초기화
const clearMessages = async () => {
  try {
    const config={
      url: "http://127.0.0.1:8000/chat/",
      method: 'post',
      headers: {
            Authorization: `Token ${authStore.token}`,
      },
      data: {
        user_id : user_id.value,
        clear:true,
      }
    }
    const response = await axios(config)
    messages.value = []; // 로컬 메시지 초기화
    console.log(response.data.response); // "대화가 초기화되었습니다."
  } catch (error) {
    console.error("Error clearing messages:", error);
  }
};

// 사용자 레벨 업데이트 함수
const updateUserLevel = async (level) => {
  try {
    const config={
      url: "http://127.0.0.1:8000/chat/",
      method: 'post',
      headers: {
            Authorization: `Token ${authStore.token}`,
      },
      data: {
        level:level
      }
    }
    const ans = await axios(config)
    console.log("사용자 레벨이 업데이트되었습니다:", level);
  } catch (error) {
    console.error("사용자 레벨 업데이트 중 오류가 발생했습니다:", error);
  }
};

</script>

<style scoped>
.moovtext:hover {
  cursor: pointer;
  font-size: 150%;;
}
.moovtext {
  color: white;
  text-align: center;
  font-family: 'Krona One';
  margin: 100px 0;
} 
.chat-container {
  width: 100%;
  max-width: 100%;
  padding: 20%;
  max-height: 80%;
  position: relative;
}

.chat-box {
  margin-top: 50px;
  margin-bottom: 100px;
  height: calc(100vh - 150px); /* 채팅 영역 크기 */
  /* overflow-y: auto; */
  padding: 10px 20%;
  color: white;
}

.fo {
  font-family: 'Noto Sans KR';
  /* font-weight: light; */
}
.message {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
}

.message div {
  max-width: 80%;
  align-self: flex-start; /* 기본값은 왼쪽 정렬 */
}

.message div.user-message {
  align-self: flex-end; /* 사용자 메시지는 오른쪽 정렬 */
}

.moov {
  margin-bottom: 10px;
  font-family: 'Krona One';

}
.you, .yourcomment {
  text-align: right;
}

.English {
  text-align: left;
}

.yourcomment {
  background-color: #ffeb3b ; 
  color: rgb(68, 68, 68);
  border-radius: 10px;
  padding: 10px;
  align-self: flex-end;
}

.Englishcomment {
  background-color: #f1f0f0;
  color: black;
  border-radius: 10px;
  padding: 10px;
  align-self: flex-start;
}

/* 채팅 쪽 */
.input-box {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.input-container {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
}

input {
  flex-grow: 1;
  width: calc(100% - 60px); /* 버튼 크기만큼 줄임 */
  padding: 10px 20px;
  border-radius: 20px;
  border: 1px solid #ccc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.send-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: background-color 0.3s;
}

.send-button:hover {
  background-color: #0056b3;
}

.clear-button {
  background-color: #ffeb3b;
  color: #4b4b4b;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: background-color 0.3s;
}

.clear-button:hover {
  background-color: #c0ad00;
  color: #ffffff;
}

</style>