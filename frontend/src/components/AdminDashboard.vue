<template>
  <div class="container-fluid">
      <nav class="navbar navbar-expand-lg navbar-dark mb-4">
        <div class="container">
          <a class="navbar-brand fw-bold">
            <i class="fas fa-crown me-2"></i>Admin Dashboard
          </a>
          <button @click="logout" class="btn btn-outline-light">
            <i class="fas fa-sign-out-alt me-2"></i>Logout
          </button>
        </div>
      </nav>
      
      <div class="container">
        <div class="row">
          <div class="col-md-3 mb-4">
            <div class="glass-card p-4 text-center">
              <i class="fas fa-book fa-2x text-white mb-3"></i>
              <h5 class="text-white">Subjects</h5>
              <h3 class="text-white fw-bold">{{stats.subjects}}</h3>
            </div>
          </div>
          <div class="col-md-3 mb-4">
            <div class="glass-card p-4 text-center">
              <i class="fas fa-bookmark fa-2x text-white mb-3"></i>
              <h5 class="text-white">Chapters</h5>
              <h3 class="text-white fw-bold">{{stats.chapters}}</h3>
            </div>
          </div>
          <div class="col-md-3 mb-4">
            <div class="glass-card p-4 text-center">
              <i class="fas fa-question-circle fa-2x text-white mb-3"></i>
              <h5 class="text-white">Quizzes</h5>
              <h3 class="text-white fw-bold">{{stats.quizzes}}</h3>
            </div>
          </div>
          <div class="col-md-3 mb-4">
            <div class="glass-card p-4 text-center">
              <i class="fas fa-users fa-2x text-white mb-3"></i>
              <h5 class="text-white">Users</h5>
              <h3 class="text-white fw-bold">{{stats.users}}</h3>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-md-4 mb-4">
            <div class="glass-card p-4">
              <h5 class="text-white mb-3"><i class="fas fa-plus me-2"></i>Add Subject</h5>
              <form @submit.prevent="addSubject">
                <input v-model="newSubject.name" class="form-control bg-transparent border-white text-white mb-2" placeholder="Subject Name" required>
                <textarea v-model="newSubject.description" class="form-control bg-transparent border-white text-white mb-3" placeholder="Description"></textarea>
                <button type="submit" class="btn modern-btn w-100">Add Subject</button>
              </form>
              <h5 class="text-white mt-4 mb-3">Existing Subjects</h5>
              <ul class="list-group">
                <li v-for="subject in subjects" :key="subject.id" class="list-group-item d-flex justify-content-between align-items-center bg-dark text-white">
                  {{ subject.name }}
                  <button @click="deleteSubject(subject.id)" class="btn btn-sm btn-danger">Delete</button>
                </li>
              </ul>
            </div>
          </div>
          
          <div class="col-md-4 mb-4">
            <div class="glass-card p-4">
              <h5 class="text-white mb-3"><i class="fas fa-plus me-2"></i>Add Chapter</h5>
              <form @submit.prevent="addChapter">
                <select v-model="newChapter.subject_id" class="form-control bg-transparent border-white text-white mb-2" required>
                  <option value="">Select Subject</option>
                  <option v-for="subject in subjects" :value="subject.id">{{subject.name}}</option>
                </select>
                <input v-model="newChapter.name" class="form-control bg-transparent border-white text-white mb-2" placeholder="Chapter Name" required>
                <textarea v-model="newChapter.description" class="form-control bg-transparent border-white text-white mb-3" placeholder="Description"></textarea>
                <button type="submit" class="btn modern-btn w-100">Add Chapter</button>
              </form>
              <h5 class="text-white mt-4 mb-3">Existing Chapters</h5>
              <ul class="list-group">
                <li v-for="chapter in chapters" :key="chapter.id" class="list-group-item d-flex justify-content-between align-items-center bg-dark text-white">
                  {{ chapter.name }}
                  <button @click="deleteChapter(chapter.id)" class="btn btn-sm btn-danger">Delete</button>
                </li>
              </ul>
            </div>
          </div>
          
          <div class="col-md-4 mb-4">
            <div class="glass-card p-4">
              <h5 class="text-white mb-3"><i class="fas fa-plus me-2"></i>Add Quiz</h5>
              <form @submit.prevent="addQuiz">
                <select v-model="newQuiz.chapter_id" class="form-control bg-transparent border-white text-white mb-2" required>
                  <option value="">Select Chapter</option>
                  <option v-for="chapter in chapters" :value="chapter.id">{{chapter.name}}</option>
                </select>
                <input v-model="newQuiz.date_of_quiz" type="date" class="form-control bg-transparent border-white text-white mb-2" required>
                <input v-model="newQuiz.time_duration" type="number" class="form-control bg-transparent border-white text-white mb-2" placeholder="Duration (minutes)" required>
                <textarea v-model="newQuiz.remarks" class="form-control bg-transparent border-white text-white mb-3" placeholder="Remarks"></textarea>
                <button type="submit" class="btn modern-btn w-100">Add Quiz</button>
              </form>
            </div>
          </div>
        </div>

        <div class="glass-card p-4 mb-4">
          <h5 class="text-white mb-3"><i class="fas fa-list me-2"></i>Manage Quizzes</h5>
          <div class="table-responsive">
            <table class="table table-dark table-striped">
              <thead>
                <tr>
                  <th>Subject</th>
                  <th>Chapter</th>
                  <th>Date</th>
                  <th>Duration</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="quiz in quizzes" :key="quiz.id">
                  <td>{{quiz.subject_name}}</td>
                  <td>{{quiz.chapter_name}}</td>
                  <td>{{quiz.date_of_quiz}}</td>
                  <td>{{quiz.time_duration}} min</td>
                  <td>
                    <button @click="manageQuestions(quiz.id)" class="btn btn-sm btn-primary me-2">
                      <i class="fas fa-question me-1"></i>Questions
                    </button>
                    <button @click="deleteQuiz(quiz.id)" class="btn btn-sm btn-danger">
                      <i class="fas fa-trash me-1"></i>Delete
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Questions Modal -->
        <div v-if="selectedQuizId" class="glass-card p-4">
          <h5 class="text-white mb-3"><i class="fas fa-question-circle me-2"></i>Manage Questions</h5>
          <form @submit.prevent="addQuestion" class="mb-4">
            <textarea v-model="newQuestion.question_statement" class="form-control bg-transparent border-white text-white mb-2" placeholder="Question Statement" required></textarea>
            <div class="row">
              <div class="col-md-6">
                <input v-model="newQuestion.option1" class="form-control bg-transparent border-white text-white mb-2" placeholder="Option 1" required>
                <input v-model="newQuestion.option2" class="form-control bg-transparent border-white text-white mb-2" placeholder="Option 2" required>
              </div>
              <div class="col-md-6">
                <input v-model="newQuestion.option3" class="form-control bg-transparent border-white text-white mb-2" placeholder="Option 3" required>
                <input v-model="newQuestion.option4" class="form-control bg-transparent border-white text-white mb-2" placeholder="Option 4" required>
              </div>
            </div>
            <select v-model="newQuestion.correct_answer" class="form-control bg-transparent border-white text-white mb-3" required>
              <option value="">Select Correct Answer</option>
              <option value="1">Option 1</option>
              <option value="2">Option 2</option>
              <option value="3">Option 3</option>
              <option value="4">Option 4</option>
            </select>
            <button type="submit" class="btn modern-btn me-2">Add Question</button>
            <button @click="selectedQuizId = null" type="button" class="btn btn-secondary">Close</button>
          </form>
          
          <div class="table-responsive">
            <table class="table table-dark">
              <thead>
                <tr>
                  <th>Question</th>
                  <th>Options</th>
                  <th>Correct</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="question in questions" :key="question.id">
                  <td>{{question.question_statement}}</td>
                  <td>
                    <small>
                      1: {{question.option1}}<br>
                      2: {{question.option2}}<br>
                      3: {{question.option3}}<br>
                      4: {{question.option4}}
                    </small>
                  </td>
                  <td>Option {{question.correct_answer}}</td>
                  <td>
                    <button @click="deleteQuestion(question.id)" class="btn btn-sm btn-danger">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
