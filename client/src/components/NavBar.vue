<template>
  <div>
    <b-navbar type="dark" variant="dark" class="py-0">
      <b-navbar-nav
        class="d-flex align-items-center justify-content-between w-100"
      >
        <div class="d-flex justify-content-start">
          <h3 class="font-weight-bold text-white py-2">Cards</h3>
        </div>

        <div class="d-flex justify-content-center">
          <b-nav-item class="text-white" :to="{ name: 'dashboard' }"
            >Dashboard</b-nav-item
          >
          <b-nav-item class="text-white" :to="{ name: 'deck' }"
            >Deck</b-nav-item
          >
        </div>
        <div class="d-flex justify-content-end">
          <div v-if="this.$route.name == 'signin'" class="text-white">
            <b-nav-item class="text-white" :to="{ name: 'register' }"
              >Register</b-nav-item
            >
          </div>
          <div v-else-if="this.$route.name == 'register'" class="text-white">
            <b-nav-item class="text-white" :to="{ name: 'signin' }"
              >Login</b-nav-item
            >
          </div>
          <div v-else>
            <b-dropdown
              right
              size="lg"
              variant="link"
              toggle-class="text-decoration-none"
              no-caret
            >
              <template #button-content>
                <img
                  class="avatar avatar-16 bg-light rounded-circle p-1"
                  :src="'https://gradient-avatar.glitch.me/' + username"
                  height="40px"
                />
              </template>
              <b-dropdown-item :to="{ name: 'profile' }"
                >Profile</b-dropdown-item
              >
              <b-dropdown-item @click="onClickLogout">Logout</b-dropdown-item>
            </b-dropdown>
          </div>
        </div>
      </b-navbar-nav>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: "NavBar",
  computed: {
    username: function () {
      let email = localStorage.getItem("email");
      return (
        email.split("@")[0].charAt(0).toUpperCase() +
        email.split("@")[0].slice(1)
      );
    },
  },
  methods: {
    async onClickLogout() {
      localStorage.removeItem("email");
      localStorage.removeItem("auth-token");
      this.$router.push("/signin");
    },
  },
};
</script>

<style></style>
