<!-- MovieListItem.vue -->

<template>
  <div class="movie-card">
    <div class="poster-container">

      <img class="poster" :src="poster" alt="영화포스터" >
      
      <!-- 마우스를 올릴 경우 -->
      <div class="overlay">

        <div class="movie-info" @click="goToDetail(movie)">
          <h3 class="movie-title">{{ movie.title }}</h3>
          <p class="overview">{{ truncateOverview(movie.overview) }}</p>

            <button @click.stop="toggleLikeMovie(movie.id)"
              class="likebtn" 
              :class="{ 'heart' : isLiked }" 
              >
              &#x2665;
            </button>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { ref, watch, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useMovieStore } from '@/stores/movie';

const router = useRouter()
const props = defineProps({
  movie:Object
})

const movieStore = useMovieStore()
// const toggleLikeMovie = movieStore.toggleLikeMovie

const isLiked = ref(props.movie.user_like_movies)
// const isLiked = computed(() => props.movie.user_like_movies);

const toggleLikeMovie = async (movieId) => {
  const result = await movieStore.toggleLikeMovie(movieId);
  isLiked.value = result.is_liked;
};

watch(() => props.movie.user_like_movies, (newValue) => {
  isLiked.value = newValue;
}, { immediate: true });

// 포스터 이미지 URL 설정
const poster = `https://image.tmdb.org/t/p/w500/${props.movie.poster_path}`

const truncateOverview = (text) => {
  if (!text || text.length === 0) {
    return '정보가 없습니다.'; 
  }
  if (text.length > 150) {
    return text.slice(0, 150) + '...';
  }
  return text;
}

// 영화 클릭 시 DetailView로 이동
const goToDetail = (movie) => {
  console.log('movie.id는 뭐냐면',props.movie.id)

  router.push({
    name:'DetailView', params:{id:props.movie.id}}) // params를 하면 router에 :id로 등록해줘야함
}


</script>

<style>
.movie-card {
  width: 100%;
  /* transform-origin: center; */
  /* align-self: center; */
  justify-content: center;
  align-items: center;
  padding: 10px;
}

.poster-container {
  position: relative;
  width: 100%;
  border-radius: 20px;
  align-self: center;
  overflow: hidden;
  padding: 5px;
  transition: transform 0.3s ease;
}

.poster {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 20px;
  transition: transform 0.3s ease;
}

.overlay {
  position: absolute;
  padding: 5px;

  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: linear-gradient(
    to bottom, 
    rgba(0, 0, 0, 0.2),   
    rgba(0, 0, 0, 0.5),   
    rgba(0, 0, 0, 0.8),    
    rgba(0, 0, 0, 0.8)    
  );
  opacity: 0;
  transition: opacity 0.3s ease;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.movie-info {
  color: white;
  width: 100%;
  height: 100%;
  padding: 20px;
  text-align: left;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: flex-start;
  margin-bottom: 10px;
  gap: 10px;
}

.movie-title {
  font-size: 1.2em;
  margin: 0;
  font-weight: bold;
  width: 100%;
  font-family: 'NoTo Sans KR';
  font-weight: light;
}

.overview {
  font-size: 0.9em;
  line-height: 1.4;
  margin: 0;
  padding: 0 10px;
  padding: 0;
  width: 100%;
  font-family: 'NoTo Sans KR';
  font-weight: lighter;
}

.poster-container:hover .overlay {
  opacity: 1;
}

.poster-container:hover  {
  transform: scale(1.05);
}

.likebtn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: white;
  transition: color 0.3s ease;
  align-self: center;
  padding: 8px;
}

.heart {
  color: #ff0000 !important; 
}

/* 선택적: 호버 효과 추가 */
.likebtn:hover {
  transform: scale(1.1);
  background-color: transparent;
}
</style>
