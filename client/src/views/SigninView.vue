<template>
  <div
    class="d-flex flex-column vh-100 justify-content-center align-items-center"
  >
    <b-col cols="8" md="5" lg="4">
      <h3 class="text-center py-2">Sign in to your account</h3>
      <b-alert show variant="danger" v-show="isError">
        {{ errorMsg }}
      </b-alert>
      <b-form @submit="onSubmit">
        <b-form-group class="py-2">
          <b-form-input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="Email"
            required
          ></b-form-input
        ></b-form-group>

        <b-form-group class="pb-2">
          <b-form-input
            v-model="form.password"
            placeholder="Password"
            type="password"
            id="password"
            required
          ></b-form-input
        ></b-form-group>

        <b-button v-if="waitingForInput" type="submit" pill variant="dark"
          >Submit</b-button
        >
        <b-button v-else variant="dark" pill disabled>
          <b-spinner small type="grow"></b-spinner>
          Submitting...
        </b-button>
      </b-form>
    </b-col>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      isError: false,
      errorMsg: "",
      waitingForInput: true,
    };
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault();

      // Reset Error Message
      this.waitingForInput = false;
      this.isError = false;
      this.errorMsg = "";

      try {
        let res = await fetch(
          "https://flshcard.herokuapp.com/login?include_auth_token",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(this.form),
            redirect: "follow",
          }
        );

        if (res.ok) {
          let ret = await res.json();
          localStorage.setItem(
            "auth-token",
            ret.response.user.authentication_token
          );
          localStorage.setItem("email", this.form.email);
          this.waitingForInput = true;
          this.$router.push("/");
        } else {
          this.waitingForInput = true;
          this.isError = true;
          this.errorMsg = "Check your Email & Password";
        }
      } catch (error) {
        this.waitingForInput = true;
        this.isError = true;
        this.errorMsg = "Check your Email & Password";
      }
    },
  },
};
</script>
