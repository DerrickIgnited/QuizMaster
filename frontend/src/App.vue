<!-- filepath: /Users/derricksamuel/Desktop/IITM/quiz_master_23f2001426/frontend/src/App.vue -->
<template>
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
</template>

<script>
import Login from './components/Login.vue';
import Register from './components/Register.vue';
import AdminDashboard from './components/AdminDashboard.vue';
import UserDashboard from './components/UserDashboard.vue';
import QuizAttempt from './components/QuizAttempt.vue';

export default {
  components: {
    Login,
    Register,
    AdminDashboard,
    UserDashboard,
    QuizAttempt
  },
  data() {
    return {
      currentView: 'login',
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
      this.currentView = 'login';
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
    }
  }
};
</script>