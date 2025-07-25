<template>
  <div class="container-fluid h-100 d-flex align-items-center justify-content-center">
    <div class="glass-card p-5" style="width: 100%; max-width: 600px;">
      <h2 class="text-pink fw-bold">Profile</h2>
      <h4 class="text-white fw-bold">Welcome to your profile!</h4>
      <div v-if="user">
        <p style="color: white;"><strong>Email:</strong> {{ user.username }}</p>
        <p style="color: white;"><strong>Full Name:</strong> {{ user.full_name }}</p>
        <p style="color: white;"><strong>Qualification:</strong> {{ user.qualification }}</p>
        <p style="color: white;"><strong>Date of Birth:</strong> {{ user.dob }}</p>
      </div>
      <div v-else>
        <p style="color: white;">Loading...</p>
      </div>
      <button class="btn modern-btn me-2" @click="isEditing = true" v-if="user">Update Profile</button>
      <button class="btn modern-btn" @click="isChangingPassword = true" v-if="user">Change Password</button>

      <div v-if="isEditing">
        <form @submit.prevent="updateProfile">
          <div class="mb-3">
            <label for="username" class="form-label text-white">Email</label>
            <input type="email" class="form-control" id="username" v-model="editedUser.username" required>
          </div>
          <div class="mb-3">
            <label for="full_name" class="form-label text-white">Full Name</label>
            <input type="text" class="form-control" id="full_name" v-model="editedUser.full_name" required>
          </div>
          <div class="mb-3">
            <label for="qualification" class="form-label text-white">Qualification</label>
            <select class="form-control bg-transparent border-white text-white" id="qualification" v-model="editedUser.qualification">
              <option value="">Select Qualification</option>
              <option value="Pre-school">Pre-school</option>
              <option value="School">School</option>
              <option value="College">College</option>
              <option value="University">University</option>
              <option value="Other">Other</option>
            </select>
          </div>
          <div class="mb-3">
            <label for="dob" class="form-label text-white">Date of Birth</label>
            <input type="date" class="form-control" id="dob" v-model="editedUser.dob">
          </div>
          <button type="submit" class="btn modern-btn me-2">Save</button>
          <button type="button" class="btn modern-btn me-2" @click="isEditing = false">Cancel</button>
        </form>
      </div>

      <div v-if="isChangingPassword">
        <form @submit.prevent="changePassword">
          <div class="mb-3">
            <label for="currentPassword" class="form-label text-white">Current Password</label>
            <input type="password" class="form-control" id="currentPassword" v-model="passwordData.currentPassword" required>
          </div>
          <div class="mb-3">
            <label for="newPassword" class="form-label text-white">New Password</label>
            <input type="password" class="form-control" id="newPassword" v-model="passwordData.newPassword" required>
          </div>
          <div class="mb-3">
            <label for="confirmNewPassword" class="form-label text-white">Confirm New Password</label>
            <input type="password" class="form-control" id="confirmNewPassword" v-model="passwordData.confirmNewPassword" required>
          </div>
          <button type="submit" class="btn modern-btn me-2">Change Password</button>
          <button type="button" class="btn modern-btn me-2" @click="isChangingPassword = false">Cancel</button>
          <div v-if="passwordChangeError" class="text-danger">{{ passwordChangeError }}</div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
const API_BASE = 'http://localhost:8001';
export default {
  name: 'Profile',
  data() {
    return {
      user: null,
      isEditing: false,
      editedUser: {
        username: '',
        full_name: '',
        qualification: '',
        dob: ''
      },
      isChangingPassword: false,
      passwordData: {
        currentPassword: '',
        newPassword: '',
        confirmNewPassword: ''
      },
      passwordChangeError: ''
    };
  },
  mounted() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const response = await fetch(`${API_BASE}/api/user/profile`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include'
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.user = await response.json();
        this.editedUser = { ...this.user }; // Clone for editing
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    },

    async updateProfile() {
      try {
        const response = await fetch(`${API_BASE}/api/user/profile`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.editedUser),
          credentials: 'include'
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const updatedUser = await response.json();
        this.user = updatedUser;
        this.isEditing = false;
        alert('Profile updated successfully!');
      } catch (error) {
        console.error('Error updating profile:', error);
        alert('Profile update failed.');
      }
    },

    async changePassword() {
      this.passwordChangeError = '';

      const { currentPassword, newPassword, confirmNewPassword } = this.passwordData;

      // Validation Checks
      if (newPassword === currentPassword) {
        this.passwordChangeError = 'New password cannot be the same as current password.';
        return;
      }

      if (newPassword !== confirmNewPassword) {
        this.passwordChangeError = 'New passwords do not match.';
        return;
      }

      try {
        const response = await fetch(`${API_BASE}/api/user/change-password`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            current_password: currentPassword,
            new_password: newPassword
          }),
          credentials: 'include'
        });

        if (!response.ok) {
          const errorData = await response.json();
          this.passwordChangeError = errorData.message || 'Failed to change password.';
          return;
        }

        alert('Password changed successfully!');
        this.isChangingPassword = false;
        this.passwordData = {
          currentPassword: '',
          newPassword: '',
          confirmNewPassword: ''
        };
      } catch (error) {
        console.error('Error changing password:', error);
        alert('Failed to change password.');
      }
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
</style>