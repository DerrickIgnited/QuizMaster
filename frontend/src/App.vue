<template>
  <Starfield />

  <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4">
    <a class="navbar-brand fw-bold" href="#" @click.prevent="currentView = 'home'">
      <i class="fas fa-graduation-cap me-2"></i> Quiz Master
    </a>
    <div class="navbar-buttons">
      <button v-if="currentUser" @click="currentView = 'profile'" class="btn modern-btn me-2">
        <i class="fas fa-user me-2"></i>Profile
      </button>
      <button v-if="currentUser" @click="currentView = userDashboardRoute" class="btn modern-btn me-2">
        <i class="fas fa-tachometer-alt me-2"></i>Dashboard
      </button>
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

  <div class="content-wrapper">
    <Login v-if="currentView === 'login'"
           @login-success="handleLoginSuccess"
           @switch-to-register="handleSwitchToRegister" />
    <Register v-else-if="currentView === 'register'"
              @switch-to-login="handleSwitchToLogin" />
    <AdminDashboard v-else-if="currentView === 'admin'"
                    @logout="handleLogout" />
<UserDashboard ref="userDashboard" v-else-if="currentView === 'user'"
               :user="currentUser"
               @logout="handleLogout"
               @start-quiz="handleStartQuiz" />
<QuizAttempt v-else-if="currentView === 'quiz'"
             :quiz-id="selectedQuizId"
             @back-to-dashboard="handleBackToDashboard" />
    <Home v-else-if="currentView === 'home'"
          @switch-to-login="handleSwitchToLogin"
          @switch-to-register="handleSwitchToRegister"
          @switch-to-about-us="handleSwitchToAboutus"
          @switch-to-contact-us="handleSwitchToContactus" />
    <AboutUs v-else-if="currentView === 'aboutus'" />
    <ContactUs v-else-if="currentView === 'contactus'" />
    <Profile v-else-if="currentView === 'profile'" />
  </div>

  <Chatbot v-if="currentView !== 'quiz'" />

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
import Chatbot from './components/Chatbot.vue';
import AboutUs from './components/AboutUs.vue';
import ContactUs from './components/ContactUs.vue';
import Profile from './components/Profile.vue';

const API_BASE = 'http://localhost:8001';
export default {
  components: {
    Starfield,
    Home,
    Login,
    Register,
    AdminDashboard,
    UserDashboard,
    QuizAttempt,
    Chatbot,
    AboutUs,
    ContactUs,
    Profile
  },
  data() {
    return {
      currentView: 'home',
      currentUser: null,
      selectedQuizId: null
    };
  },
  created() {
    // Load user from localStorage if available
    const userStr = localStorage.getItem('currentUser');
    if (userStr) {
      try {
        const user = JSON.parse(userStr);
        this.currentUser = user;
        this.currentView = user.role === 'admin' ? 'admin' : 'user';
      } catch (e) {
        localStorage.removeItem('currentUser');
      }
    }
  },
  watch: {
    currentView(newView) {
      // Prevent access to admin dashboard if user is not admin
      if (newView === 'admin' && (!this.currentUser || this.currentUser.role !== 'admin')) {
        this.currentView = this.currentUser ? 'user' : 'login';
      }
      // Prevent access to user dashboard if user is not user
      if (newView === 'user' && (!this.currentUser || this.currentUser.role !== 'user')) {
        this.currentView = this.currentUser ? 'admin' : 'login';
      }
    }
  },
  methods: {
    handleLoginSuccess(user) {
      this.currentUser = user;
      localStorage.setItem('currentUser', JSON.stringify(user));
      if (user && user.role) {
        this.currentView = user.role === 'admin' ? 'admin' : 'user';
      }
    },
    handleLogout() {
      this.currentUser = null;
      this.currentView = 'home';
      this.selectedQuizId = null;
      localStorage.removeItem('currentUser');
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
  if (this.currentUser.role === 'user' && this.$refs.userDashboard) {
    this.$refs.userDashboard.loadDashboard();
  }
},
    logout() {
      fetch(`${API_BASE}/api/auth/logout`, { method: 'POST', credentials: 'include' })
        .then(() => {
          this.handleLogout();
        })
        .catch(err => console.error('Logout failed:', err));
    },
    handleSwitchToAboutus() {
      this.currentView = 'aboutus';
    },
    handleSwitchToContactus() {
      this.currentView = 'contactus';
    }
  },
  computed: {
    userDashboardRoute() {
      return this.currentUser?.role === 'admin' ? 'admin' : 'user';
    }
  }
};
</script>

<style scoped>
nav.navbar {
  margin-bottom: 2rem;
}

.navbar-buttons {
  margin-left: 70%;
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

.content-wrapper {
  padding-bottom: 80px;
}

</style>
