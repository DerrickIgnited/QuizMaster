<template>
  <div class="container-fluid h-100 d-flex align-items-center justify-content-center">
    <div class="glass-card p-5" style="width: 100%; max-width: 800px;">
      <div class="text-center mb-4">
        <h2 class="text-pink fw-bold" style="font-size: 2rem;">Contact Us</h2>
        <p class="text-white-50" style="font-size: 1.1rem;">
          Have questions or feedback? We'd love to hear from you! Reach out to us at support@quizmaster.com or use the contact form on our website.
        </p>
      </div>
      <div class="mt-4">
        <form @submit.prevent="submitForm">
          <div class="mb-3">
            <label for="name" class="form-label text-white">Name</label>
            <input type="text" class="form-control" id="name" v-model="name" required>
          </div>
          <div class="mb-3">
            <label for="email" class="form-label text-white">Email address</label>
            <input type="email" class="form-control" id="email" v-model="email" required>
          </div>
          <div class="mb-3">
            <label for="message" class="form-label text-white">Message</label>
            <textarea class="form-control" id="message" rows="3" v-model="message" required></textarea>
          </div>
          <button type="submit" class="btn btn-pink">Submit</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ContactUs',
  data() {
    return {
      name: '',
      email: '',
      message: ''
    };
  },
  methods: {
    submitForm() {
      // In a real application, you would send this data to a backend API
      // For this example, we'll just log it to the console.
      console.log('Form submitted:', {
        name: this.name,
        email: this.email,
        message: this.message
      });
      alert('Thank you for your message!');
      this.name = '';
      this.email = '';
      this.message = '';
    }
  }
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
.btn-pink {
  background-color: #ff007f;
  border-color: #ff007f;
}
</style>
