<template>
  <div> 

      <div class="chat-box test-list" >
        <div class="home" @click="goToHome" >
        <!-- <i class="fa-solid fa-house"></i> -->
         <h1 class="home">MOOV</h1>
        </div>

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

      </div>
      <!-- 입력 박스는 그대로 유지 -->
      <div class="input-box">

        <div class="input-container">
          <input
            v-model="prompt"
            type="text"
            @keyup.enter="sendMessage"
            placeholder="입력해주세요."
            />
            <button @click="sendMessage" class="send-button">
              <i class="fa-solid fa-paper-plane"></i>
            </button>
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
const router = useRouter()

// user정보 가져오기
onMounted( async () => {
  if (authStore.token) {
    userStore.getUser()
    username.value = userStore.user.username
    console.log(userStore.user.username, '님, 테스트 시작합니다.')
  }
})

const goToHome = () => {
  router.push({name:'MovieView'})
} 


const prompt = ref("");
const messages = ref([]);
const user_level = ref("")
const level_list = ['Beginner','Elementary','Intermediate','Upper-Intermediate','Advanced']

const sendMessage = async () => {
  if (!prompt.value.trim) return;

  messages.value.push({ role: "user", content: prompt.value });

  try {
    const response = await axios.post("http://127.0.0.1:8000/chat/", {
      prompt : prompt.value, // 사용자 입력
    }, {
      headers : {
        "Content-Type" : "application/json", // Json 데이터로 전송
      }
    })

    const chatResponse = response.data.response;
    // for (level of level_list) {
    //   if (level.exist(chatResponse)) {
    //   user_level.value = level
    //   } return level
    // }

    messages.value.push({ role : "assistant", content : chatResponse})
  } catch (error) {
    console.error("Error sending message:", error)
    messages.value.push({
      role : "assistant",
      content: "요청 처리에 문제가 발생했습니다. 다시 시도해주세요."
    })
  }
  
  prompt.value = ""
}

</script>

<style scoped>
.home:hover {
  cursor: pointer;
  font-size: 150%;;
  }
.home {
  text-align: center;
  font-family: 'Krona One';
  margin: 20px 0;
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
  position: fixed;
  bottom: 0;
  left: 0;
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
  margin-bottom: 50px;
  max-width: 1000px;
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

.send-button i {
  font-size: 18px;
}
</style>