<!-- filepath: /Users/derricksamuel/Desktop/IITM/quiz_master_23f2001426/frontend/src/components/Register.vue -->
<template>
  <div class="container-fluid h-100 d-flex align-items-center justify-content-center">
    <div class="glass-card p-5" style="width: 100%; max-width: 500px;">
      <div class="text-center mb-4">
        <i class="fas fa-user-plus fa-3x text-white mb-3"></i>
        <h2 class="text-white fw-bold">Create Account</h2>
        <p class="text-white-50">Join Quiz Master today</p>
      </div>
      <form @submit.prevent="register">
        <div class="row">
          <div class="col-md-6 mb-3">
            <input v-model="user.username" type="email" class="form-control bg-transparent border-white text-white" placeholder="Email" required>
          </div>
          <div class="col-md-6 mb-3">
            <input v-model="user.full_name" type="text" class="form-control bg-transparent border-white text-white" placeholder="Full Name" required>
          </div>
        </div>
        <div class="row">
          <div class="col-md-6 mb-3">
            <input v-model="user.password" type="password" class="form-control bg-transparent border-white text-white" placeholder="Password" required>
          </div>
          <div class="col-md-6 mb-3">
            <select v-model="user.qualification" class="form-control bg-transparent border-white text-white" required>
              <option value="">Select Qualification</option>
              <option value="Pre-school">Pre-school</option>
              <option value="School">School</option>
              <option value="College">College</option>
              <option value="University">University</option>
              <option value="Other">Other</option>
            </select>
          </div>
        </div>
        <div class="mb-4">
          <input v-model="user.dob" type="date" class="form-control bg-transparent border-white text-white">
        </div>
        <button type="submit" class="btn modern-btn w-100 py-3 mb-3">
          <i class="fas fa-user-plus me-2"></i>Create Account
        </button>
        <div class="text-center">
          <button type="button" @click="$emit('switch-to-login')" class="btn btn-link text-white">
            Already have an account? Sign In
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
      user: { username: '', password: '', full_name: '', qualification: '', dob: '' }
    }
  },
  methods: {
    async register() {
      try {
        const response = await fetch(`${API_BASE}/api/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.user)
        });
        const data = await response.json();
        if (data.success) {
          alert('Registration successful! Please login.');
          this.$emit('switch-to-login');
        } else {
          alert(data.message);
        }
      } catch (error) {
        alert('Registration failed');
      }
    }
  }
}
</script>
<style scoped>
input::placeholder,
textarea::placeholder,
select::placeholder {
  color: #ccc;
  opacity: 1;
}
</style>