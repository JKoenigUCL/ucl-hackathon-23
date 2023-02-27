<script setup>
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/css/index.css";
</script>

<template>
  <main id="new-user-view">
    <loading
      v-model:active="isLoading"
      :is-full-page="fullPage"
      :height="128"
      :width="128"
      :opacity="1.0"
      background-color="black"
    />
    <h1>Create a New Account</h1>
    <form id="new-user-form" onsubmit="return false;">
      <input type="text" v-model="username" placeholder="Choose a Username" />
      <input type="password" v-model="password" placeholder="Choose a Password" />
      <input type="password" v-model="confirmPassword" placeholder="Confirm Password" />
      <button @click="createUser">Create Account</button>
      <p
        class="error"
        :style="{ visibility: err_create_failed ? 'visible' : 'hidden' }"
      >
        Error: failed to create account
      </p>
    </form>
  </main>
</template>
<script>
import { mapWritableState } from "pinia";
import { useAuthStore } from "@/stores/auth";

export default {
  methods: {
    createUser() {
      this.isLoading = true;
      if (this.password !== this.confirmPassword) {
        this.err_create_failed = true;
        this.isLoading = false;
        return;
      }
      this.$http
        .post(this.$backendUrl + "user/createapi", null, {
          params: {
            username: this.username,
            password: this.password,
          },
        })
        .then((response) => {
          if (response.data["message"] == "success") {
            this.logged_in = this.username;
            this.$router.push("/search");
          } else {
            this.err_create_failed = true;
          }
        })
        .catch(() => {
          this.err_create_failed = true;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
  },
  data() {
    return {
      err_create_failed: false,
      isLoading: false,
      username: "",
      password: "",
      confirmPassword: "",
    };
  },
  computed: {
    ...mapWritableState(useAuthStore, ["logged_in"]),
  },
};
</script>