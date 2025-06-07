<template>
  <div class="min-h-screen bg-gray-100 p-4">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold text-center mb-8">Panel Administratora Familiady</h1>

      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">Wybierz pytanie</h2>
        <div class="grid gap-4">
          <select 
            v-model="selectedQuestionIndex" 
            class="w-full p-2 border border-gray-300 rounded-md"
          >
            <option v-for="(question, index) in questions" :key="index" :value="index">
              {{ question.pytanie }}
            </option>
          </select>

          <div class="flex space-x-2">
            <button 
              v-if="!currentQuestion"
              @click="startGame" 
              class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md"
            >
              Rozpocznij grę
            </button>
            <button 
              v-if="currentQuestion"
              @click="changeQuestion" 
              class="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-md"
            >
              Zmień pytanie
            </button>
          </div>
        </div>
      </div>

      <div v-if="currentQuestion" class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">{{ currentQuestion.pytanie }}</h2>


        <!-- Points Pool Display -->
        <div class="mb-6 p-4 bg-yellow-100 rounded-lg border border-yellow-400">
          <div class="flex justify-between items-center">
            <div>
              <h3 class="text-lg font-semibold text-yellow-800">Pula punktów:</h3>
              <p class="text-2xl font-bold text-yellow-600">{{ pointsPool }} pkt</p>
            </div>
            <div class="flex space-x-2">
              <button 
                @click="awardPointsToTeam(1)" 
                class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md"
                :disabled="pointsPool === 0"
              >
                Przyznaj punkty Drużynie 1
              </button>
              <button 
                @click="awardPointsToTeam(2)" 
                class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md"
                :disabled="pointsPool === 0"
              >
                Przyznaj punkty Drużynie 2
              </button>
            </div>
          </div>
        </div>

        <div class="space-y-4">
          <div v-for="(answer, index) in currentQuestion.odpowiedzi" :key="index" class="flex items-center justify-between p-3 border border-gray-200 rounded-md">
            <div class="flex items-center">
              <span class="font-medium mr-2">{{ index + 1 }}.</span>
              <span>{{ answer.odpowiedź }}</span>
            </div>
            <div class="flex items-center">
              <span class="font-medium mr-2">{{ answer.punkty }} pkt</span>
              <button 
                @click="revealedAnswers.includes(index) ? unrevealAnswer(index) : revealAnswer(index)"
                class="ml-2 px-3 py-1 bg-green-600 hover:bg-green-700 text-white rounded-md"
              >
                {{ revealedAnswers.includes(index) ? 'Odkryte' : 'Odkryj' }}
              </button>
            </div>
          </div>
        </div>

        <div class="mt-6 space-y-4">
          <!-- Question Selection Controls -->
          <div class="flex items-center space-x-2 py-2 bg-gray-50 rounded-lg">
            <div class="flex-grow">
              <select 
                v-model="selectedQuestionIndex" 
                class="w-full p-2 border border-gray-300 rounded-md"
              >
                <option v-for="(question, index) in questions" :key="index" :value="index">
                  {{ question.pytanie }}
                </option>
              </select>
            </div>
            <button 
              @click="changeQuestion" 
              class="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-md whitespace-nowrap"
            >
              Zmień pytanie
            </button>
            <p>
              lub
            </p>
            <button 
              @click="nextQuestion" 
              class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md whitespace-nowrap"
            >
              Kolejne pytanie
            </button>
          </div>

          <!-- Game Controls -->
          <div class="flex justify-between">
            <div>
              <button
                @click="addStrike"
                class="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-md mr-2"
                :disabled="strikes >= 3"
              >
                Dodaj X
              </button>
              <span class="text-xl font-bold">
                {{ 'X'.repeat(strikes) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div v-if="currentQuestion" class="bg-white rounded-lg shadow-md p-6 mb-6">
        <div class="flex gap-5">
          <div>
            <button
                @click="resetGame"
                class="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-md"
                :disabled="!doesUserWantToEndGame"
            >
              Resetuj grę
            </button>
          </div>
          <div class="flex items-center gap-2">
            <input type="checkbox" v-model="doesUserWantToEndGame" value="false">
            <p>
              POTWIERDZAM, IŻ CHCĘ ZRESETOWAĆ GRE
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

interface Answer {
  odpowiedź: string;
  punkty: number;
}

interface Question {
  pytanie: string;
  odpowiedzi: Answer[];
}

// State
const doesUserWantToEndGame = ref(false);
const questions = ref<Question[]>([]);
const selectedQuestionIndex = ref<number>(0);
const currentQuestion = ref<Question | null>(null);
const revealedAnswers = ref<number[]>([]);
const strikes = ref<number>(0);
const team1Score = ref<number>(0);
const team2Score = ref<number>(0);
const activeTeam = ref<number>(1); // 1 for team 1, 2 for team 2
const pointsPool = ref<number>(0); // Points accumulated from revealed answers

// Computed
// const currentQuestionData = computed(() => {
//   return selectedQuestionIndex.value !== null ? questions.value[selectedQuestionIndex.value] : null;
// });

// Methods
const loadQuestions = async () => {
  try {
    // Load questions from the JSON file in the /data directory
    const response = await fetch('/data/familiada_pytania.json');
    if (!response.ok) {
      throw new Error(`Failed to load questions: ${response.status} ${response.statusText}`);
    }
    questions.value = await response.json();
    console.log('Loaded questions:', questions.value.length);
  } catch (error) {
    console.error('Error loading questions:', error);
    alert('Nie udało się załadować pytań. Sprawdź czy plik JSON jest dostępny w katalogu /data.');
  }
};

const startGame = () => {
  if (selectedQuestionIndex.value !== null) {
    currentQuestion.value = questions.value[selectedQuestionIndex.value];
    revealedAnswers.value = [];
    strikes.value = 0;
    team1Score.value = 0;
    team2Score.value = 0;
    activeTeam.value = 1;
    pointsPool.value = 0;

    // Update localStorage to sync with game view
    updateGameState();
  }
};

const revealAnswer = (index: number) => {
  if (!revealedAnswers.value.includes(index)) {
    revealedAnswers.value.push(index);
    if (currentQuestion.value) {
      // Add points to the pool instead of directly to team scores
      pointsPool.value += currentQuestion.value.odpowiedzi[index].punkty;
    }

    // Update localStorage to sync with game view
    updateGameState();
  }
};

const unrevealAnswer = (index: number) => {
  console.log('unrevealAnswer', index);
  if (revealedAnswers.value.includes(index)) {
    revealedAnswers.value = revealedAnswers.value.filter(i => i !== index);
    if (currentQuestion.value) {
      // Add points to the pool instead of directly to team scores
      pointsPool.value -= currentQuestion.value.odpowiedzi[index].punkty;
    }

    updateGameState();
  }
}

const addStrike = () => {
  if (strikes.value < 3) {
    strikes.value++;

    // Update localStorage to sync with game view
    updateGameState();
  }
};

const awardPointsToTeam = (team: number) => {
  if (pointsPool.value > 0) {
    if (team === 1) {
      team1Score.value += pointsPool.value;
    } else {
      team2Score.value += pointsPool.value;
    }
    pointsPool.value = 0;

    // Update localStorage to sync with game view
    updateGameState();

    // Force a localStorage event to ensure immediate update
    window.dispatchEvent(new StorageEvent('storage', {
      key: 'familiadaGameState'
    }));
  }
};

const nextQuestion = () => {
  if (questions.value.length > 0) {
    // Increment the question index with wraparound
    selectedQuestionIndex.value = (selectedQuestionIndex.value + 1) % questions.value.length;

    // Set the new current question
    currentQuestion.value = questions.value[selectedQuestionIndex.value];

    // Reset answers, strikes, and points pool, but keep scores
    revealedAnswers.value = [];
    strikes.value = 0;
    pointsPool.value = 0;

    // Update localStorage to sync with game view
    updateGameState();
  }
};

const changeQuestion = () => {
  if (questions.value.length > 0 && selectedQuestionIndex.value !== null) {
    // Set the current question based on the selected index
    currentQuestion.value = questions.value[selectedQuestionIndex.value];

    // Reset answers, strikes, and points pool, but keep scores
    revealedAnswers.value = [];
    strikes.value = 0;
    pointsPool.value = 0;

    // Update localStorage to sync with game view
    updateGameState();
  }
};

const resetGame = () => {
  currentQuestion.value = null;
  revealedAnswers.value = [];
  strikes.value = 0;
  team1Score.value = 0;
  team2Score.value = 0;
  activeTeam.value = 1;
  pointsPool.value = 0;

  // Update localStorage to sync with game view
  updateGameState();
};

const updateGameState = () => {
  const gameState = {
    currentQuestion: currentQuestion.value,
    revealedAnswers: revealedAnswers.value,
    strikes: strikes.value,
    team1Score: team1Score.value,
    team2Score: team2Score.value,
    activeTeam: activeTeam.value,
    pointsPool: pointsPool.value
  };

  localStorage.setItem('familiadaGameState', JSON.stringify(gameState));
};

// Lifecycle hooks
onMounted(() => {
  loadQuestions();

  // Try to restore game state from localStorage
  const savedState = localStorage.getItem('familiadaGameState');
  if (savedState) {
    try {
      const parsedState = JSON.parse(savedState);
      currentQuestion.value = parsedState.currentQuestion;
      revealedAnswers.value = parsedState.revealedAnswers;
      strikes.value = parsedState.strikes;

      // Restore team scores, active team, and points pool
      team1Score.value = parsedState.team1Score || 0;
      team2Score.value = parsedState.team2Score || 0;
      activeTeam.value = parsedState.activeTeam || 1;
      pointsPool.value = parsedState.pointsPool || 0;

      // Find the index of the current question
      if (currentQuestion.value) {
        const index = questions.value.findIndex(q => q.pytanie === currentQuestion.value?.pytanie);
        if (index !== -1) {
          selectedQuestionIndex.value = index;
        }
      }
    } catch (error) {
      console.error('Error parsing saved game state:', error);
    }
  }
});
</script>
