<template>
  <div class="container-fluid">
      
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
              <input v-model="searchSubject" class="form-control bg-transparent border-white text-white mb-3" placeholder="Search Subjects">
      <ul class="list-group">
        <li v-for="subject in filteredSubjects" :key="subject.id" class="list-group-item d-flex justify-content-between align-items-center bg-dark text-white">
          <div v-if="editSubjectId !== subject.id">
            {{ subject.name }}
          </div>
          <div v-else>
            <input v-model="editSubjectData.name" class="form-control bg-transparent border-white text-white mb-1" />
            <textarea v-model="editSubjectData.description" class="form-control bg-transparent border-white text-white mb-1"></textarea>
          </div>
          <div>
            <button v-if="editSubjectId !== subject.id" @click="startEditSubject(subject)" class="btn modern-btn w-10 me-1">Edit</button>
            <div v-if="editSubjectId === subject.id" class="d-flex align-items-center">
              <button @click="updateSubject(subject.id)" class="btn modern-btn w-10 me-1">Save</button>
              <button @click="cancelEditSubject" class="btn modern-btn w-10 me-1">Cancel</button>
            </div>
            <button v-if="editSubjectId !== subject.id" @click="deleteSubject(subject.id)" class="btn modern-btn w-10">Delete</button>
          </div>
        </li>
      </ul>
            </div>
          </div>
          
          <div class="col-md-4 mb-4">
            <div class="glass-card p-4">
              <h5 class="text-white mb-3"><i class="fas fa-plus me-2"></i>Add Chapter</h5>
              <form @submit.prevent="addChapter">
              <select v-model.number="newChapter.subject_id" class="form-control bg-transparent border-white text-white mb-2" required>
                  <option value="">Select Subject</option>
                  <option v-for="subject in subjects" :value="subject.id">{{subject.name}}</option>
                </select>
                <input v-model="newChapter.name" class="form-control bg-transparent border-white text-white mb-2" placeholder="Chapter Name" required>
                <textarea v-model="newChapter.description" class="form-control bg-transparent border-white text-white mb-3" placeholder="Description"></textarea>
                <button type="submit" class="btn modern-btn w-100">Add Chapter</button>
              </form>
              <h5 class="text-white mt-4 mb-3">Existing Chapters</h5>
              <input v-model="searchChapter" class="form-control bg-transparent border-white text-white mb-3" placeholder="Search Chapters">
      <ul class="list-group">
        <li v-for="chapter in filteredChapters" :key="chapter.id" class="list-group-item d-flex justify-content-between align-items-center bg-dark text-white">
          <div v-if="editChapterId !== chapter.id">
            {{ chapter.name }}
          </div>
          <div v-else>
            <select v-model.number="editChapterData.subject_id" class="form-control bg-transparent border-white text-white mb-1">
              <option v-for="subject in subjects" :value="subject.id" :key="subject.id">{{ subject.name }}</option>
            </select>
            <input v-model="editChapterData.name" class="form-control bg-transparent border-white text-white mb-1" />
            <textarea v-model="editChapterData.description" class="form-control bg-transparent border-white text-white mb-1"></textarea>
          </div>
          <div>
            <button v-if="editChapterId !== chapter.id" @click="startEditChapter(chapter)" class="btn modern-btn w-10 me-1">Edit</button>
            <div v-if="editChapterId === chapter.id" class="d-flex align-items-center">
              <button @click="updateChapter(chapter.id)" class="btn modern-btn w-10 me-1">Save</button>
              <button @click="cancelEditChapter" class="btn modern-btn w-10 me-1">Cancel</button>
            </div>
            <button v-if="editChapterId !== chapter.id" @click="deleteChapter(chapter.id)" class="btn modern-btn w-10">Delete</button>
          </div>
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
              <br>
              <div class="col-md-6">
                <button @click="triggerReminders" class="btn btn-sm modern-btn">
                  <i class="fas fa-bell me-1"></i>Trigger Exports
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="glass-card p-4 mb-4">
          <h5 class="text-white mb-3"><i class="fas fa-list me-2"></i>Manage Quizzes</h5>
          <input v-model="searchQuiz" class="form-control bg-transparent border-white text-white mb-3" placeholder="Search Quizzes">
          <div class="table-responsive">
            <table class="table table-dark table-striped">
              <thead>
                <tr>
                  <th>Subject</th>
                  <th>Chapter</th>
                  <th>Name</th>
                  <th>Date</th>
                  <th>Duration</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="quiz in filteredQuizzes" :key="quiz.id">
                  <td>{{quiz.subject_name}}</td>
                  <td>{{quiz.chapter_name}}</td>
                  <td>{{quiz.remarks}}</td>
                  <td>{{quiz.date_of_quiz}}</td>
                  <td>{{quiz.time_duration}} min</td>
