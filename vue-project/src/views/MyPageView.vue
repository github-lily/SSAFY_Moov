<template>
  <HeaderNav/>
  <div class="container">
    <div class="mypage-container">

      <div class="profile-container">
        <p class="hello">안녕하세요. {{ username }}님!</p>
        <div class="img-box">
          <img src="@/assets/profile.png" alt="프로필 이미지">
        </div>
        <p class="level">{{ username }}님의 level</p>
      </div>
      
      <div class="userinfo">

        <div class="my-favorites components">
          <p class="favorite"> My Favorites</p>
          <div v-if="likemovies.length > 0">
            <MovieList :movies="likemovies" />
          </div>
          <div v-else>
            <p class="no-likes">영화를 찜해보세요!</p>
          </div>

        </div>


        <div class="my-comments components">
          <p class="favorite">My Comments</p>
          <div v-if="commentmovies.length > 0">
            <MovieList :movies="commentmovies"/>
          </div>
          <div v-else>
            <p class="no-comment">댓글을 작성해보세요!</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  
</template>

<script setup>
import HeaderNav from '@/components/common/HeaderNav.vue';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/stores/auth';
// import LikeMovies from '@/components/movie/LikeMovies.vue';
import MovieList from '@/components/movie/MovieList.vue';
import { useUserStore } from '@/stores/user';
import { ref, onMounted } from 'vue';
import axios from 'axios';


const authStore = useAuthStore()
const {username} = storeToRefs(authStore)
console.log(username.value, '님의 마이페이지')

const userStore = useUserStore()

//로그인 사용자가 작성한 댓글들의 전체 영화목록
const commentmovies = ref([])
const likemovies = ref([])

const API_URL = 'http://127.0.0.1:8000';


onMounted(async () => {
  if (username.value) {
    try {
      // 유저 정보 가져오기
      const user = await userStore.getUser();
      console.log('현재 유저 정보:', user); //잘 나옴

      if (user.id) {
        
        // 댓글 단 영화 목록 가져오기
        const commentResponse = await axios({
          method: 'get',
          url: `${API_URL}/api/v1/movies/${username.value}/comments/`,
          headers: {
            Authorization: `Token ${authStore.token}`,
          },
        });
        commentmovies.value = commentResponse.data;
        console.log('사용자가 댓글 단 영화 목록:', commentmovies.value);

        // 좋아요한 영화 목록 가져오기
        const likeResponse = await axios({
          method: 'get',
          url: `${API_URL}/api/v1/mypage/${user.id}/likemovieslist/`,
          headers: {
            Authorization: `Token ${authStore.token}`,
          },
        });
        likemovies.value = likeResponse.data;
        console.log('사용자가 좋아요한 영화 목록:', likemovies.value); // 잘 나옴
      } 
    } catch (error) {
      console.error('데이터 가져오기 실패:', error);
    }
  } 
});


</script>

<style scoped>
.mypage-container {
  width: 100%;
  /* border: 1px solid white; */
  display: flex;
  flex-direction: column;
  margin-top: 50px;
  /* justify-content: center; */
  /* align-items: center; */
}

.profile-container {
  width: 50%;
  height: 100%;
  /* border: 1px solid red; */
  display: flex;
  flex-direction: column;
  align-self: center;
  justify-content: center;
  align-items: center;
}

img {
  width: 100%;
}

.hello {
  font-size:2em;
  font-family: 'Noto Sans KR';
  color: white;
  font-weight: lighter;
}

.img-box {
  width: 300px;
  height: 300px;
  background-color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.level {
  font-size: 1.2em;
  color: white;
  font-family: 'Noto Sans KR';
  font-weight: lighter;
  padding-top: 20px;
  margin-bottom: 0;
}

.useinfo {
  border: 1px solid #ffeb3b;

}
.components {
  margin-top: 50px;
}

.favorite {
  color: white;
  font-size: 2em;
  font-family: 'Krona One';
}

.no-comment, .no-likes {
  font-family: 'Noto Sans KR';
  color: rgb(202, 202, 202);
}
</style>