<template>
  <div class="container-fluid h-100 d-flex align-items-center justify-content-center">
    <div class="glass-card p-5" style="width: 100%; max-width: 600px;">
      <div class="text-center mb-4">
        <h2 class="text-pink fw-bold">Contact Us</h2>
        <p class="text-white-50">
          Have questions or feedback? We'd love to hear from you! Reach out to us at support@quizmaster.com or use the contact form on our website.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ContactUs'
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
