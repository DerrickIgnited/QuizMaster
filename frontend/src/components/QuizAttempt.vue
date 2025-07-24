<!-- filepath: /Users/derricksamuel/Desktop/IITM/quiz_master_23f2001426/frontend/src/components/QuizAttempt.vue -->
<template>
  <div class="container-fluid">
      <nav class="navbar navbar-expand-lg navbar-dark mb-4">
        <div class="container">
          <a class="navbar-brand fw-bold">
            <i class="fas fa-question-circle me-2"></i>{{quiz.subject_name}} - {{quiz.chapter_name}}
          </a>
          <div class="navbar-text">
            <i class="fas fa-clock me-2"></i>
            <span class="fw-bold" :class="timeLeft <= 300 ? 'text-warning' : 'text-white'">
              {{Math.floor(timeLeft/60)}}:{{(timeLeft%60).toString().padStart(2,'0')}}
            </span>
          </div>
        </div>
      </nav>
      
      <div class="container">
        <div class="glass-card p-4">
          <div class="progress mb-4" style="height: 10px;">
            <div class="progress-bar bg-gradient" :style="{width: ((currentQuestion + 1) / questions.length * 100) + '%'}"></div>
          </div>
          
          <div v-if="!showResults && questions.length > 0">
            <div class="mb-4">
              <h6 class="text-white-50">Question {{currentQuestion + 1}} of {{questions.length}}</h6>
              <h4 class="text-white mb-4">{{questions[currentQuestion].question_statement}}</h4>
              
              <div class="row">
                <div class="col-md-6 mb-2">
                  <button @click="selectAnswer(1)" 
                          :class="['btn', 'w-100', 'text-start', 'p-3', answers[questions[currentQuestion].id] === 1 ? 'btn-primary' : 'btn-outline-light']">
                    A. {{questions[currentQuestion].option1}}
                  </button>
                </div>
                <div class="col-md-6 mb-2">
                  <button @click="selectAnswer(2)" 
                          :class="['btn', 'w-100', 'text-start', 'p-3', answers[questions[currentQuestion].id] === 2 ? 'btn-primary' : 'btn-outline-light']">
                    B. {{questions[currentQuestion].option2}}
                  </button>
                </div>
                <div class="col-md-6 mb-2">
                  <button @click="selectAnswer(3)" 
                          :class="['btn', 'w-100', 'text-start', 'p-3', answers[questions[currentQuestion].id] === 3 ? 'btn-primary' : 'btn-outline-light']">
                    C. {{questions[currentQuestion].option3}}
                  </button>
                </div>
                <div class="col-md-6 mb-2">
                  <button @click="selectAnswer(4)" 
                          :class="['btn', 'w-100', 'text-start', 'p-3', answers[questions[currentQuestion].id] === 4 ? 'btn-primary' : 'btn-outline-light']">
                    D. {{questions[currentQuestion].option4}}
                  </button>
                </div>
              </div>
            </div>
            
            <div class="d-flex justify-content-between">
              <button @click="previousQuestion" :disabled="currentQuestion === 0" class="btn btn-outline-light">
                <i class="fas fa-chevron-left me-2"></i>Previous
              </button>
              
              <button v-if="currentQuestion < questions.length - 1" @click="nextQuestion" class="btn modern-btn">
                Next <i class="fas fa-chevron-right ms-2"></i>
              </button>
              
              <button v-else @click="submitQuiz" class="btn btn-success">
                <i class="fas fa-check me-2"></i>Submit Quiz
              </button>
            </div>
          </div>
          <div v-else-if="!showResults && questions.length === 0" class="text-center text-white">
            <h4>No questions available for this quiz.</h4>
          </div>
          <div v-else class="text-center">
            <i class="fas fa-trophy fa-4x text-warning mb-4"></i>
            <h2 class="text-white mb-3">Quiz Completed!</h2>
            <h4 class="text-white mb-4">Your Score: {{result.score}} / {{result.total_questions}}</h4>
            <div class="mb-4">
              <div class="progress" style="height: 20px;">
                <div class="progress-bar bg-success" :style="{width: (result.score / result.total_questions * 100) + '%'}">
                  {{Math.round(result.score / result.total_questions * 100)}}%
                </div>
              </div>
            </div>
            <button @click="$emit('back-to-dashboard')" class="btn modern-btn">
              <i class="fas fa-home me-2"></i>Back to Dashboard
            </button>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
const API_BASE = 'http://localhost:8001';
export default {
  props: ['quizId'],
  data() {
    return {
      quiz: {},
      questions: [],
      answers: {},
      currentQuestion: 0,
      timeLeft: 0,
      timer: null,
      showResults: false,
      result: {}
    };
  },
  mounted() {
    this.loadQuiz();
    this.startTimer();
  },
  beforeUnmount() {
    if (this.timer) clearInterval(this.timer);
  },
  methods: {
    async loadQuiz() {
      try {
        const response = await fetch(`${API_BASE}/api/quiz/attempt/${this.quizId}`, { credentials: 'include' });
        const data = await response.json();
        this.quiz = data.quiz;
        this.questions = data.questions || [];
        this.timeLeft = this.quiz.time_duration * 60;
      } catch (error) {
        console.error('Failed to load quiz:', error);
        this.questions = [];
      }
    },
    startTimer() {
      if (this.timer) clearInterval(this.timer);
      this.timer = setInterval(() => {
        if (this.timeLeft > 0) {
          this.timeLeft--;
        } else {
          this.submitQuiz();
        }
      }, 1000);
    },
    selectAnswer(option) {
      const qid = this.questions[this.currentQuestion].id;
      this.answers[qid] = option;
    },
    nextQuestion() {
      if (this.currentQuestion < this.questions.length - 1) {
        this.currentQuestion++;
      }
    },
    previousQuestion() {
      if (this.currentQuestion > 0) {
        this.currentQuestion--;
      }
    },
    async submitQuiz() {
      if (this.timer) clearInterval(this.timer);
      try {
        const response = await fetch(`${API_BASE}/api/quiz/submit/${this.quizId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({ answers: this.answers })
        });
        this.result = await response.json();
        this.showResults = true;
      } catch (error) {
        console.error('Failed to submit quiz:', error);
      }
    }
  }
};
</script>