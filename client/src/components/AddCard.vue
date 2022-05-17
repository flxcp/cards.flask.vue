<template>
  <div>
    <b-button class="mx-1" pill variant="dark" @click="$bvModal.show('addCard')"
      ><b-icon-plus-circle-fill></b-icon-plus-circle-fill
    ></b-button>
    <div>
      <b-modal id="addCard" centered hide-header hide-footer>
        <div>
          <div class="d-flex justify-content-between">
            <h5 class="pt-2">Create New Card</h5>
            <button
              type="button"
              class="btn shadow-none py-1"
              @click="$bvModal.hide('addCard')"
            >
              <b-icon-x-circle-fill></b-icon-x-circle-fill>
            </button>
          </div>
          <b-form @submit="onClickCreate" class="mx-4 mt-2 mb-3">
            <b-form-group id="question" label="Question" label-for="question">
              <b-form-input
                id="question"
                type="text"
                v-model="form.question"
                required
              ></b-form-input>
            </b-form-group>

            <b-form-group id="answer" label="Answer" label-for="answer">
              <b-form-input
                id="answer"
                type="text"
                v-model="form.answer"
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
                >Create Card</b-button
              >
              <b-button v-else variant="dark" pill disabled size="sm">
                <b-spinner small type="grow"></b-spinner>
                Creating
              </b-button>
            </span>
          </b-form>
        </div>
      </b-modal>
    </div>
    <!-- Edit Modal End -->
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "AddCard",
  props: {
    deck_id: {
      required: true,
    },
  },
  data() {
    return {
      form: {
        deck_id: parseInt(this.deck_id),
        question: "",
        answer: "",
      },
      waitingForInput: true,
    };
  },
  methods: {
    ...mapActions(["addCard"]),
    async onClickCreate(event) {
      event.preventDefault();
      this.waitingForInput = false;
      await this.addCard(this.form);
      this.$bvModal.hide("addCard");
      this.form.question = "";
      this.form.answer = "";
      this.waitingForInput = true;
    },
  },
};
</script>

<style scoped></style>
