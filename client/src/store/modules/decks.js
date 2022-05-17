const state = {
  decks: [],
};

const getters = {
  allDecks: (state) => state.decks,
};

const mutations = {
  setDecks: (state, decks) => (state.decks = decks),
  addDeck: (state, deck) => state.decks.unshift(deck),
  deleteDeck: (state, deck) =>
    (state.decks = state.decks.filter((d) => d.id !== deck.id)),
  updateDeck: (state, deck) => {
    const index = state.decks.findIndex((d) => d.id === deck.id);
    if (index !== -1) {
      state.decks[index] = deck;
    }
  },
};

const actions = {
  async getAllDecks({ commit }) {
    try {
      let res = await fetch("https://flshcard.herokuapp.com/api/decks/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth-token"),
        },
      });

      if (res.ok) {
        let ret = await res.json();
        commit("setDecks", ret.decks);
      } else {
        console.log("error");
      }
    } catch (error) {
      console;
    }
  },

  async createDeck({ commit }, deck) {
    try {
      let res = await fetch("https://flshcard.herokuapp.com/api/deck/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth-token"),
        },
        body: JSON.stringify(deck),
      });
      if (res.ok) {
        let ret = await res.json();
        commit("addDeck", ret);
      } else {
        console.log("error");
      }
    } catch (error) {
      console;
    }
  },

  async deleteDeck({ commit }, deck) {
    try {
      let res = await fetch(
        `https://flshcard.herokuapp.com/api/deck/${deck.id}/`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
        }
      );
      if (res.ok) {
        commit("deleteDeck", deck);
      } else {
        console.log("error");
      }
    } catch (error) {
      console;
    }
  },

  async updateDeck({ commit }, deck) {
    try {
      let res = await fetch(
        `https://flshcard.herokuapp.com/api/deck/${deck.id}/`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
          body: JSON.stringify({
            name: deck.updated_name,
            description: deck.updated_description,
            status: deck.status,
          }),
        }
      );
      if (res.ok) {
        let ret = await res.json();
        commit("updateDeck", ret);
        return ret;
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
