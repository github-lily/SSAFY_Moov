<template>
  <div class="container">
    <HeaderNav />

    <div class="movie-container">
      <div class="movie-poster">        
        <img v-if="moviePoster" :src="moviePoster" alt="Movie Poster">
      </div>
      <div class="movie-contents">
        <div class="top-contents">
          <p v-if="movie.title" class="title">{{ movie.title }}</p>
          <p v-if="movie.runtime" class="runtime">
            {{ Math.floor(movie.runtime / 60) }}시간 {{movie.runtime % 60}}분
          </p>
          <p v-if="movie.vote_average" class="vote_average">평점: {{ movie.vote_average.toFixed(1) }}</p>
        </div>
        <div class="botton-contents">|
          <p class="genres" v-if="movie.genres && movie.genres.length > 0" v-for="genre in movie.genres" :key="genre.name">{{ genre.name }} </p>|
          <p v-if="movie.director" class="director">감독: {{ movie.director.name }}</p>
          <p class="actors-title">
            출연진:
            <!-- 3명까지만 출력하기 -->
            <p class="actors" v-if="movie.actors && movie.actors.length > 0" v-for="(actor, index) in movie.actors.slice(0, 3)" :key="actor.name">&nbsp;{{ actor.name }}<span v-if="index < 2">, </span></p>
            등
          </p>

          <p class="movie_overview" v-if="movie.overview">{{ movie.overview }}</p>
        </div>
      </div>
    </div>

    <div class="comments-container">
      <p class="comment-title">Comments</p>
      <div class="comments-list">
          <MovieComment 
          :movieId = 'movieId'/>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'

import HeaderNav from '@/components/common/HeaderNav.vue'
import MovieComment from '@/components/movie/MovieComment.vue'

import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { useMovieStore } from '@/stores/movie'


const store = useMovieStore()
const authStore = useAuthStore()
const userStore = useUserStore()
const route = useRoute()

const movie = ref({
  title: '',
  runtime: null,
  vote_average: null,
  director: { name: '' },
  genres: [],
  overview: ''
})


const movieId = route.params.id

const moviePoster = computed(() => {
  return movie.value && movie.value.poster_path
    ? `https://image.tmdb.org/t/p/w500/${movie.value.poster_path}`
    : null
})

// 단일 비동기 함수로 다시 통합
const fetchMovieData = async () => {
  try {
    // 영화 상세 정보 가져오기
    const res = await axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/movies/${movieId}/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
    movie.value = res.data
    
    // 댓글 정보는 한 번만 가져오기
    if (!store.comments.length || store.comments[0]?.movieId !== movieId) {
      await store.getMovieComments(movieId)
    }
  } catch (err) {
    console.error('Error fetching movie details:', err)
  }
}

onMounted(() => {
  fetchMovieData()
})

</script>

<style scoped>

.movie-container {
  height: 500px;
  width: 100%;
  /* background-color: white; */
  border-radius: 50px;
  display: flex;
  justify-content: space-between;
  align-items: stretch;
  margin-bottom: 100px;
}

.movie-poster {
  height: 100%;
  width: 50%;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  /* 자식 요소가 부모 영역을 벗어나지 않도록 설정 */
  overflow: hidden;
}

img {
  max-width: 100%;
  max-height: 100%;
}

.movie-contents {
  height: 100%;
  width: 50%;
  font-family: 'Noto Sans KR';
  color: white;
  margin-bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: end;

}

.top-contents {
  display: flex;
  bottom: 0px;
  align-items: end;
  margin-bottom: 20px;
}

.title {
  font-size: 2em;
  font-weight: bold;
  margin-right: 20px;
  margin-bottom: 0;
}

.runtime {
  margin-right: 20px;
  font-size: 1em;
  margin-bottom: 5px;
  color: #a7a7a7;
}

.vote_average {
  margin-right: 20px;
  font-size: 1em;
  margin-bottom: 5px;
  color: #a7a7a7;

}

.director {
  font-weight: lighter;
  margin-bottom: 5px;
}


.genres {
  display: inline-block;
  margin-right: 10px;
  font-weight: lighter;
  margin-bottom: 5px;
}

.actors-title {
  font-weight: lighter;
  
}
.actors {
  display: inline-block;
  font-weight: lighter;
}

.movie_overview {
  margin-right: 60px;
  margin-bottom: 40px;
  color: #a7a7a7;

}



/* comment */
.comment-title {
  margin: 20px 0;
  font-family: 'Krona One';
  font-size: 20px;
  color: white;
}

.comments-list {
  width: 100%;
  /* background-color: #ffffff; */
  height: 100vh;
}


</style>