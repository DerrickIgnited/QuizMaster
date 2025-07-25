<template>
  <div class="container-fluid">
    <div class="container py-5">

      <!-- Welcome Card -->
      <div class="row justify-content-center mb-4">
        <div class="col-md-10">
          <div class="glass-card p-5 text-center">
            <i class="fas fa-graduation-cap fa-3x text-white mb-3"></i>
            <h2 class="text-white fw-bold mb-3">Welcome to Quiz Master</h2>
            <p class="text-white-50">
              Your ultimate quiz platform to test your knowledge, track your progress, and challenge yourself or your friends!
            </p>
          </div>
        </div>
      </div>

      <!-- Features -->
      <div class="row justify-content-center mb-4">
        <div class="col-md-5 mb-4" v-for="(feature, i) in features" :key="i">
          <div class="glass-card p-4 h-100">
            <h5 class="text-white"><i :class="feature.icon + ' me-2 text-' + feature.color"></i>{{ feature.title }}</h5>
            <p class="text-white-50">{{ feature.desc }}</p>
          </div>
        </div>
      </div>

      <!-- Spline Viewer -->
      <div class="row justify-content-center mb-4" style="background-color: transparent;">
        <div class="col-md-10" style="background-color: transparent;">
          <spline-viewer url="https://prod.spline.design/9PvjbUlSfD1a59Oj/scene.splinecode" style="width: 100%; height: 500px;"></spline-viewer>
        </div>
      </div>

      <!-- Why Choose Quiz Master -->
      <div class="row justify-content-center mb-4">
        <div class="col-md-10">
          <div class="glass-card p-4">
            <h5 class="text-white mb-3"><i class="fas fa-lightbulb me-2"></i>Why Choose Quiz Master?</h5>
            <ul class="text-white-50 list-unstyled ps-3">
              <li><i class="fas fa-check text-success me-2"></i>No ads, no distractions</li>
              <li><i class="fas fa-check text-success me-2"></i>Gamified learning experience</li>
              <li><i class="fas fa-check text-success me-2"></i>Adaptive scoring engine</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Stats Section -->
      <div class="row justify-content-center mb-4">
        <div class="col-md-10">
          <div class="glass-card p-4 text-center">
            <h5 class="text-white mb-3"><i class="fas fa-signal me-2"></i>Platform Stats</h5>
            <div class="row text-white-50">
              <div class="col-md-4">
                <h3 class="fw-bold text-white">1.2K+</h3>
                <p>Registered Users</p>
              </div>
              <div class="col-md-4">
                <h3 class="fw-bold text-white">5K+</h3>
                <p>Quizzes Taken</p>
              </div>
              <div class="col-md-4">
                <h3 class="fw-bold text-white">92%</h3>
                <p>Avg User Accuracy</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Testimonials -->
      <div class="row justify-content-center mb-4">
        <div class="col-md-5 mb-3" v-for="(testimonial, index) in testimonials" :key="index">
          <div class="glass-card p-3 text-white-50 fst-italic">
            <p>"{{ testimonial.text }}"</p>
            <small class="text-white d-block mt-2 text-end">— {{ testimonial.author }}</small>
          </div>
        </div>
      </div>

      <!-- Login/Register CTA -->
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="glass-card p-4 text-center">
            <h4 class="text-white mb-3">Ready to challenge your brain?</h4>
            <button @click="$emit('switch-to-login')" class="btn modern-btn me-2"><i class="fas fa-sign-in-alt me-2"></i>Login</button>
            <button @click="$emit('switch-to-register')" class="btn modern-btn me-2"><i class="fas fa-user-plus me-2"></i>Register</button>
            <button @click="$emit('switch-to-about-us')" class="btn modern-btn me-2">About Us</button>
            <button @click="$emit('switch-to-contact-us')" class="btn modern-btn me-2">Contact Us</button>
          </div>
        </div>
      </div>
      
      <!-- Modals -->
      <Login v-if="showLogin" @close="showLogin = false" @login-success="onLoginSuccess"/>
      <Register v-if="showRegister" @close="showRegister = false" @register-success="onRegisterSuccess"/>

    </div>
  </div>
</template>

<script>
import Register from './Register.vue'
import Login from './Login.vue'

export default {
  name: 'Home',
  components: {
    Register,
    Login
  },
  data() {
    return {
      showLogin: false,
      showRegister: false,
      features: [
        {
          title: 'Create & Attempt Quizzes',
          desc: 'Build your own quizzes or test your skills with existing ones.',
          icon: 'fas fa-pen',
          color: 'success'
        },
        {
          title: 'Track Progress',
          desc: 'Get insights into your performance with score history.',
          icon: 'fas fa-chart-line',
          color: 'info'
        },
        {
          title: 'Compete with Friends',
          desc: 'Challenge your friends and climb the leaderboard.',
          icon: 'fas fa-user-friends',
          color: 'warning'
        },
        {
          title: 'Admin Dashboard',
          desc: 'Manage quizzes, users, and monitor platform activity.',
          icon: 'fas fa-cogs',
          color: 'danger'
        }
      ],
      testimonials: [
        { text: 'Quiz Master helped me prep smarter for my UPSC.', author: 'Aarav, Delhi' },
        { text: 'We use it for our college quiz competitions!', author: 'Shruti, VIT Chennai' }
      ]
    };
  },
  mounted() {
    const script = document.createElement('script');
    script.type = 'module';
    script.src = 'https://unpkg.com/@splinetool/viewer@1.10.37/build/spline-viewer.js';
    document.head.appendChild(script);
  },
  methods: {
    onLoginSuccess(user) {
      this.$emit('login-success', user);
      this.showLogin = false;
    },
    onRegisterSuccess(user) {
      this.$emit('register-success', user);
      this.showRegister = false;
    }
  }
};
</script>

<style scoped>
.glass-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
}
</style>
