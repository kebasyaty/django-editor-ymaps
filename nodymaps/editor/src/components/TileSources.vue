<!--
------------------------------------
Component for selecting Tile Source.
------------------------------------
-->
<template>
  <v-container fluid>
    <v-hover v-slot:default="{ hover }" v-for="tile in tiles" :key="`tile-${tile.id}`">
      <v-card :elevation="hover ? maxElevation : minElevation" class="djeym-curs-p mb-4"
        @click="tileSourceReplacement(tile.id, tile.isActive)">
        <v-container fluid class="py-0">
          <div v-if="tile.isActive" class="ml-2 pb-1 active-tile">
            <v-icon small color="red">mdi-circle</v-icon>
          </div>
          <v-row>
            <v-col cols="4">
              <v-img :src="tile.img" class="pos-screenshot"></v-img>
            </v-col>
            <v-col cols="8">
              <div class="subtitle-1 font-weight-medium text-truncate">
                {{ tile.title }}
              </div>
              <div class="body-2 font-weight-light">
                <span class="font-italic">max zoom</span>
                : {{ tile.maxZoom }}
              </div>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-hover>
  </v-container>
</template>

<script>
import { mapState, mapMutations, mapActions } from "vuex";

export default {
  name: "TileSources",
  data: () => ({}),
  computed: {
    ...mapState("tileSources", ["tiles"]),
    ...mapState("generalSettings", ["minElevation", "maxElevation"]),
  },
  methods: {
    ...mapMutations(["setMapSettingsDrawer"]),
    ...mapMutations("modals", [
      // Message
      "messageDialogShow", // Open
      "messageDialogClose", // Close
    ]),
    ...mapMutations("tileSources", ["setDataActionAjaxReplacement"]),
    ...mapActions("tileSources", ["actionAjaxReplacement"]),
    tileSourceReplacement(id, isActive) {
      if (!isActive) {
        this.setMapSettingsDrawer(false);
        this.setDataActionAjaxReplacement({ id: id });
        this.messageDialogShow({
          status: "accent",
          title: this.$t("message.85"),
          text: this.$t("message.44"),
          cancelBtn: true,
          okBtn: true,
          actionBtnCancel: () => {
            this.messageDialogClose();
            this.setMapSettingsDrawer(true);
          },
          actionBtnOk: this.actionAjaxReplacement,
        });
      }
    },
  },
};
</script>

<style scoped>
.active-tile {
  position: absolute;
  top: 1px;
  right: 7px;
}

.pos-screenshot {
  position: relative;
  top: 2px;
  left: 2px;
}
</style>
