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
  <div class="vh-100 mx-5" v-else>
    <div class="d-flex justify-content-between align-items-center py-3">
      <div class="reviewButton d-flex justify-content-start">
        <b-button
          pill
          class="ml-1"
          variant="dark"
          :to="{ name: 'cards', params: { id: this.$route.params.id } }"
          ><b-icon-layers-fill></b-icon-layers-fill
        ></b-button>
      </div>
      <div class="d-flex justify-content-center align-items-center">
        <h4 class="mb-0">{{ deckName }}</h4>
      </div>
      <div class="status d-flex justify-content-end">
        <div class="stack">
          <b-icon-layers-fill></b-icon-layers-fill>
          <span class="ml-2 mr-1">{{ cards_reviewed }}</span>
          <span>/</span>
          <span class="ml-1">{{ deck_length }}</span>
        </div>
      </div>
    </div>
    <div
      class="align-items-center flex-column h-100"
      :class="{ 'd-flex': !review_finished }"
    >
      <b-col cols="8" md="6" v-show="!review_finished">
        <div class="my-5" style="height: 20rem">
          <b-card class="p-xs-3 p-md-5 shadow">
            <b-card-body>
              <h1
                class="question card-title text-center p-3 text-wrap"
                style="font-size: 60px"
              >
                {{ card.question }}
              </h1>
              <h4
                v-show="showAnswer"
                class="answer card-subtitle text-muted text-center text-capitalize"
              >
                {{ card.answer }}
              </h4>
            </b-card-body>
          </b-card>
        </div>
      </b-col>
      <div v-show="!review_finished">
        <h3></h3>
        <div class="ans" v-show="showAnswer">
          <h3></h3>
        </div>
        <div class="d-flex justify-content-center py-4 flex-column">
          <div class="showAns">
            <b-button
              pill
              variant="dark"
              @click="onClickShowAnswer"
              v-show="!showAnswer"
              >Show Answer</b-button
            >
            <div v-show="showAnswer" class="showOptions">
              <b-button
                pill
                class="mx-2"
                variant="success"
                @click="onClickReview(3)"
                >Easy</b-button
              >
              <b-button
                pill
                class="mx-2"
                variant="warning"
                @click="onClickReview(2)"
                >Medium</b-button
              >
              <b-button
                pill
                class="mx-2"
                variant="danger"
                @click="onClickReview(1)"
                >Hard</b-button
              >
            </div>
          </div>
        </div>
      </div>
      <div
        v-show="review_finished"
        class="justify-content-center align-items-center h-100"
        :class="{ 'd-flex': review_finished }"
      >
        <h3 class="text-center p-3 text-wrap h-50" style="font-size: 40px">
          You Have Completed Review <br />for {{ deckName }} Deck
        </h3>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "ReviewDeck",
  data() {
    return {
      loading: false,
      card: {
        id: 0,
        question: "",
        answer: "",
      },
      cards: [],
      cards_reviewed: 1,
      deck_length: 0,
      showAnswer: false,
      review_finished: false,
    };
  },
  computed: {
    ...mapGetters(["allCards", "deckName"]),
  },
  methods: {
    ...mapActions(["cardReview", "getAllCards"]),
    onClickShowAnswer() {
      this.showAnswer = !this.showAnswer;
    },
    onClickReview(resp) {
      this.showAnswer = !this.showAnswer;
      this.cardReview({
        id: this.card.id,
        response: resp,
      });
      if (this.cards.length > 1) {
        if (resp === 1) {
          this.cards.push(this.cards.shift());
        } else {
          this.cards.shift();
        }
        this.cards_reviewed++;
        let next_card = this.cards[0];
        this.card.id = next_card.id;
        this.card.question = next_card.question;
        this.card.answer = next_card.answer;
      } else {
        this.cards = this.cards.shift();
        this.review_finished = true;
      }
    },
  },
  async created() {
    this.loading = true;
    await this.getAllCards(this.$route.params.id);
    this.deck_length = this.allCards.length;
    this.cards = [...this.allCards];
    let next_card = this.cards[0];
    this.card.id = next_card.id;
    this.card.question = next_card.question;
    this.card.answer = next_card.answer;
    this.loading = false;
  },
};
</script>

<style></style>
