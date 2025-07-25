<template>
  <div class="container-fluid d-flex justify-content-center">
      
      <div class="container">
        <div class="row justify-content-center">
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
              <div class="col-md-6">
                <button @click="triggerReminders" class="btn btn-sm modern-btn">
                  <i class="fas fa-bell me-1"></i>Trigger Exports
                </button>
              </div>
            </div>
          </div>
          
          <div class="row mb-4 justify-content-center">
            <div class="col-md-8">
              <div class="glass-card p-4">
                <h5 class="text-white mb-3"><i class="fas fa-chart-bar me-2"></i>Previous Test Scores</h5>
                <canvas ref="chartRef" style="max-height: 250px;"></canvas>
              </div>
            </div>
          </div>

          <div class="col-md-8">
            <div class="row justify-content-center">
              <div class="col-md-6">
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
              </div>
              <div class="col-md-6">
                <div class="glass-card p-4 mb-4">
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
      </div>
    </div>
</template>

<script>
import { defineComponent, ref, onMounted, watch } from 'vue';
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  CategoryScale,
  Tooltip,
  Legend
} from 'chart.js';

Chart.register(LineController, LineElement, PointElement, LinearScale, Title, CategoryScale, Tooltip, Legend);

const API_BASE = 'http://localhost:8001';

export default defineComponent({
  props: ['user'],
  setup() {
    const quizzes = ref([]);
    const scores = ref([]);
    const recentScores = ref([]);
    const averageScore = ref(0);
    const chartRef = ref(null);
    let chartInstance = null;

    const loadDashboard = async () => {
      try {
        const response = await fetch(`${API_BASE}/api/user/dashboard`, { credentials: 'include' });
        const data = await response.json();
        quizzes.value = data.quizzes;
        scores.value = data.scores;
        recentScores.value = data.recentScores || [];
        averageScore.value = data.averageScore || 0;
        updateChart();
      } catch (error) {
        alert('Failed to load dashboard');
      }
    };

    const updateChart = () => {
      if (!chartRef.value) return;
      if (chartInstance) {
        chartInstance.destroy();
      }
      const labels = scores.value.map((score, index) => score.chapter_name + ' #' + (index + 1));
      const dataPoints = scores.value.map(score => score.total_scored);

      chartInstance = new Chart(chartRef.value, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Test Scores',
            data: dataPoints,
            fill: false,
            borderColor: '#ff6384',
            backgroundColor: '#ff6384',
            tension: 0.3,
            pointHoverRadius: 7,
            pointRadius: 5,
            pointHoverBackgroundColor: '#ff6384',
            pointHoverBorderColor: '#fff'
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              labels: {
                color: 'white'
              }
            },
            tooltip: {
              enabled: true,
              mode: 'nearest',
              intersect: false,
              backgroundColor: '#333',
              titleColor: '#fff',
              bodyColor: '#fff'
            },
            title: {
              display: true,
              text: 'Previous Test Scores',
              color: 'white',
              font: {
                size: 16,
                weight: 'bold'
              }
            }
          },
          scales: {
            x: {
              ticks: {
                color: 'white'
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              }
            },
            y: {
              beginAtZero: true,
              ticks: {
                color: 'white'
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              }
            }
          },
          interaction: {
            mode: 'nearest',
            intersect: false
          }
        }
      });
    };

    onMounted(() => {
      loadDashboard();
    });

    watch(scores, () => {
      updateChart();
    });

    const startQuiz = function(quizId) {
      this.$emit('start-quiz', quizId);
    };

    const logout = () => {
      fetch(`${API_BASE}/api/auth/logout`, { method: 'POST', credentials: 'include' })
        .then(() => {
          // emit logout event
        });
    };

    return {
      quizzes,
      scores,
      recentScores,
      averageScore,
      chartRef,
      loadDashboard,
      startQuiz,
      logout
    };
  },
  methods: {
    async triggerReminders() {
      try {
        const response = await fetch(`${API_BASE}/api/user/trigger-reminders`, {
          method: 'POST',
          credentials: 'include'
        });

        const data = await response.json();

        if (response.ok) {
          alert(data.message || 'Reminders triggered successfully');
        } else {
          alert(data.error || 'Failed to trigger reminders');
        }
      } catch (error) {
        alert('Something went wrong while triggering reminders.');
        console.error(error);
      }
    }
  }
});
</script>
