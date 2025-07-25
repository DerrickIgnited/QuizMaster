<template>
  <div class="container-fluid h-100 d-flex align-items-center justify-content-center">
    <div class="glass-card p-5" style="width: 100%; max-width: 600px;">
      <div class="text-center mb-4">
        <h2 class="text-pink fw-bold">About Us</h2>
        <p class="text-white-50">
          Welcome to Quiz Master! We are dedicated to providing the best quiz platform to help you test your knowledge, track your progress, and challenge yourself or your friends. Our mission is to make learning fun and engaging through gamified quizzes and adaptive scoring.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutUs'
}
</script>

<style scoped>
.glass-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
}
.text-pink {
  color: #ff007f; /* Use pink color consistent with Login.vue */
}
</style>
