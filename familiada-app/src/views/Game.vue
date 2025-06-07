<template>
  <div class="min-h-screen bg-blue-900 flex flex-col items-center justify-center p-4">
    <!-- Game Header -->
    <div class="w-full max-w-5xl mb-8">
      <h1 class="text-4xl md:text-6xl font-bold text-yellow-400 text-center">FAMILIADA</h1>
    </div>

    <!-- Game Board -->
    <div v-if="currentQuestion" class="w-full max-w-5xl">
      <!-- Question -->
      <div class="bg-blue-800 p-4 rounded-t-lg border-2 border-yellow-400">
        <h2 class="text-2xl md:text-3xl font-bold text-white text-center">
          {{ currentQuestion.pytanie }}
        </h2>
      </div>

      <!-- Answers Board -->
      <div class="bg-black p-6 rounded-b-lg border-2 border-t-0 border-yellow-400">
        <div class="grid grid-cols-1 gap-4">
          <div 
            v-for="(answer, index) in currentQuestion.odpowiedzi" 
            :key="index"
            class="bg-blue-950 rounded-md overflow-hidden"
          >
            <div class="flex items-center justify-between">
              <!-- Answer Number -->
              <div class="bg-blue-700 text-white font-bold text-xl w-12 h-12 flex items-center justify-center">
                {{ index + 1 }}
              </div>

              <!-- Answer Content -->
              <div 
                class="flex-1 px-4 py-2 transition-all duration-500"
                :class="{ 'bg-blue-950': !isAnswerRevealed(index), 'bg-blue-800': isAnswerRevealed(index) }"
              >
                <div v-if="isAnswerRevealed(index)" class="flex justify-between items-center">
                  <span class="text-white text-xl font-medium">{{ answer.odpowiedź }}</span>
                  <span class="text-yellow-400 font-bold text-xl">{{ answer.punkty }}</span>
                </div>
                <div v-else class="h-8 w-full bg-blue-950"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Strikes, Points Pool, and Scores -->
        <div class="mt-6 flex justify-between space-y-4">
          <!-- Strikes and Points Pool -->
          <div class="flex justify-between gap-4 items-center">
            <div v-for="_ in [...Array(strikes).keys()]" class="text-red-600 text-4xl font-bold">
              {{ 'X' }}
            </div>
          </div>

          <!-- Team Scores -->
          <div class="flex justify-end space-x-4">
            <!-- Points Pool -->
            <div v-if="pointsPool > 0" class="bg-yellow-500 px-6 py-3 rounded-md border-2 border-yellow-400 animate-pulse">
              <span class="text-white text-xl font-bold">Pula punktów: </span>
              <span class="text-white text-2xl font-bold">{{ pointsPool }}</span>
            </div>

            <!-- Team 1 Score -->
            <div class="bg-blue-800 px-6 py-3 rounded-md border-2 border-yellow-400">
              <span class="text-white text-xl font-bold">Drużyna 1: </span>
              <span class="text-yellow-400 text-2xl font-bold">{{ team1Score }}</span>
            </div>

            <!-- Team 2 Score -->
            <div class="bg-blue-800 px-6 py-3 rounded-md border-2 border-yellow-400">
              <span class="text-white text-xl font-bold">Drużyna 2: </span>
              <span class="text-yellow-400 text-2xl font-bold">{{ team2Score }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Waiting Screen -->
    <div v-else class="flex flex-col items-center justify-center">
      <div class="text-white text-2xl mb-4">Oczekiwanie na rozpoczęcie gry...</div>
        <a href="/admin">Panel Administratorski</a>
      <div class="animate-bounce text-yellow-400 text-4xl">⏳</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

interface Answer {
  odpowiedź: string;
  punkty: number;
}

interface Question {
  pytanie: string;
  odpowiedzi: Answer[];
}

// State
const currentQuestion = ref<Question | null>(null);
const revealedAnswers = ref<number[]>([]);
const strikes = ref<number>(0);
const team1Score = ref<number>(0);
const team2Score = ref<number>(0);
const activeTeam = ref<number>(1);
const pointsPool = ref<number>(0);

// Methods
const isAnswerRevealed = (index: number): boolean => {
  return revealedAnswers.value.includes(index);
};

const handleStorageChange = (event: StorageEvent) => {
  if (event.key === 'familiadaGameState') {
    loadGameState();
  }
};

const loadGameState = () => {
  const savedState = localStorage.getItem('familiadaGameState');
  if (savedState) {
    try {
      const parsedState = JSON.parse(savedState);
      currentQuestion.value = parsedState.currentQuestion;
      revealedAnswers.value = parsedState.revealedAnswers;
      strikes.value = parsedState.strikes;

      // Load team scores, active team, and points pool
      team1Score.value = parsedState.team1Score || 0;
      team2Score.value = parsedState.team2Score || 0;
      activeTeam.value = parsedState.activeTeam || 1;
      pointsPool.value = parsedState.pointsPool || 0;
    } catch (error) {
      console.error('Error parsing saved game state:', error);
    }
  }
};

// Sound effects (optional)
const playRevealSound = () => {
  const audio = new Audio('/sounds/reveal.mp3');
  audio.play().catch(e => console.log('Sound play failed:', e));
};

const playStrikeSound = () => {
  const audio = new Audio('/sounds/strike.mp3');
  audio.play().catch(e => console.log('Sound play failed:', e));
};

// Watch for changes in revealed answers to play sound
const prevRevealedCount = ref(0);
const prevStrikes = ref(0);

// Lifecycle hooks
onMounted(() => {
  // Load initial state
  loadGameState();

  // Listen for storage events from admin panel
  window.addEventListener('storage', handleStorageChange);

  // Set up watchers for sound effects
  setInterval(() => {
    if (revealedAnswers.value.length > prevRevealedCount.value) {
      playRevealSound();
      prevRevealedCount.value = revealedAnswers.value.length;
    }

    if (strikes.value > prevStrikes.value) {
      playStrikeSound();
      prevStrikes.value = strikes.value;
    }
  }, 500);
});

onUnmounted(() => {
  window.removeEventListener('storage', handleStorageChange);
});
</script>

<style scoped>
/* Add any component-specific styles here */
</style>