<td>
  <div v-if="editQuizId !== quiz.id" class="d-flex align-items-center">
    <button @click="manageQuestions(quiz.id)" class="btn modern-btn w-10 me-1">
      Questions
    </button>
    <button @click="startEditQuiz(quiz)" class="btn modern-btn w-10 me-1">Edit</button>
    <button @click="deleteQuiz(quiz.id)" class="btn modern-btn w-10">
      <i class="fas fa-trash me-1"></i>Delete
    </button>
  </div>
  <div v-else>
    <select v-model="editQuizData.chapter_id" class="form-control bg-transparent border-white text-white mb-2" required>
      <option value="">Select Chapter</option>
      <option v-for="chapter in chapters" :value="chapter.id" :key="chapter.id">{{ chapter.name }}</option>
    </select>
    <input v-model="editQuizData.date_of_quiz" type="date" class="form-control bg-transparent border-white text-white mb-2" required />
    <input v-model="editQuizData.time_duration" type="number" class="form-control bg-transparent border-white text-white mb-2" placeholder="Duration (minutes)" required />
    <textarea v-model="editQuizData.remarks" class="form-control bg-transparent border-white text-white mb-3" placeholder="Remarks"></textarea>
    <button @click="updateQuiz(quiz.id)" class="btn modern-btn w-10 me-1">Save</button>
    <button @click="cancelEditQuiz" class="btn modern-btn w-10 me-1">Cancel</button>
  </div>
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
            <button @click="selectedQuizId = null" type="button" class="btn modern-btn w-10">Close</button>
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
                    <div v-if="editQuestionId !== question.id">
                      <div>
                        <button @click="startEditQuestion(question)" class="btn modern-btn w-10 me-1">Edit</button>
                        <button @click="deleteQuestion(question.id)" class="btn modern-btn w-10">Delete</button>
                      </div>
                    </div>
                    <div v-else>
                      <textarea v-model="editQuestionData.question_statement" class="form-control bg-transparent border-white text-white mb-2" required></textarea>
                      <div class="row">
                        <div class="col-md-6">
                          <input v-model="editQuestionData.option1" class="form-control bg-transparent border-white text-white mb-2" placeholder="Option 1" required />
                          <input v-model="editQuestionData.option2" class="form-control bg-transparent border-white text-white mb-2" placeholder="Option 2" required />
                        </div>
                        <div class="col-md-6">
                          <input v-model="editQuestionData.option3" class="form-control bg-transparent border-white text-white mb-2" placeholder="Option 3" required />
                          <input v-model="editQuestionData.option4" class="form-control bg-transparent border-white text-white mb-2" placeholder="Option 4" required />
                        </div>
                      </div>
                      <select v-model="editQuestionData.correct_answer" class="form-control bg-transparent border-white text-white mb-3" required>
                        <option value="">Select Correct Answer</option>
                        <option value="1">Option 1</option>
                        <option value="2">Option 2</option>
                        <option value="3">Option 3</option>
                        <option value="4">Option 4</option>
                      </select>
                      <button @click="updateQuestion(question.id)" class="btn modern-btn w-10 me-1">Save</button>
                      <button @click="cancelEditQuestion" class="btn modern-btn w-10">Cancel</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <br>

      <div class="glass-card p-4 mb-4" style="width: 51.3%;margin-left: 24.4%;">
        <h5 class="text-white mb-3"><i class="fas fa-users me-2"></i>Users and Average Scores</h5>
        <input v-model="searchUser" class="form-control bg-transparent border-white text-white mb-3" placeholder="Search Users">
        <div class="table-responsive">
          <table class="table table-dark table-striped">
            <thead>
              <tr>
                <th>Email</th>
                <th>Full Name</th>
                <th>Average Score</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in filteredUsers" :key="user.id">
                <td>{{ user.username }}</td>
                <td>{{ user.full_name }}</td>
                <td>{{ user.average_score.toFixed(2) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>


</template>

<script>
const API_BASE = 'http://localhost:8001';
export default {
  data() {
    return {
      searchUser: '',
      stats: { subjects: 0, chapters: 0, quizzes: 0, users: 0 },
      subjects: [],
      chapters: [],
      quizzes: [],
      users: [],
      questions: [],
      selectedQuizId: null,
      newSubject: { name: '', description: '' },
      newChapter: { name: '', description: '', subject_id: '' },
      newQuiz: { chapter_id: '', date_of_quiz: '', time_duration: '', remarks: '' },
      newQuestion: { question_statement: '', option1: '', option2: '', option3: '', option4: '', correct_answer: '' },
      searchSubject: '',
      searchChapter: '',
      searchQuiz: '',
      editSubjectId: null,
      editSubjectData: { name: '', description: '' },
      editChapterId: null,
      editChapterData: { name: '', description: '', subject_id: '' },
      editQuizId: null,
      editQuizData: { chapter_id: '', date_of_quiz: '', time_duration: '', remarks: '' },
      editQuestionId: null,
      editQuestionData: { question_statement: '', option1: '', option2: '', option3: '', option4: '', correct_answer: '' },
    };
  },
  async mounted() {
    await this.loadData();
    await this.loadUsers();
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
            users: this.stats.users // keep current users count here
          };
        } catch (error) {
          console.error('Failed to load data:', error);
        }
      },
      async loadUsers() {
        try {
          const response = await fetch(`${API_BASE}/api/admin/users`, { credentials: 'include' });
          if (response.ok) {
            this.users = await response.json();
            this.stats.users = this.users.length; // update users count here
          } else {
            console.error('Failed to load users');
          }
        } catch (error) {
          console.error('Failed to load users:', error);
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
        // Find chapters for this subject
        const chaptersToDelete = this.chapters.filter(chap => chap.subject_id === subjectId);
        for (const chapter of chaptersToDelete) {
          // Find quizzes for this chapter
          const quizzesToDelete = this.quizzes.filter(quiz => quiz.chapter_id === chapter.id);
          for (const quiz of quizzesToDelete) {
            // Fetch questions for this quiz
            const questionsRes = await fetch(`${API_BASE}/api/admin/questions/${quiz.id}`, { credentials: 'include' });
            if (questionsRes.ok) {
              const questions = await questionsRes.json();
              // Delete each question
              for (const question of questions) {
                await fetch(`${API_BASE}/api/admin/questions/${question.id}`, {
                  method: 'DELETE',
                  credentials: 'include'
                });
              }
            }
            // Delete quiz
            await fetch(`${API_BASE}/api/admin/quizzes/${quiz.id}`, {
              method: 'DELETE',
              credentials: 'include'
            });
          }
          // Delete chapter
          await fetch(`${API_BASE}/api/admin/chapters/${chapter.id}`, {
            method: 'DELETE',
            credentials: 'include'
          });
        }
        // Delete subject
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
        // Find quizzes for this chapter
        const quizzesToDelete = this.quizzes.filter(quiz => quiz.chapter_id === chapterId);
        for (const quiz of quizzesToDelete) {
          // Fetch questions for this quiz
          const questionsRes = await fetch(`${API_BASE}/api/admin/questions/${quiz.id}`, { credentials: 'include' });
          if (questionsRes.ok) {
            const questions = await questionsRes.json();
            // Delete each question
            for (const question of questions) {
              await fetch(`${API_BASE}/api/admin/questions/${question.id}`, {
                method: 'DELETE',
                credentials: 'include'
              });
            }
          }
          // Delete quiz
          await fetch(`${API_BASE}/api/admin/quizzes/${quiz.id}`, {
            method: 'DELETE',
            credentials: 'include'
          });
        }
        // Delete chapter
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
        // Fetch questions for this quiz
        const questionsRes = await fetch(`${API_BASE}/api/admin/questions/${quizId}`, { credentials: 'include' });
        if (questionsRes.ok) {
          const questions = await questionsRes.json();
          // Delete each question
          for (const question of questions) {
            await fetch(`${API_BASE}/api/admin/questions/${question.id}`, {
              method: 'DELETE',
              credentials: 'include'
            });
          }
        }
        // Delete quiz
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
        const response = await fetch(`${API_BASE}/api/admin/questions/${questionId}`, {
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
    startEditSubject(subject) {
      this.editSubjectId = subject.id;
      this.editSubjectData = { name: subject.name, description: subject.description };
    },
    cancelEditSubject() {
      this.editSubjectId = null;
      this.editSubjectData = { name: '', description: '' };
    },
    async updateSubject(subjectId) {
      try {
        const response = await fetch(`${API_BASE}/api/admin/subjects/${subjectId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(this.editSubjectData)
        });
        if (response.ok) {
          this.cancelEditSubject();
          await this.loadData();
        } else {
          alert('Failed to update subject');
        }
      } catch (error) {
        alert('Failed to update subject');
      }
    },
    startEditChapter(chapter) {
      this.editChapterId = chapter.id;
      this.editChapterData = { name: chapter.name, description: chapter.description, subject_id: chapter.subject_id };
    },
    cancelEditChapter() {
      this.editChapterId = null;
      this.editChapterData = { name: '', description: '', subject_id: '' };
    },
    async updateChapter(chapterId) {
      try {
        const response = await fetch(`${API_BASE}/api/admin/chapters/${chapterId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(this.editChapterData)
        });
        if (response.ok) {
          this.cancelEditChapter();
          await this.loadData();
        } else {
          alert('Failed to update chapter');
        }
      } catch (error) {
        alert('Failed to update chapter');
      }
    },
    startEditQuiz(quiz) {
      this.editQuizId = quiz.id;
      this.editQuizData = { chapter_id: quiz.chapter_id, date_of_quiz: quiz.date_of_quiz, time_duration: quiz.time_duration, remarks: quiz.remarks };
    },
    cancelEditQuiz() {
      this.editQuizId = null;
      this.editQuizData = { chapter_id: '', date_of_quiz: '', time_duration: '', remarks: '' };
    },
    async updateQuiz(quizId) {
      try {
        const response = await fetch(`${API_BASE}/api/admin/quizzes/${quizId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(this.editQuizData)
        });
        if (response.ok) {
          this.cancelEditQuiz();
          await this.loadData();
        } else {
          alert('Failed to update quiz');
        }
      } catch (error) {
        alert('Failed to update quiz');
      }
    },
    startEditQuestion(question) {
      this.editQuestionId = question.id;
      this.editQuestionData = {
        question_statement: question.question_statement,
        option1: question.option1,
        option2: question.option2,
        option3: question.option3,
        option4: question.option4,
        correct_answer: question.correct_answer
      };
    },
    cancelEditQuestion() {
      this.editQuestionId = null;
      this.editQuestionData = { question_statement: '', option1: '', option2: '', option3: '', option4: '', correct_answer: '' };
    },
    async updateQuestion(questionId) {
      try {
        const response = await fetch(`${API_BASE}/api/admin/questions/${questionId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(this.editQuestionData)
        });
        if (response.ok) {
          this.cancelEditQuestion();
          await this.manageQuestions(this.selectedQuizId);
        } else {
          alert('Failed to update question');
        }
      } catch (error) {
        alert('Failed to update question');
      }
    },
    logout() {
      fetch(`${API_BASE}/api/auth/logout`, { method: 'POST', credentials: 'include' })
        .then(() => this.$emit('logout'));
    },
    async triggerReminders() {
      try {
        const response = await fetch(`${API_BASE}/api/admin/trigger-reminders`, {
          method: 'POST',
          credentials: 'include'
        });

        const data = await response.json();

        if (response.ok) {
          alert(data.message || 'Reminders triggered successfully');
        } else {
          alert(data.error || 'Failed to trigger reminders');
        }
      } catch (error) {
        alert('Something went wrong while triggering reminders.');
        console.error(error);
      }
    }
  },
  computed: {
    filteredSubjects() {
      const s = this.searchSubject.toLowerCase();
      return !s ? this.subjects : this.subjects.filter(sub => sub.name.toLowerCase().includes(s));
    },
    filteredChapters() {
      const s = this.searchChapter.toLowerCase();
      return !s ? this.chapters : this.chapters.filter(chap => chap.name.toLowerCase().includes(s));
    },
    filteredQuizzes() {
      const s = this.searchQuiz.toLowerCase();
      return !s ? this.quizzes : this.quizzes.filter(q =>
        q.subject_name?.toLowerCase().includes(s) ||
        q.chapter_name?.toLowerCase().includes(s) ||
        q.date_of_quiz?.toLowerCase().includes(s) ||
        q.time_duration?.toString().includes(s) ||
        q.remarks?.toLowerCase().includes(s)
      );
    },
    filteredUsers() {
      const s = this.searchUser.toLowerCase();
      return !s ? this.users : this.users.filter(user => user.username.toLowerCase().includes(s) || user.full_name.toLowerCase().includes(s));
    }
  }
};
</script>
<style scoped>
input::placeholder,
textarea::placeholder,
select::placeholder {
  color: #ccc;
  opacity: 1;
}
</style>