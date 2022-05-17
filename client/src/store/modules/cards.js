const state = {
  deck_name: "",
  cards: [],
};

const getters = {
  deckName: (state) => state.deck_name,
  allCards: (state) => state.cards,
};

const mutations = {
  setDeckName(state, name) {
    state.deck_name = name;
  },
  setCards: (state, cards) => (state.cards = cards),
  addCard: (state, card) => state.cards.unshift(card),
  deleteCard: (state, card) =>
    (state.cards = state.cards.filter((c) => c.id !== card.id)),
  updateCard: (state, card) => {
    const index = state.cards.findIndex((c) => c.id === card.id);
    if (index !== -1) {
      state.cards[index] = card;
    }
  },
};

const actions = {
  async getAllCards({ commit }, deckId) {
    try {
      let res = await fetch(
        `https://flshcard.herokuapp.com/api/deck/${deckId}/`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
        }
      );
      if (res.ok) {
        let ret = await res.json();
        commit("setDeckName", ret.name);
        commit("setCards", ret.cards);
      } else {
        console.log("error");
      }
    } catch (error) {
      console;
    }
  },

  async addCard({ commit }, card) {
    try {
      let res = await fetch(`https://flshcard.herokuapp.com/api/card/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth-token"),
        },
        body: JSON.stringify(card),
      });
      if (res.ok) {
        let ret = await res.json();
        commit("addCard", ret);
      } else {
        console.log("error");
      }
    } catch (error) {
      console;
    }
  },
  async deleteCard({ commit }, card) {
    try {
      let res = await fetch(
        `https://flshcard.herokuapp.com/api/card/${card.id}/`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
        }
      );
      if (res.ok) {
        commit("deleteCard", card);
      } else {
        console.log("error");
      }
    } catch (error) {
      console;
    }
  },
  async updateCard({ commit }, card) {
    try {
      let res = await fetch(
        `https://flshcard.herokuapp.com/api/card/${card.id}/`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
          body: JSON.stringify({
            question: card.updated_question,
            answer: card.updated_answer,
            deck_id: card.deck_id,
          }),
        }
      );
      if (res.ok) {
        let ret = await res.json();
        commit("updateCard", ret);
        return ret;
      } else {
        console.log("error");
      }
    } catch (error) {
      console;
    }
  },

  async cardReview({ commit }, card) {
    try {
      let res = await fetch(
        `https://flshcard.herokuapp.com/api/card/${card.id}/res/${card.response}/`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
        }
      );
      if (res.ok) {
        let ret = await res.json();
        commit("updateCard", ret);
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