const API_BASE = 'http://localhost:8001';
export default {
  data() {
    return {
      stats: { subjects: 0, chapters: 0, quizzes: 0, users: 0 },
      subjects: [],
      chapters: [],
      quizzes: [],
      questions: [],
      selectedQuizId: null,
      newSubject: { name: '', description: '' },
      newChapter: { name: '', description: '', subject_id: '' },
      newQuiz: { chapter_id: '', date_of_quiz: '', time_duration: '', remarks: '' },
      newQuestion: { question_statement: '', option1: '', option2: '', option3: '', option4: '', correct_answer: '' }
    }
  },
  async mounted() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      try {
        const [subjectsRes, chaptersRes, quizzesRes] = await Promise.all([
          fetch(`${API_BASE}/api/admin/subjects`, { credentials: 'include' }),
          fetch(`${API_BASE}/api/admin/chapters`, { credentials: 'include' }),
          fetch(`${API_BASE}/api/admin/quizzes`, { credentials: 'include' })
        ]);
        
        this.subjects = await subjectsRes.json();
        this.chapters = await chaptersRes.json();
        this.quizzes = await quizzesRes.json();
        
        this.stats = {
          subjects: this.subjects.length,
          chapters: this.chapters.length,
          quizzes: this.quizzes.length,
          users: 50 // Mock data
        };
      } catch (error) {
        console.error('Failed to load data:', error);
      }
    },
    async addSubject() {
      try {
        const response = await fetch(`${API_BASE}/api/admin/subjects`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(this.newSubject)
        });
        
        if (response.ok) {
          this.newSubject = { name: '', description: '' };
          await this.loadData();
        }
      } catch (error) {
        alert('Failed to add subject');
      }
    },
    async addChapter() {
      try {
        const response = await fetch(`${API_BASE}/api/admin/chapters`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(this.newChapter)
        });
        
        if (response.ok) {
          this.newChapter = { name: '', description: '', subject_id: '' };
          await this.loadData();
        }
      } catch (error) {
        alert('Failed to add chapter');
      }
    },
    async addQuiz() {
      try {
        const response = await fetch(`${API_BASE}/api/admin/quizzes`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(this.newQuiz)
        });
        
        if (response.ok) {
          this.newQuiz = { chapter_id: '', date_of_quiz: '', time_duration: '', remarks: '' };
          await this.loadData();
        }
      } catch (error) {
        alert('Failed to add quiz');
      }
    },
    async manageQuestions(quizId) {
      this.selectedQuizId = quizId;
      try {
        const response = await fetch(`${API_BASE}/api/admin/questions/${quizId}`, { credentials: 'include' });
        this.questions = await response.json();
      } catch (error) {
        console.error('Failed to load questions:', error);
      }
    },
    async addQuestion() {
      try {
        const response = await fetch(`${API_BASE}/api/admin/questions/${this.selectedQuizId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(this.newQuestion)
        });
        
        if (response.ok) {
          this.newQuestion = { question_statement: '', option1: '', option2: '', option3: '', option4: '', correct_answer: '' };
          await this.manageQuestions(this.selectedQuizId);
        }
      } catch (error) {
        alert('Failed to add question');
      }
    },
    async deleteSubject(subjectId) {
      if (!confirm('Are you sure you want to delete this subject? This will also delete related chapters, quizzes, and questions.')) return;
      try {
        const response = await fetch(`${API_BASE}/api/admin/subjects/${subjectId}`, {
          method: 'DELETE',
          credentials: 'include'
        });
        if (response.ok) {
          await this.loadData();
          if (this.selectedQuizId) {
            this.selectedQuizId = null;
            this.questions = [];
          }
        } else {
          alert('Failed to delete subject');
        }
      } catch (error) {
        alert('Failed to delete subject');
      }
    },
    async deleteChapter(chapterId) {
      if (!confirm('Are you sure you want to delete this chapter? This will also delete related quizzes and questions.')) return;
      try {
        const response = await fetch(`${API_BASE}/api/admin/chapters/${chapterId}`, {
          method: 'DELETE',
          credentials: 'include'
        });
        if (response.ok) {
          await this.loadData();
          if (this.selectedQuizId) {
            this.selectedQuizId = null;
            this.questions = [];
          }
        } else {
          alert('Failed to delete chapter');
        }
      } catch (error) {
        alert('Failed to delete chapter');
      }
    },
    async deleteQuiz(quizId) {
      if (!confirm('Are you sure you want to delete this quiz? This will also delete related questions.')) return;
      try {
        const response = await fetch(`${API_BASE}/api/admin/quizzes/${quizId}`, {
          method: 'DELETE',
          credentials: 'include'
        });
        if (response.ok) {
          await this.loadData();
          if (this.selectedQuizId === quizId) {
            this.selectedQuizId = null;
            this.questions = [];
          }
        } else {
          alert('Failed to delete quiz');
        }
      } catch (error) {
        alert('Failed to delete quiz');
      }
    },
    async deleteQuestion(questionId) {
      if (!confirm('Are you sure you want to delete this question?')) return;
      try {
        const response = await fetch(`${API_BASE}/api/admin/questions/${this.selectedQuizId}/${questionId}`, {
          method: 'DELETE',
          credentials: 'include'
        });
        if (response.ok) {
          await this.manageQuestions(this.selectedQuizId);
        } else {
          alert('Failed to delete question');
        }
      } catch (error) {
        alert('Failed to delete question');
      }
    },
    logout() {
      fetch(`${API_BASE}/api/auth/logout`, { method: 'POST', credentials: 'include' })
        .then(() => this.$emit('logout'));
    }
  }
};
</script>
