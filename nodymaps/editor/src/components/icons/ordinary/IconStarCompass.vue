<template>
  <svg :class="classes" xmlns="http://www.w3.org/2000/svg" :width="computedWidth" :height="height"
    :viewBox="computedViewBox" :aria-labelledby="iconName" role="presentation">
    <path
      d="m18.524 9.015-5.194-1.427 1.764-3.101c0.108-0.19 0.076-0.429-0.078-0.583-0.155-0.155-0.395-0.187-0.584-0.079l-3.083 1.754-1.435-5.222c-0.057-0.211-0.249-0.357-0.468-0.357-0.218 0-0.41 0.146-0.468 0.357l-1.425 5.185-3.014-1.714c-0.19-0.109-0.429-0.077-0.584 0.079-0.154 0.154-0.187 0.393-0.078 0.583l1.725 3.033-5.22 1.434c-0.211 0.058-0.357 0.25-0.357 0.469s0.146 0.41 0.357 0.468l5.178 1.423-1.747 3.07c-0.109 0.191-0.076 0.43 0.078 0.584 0.155 0.154 0.395 0.188 0.584 0.08l3.021-1.719 1.434 5.221c0.058 0.209 0.25 0.355 0.468 0.355 0.219 0 0.411-0.146 0.469-0.355l1.437-5.232 3.1 1.764c0.075 0.041 0.158 0.063 0.241 0.063h9e-3c0.269 0 0.485-0.217 0.485-0.486 0-0.119-0.043-0.229-0.115-0.314l-1.689-2.969 5.19-1.426c0.211-0.058 0.357-0.25 0.357-0.468s-0.147-0.412-0.358-0.47zm-17.881 0.408 0.12-0.033 8.495 0.126-1.964 1.735-6.651-1.828zm6.975-2.156 1.827-6.65 0.033 0.12-0.125 8.495-1.735-1.965zm1.835 2.188-0.034-0.035 0.034 0.035zm0.033 0.223 1.735 1.963-1.828 6.65-0.033-0.119 0.126-8.494zm4.992 4.858-2.879-2.965-0.089 0.025 1.171-0.322 1.885 3.313-0.088-0.051zm3.664-5.017-8.495-0.126 1.964-1.734 6.65 1.827-0.119 0.033zm-3.545-5.196-0.05 0.088-3.003 2.915 0.011 0.042-0.313-1.137 3.355-1.908zm-7.25 3.004-1.09 0.299-1.877-3.3 0.088 0.05 2.868 2.954 0.011-3e-3zm0.249 5.354-3.287 1.869 0.051-0.088 2.941-2.855 0.295 1.074z"
      :fill="color" />
  </svg>
</template>

<script>
export default {
  name: "IconStarCompass",
  props: {
    iconName: {
      type: String,
      default: "Star Compass",
    },
    classes: {
      type: String,
      default: "",
    },
    height: {
      type: [Number, String],
      default: 64,
    },
    color: {
      type: String,
      default: "currentColor",
    },
  },
  data: () => ({
    drawer: null,
    viewBox: [0, 0, 18.908, 18.908],
  }),
  computed: {
    description() {
      const name = this.iconName;
      return (
        name[0].toLocaleUpperCase() +
        name.slice(1) +
        " - " +
        this.$t("message.1")
      );
    },
    computedViewBox() {
      return this.viewBox.join(" ");
    },
    computedWidth() {
      const height = this.height.toString();
      const unit = height.match(
        /px|%|em|ex|cm|mm|in|pt|pc|ch|rem|vh|vw|vmin|vmax$/,
      );
      return (
        Math.ceil(this.viewBox[2] * (parseFloat(height) / this.viewBox[3])) +
        (unit ? unit[0] : "")
      );
    },
  },
};
</script>
