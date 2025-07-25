<template>
  <div class="container-fluid h-100 d-flex align-items-center justify-content-center">
    <div class="glass-card p-5" style="width: 100%; max-width: 800px;">
      <div class="text-center mb-">
        <h2 class="text-pink fw-bold" style="font-size: 2rem;">About Us</h2>
        <p class="text-white-50" style="font-size: 1.1rem;">
          Welcome to Quiz Master! We are dedicated to providing the best quiz platform to help you test your knowledge, track your progress, and challenge yourself or your friends. Our mission is to make learning fun and engaging through gamified quizzes and adaptive scoring. We offer a wide variety of quizzes, from general knowledge to specialized topics, all designed to help you learn and have fun.
        </p>
      </div>
      <div class="mt-4">
        <h3 class="text-white fw-bold">Frequently Asked Questions</h3>
        <div class="faq-item" v-for="(faq, index) in faqs" :key="index">
          <div class="faq-question d-flex justify-content-between align-items-center py-2" @click="faq.open = !faq.open">
            <span class="text-white">{{ faq.question }}</span>
            <span class="faq-icon" >
              <svg v-if="!faq.open" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" class="bi bi-plus" viewBox="0 0 16 16">
                <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" class="bi bi-dash" viewBox="0 0 16 16">
                <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z"/>
              </svg>
            </span>
          </div>
          <div class="faq-answer text-white-50 py-2" v-if="faq.open" v-html="faq.answer"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutUs',
  data() {
    return {
      faqs: [
        {
          question: 'How do I create an account?',
          answer: 'To create an account, click on the "Register" button and fill out the registration form.  You will need to provide a valid email address and choose a password.'
        },
        {
          question: 'How do I take a quiz?',
          answer: 'Once you are logged in, you can browse available quizzes and click on the "Start Quiz" button to begin.  Follow the instructions on the screen to answer the questions.'
        },
        {
          question: 'How can I track my progress?',
          answer: 'Your progress is automatically tracked. You can view your scores and performance history in your dashboard.'
        },
        {
          question: 'How do I reset my password?',
          answer: 'If you have forgotten your password, click on the "Forgot Password" link on the login page.  Follow the instructions sent to your registered email address to reset your password.'
        }
      ]
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
.faq-item {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.faq-question {
  cursor: pointer;
}
.faq-icon {
  width: 20px;
  text-align: center;
}
</style>
