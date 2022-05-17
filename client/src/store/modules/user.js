const state = {
  email: "",
  profile: {
    email_format: "",
    webhook_url: "",
    communication_preference: "",
  },
};

const getters = {
  email: (state) => state.email,
  profile: (state) => state.profile,
};

const mutations = {
  setEmail(state, email) {
    state.email = email;
    localStorage.setItem("email", email);
  },
  setProfile(state, profile) {
    state.profile.email_format = profile.email_format;
    state.profile.webhook_url = profile.webhook_url;
    state.profile.communication_preference = profile.communication_preference;
  },
};

const actions = {
  getEmail({ commit }) {
    commit("setEmail", localStorage.getItem("email"));
  },

  async getUserProfile({ commit }) {
    try {
      let res = await fetch(`https://flshcard.herokuapp.com/api/user/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth-token"),
        },
      });
      if (res.ok) {
        let profile = await res.json();
        commit("setProfile", profile);
      } else {
        console.log("error");
      }
    } catch (error) {
      console;
    }
  },

  async updateEmail({ commit }, email) {
    try {
      let res = await fetch(`https://flshcard.herokuapp.com/api/email/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth-token"),
        },
        body: JSON.stringify({
          email: email,
        }),
      });
      if (res.ok) {
        commit("setEmail", email);
      } else {
        console.log("error");
      }
    } catch (error) {
      console;
    }
  },

  async updateUserProfile({ commit }, profile) {
    try {
      let res = await fetch(`https://flshcard.herokuapp.com/api/user/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth-token"),
        },
        body: JSON.stringify(profile),
      });
      if (res.ok) {
        let ret = await res.json();
        commit("setProfile", ret);
      } else {
        console.log("error");
      }
    } catch (error) {
      console;
    }
  },
};

export default {
  state,
  getters,
  mutations,
  actions,
};
