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
  <div class="decks" v-else>
    <div
      class="mb-4 mt-2 px-4 d-flex justify-content-between align-items-center"
    >
      <h3 class="mb-0">Decks</h3>
      <div class="d-flex align-items-center">
        <AddDeck />
      </div>
    </div>
    <div class="d-flex justify-content-center">
      <b-col cols="10" md="10">
        <b-card-group columns>
          <div v-for="deck in allDecks" :key="deck.id" class="deck">
            <DeckComp :deck="deck" />
          </div>
        </b-card-group>
      </b-col>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import DeckComp from "../components/DeckComp";
import AddDeck from "../components/AddDeck";

export default {
  name: "DeckView",
  data() {
    return {
      loading: false,
    };
  },
  components: {
    AddDeck,
    DeckComp,
  },
  methods: {
    ...mapActions(["getAllDecks", "deleteDeck", "updateDeck"]),
  },
  computed: mapGetters(["allDecks"]),
  async created() {
    this.loading = true;
    await this.getAllDecks();
    this.loading = false;
  },
};
</script>

<style></style>
