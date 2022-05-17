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
  <div v-else>
    <div class="px-md-5 py-md-3 px-3 py-2">
      <div class="DashBoard-header py-3">
        <h2>
          Welcome <strong>{{ username }}</strong>
        </h2>
      </div>
      <div class="px-5 py-3">
        <b-card-group deck>
          <b-card class="shadow" style="border-radius: 0.5rem">
            <div class="d-flex justify-content-between px-4">
              <div>
                <b-card-text
                  class="text-uppercase text-muted mb-2 fw-bold"
                  style="font-size: 0.725rem; color: #95aac9"
                >
                  Easy
                </b-card-text>
                <b-card-text class="h1 font-weight-bold mb-0">{{
                  score[3]
                }}</b-card-text>
              </div>

              <div class="d-flex align-items-center">
                <b-icon-arrow-up-circle-fill
                  class="h1"
                  variant="success"
                  v-if="score[3] >= 20"
                >
                  ></b-icon-arrow-up-circle-fill
                >
                <b-icon-dash-circle-fill
                  class="h1"
                  variant="warning"
                  v-else-if="score[3] === 0"
                >
                  ></b-icon-dash-circle-fill
                >
                <b-icon-arrow-down-circle-fill
                  class="h1"
                  variant="danger"
                  v-else-if="0 > score[3] < 20"
                >
                  ></b-icon-arrow-down-circle-fill
                >
              </div>
            </div>
          </b-card>
          <b-card class="shadow" style="border-radius: 0.5rem">
            <div class="d-flex justify-content-between px-4">
              <div>
                <b-card-text
                  class="text-uppercase text-muted mb-2 fw-bold"
                  style="font-size: 0.725rem; color: #95aac9"
                >
                  Medium
                </b-card-text>
                <b-card-text class="h1 font-weight-bold mb-0">{{
                  score[2]
                }}</b-card-text>
              </div>

              <div class="d-flex align-items-center">
                <b-icon-arrow-up-circle-fill
                  class="h1"
                  variant="success"
                  v-if="score[2] >= 1"
                >
                  ></b-icon-arrow-up-circle-fill
                >
                <b-icon-dash-circle-fill
                  class="h1"
                  variant="warning"
                  v-else-if="score[2] === 0"
                >
                  ></b-icon-dash-circle-fill
                >
                <b-icon-arrow-down-circle-fill
                  class="h1"
                  variant="danger"
                  v-else-if="0 > score[2] < 1"
                >
                  ></b-icon-arrow-down-circle-fill
                >
              </div>
            </div>
          </b-card>
          <b-card class="shadow" style="border-radius: 0.5rem">
            <div class="d-flex justify-content-between px-4">
              <div>
                <b-card-text
                  class="text-uppercase text-muted mb-2 fw-bold"
                  style="font-size: 0.725rem; color: #95aac9"
                >
                  Hard
                </b-card-text>
                <b-card-text class="h1 font-weight-bold mb-0">{{
                  score[1]
                }}</b-card-text>
              </div>

              <div class="d-flex align-items-center">
                <b-icon-arrow-up-circle-fill
                  class="h1"
                  variant="success"
                  v-if="score[1] >= 20"
                >
                  ></b-icon-arrow-up-circle-fill
                >
                <b-icon-dash-circle-fill
                  class="h1"
                  variant="warning"
                  v-else-if="score[1] === 0"
                >
                  ></b-icon-dash-circle-fill
                >
                <b-icon-arrow-down-circle-fill
                  class="h1"
                  variant="danger"
                  v-else-if="0 > score[1] < 20"
                >
                  ></b-icon-arrow-down-circle-fill
                >
              </div>
            </div>
          </b-card>
          <b-card class="shadow" style="border-radius: 0.5rem">
            <div class="d-flex justify-content-between px-4">
              <div>
                <b-card-text
                  class="text-uppercase text-muted mb-2 fw-bold"
                  style="font-size: 0.725rem; color: #95aac9"
                >
                  Total Score
                </b-card-text>
                <b-card-text class="h1 font-weight-bold mb-0">{{
                  totalScore()
                }}</b-card-text>
              </div>

              <div class="d-flex align-items-center">
                <b-icon-arrow-up-circle-fill
                  class="h1"
                  variant="success"
                  v-if="totalScore() >= 20"
                >
                  ></b-icon-arrow-up-circle-fill
                >
                <b-icon-dash-circle-fill
                  class="h1"
                  variant="warning"
                  v-else-if="totalScore() === 0"
                >
                  ></b-icon-dash-circle-fill
                >
                <b-icon-arrow-down-circle-fill
                  class="h1"
                  variant="danger"
                  v-else-if="0 > totalScore() < 20"
                >
                  ></b-icon-arrow-down-circle-fill
                >
              </div>
            </div>
          </b-card>
        </b-card-group>
        <div class="py-5">
          <h3 class="py-3">Incomplete Decks</h3>
          <b-card-group deck>
            <div v-for="deck in recentDecks" :key="deck.id" class="deck">
              <router-link
                :to="{ name: 'cards', params: { id: deck.id } }"
                class="text-dark text-decoration-none"
              >
                <b-card class="shadow" style="border-radius: 0.5rem">
                  <b-card-body class="py-2 px-4">
                    <div
                      class="d-flex justify-content-center align-items-center"
                    >
                      <b-icon-layers-fill></b-icon-layers-fill>
                      <span class="ml-2 mr-1">{{ cardsReviewed(deck) }}</span>
                      <span>/</span>
                      <span class="ml-1">{{ deck.cards.length }}</span>
                    </div>
                    <b-card-title class="h1 text-center py-5 my3">
                      {{ deck.name }}
                    </b-card-title>
                    <div class="d-flex justify-content-center">
                      <b-badge variant="warning">{{
                        deckScore(deck.cards)
                      }}</b-badge>
                    </div>
                  </b-card-body>
                </b-card>
              </router-link>
            </div>
          </b-card-group>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "DashboardView",
  methods: {
    ...mapActions(["getAllDecks"]),
    totalScore() {
      return this.score[1] + this.score[2] + this.score[3] + this.score[4];
    },
    cardsReviewed(deck) {
      return deck.cards.filter((card) => card.response !== 0).length;
    },
    deckScore(cards) {
      let score = 0;
      cards.forEach((card) => {
        score += card.response;
      });
      return score;
    },
  },
  computed: {
    ...mapGetters(["allDecks"]),
    username: function () {
      let email = localStorage.getItem("email");
      return (
        email.split("@")[0].charAt(0).toUpperCase() +
        email.split("@")[0].slice(1)
      );
    },
  },
  data() {
    return {
      loading: true,
      score: {
        1: 0,
        2: 0,
        3: 0,
      },
      recentDecks: [],
    };
  },
  async created() {
    this.loading = true;
    await this.getAllDecks();
    this.recentDecks = await this.allDecks
      .filter((deck) => deck.status === 0)
      .sort((a, b) => {
        return new Date(b.date) - new Date(a.date);
      })
      .slice(0, 4);

    await this.allDecks.forEach((deck) => {
      deck.cards.forEach((card) => {
        this.score[card.response] += 1;
      });
    });
    this.loading = false;
  },
};
</script>

<style></style>
