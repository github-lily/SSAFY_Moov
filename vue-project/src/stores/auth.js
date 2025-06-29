import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import router from '@/router'
import { useUserStore } from './user'

export const useAuthStore = defineStore('auth', () => {
  
  const AI_API_KEY = import.meta.env.VITE_OPEN_AI_API_KEY
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)               // 토큰을 받아서 저장할 변수
  const router = useRouter()
  const username = ref('')
  const userStore = useUserStore()
  
  // 로그인 여부 확인
  const isLogin = computed(()=> {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  
  
  // 회원가입 요청 액션
  const signUp = async function(payload) {
    const {username: signUpUsername, password1, password2} = payload
    
    try {
      const res = await axios ({
        method:'post',
        url:`${API_URL}/accounts/signup/`,
        data: {
          username: signUpUsername, password1, password2
        }
    })
    token.value = res.data.key
    username.value = signUpUsername
    await userStore.getUser()
    router.replace({name:'TestPreView'})
    console.log(signUpUsername, '님 회원가입 성공')
  } catch (err) {
    console.log(err)
    }
  }

  
  
  // 로그인 성공하면 token 변수에 토큰을 저장
  const logIn = async function(payload) {
    const {username: loginUsername, password} = payload
    

    try {
      const res = await axios({
        method: 'post', 
        url:`${API_URL}/accounts/login/`,
        data: {
        username: loginUsername, password,
        }
      })
      token.value = res.data.key
      username.value = loginUsername

      //사용자 정보 가져옴
      await userStore.getUser()

      router.push({name: 'MovieView'})
      console.log(loginUsername, '님 로그인 성공')
    } catch (err) {
      console.log(err)
      alert('사용자 정보가 없습니다.')
    }
  }

  // 로그아웃
  const logOut = function() {
    axios({
      method:'post',
      url:`${API_URL}/accounts/logout/`,
      headers : {Authorization:`Token ${token.value}`}
    })
    .then(res=> {
      console.log(res.data)
      token.value = null
      username.value=''
      router.push('/')
      // router.push({name:'LogInView'})
    })
    .catch(err=>console.log(err))
  }

  function setUsername(newUsername) {
    username.value = newUsername
  }
  
  return  { API_URL, signUp, logIn, logOut, token, isLogin, setUsername, username}
},{ persist: true })