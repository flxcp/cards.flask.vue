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
    <div
      class="mb-4 mt-2 px-4 d-flex justify-content-between align-items-center"
    >
      <h3 class="mb-0">{{ deckName }}</h3>
      <div class="d-flex align-items-center">
        <AddCard :deck_id="this.$route.params.id" />
        <b-button class="mx-1" pill variant="dark" @click="onClickDownload"
          ><b-icon-cloud-arrow-down-fill></b-icon-cloud-arrow-down-fill
        ></b-button>
        <b-button
          class="mx-1"
          pill
          variant="dark"
          @click="$bvModal.show('uploadDeck')"
          ><b-icon-cloud-arrow-up-fill></b-icon-cloud-arrow-up-fill
        ></b-button>
        <!-- Upload Modal Start -->
        <div>
          <b-modal id="uploadDeck" centered hide-header hide-footer>
            <div>
              <div class="d-flex justify-content-between">
                <h5 class="my-2">Import Deck</h5>
                <button
                  type="button"
                  class="btn shadow-none mb-4"
                  @click="$bvModal.hide('uploadDeck')"
                >
                  <b-icon-x-circle-fill></b-icon-x-circle-fill>
                </button>
              </div>
              <b-form @submit="onClickUpload" class="mx-4 mb-3 mb-2">
                <b-form-file
                  v-model="import_file"
                  placeholder="Choose a file or drop it here..."
                  drop-placeholder="Drop file here..."
                  accept=".csv"
                ></b-form-file>
                <span class="d-flex justify-content-end mt-3">
                  <b-button
                    v-if="waitingForInput"
                    type="submit"
                    pill
                    variant="dark"
                    size="sm"
                    >Upload</b-button
                  >
                  <b-button v-else variant="dark" pill disabled size="sm">
                    <b-spinner small type="grow"></b-spinner>
                    Uploading
                  </b-button>
                </span>
              </b-form>
            </div>
          </b-modal>
        </div>
        <!-- Upload Modal End -->
        <b-button
          pill
          class="ml-1"
          variant="dark"
          :to="{ name: 'review', params: { id: this.$route.params.id } }"
          ><b-icon-play-circle-fill></b-icon-play-circle-fill
        ></b-button>
      </div>
    </div>
    <div class="d-flex justify-content-center">
      <b-col cols="10" md="10">
        <b-card-group columns>
          <div v-for="card in allCards" :key="card.id" class="cards">
            <CardComp :card="card" />
          </div>
        </b-card-group>
      </b-col>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from "vuex";
import CardComp from "../components/CardComp";
import AddCard from "../components/AddCard";

export default {
  name: "CardsView",
  data() {
    return {
      loading: false,
      import_file: null,
      waitingForInput: true,
    };
  },
  components: {
    CardComp,
    AddCard,
  },
  methods: {
    ...mapActions(["getAllCards", "deleteCard", "updateCard"]),
    ...mapMutations(["setCards"]),

    async onClickUpload(event) {
      event.preventDefault();
      this.waitingForInput = false;
      const formData = new FormData();
      formData.append("file", this.import_file);

      try {
        let res = await fetch(
          `https://flshcard.herokuapp.com/api/deckimport/${this.$route.params.id}/`,
          {
            method: "POST",
            headers: {
              "Authentication-Token": localStorage.getItem("auth-token"),
            },
            body: formData,
          }
        );
        if (res.ok) {
          let data = await res.json();
          this.setCards(data.cards);

          this.waitingForInput = true;
          this.$bvToast.toast("Successfully Uploaded File", {
            title: "Import Deck",
            variant: "success",
            solid: true,
          });
          this.$bvModal.hide("uploadDeck");
        } else {
          this.waitingForInput = true;
          this.$bvToast.toast("File Upload Failed", {
            title: "Import Deck Error",
            variant: "danger",
            solid: true,
          });
          this.$bvModal.hide("uploadDeck");
        }
      } catch (error) {
        this.waitingForInput = true;
        this.$bvToast.toast("File Upload Failed", {
          title: "Import Deck Error",
          variant: "danger",
          solid: true,
        });
        this.$bvModal.hide("uploadDeck");
      }
    },

    async onClickDownload() {
      try {
        let res = await fetch(
          `https://flshcard.herokuapp.com/api/deckexport/${this.$route.params.id}/`,
          {
            method: "GET",
            headers: {
              "Authentication-Token": localStorage.getItem("auth-token"),
            },
          }
        );
        if (res.ok) {
          let blob = await res.blob();
          let url = window.URL.createObjectURL(blob);
          let a = document.createElement("a");
          a.href = url;
          a.download = "deck.csv";
          a.click();
        } else {
          this.$bvToast.toast("File Download Failed", {
            title: "Export Deck",
            variant: "danger",
            solid: true,
          });
        }
      } catch (error) {
        this.$bvToast.toast("File Download Failed", {
          title: "Export Deck",
          variant: "danger",
          solid: true,
        });
      }
    },
  },
  computed: {
    ...mapGetters(["allCards", "deckName"]),
  },
  async created() {
    this.loading = true;
    await this.getAllCards(this.$route.params.id);
    this.loading = false;
  },
};
</script>

<style></style>
