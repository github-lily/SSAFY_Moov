<template>
  <div class="container">
    <HeaderNav />
    <div class="intro">
      <div class="intro-left">
        <p class="introtext">Learn English,<br> Enjoy Movies,<br> Love the Journey!</p>
        <p class="introtext2">
          At Moov. <br> we help you learn English through carefully selected movies <br> that match your proficiency level. <br> Start you journey today.
        </p>
      </div>
      <div class="intro-right">
        <div class="mainmovie"></div>
        <button class="test" @click="goToTest">TEST &#9654</button>
      </div>
    </div>

    <div class="recom">
      <h3>Today's recommendation</h3>
      <!-- 레벨 선택 버튼 -->
      <div class="level-buttons">
        <button
          v-for="level in levelOptions"
          :key="level"
          :class="['level-button', { active: selectedLevel === level }]"
          @click="selectLevel(level)"
        >
          {{ level }}
        </button>
      </div>
        <!-- 장르 선택 -->
        <select id="genre-select" v-model="selectedGenre" class="custom-select">
          <option value="" selected disabled hidden class="placeholder-option">All Genre</option>
          <option class="lists" v-for="genre in availableGenres" 
          :key="genre" :value="genre">{{ genre }}</option>
        </select>
    </div>
      
      <!-- 필터된 영화들만 출력 -->
      <MovieList :movies="filteredMovies"/>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useMovieStore } from '@/stores/movie';
import { useAuthStore } from '@/stores/auth';
import { useUserStore } from '@/stores/user';
import HeaderNav from '@/components/common/HeaderNav.vue';
import MovieList from '@/components/movie/MovieList.vue';

const router = useRouter();
const store = useMovieStore();
const authStore = useAuthStore();
const userStore = useUserStore();

const movies = ref([]);
const selectedGenre = ref("");
const selectedLevel = ref(""); // 현재 선택된 레벨

const goToTest = () => {
  router.push({name:'TestView'})
}

// 레벨별 장르 매핑
const levelGenreMapping = {
  1: ['애니메이션', '가족'],
  2: ['TV 영화', '로맨스', '코미디'],
  3: ['드라마', '판타지', '어드벤처'],
  4: ['범죄', '역사', '음악', '미스터리', '액션', '스릴러', '공포'],
  5: ['SF', '다큐멘터리', '음악', '서부', '전쟁']
};

// 레벨 옵션
const levelOptions = [1, 2, 3, 4, 5];

// 사용 가능한 장르 (선택된 레벨에 따라 변경)
const availableGenres = ref(['All Genre']);

// 특정 레벨 선택 시 호출되는 함수
const selectLevel = (level) => {
  selectedLevel.value = level;
  availableGenres.value = ['All Genre', ...levelGenreMapping[level]];
  selectedGenre.value = ""; // 장르 초기화
};

// 영화 필터링 로직
const filteredMovies = computed(() => {
  let result = movies.value;

  // 레벨 필터링
  if (selectedLevel.value) {
    const levelGenres = levelGenreMapping[selectedLevel.value];
    result = result.filter(movie =>
      movie.genres.some(genre => levelGenres.includes(genre.name))
    );
  }

  // 장르 필터링
  if (selectedGenre.value) {
    result = result.filter(movie =>
      movie.genres.some(genre => genre.name === selectedGenre.value)
    );
  }

  return result;
});

// 영화 장르 (id와 name이 매칭된 형태로 저장)
const genres = ref([
  { id: 28, name: "액션" },
  { id: 12, name: "어드벤처" },
  { id: 16, name: "애니메이션" },
  { id: 35, name: "코미디" },
  { id: 80, name: "범죄" },
  { id: 99, name: "다큐멘터리" },
  { id: 18, name: "드라마" },
  { id: 10751, name: "가족" },
  { id: 14, name: "판타지" },
  { id: 36, name: "역사" },
  { id: 27, name: "공포" },
  { id: 10402, name: "음악" },
  { id: 9648, name: "미스터리" },
  { id: 10749, name: "로맨스" },
  { id: 878, name: "SF" },
  { id: 10770, name: "TV 영화" },
  { id: 53, name: "스릴러" },
  { id: 10752, name: "전쟁" },
  { id: 37, name: "서부" }
]);

onMounted(() => {
  store.getMovies();
  movies.value = store.movies;
  
  if (authStore.token) {
    const user = userStore.getUser()
    console.log('현재 로그인한 유저 정보:', user)
  console.log(userStore.user.username, '님의 메인페이지')
    
    console.log('유저의 토큰:', authStore.token)
  } else {
    console.log('로그인이 필요합니다.')
  }
})

  if (authStore.token) {
    userStore.getUser();
  }
;

</script>

<style scoped>

body {
  position: relative;
}

.contanier {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    overflow: visible;
}

/* --------------------------------------------------------- */
/* nav bar 하단 */
.intro {
  width: 100%;
  height: 500px;
  display: flex;
  margin-bottom: 30px;
}

.intro-left {
  height: 100%;
  width: 70%; 
  margin-right: 20px;
  background-color: white;
  border-radius: 20px;
}

.intro-right {
  height: 100%;
  width: 30%;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
}

.mainmovie {
  width: 100%;
  height: 50%;
  background-color: white;
  border-radius: 20px;
  margin-bottom: 20px;
}

.test {
  width: 240px;
  height: 240px;
  background-color: #ffeb3b  !important; 
  border-radius: 50%;
  align-self: flex-end;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Krona One';
  border: none;
  color: black;
}

.introtext {
  padding-left: 3%;
  padding-top: 5%;
  font-size: 70px;
  font-family: 'Krona One';
  line-height: 80px;
  letter-spacing: -0.1em;
}

.introtext2 {
  padding-left: 3%;
  padding-top: 12%;
  font-family: 'Krona One';
  line-height: 19px;
  letter-spacing: -0.1em;
  align-self: end;
  color: rgb(148, 148, 148);
}


.recom  {
  display: flex;
  padding: 20px 0;
  /* justify-content: center; */
  align-items: center;

}

.custom-select {
  background-color: transparent;
  color: white;
  padding: 8px;
  font-family: 'NoTo Sans KR';
  border: none;
  border-bottom: 0.1px solid rgb(161, 161, 161);
  margin-right: 20px;
}

.custom-select:focus {
  outline: none;
}

h3 {
  font-size: 2em;
  font-family: 'Krona One';
  color: white;
  margin-right: 100px;
}

.lists {
  background-color: rgb(54, 54, 54); 
  color: white;           
  font-family: 'NoTo Sans KR';
  font-weight: lighter;
  /* text-align: center; */
  /* padding: auto; */
}

.level-buttons {
  display: flex;
  gap: 10px;
  margin-right: 20px;
}

.level-button {
  padding: 10px 20px; 
  background-color: #555;
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-family: 'Krona One';
}

.level-button.active {
  background-color: #ffeb3b;
  color: black;
}

.level-button:hover {
  background-color: #ffeb3b;
  color: black;
}

</style>
