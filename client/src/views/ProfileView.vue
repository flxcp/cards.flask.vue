<template>
  <div
    v-if="loading"
    class="h-75 d-flex justify-content-center align-items-center"
  >
    <b-spinner
      style="width: 3rem; height: 3rem"
      label="Large Spinner"
      type="grow"
    ></b-spinner>
  </div>
  <div class="my-2 mx-5" v-else>
    <h3>User Profile</h3>
    <div class="my-5">
      <span>
        <b-container>
          <b-form @submit="updateEmailForm">
            <b-form-group
              id="email"
              label-cols-sm="5"
              label-cols-lg="4"
              content-cols-sm
              content-cols-lg="7"
              label="Enter your email"
              label-for="email_title"
            >
              <b-form-input
                id="email_title"
                v-model="user_input.email"
                type="email"
                required
              >
              </b-form-input>
              <div class="my-4">
                <b-button
                  v-if="waitingForEmail"
                  size="sm"
                  type="submit"
                  pill
                  variant="dark"
                  >Update Email</b-button
                >
                <b-button v-else variant="dark" size="sm" pill disabled>
                  <b-spinner small type="grow"></b-spinner>
                  Updating
                </b-button>
              </div>
            </b-form-group>
          </b-form>
        </b-container>
      </span>
      <span>
        <b-container>
          <b-form @submit="updatePasswordForm">
            <b-form-group
              id="password"
              label-cols-sm="5"
              label-cols-lg="4"
              content-cols-sm
              content-cols-lg="7"
              label="Enter your Password"
              label-for="password_title"
            >
              <b-form-input
                id="password_title"
                v-model="user_input.password"
                type="text"
                required
              >
              </b-form-input>
              <div class="my-4">
                <b-button
                  v-if="waitingForPassword"
                  size="sm"
                  type="submit"
                  pill
                  variant="dark"
                  >Update Password</b-button
                >
                <b-button v-else variant="dark" size="sm" pill disabled>
                  <b-spinner small type="grow"></b-spinner>
                  Updating
                </b-button>
              </div>
            </b-form-group>
          </b-form>
        </b-container>
      </span>
      <span>
        <b-container>
          <b-form @submit="updateUserProfileForm">
            <b-form-group
              id="preferences"
              label-cols-sm="5"
              label-cols-lg="4"
              content-cols-sm
              content-cols-lg="7"
              label="Choose Your Preferences"
              label-for="email_format"
            >
              <b-form-group
                label="Format of Monthly Email"
                v-slot="{ email_format }"
              >
                <b-form-radio-group
                  id="email_format"
                  v-model="form.email_format"
                  :aria-describedby="email_format"
                  name="sub-email_format"
                >
                  <b-form-radio value="email">Email</b-form-radio>
                  <b-form-radio value="pdf">PDF</b-form-radio>
                </b-form-radio-group>
              </b-form-group>
              <b-form-group
                label="Communication Preference for Daily Remainder"
                v-slot="{ communication_preference }"
              >
                <b-form-radio-group
                  id="communication_preference"
                  v-model="form.communication_preference"
                  :aria-describedby="communication_preference"
                  name="sub-communication_preference"
                >
                  <b-form-radio value="email">Email</b-form-radio>
                  <b-form-radio value="chat">Chat</b-form-radio>
                </b-form-radio-group>
              </b-form-group>
              <b-form-input
                id="webhook_url"
                type="text"
                v-model="form.webhook_url"
                v-if="form.communication_preference === 'chat'"
              >
              </b-form-input>
              <div class="my-4">
                <b-button
                  v-if="waitingForPref"
                  type="submit"
                  size="sm"
                  pill
                  variant="dark"
                  >Update Preference</b-button
                >
                <b-button v-else variant="dark" size="sm" pill disabled>
                  <b-spinner small type="grow"></b-spinner>
                  Updating
                </b-button>
              </div>
            </b-form-group>
          </b-form>
        </b-container>
      </span>
    </div>
  </div>
</template>

<script>
import router from "@/router";
import { mapGetters, mapActions } from "vuex";

export default {
  name: "ProfileView",
  data() {
    return {
      loading: false,
      form: {
        email_format: "",
        webhook_url: "",
        communication_preference: "",
      },
      user_input: {
        email: "",
        password: "",
      },
      isError: false,
      errorMsg: "",
      waitingForEmail: true,
      waitingForPassword: true,
      waitingForPref: true,
    };
  },
  watch: {},
  components: {},
  methods: {
    ...mapActions([
      "getEmail",
      "getUserProfile",
      "updateEmail",
      "updateUserProfile",
      "updatePassword",
    ]),
    async updateEmailForm(event) {
      event.preventDefault();
      this.waitingForEmail = false;
      await this.updateEmail(this.user_input.email);
      this.waitingForEmail = true;
    },
    async updatePasswordForm(event) {
      event.preventDefault();
      this.waitingForPassword = false;
      try {
        let res = await fetch(`https://flshcard.herokuapp.com/api/password/`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
          body: JSON.stringify({
            password: this.user_input.password,
          }),
        });
        if (!res.ok) {
          console.log("error");
        }
      } catch (error) {
        console;
      }
      this.waitingForPassword = true;
      router.push("/signin");
    },
    async updateUserProfileForm(event) {
      event.preventDefault();
      this.waitingForPref = false;
      await this.updateUserProfile(this.form);
      this.waitingForPref = true;
    },
  },
  computed: mapGetters(["email", "profile"]),
  async created() {
    this.loading = true;
    await this.getUserProfile();
    this.getEmail();
    this.form.email_format = this.profile.email_format;
    this.form.communication_preference = this.profile.communication_preference;
    this.form.webhook_url = this.profile.webhook_url;
    this.user_input.email = this.email;
    this.loading = false;
  },
};
</script>

<style>
#email__BV_label_,
#password__BV_label_,
#preferences__BV_label_ {
  font-size: 1.2rem;
  font-weight: 600;
}
</style>
