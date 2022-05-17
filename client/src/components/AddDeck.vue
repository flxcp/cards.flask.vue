<template>
  <div>
    <b-button class="mx-1" pill variant="dark" @click="$bvModal.show('addDeck')"
      ><b-icon-plus-circle-fill></b-icon-plus-circle-fill
    ></b-button>
    <div>
      <b-modal id="addDeck" centered hide-header hide-footer>
        <div>
          <div class="d-flex justify-content-between">
            <h5 class="pt-2">Create New Deck</h5>
            <button
              type="button"
              class="btn shadow-none py-1"
              @click="$bvModal.hide('addDeck')"
            >
              <b-icon-x-circle-fill></b-icon-x-circle-fill>
            </button>
          </div>
          <b-form @submit="onClickCreateDeck" class="mx-4 mt-2 mb-3">
            <b-form-group id="name" label="Name" label-for="name">
              <b-form-input
                id="name"
                type="text"
                v-model="form.name"
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
                v-model="form.description"
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
                >Create Deck</b-button
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
  name: "AddDeck",
  data() {
    return {
      form: {
        name: "",
        description: "",
      },
      waitingForInput: true,
    };
  },
  methods: {
    ...mapActions(["createDeck"]),
    async onClickCreateDeck(event) {
      event.preventDefault();
      this.waitingForInput = false;
      await this.createDeck(this.form);
      this.$bvModal.hide("addDeck");
      this.name = "";
      this.description = "";
      this.waitingForInput = true;
    },
  },
};
</script>

<style></style>
