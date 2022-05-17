<template>
  <b-card class="shadow" style="border-radius: 0.5rem">
    <b-card-text>
      <b-badge variant="primary" v-if="form.response === 0"> New </b-badge>
      <b-badge variant="danger" v-else-if="form.response === 1">Hard</b-badge>
      <b-badge variant="warning" v-else-if="form.response === 2"
        >Medium</b-badge
      >
      <b-badge variant="success" v-else-if="form.response === 3">Easy</b-badge>
    </b-card-text>
    <div
      class="d-flex justify-content-center align-items-center flex-column mb-0 text-capitalize"
    >
      <b-col cols="10">
        <div class="my-md-4 my-sm-3">
          <h3 class="text-center text-wrap">{{ form.question }}</h3>
          <h5
            class="text-center text-wrap card-subtitle text-muted text-center text-capitalize mt-2"
          >
            {{ form.answer }}
          </h5>
        </div>
      </b-col>
    </div>
    <!-- Edit & Delete Badge -->
    <div class="cardButtons d-flex justify-content-end pt-2">
      <b-card-text>
        <b-link
          @click="$bvModal.show('editCard' + card.id)"
          class="btn shadow-none py-0 px-1"
          ><b-badge variant="dark">Edit</b-badge></b-link
        >
        <b-link
          @click="$bvModal.show('deleteCard' + card.id)"
          class="btn shadow-none py-0 px-1"
          ><b-badge variant="danger">Delete</b-badge></b-link
        ></b-card-text
      >
    </div>
    <!-- Delete Modal Start -->
    <b-modal :id="'deleteCard' + card.id" centered hide-header hide-footer>
      <div class="d-flex justify-content-end">
        <button
          type="button"
          class="btn shadow-none py-1"
          @click="$bvModal.hide('deleteCard' + card.id)"
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
          @click="$bvModal.hide('deleteCard' + card.id)"
          >Save</b-button
        >
        <span class="d-flex justify-content-end">
          <b-button
            v-if="waitingDelete"
            pill
            variant="danger"
            @click="onClickDelete(card)"
            size="sm"
            >Delete Card</b-button
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
      <b-modal :id="'editCard' + card.id" centered hide-header hide-footer>
        <div>
          <div class="d-flex justify-content-between">
            <h5 class="pt-2">Edit Card</h5>
            <button
              type="button"
              class="btn shadow-none py-1"
              @click="$bvModal.hide('editCard' + card.id)"
            >
              <b-icon-x-circle-fill></b-icon-x-circle-fill>
            </button>
          </div>
          <b-form @submit="onClickUpdate" class="mx-4 mt-2 mb-3">
            <b-form-group id="question" label="Question" label-for="question">
              <b-form-input
                id="question"
                type="text"
                v-model="form.updated_question"
                required
              ></b-form-input>
            </b-form-group>

            <b-form-group id="answer" label="Answer" label-for="answer">
              <b-form-input
                id="answer"
                type="text"
                v-model="form.updated_answer"
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
                >Update Card</b-button
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
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "CardComp",
  props: {
    card: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      form: {
        id: this.card.id,
        deck_id: this.card.deck_id,
        question: this.card.question,
        answer: this.card.answer,
        response: this.card.response,
        updated_question: this.card.question,
        updated_answer: this.card.answer,
      },
      waitingForInput: true,
      waitingDelete: true,
    };
  },
  methods: {
    ...mapActions(["deleteCard", "updateCard"]),
    async onClickUpdate(event) {
      event.preventDefault();
      this.waitingForInput = false;
      let upCard = await this.updateCard(this.form);

      // Update the card
      if (upCard) {
        this.form.question = upCard.question;
        this.form.answer = upCard.answer;
        this.form.deck_id = upCard.deck_id;
        this.form.response = upCard.response;
      }

      this.waitingForInput = true;
      this.$bvModal.hide("editCard" + this.form.id);
    },
    async onClickDelete(card) {
      this.waitingDelete = false;
      await this.deleteCard(card);
      this.waitingDelete = true;
      this.$bvModal.hide("deleteCard" + this.form.id);
    },
  },
};
</script>

<style scoped></style>
