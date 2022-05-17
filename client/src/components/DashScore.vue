<template>
  <div>
    <p>Hello</p>
  </div>
</template>

<script>
export default {
  name: "DashScore",
  props: {
    decks: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      score: {
        1: 0,
        2: 0,
        3: 0,
      },
    };
  },
  computed: {
    total() {
      return this.score.easy + this.score.medium + this.score.hard;
    },
  },
  created() {
    // loop through deck and get score in cards inside deck
    this.decks.forEach((deck) => {
      deck.cards.forEach((card) => {
        this.score[card.response] += 1;
      });
    });
  },
};
</script>

<style></style>
