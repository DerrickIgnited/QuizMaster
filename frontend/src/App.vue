e <!-- filepath: /Users/derricksamuel/Desktop/IITM/quiz_master_23f2001426/frontend/src/App.vue -->
<template>
  <Starfield />

  <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4">
    <a class="navbar-brand fw-bold" href="#" @click.prevent="currentView = 'home'">
      <i class="fas fa-graduation-cap me-2"></i> Quiz Master
    </a>
    <div class="ms-auto">
      <button v-if="currentUser" @click="logout" class="btn modern-btn me-2">
        <i class="fas fa-sign-out-alt me-2"></i>Logout
      </button>
      <button v-else @click="handleSwitchToLogin" class="btn modern-btn me-2">
        <i class="fas fa-sign-in-alt me-2"></i>Login
      </button>
      <button @click="handleSwitchToRegister" class="btn modern-btn">
        <i class="fas fa-user-plus me-2"></i>Register
      </button>
    </div>
  </nav>

  <Login v-if="currentView === 'login'"
         @login-success="handleLoginSuccess"
         @switch-to-register="handleSwitchToRegister" />
  <Register v-else-if="currentView === 'register'"
            @switch-to-login="handleSwitchToLogin" />
  <AdminDashboard v-else-if="currentView === 'admin'"
                  @logout="handleLogout" />
  <UserDashboard v-else-if="currentView === 'user'"
                 :user="currentUser"
                 @logout="handleLogout"
                 @start-quiz="handleStartQuiz" />
  <QuizAttempt v-else-if="currentView === 'quiz'"
               :quiz-id="selectedQuizId"
               @back-to-dashboard="handleBackToDashboard" />
  <Home v-else-if="currentView === 'home'"
        @switch-to-login="handleSwitchToLogin"
        @switch-to-register="handleSwitchToRegister" />
  <footer class="app-footer glass-footer py-4 px-3 bg-dark">
    <div class="container d-flex flex-column justify-content-center align-items-center text-center">
      <div class="mb-3 mb-md-0 text-white">
        <i class="fas fa-graduation-cap me-2 text-primary"></i>
        <span class="fw-bold">Quiz Master</span> © 2025 — All rights reserved.
      </div>
    </div>
  </footer>
</template>

<script>
import Login from './components/Login.vue';
import Register from './components/Register.vue';
import AdminDashboard from './components/AdminDashboard.vue';
import UserDashboard from './components/UserDashboard.vue';
import QuizAttempt from './components/QuizAttempt.vue';
import Starfield from './components/Starfield.vue';
import Home from './components/Home.vue';

const API_BASE = 'http://localhost:8001';
export default {
  components: {
    Starfield,
    Home,
    Login,
    Register,
    AdminDashboard,
    UserDashboard,
    QuizAttempt
  },
  data() {
    return {
      currentView: 'home',
      currentUser: null,
      selectedQuizId: null
    };
  },
  methods: {
    handleLoginSuccess(user) {
      this.currentUser = user;
      this.currentView = user.role === 'admin' ? 'admin' : 'user';
    },
    handleLogout() {
      this.currentUser = null;
      this.currentView = 'home';
      this.selectedQuizId = null;
    },
    handleSwitchToRegister() {
      this.currentView = 'register';
    },
    handleSwitchToLogin() {
      this.currentView = 'login';
    },
    handleStartQuiz(quizId) {
      this.selectedQuizId = quizId;
      this.currentView = 'quiz';
    },
    handleBackToDashboard() {
      this.currentView = this.currentUser.role === 'admin' ? 'admin' : 'user';
      this.selectedQuizId = null;
    },
    logout() {
      fetch(`${API_BASE}/api/auth/logout`, { method: 'POST', credentials: 'include' })
        .then(() => {
        this.handleLogout();
      })
      .catch(err => console.error('Logout failed:', err));
    }
  }
};
</script>
<style scoped>
nav.navbar {
  margin-bottom: 2rem;
}

.app-footer {
  font-size: 1rem;
  position: fixed;
  bottom: 0;
  width: 100%;
  height: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1030;
}

.footer-links a {
  text-decoration: none;
}

.footer-links a:hover {
  text-decoration: underline;
}
</style>