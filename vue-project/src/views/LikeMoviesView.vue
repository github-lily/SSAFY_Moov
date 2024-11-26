<template>
  <div>
    <HeaderNav />
    <div class="container">
      <div class="my-favorites components">
            <p class="favorite"> My Favorites</p>
            <div v-if="likemovies.length > 0">
              <MovieList :movies="likemovies" />
            </div>
            <div v-else>
              <p class="no-likes">영화를 찜해보세요!</p>
            </div>

          </div>
      </div>
  </div>
</template>

<script setup>
import HeaderNav from '@/components/common/HeaderNav.vue';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/stores/auth';
import MovieList from '@/components/movie/MovieList.vue';
import { useUserStore } from '@/stores/user';
import { ref, onMounted } from 'vue';
import axios from 'axios';


const authStore = useAuthStore()
const {username} = storeToRefs(authStore)

const userStore = useUserStore()
const likemovies = ref([])

const API_URL = 'http://127.0.0.1:8000';


onMounted(async () => {
  if (username.value) {
    try {
      // 유저 정보 가져오기
      const user = await userStore.getUser();

      if (user.id) {
        const likeResponse = await axios({
          method: 'get',
          url: `${API_URL}/api/v1/mypage/${user.id}/likemovieslist/`,
          headers: {
            Authorization: `Token ${authStore.token}`,
          },
        });
        likemovies.value = likeResponse.data;
      } 
    } catch (error) {
      console.error('데이터 가져오기 실패:', error);
    }
  } 
});


</script>

<style scoped>
.my-favorites {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
}

.favorite{
  font-family: 'Krona One';
  font-size: 2em;
}

.no-likes{
  font-family: 'Noto Sans KR';
  font-weight: lighter;
}
</style>