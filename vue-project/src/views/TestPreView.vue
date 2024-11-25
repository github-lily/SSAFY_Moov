<template>
  <div class="texts">
    <p class="welcome">Welcome to</p>
    <h1>MOOV.</h1>
    <p class="contexts">반갑습니다. {{username}} 님! <br> {{username}}님에게 맞는 영화를 추천해드릴게요!</p>
  </div>

  <button class="arrow-button" @click="goToTestView">&#8594;</button>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth'; // 회원가입쪽
import { useUserStore } from '@/stores/user'; // d유저 정보쪽
import { onMounted } from 'vue';
import { ref } from 'vue';


const userStore = useUserStore()
const authStore = useAuthStore()
const router = useRouter()
const username = ref('')

// import { storeToRefs } from 'pinia';
// storeToRefs로 반응형 상태 추출
// const {username} = storeToRefs(store)
// console.log(username.value)

const goToTestView = () => {
  router.push({name: 'TestView'})
}


// 로그인 한 사용자 정보 가져오기
onMounted( async () => {
  if (authStore.token) {
    userStore.getUser()
    username.value = userStore.user.username
    console.log(userStore.user.username, '님, 테스트 예정입니다.')
  }
})

</script>

<style scoped>
.texts {
  color: white;
  height: 100vh;
  padding-left: 80px;
  padding-top: 100px;
}

.welcome {
  font-size: 2vw;
  margin-bottom: 0;
  font-family: 'Krona One';
}

h1 {
  font-size: 6vw;
  margin-bottom: 30px;
  font-family: 'Krona One';
}

.contexts {
  font-size: 2vw;
  font-family: 'NoTo Sans Kr';
  font-weight: 200;
}

.arrow-button {
  position: absolute;
  bottom: 50px;
  right: 50px;
  background-color: transparent;
  font-size: 10vw;
  color: white;
  border: none;
}
</style>