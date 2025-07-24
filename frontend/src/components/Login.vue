<!-- filepath: /Users/derricksamuel/Desktop/IITM/quiz_master_23f2001426/frontend/src/components/Register.vue -->
<template>
  <div class="container-fluid h-100 d-flex align-items-center justify-content-center">
    <div class="glass-card p-5" style="width: 100%; max-width: 400px;">
      <div class="text-center mb-4">
        <i class="fas fa-graduation-cap fa-3x text-white mb-3"></i>
        <h2 class="text-white fw-bold">Quiz Master V2</h2>
        <p class="text-white-50">Sign in to your account</p>
      </div>
      <form @submit.prevent="login">
        <div class="mb-3">
          <div class="input-group">
            <span class="input-group-text bg-transparent border-white text-white">
              <i class="fas fa-envelope"></i>
            </span>
            <input v-model="credentials.username" type="email" class="form-control bg-transparent border-white text-white" placeholder="Email" required>
          </div>
        </div>
        <div class="mb-4">
          <div class="input-group">
            <span class="input-group-text bg-transparent border-white text-white">
              <i class="fas fa-lock"></i>
            </span>
            <input v-model="credentials.password" type="password" class="form-control bg-transparent border-white text-white" placeholder="Password" required>
          </div>
        </div>
        <button type="submit" class="btn modern-btn w-100 py-3 mb-3">
          <i class="fas fa-sign-in-alt me-2"></i>Sign In
        </button>
        <div class="text-center">
          <button type="button" @click="$emit('switch-to-register')" class="btn btn-link text-white">
            Don't have an account? Register
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
const API_BASE = 'http://localhost:8001';
export default {
  data() {
    return {
      credentials: { username: '', password: '' }
    }
  },
  methods: {
    async login() {
      try {
        const response = await fetch(`${API_BASE}/api/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(this.credentials)
        });
        const data = await response.json();
        if (data.success) {
          this.$emit('login-success', data.user);
        } else {
          alert(data.message);
        }
      } catch (error) {
        alert('Login failed');
      }
    }
  }
}
</script>