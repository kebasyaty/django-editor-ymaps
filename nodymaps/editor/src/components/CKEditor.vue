<!--
-----------------------------------------
Component for the text editor 'CKEditor'.
-----------------------------------------
-->
<template>
  <v-conteiner fluid>
    <v-row style="min-width: 380px; height: 500px; overflow-y: scroll">
      <textarea id="djeym-component-ckeditor"></textarea>
    </v-row>
  </v-conteiner>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "CKEditor",
  computed: {
    ...mapState(["dataAction"]),
    ...mapState("contextmenuPlacemark", {
      headerPlacemark: "header",
      bodyPlacemark: "body",
      footerPlacemark: "footer",
    }),
    ...mapState("contextmenuRoute", {
      headerRoute: "header",
      bodyRoute: "body",
      footerRoute: "footer",
    }),
    ...mapState("contextmenuTerritory", {
      headerTerritory: "header",
      bodyTerritory: "body",
      footerTerritory: "footer",
    }),
  },
  mounted() {
    let config = window.$("#id_ckeditor_textarea").data("config");
    window.djeymCKEditor = window.$("#djeym-component-ckeditor");
    window.djeymCKEditor.ckeditor(config);
    window.runCKEditorResizeImage();
    window.djeymCKEditor.val(this[this.dataAction.position]);
  },
  beforeDestroy() {
    window.djeymCKEditor.ckeditor().editor.destroy();
    window.djeymCKEditor.remove();
    window.djeymCKEditor = null;
  },
};
</script>
