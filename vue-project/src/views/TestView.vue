<template>
  <div> 
    <h1>Test Page</h1>
    <!-- 나중에 지울 코드 -->
    <RouterLink :to="{name:'MovieView'}">Go Movies</RouterLink>

    <!-- chat gpt english level test -->
    <div class="chat-box">
      <!-- 주고 받는 데이터를 실시간(stream)으로 출력 -->
      <div v-for="(message, index) in messages" :key="index" class="message">
        <div v-if="message.role === 'user'">
          <p><strong>{{ username }}</strong> {{ message.content }}</p>
        </div>
        <div v-else>
          <p><strong>Tester:</strong> {{ message.content }}</p>
        </div>
      </div>
    </div>
    <div class="input-box">
      <div>
        <input
        v-model="prompt"
        type="text"
        @keyup.enter="sendMessage"
        />
      </div>
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import axios from "axios"
import { onMounted, ref } from 'vue';
import { useUserStore } from '@/stores/user';
import { useAuthStore } from '@/stores/auth';

const userStore = useUserStore()
const authStore = useAuthStore()
const username = ref('')

// user정보 가져오기
onMounted( async () => {
  if (authStore.token) {
    userStore.getUser()
    username.value = userStore.user.username
    console.log(userStore.user.username, '님, 테스트 예정입니다.')
  }
})




const prompt = ref("");
const messages = ref([]);

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
h1 {
  color: white;
}


/* gpt가 만들어준 스타일 */
.chat-box {
  height: 300px;
  overflow-y: scroll;
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  color : white
}

.message {
  margin-bottom: 10px;
}

.input-box {
  display: flex;
  gap: 10px;
}

input {
  flex: 1;
  padding: 5px;
  border: 1px solid #ccc;
}

button {
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

</style>