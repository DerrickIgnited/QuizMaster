<!-- filepath: /Users/derricksamuel/Desktop/IITM/quiz_master_23f2001426/frontend/src/components/UserDashboard.vue -->
<template>
  <div class="container-fluid">
      
      <div class="container">
        <div class="row">
          <div class="col-md-8">
            <div class="glass-card p-4 mb-4">
              <h5 class="text-white mb-4"><i class="fas fa-clipboard-list me-2"></i>Available Quizzes</h5>
              <div class="row">
                <div v-for="quiz in quizzes" :key="quiz.id" class="col-md-6 mb-3">
                  <div class="quiz-card glass-card p-3">
                    <h6 class="text-white">{{quiz.subject_name}}</h6>
                    <p class="text-white-50 mb-2">{{quiz.chapter_name}}</p>
                    <div class="d-flex justify-content-between align-items-center">
                      <small class="text-white-50">
                        <i class="fas fa-clock me-1"></i>{{quiz.time_duration}} min
                      </small>
                      <button @click="startQuiz(quiz.id)" class="btn btn-sm modern-btn">
                        <i class="fas fa-play me-1"></i>Start
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="col-md-4">
            <div class="glass-card p-4 mb-4">
              <h5 class="text-white mb-3"><i class="fas fa-chart-bar me-2"></i>Your Stats</h5>
              <div class="text-center">
                <div class="mb-3">
                  <h3 class="text-white fw-bold">{{scores.length}}</h3>
                  <p class="text-white-50">Quizzes Completed</p>
                </div>
                <div class="mb-3">
                  <h3 class="text-white fw-bold">{{averageScore.toFixed(1)}}%</h3>
                  <p class="text-white-50">Average Score</p>
                </div>
              </div>
            </div>
            
            <div class="glass-card p-4">
              <h5 class="text-white mb-3"><i class="fas fa-history me-2"></i>Recent Scores</h5>
              <div class="d-flex justify-content-between mb-2">
                <span class="text-white-50">Chapter Name</span>
                <span class="text-white fw-bold">Score</span>
              </div>
              <div v-for="score in recentScores" :key="score.id" class="d-flex justify-content-between mb-2">
                <span class="text-white-50">{{score.chapter_name}}</span>
                <span class="text-white fw-bold">{{score.total_scored}}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
const API_BASE = 'http://localhost:8001';
export default {
  props: ['user'],
  data() {
    return {
      quizzes: [],
      scores: [],
      recentScores: [],
      averageScore: 0
    };
  },
  mounted() {
    this.loadDashboard();
  },
  methods: {
    async loadDashboard() {
      try {
        const response = await fetch(`${API_BASE}/api/user/dashboard`, { credentials: 'include' });
        const data = await response.json();
        this.quizzes = data.quizzes;
        this.scores = data.scores;
        this.recentScores = data.recentScores || [];
        this.averageScore = data.averageScore || 0;
      } catch (error) {
        alert('Failed to load dashboard');
      }
    },
    startQuiz(quizId) {
      this.$emit('start-quiz', quizId);
    },
    logout() {
      fetch(`${API_BASE}/api/auth/logout`, { method: 'POST', credentials: 'include' })
        .then(() => this.$emit('logout'));
    }
  }
};
</script>