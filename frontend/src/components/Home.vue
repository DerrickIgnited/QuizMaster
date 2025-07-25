<template>
  <div class="home-container">
    <h1>Welcome to Quiz Master</h1>
    <p>Your ultimate quiz platform to test your knowledge and challenge yourself!</p>
    <p>Features include:</p>
    <ul>
      <li>Create and attempt quizzes</li>
      <li>Track your progress and scores</li>
      <li>Compete with friends and other users</li>
      <li>Admin dashboard for managing quizzes and users</li>
    </ul>
    <div class="buttons">
      <button @click="$emit('switch-to-login')" class="btn modern-btn me-2">Login</button>
      <button @click="$emit('switch-to-register')" class="btn modern-btn">Register</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
};
</script>

<style scoped>
.home-container {
  max-width: 600px;
  margin: 2rem auto;
  text-align: center;
}
.buttons {
  margin-top: 1.5rem;
}
.btn {
  padding: 0.5rem 1.5rem;
  font-size: 1.1rem;
  cursor: pointer;
}
</style>
