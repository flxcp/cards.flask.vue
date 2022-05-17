<template>
  <router-link
    :to="{ name: 'cards', params: { id: deck.id } }"
    class="text-dark text-decoration-none"
  >
    <b-card class="shadow m-2" style="border-radius: 0.5rem">
      <div class="cardStats d-flex justify-content-between">
        <b-card-text>
          <span v-if="deck.cards.length > 0">
            <b-badge variant="danger" v-if="deck.status === 0"
              >Incomplete</b-badge
            >
            <b-badge variant="success" v-else>Complete</b-badge>
          </span>
          <b-badge variant="dark" v-else>New</b-badge>
          <span v-if="deckScore">
            <b-badge class="ml-2" variant="dark">{{ deckScore }}</b-badge>
          </span>
          <b-badge variant="primary" class="mt-0 ml-2">{{
            deck.date.split("T")[0].split("-")[2] +
            "." +
            deck.date.split("T")[0].split("-")[1] +
            "." +
            deck.date.split("T")[0].split("-")[0]
          }}</b-badge>
        </b-card-text>
        <div class="stack">
          <b-icon-layers-fill></b-icon-layers-fill>
          <span class="ml-2">{{ deck.cards.length }}</span>
        </div>
      </div>
      <div
        class="d-flex justify-content-center align-items-center flex-column mb-0 text-capitalize"
      >
        <b-col cols="10">
          <div class="my-md-4 my-sm-3">
            <h2 class="text-center text-wrap">{{ form.name }}</h2>
            <h6
              class="text-center text-wrap card-subtitle text-muted text-center text-capitalize mt-2"
            >
              {{ form.description }}
            </h6>
          </div>
        </b-col>
      </div>
      <!-- Edit & Delete Badge -->
      <div class="cardButtons d-flex justify-content-end pt-2">
        <b-card-text>
          <b-link
            @click="$bvModal.show('editDeck' + deck.id)"
            class="btn shadow-none py-0 px-1"
            ><b-badge variant="dark">Edit</b-badge></b-link
          >
          <b-link
            @click="$bvModal.show('deleteDeck' + deck.id)"
            class="btn shadow-none py-0 px-1"
            ><b-badge variant="danger">Delete</b-badge></b-link
          ></b-card-text
        >
      </div>
      <!-- Delete Modal Start -->
      <b-modal :id="'deleteDeck' + deck.id" centered hide-header hide-footer>
        <div class="d-flex justify-content-end">
          <button
            type="button"
            class="btn shadow-none py-1"
            @click="$bvModal.hide('deleteDeck' + deck.id)"
          >
            <b-icon-x-circle-fill></b-icon-x-circle-fill>
          </button>
        </div>
        <div
          class="d-flex flex-column align-items-center justify-content-center mt-2 mb-3"
        >
          <b-icon-x-square-fill
            class="mb-4 mt-3"
            variant="danger"
            font-scale="4"
          ></b-icon-x-square-fill>
          <h5>Are You Sure?</h5>
        </div>
        <div class="d-flex justify-content-end mt-4">
          <b-button
            class="mx-2"
            pill
            size="sm"
            variant="success"
            @click="$bvModal.hide('deleteDeck' + deck.id)"
            >Save</b-button
          >
          <span class="d-flex justify-content-end">
            <b-button
              v-if="waitingDelete"
              pill
              variant="danger"
              @click="onClickDelete(deck)"
              size="sm"
              >Delete Deck</b-button
            >
            <b-button v-else variant="danger" pill disabled size="sm">
              <b-spinner small type="grow"></b-spinner>
              Deleting
            </b-button>
          </span>
        </div>
      </b-modal>
      <!-- Delete Modal End -->
      <!-- Edit Modal Start -->
      <div>
        <b-modal :id="'editDeck' + deck.id" centered hide-header hide-footer>
          <div>
            <div class="d-flex justify-content-between">
              <h5 class="pt-2">Edit Deck</h5>
              <button
                type="button"
                class="btn shadow-none py-1"
                @click="$bvModal.hide('editDeck' + deck.id)"
              >
                <b-icon-x-circle-fill></b-icon-x-circle-fill>
              </button>
            </div>
            <b-form @submit="onClickUpdate" class="mx-4 mt-2 mb-3">
              <b-form-group id="name" label="Name" label-for="name">
                <b-form-input
                  id="name"
                  type="text"
                  v-model="form.updated_name"
                  required
                ></b-form-input>
              </b-form-group>

              <b-form-group
                id="description"
                label="Description"
                label-for="description"
              >
                <b-form-input
                  id="description"
                  type="text"
                  v-model="form.updated_description"
                  required
                ></b-form-input>
              </b-form-group>
              <span class="d-flex justify-content-end">
                <b-button
                  v-if="waitingForInput"
                  type="submit"
                  pill
                  variant="dark"
                  size="sm"
                  >Update Deck</b-button
                >
                <b-button v-else variant="dark" pill disabled size="sm">
                  <b-spinner small type="grow"></b-spinner>
                  Updating
                </b-button>
              </span>
            </b-form>
          </div>
        </b-modal>
      </div>
      <!-- Edit Modal End -->
    </b-card>
  </router-link>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "DeckComp",
  props: {
    deck: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      form: {
        id: this.deck.id,
        name: this.deck.name,
        description: this.deck.description,
        status: this.deck.status,
        updated_name: this.deck.name,
        updated_description: this.deck.description,
      },
      waitingForInput: true,
      waitingDelete: true,
    };
  },
  methods: {
    ...mapActions(["deleteDeck", "updateDeck"]),
    async onClickUpdate(event) {
      event.preventDefault();
      this.waitingForInput = false;
      let upDeck = await this.updateDeck(this.form);
      if (upDeck) {
        this.form.name = upDeck.name;
        this.form.description = upDeck.description;
        this.form.status = upDeck.status;
      }
      this.waitingForInput = true;
      this.$bvModal.hide("editDeck" + this.form.id);
    },
    async onClickDelete(card) {
      this.waitingDelete = false;
      await this.deleteDeck(card);
      this.waitingDelete = true;
      this.$bvModal.hide("deleteDeck" + this.form.id);
    },
  },
  computed: {
    deckScore: function () {
      let total = 0;
      for (let i = 0; i < this.deck.cards.length; i++) {
        total += parseInt(this.deck.cards[i].response);
      }
      return total;
    },
  },
};
</script>

<style scoped></style>
