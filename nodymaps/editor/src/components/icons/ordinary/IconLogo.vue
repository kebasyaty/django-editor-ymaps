<template>
  <v-tooltip bottom>
    <template #activator="{ on }">
      <svg
        v-on="on"
        :class="classes"
        xmlns="http://www.w3.org/2000/svg"
        :width="computedWidth"
        :height="height"
        :viewBox="computedViewBox"
        :aria-labelledby="iconName"
        role="presentation"
      >
        <g stroke-width="1.0086" :fill="color">
          <path
            d="m13.057 74.339q-0.9717 0-1.7006-0.7045-0.65591-0.6802-0.65591-1.7006v-18.973q0-1.0446 0.65591-1.7006 0.70451-0.7045 1.7006-0.7045h0.02433q4.6643 0 7.9439 3.0123 2.9881 2.7451 2.9881 7.2637 0 7.7495-2.9881 10.494-3.2796 3.0123-7.9439 3.0123zm-6.8022-26.916q-0.92313 0.07288-1.5304 0.7045-0.63162 0.65591-0.63162 1.6033v25.265q0 0.9717 0.60733 1.6519 0.63162 0.65591 1.6033 0.7045 6.0247 0.29152 7.6281 0.29152 8.697 0 13.58-4.2513 4.5185-4.0327 4.5185-10.641 0-7.3608-5.5145-11.661-5.2231-4.0327-13.386-4.0327-1.6277 0-6.875 0.3644z"
            style="
              font-feature-settings: normal;
              font-variant-caps: normal;
              font-variant-ligatures: normal;
              font-variant-numeric: normal;
            "
          />
          <path
            d="m44.648 75.506q0 5.1501-2.5508 8.4297-2.9638 3.7654-8.0897 2.7451-0.43727-0.09717-1.0932-0.38869-1.5548-0.75308-1.5548-2.4536 0-1.0689 0.70451-1.8706 0.72879-0.77737 1.822-0.77737 0.94746 0 1.822-0.46157 2.1135-0.99602 2.1135-4.7371v-16.13q0-1.409 0.99603-2.405 0.94746-0.9717 2.3808-0.9717h0.09717q1.4333-0.02429 2.3808 0.9717 0.9717 0.99602 0.9717 2.405zm-1.0689-22.301q-1.0689 1.1418-2.6479 1.1418-1.5304 0-2.6723-1.1418-1.0689-1.0689-1.0689-2.6237t1.0689-2.6479q1.0689-1.1175 2.6723-1.1175 1.579 0 2.6479 1.1175 1.0446 1.0932 1.0689 2.6479-0.02433 1.4575-1.0689 2.6237z"
            style="
              font-feature-settings: normal;
              font-variant-caps: normal;
              font-variant-ligatures: normal;
              font-variant-numeric: normal;
            "
          />
          <path
            d="m58.248 72.324v-7.6766l8.8188 0.21864q1.0932 0.02429 1.9435-0.80167 0.80168-0.77737 0.80168-1.9435v-0.09717q0.02433-1.1418-0.77738-1.8948-0.87455-0.82596-1.9677-0.80167l-8.8188 0.21864v-6.8993l9.3529 0.43727q0.94746 0.04859 1.7734-0.60733 0.26722-0.21864 0.94746-1.5548l0.02433-0.09717q0.65592-1.3361-0.53444-2.7937-0.77738-0.9717-2.1621-0.9717h-12.365q-1.8463 0-3.061 1.2389-1.2875 1.3361-1.2875 3.1095v21.961q0 1.7734 1.2875 3.061t3.061 1.2875h13.021q1.1661 0.02429 1.9677-0.80168 0.80168-0.77738 0.80168-1.9435v-0.09717q0-1.2146-0.80168-1.9435-0.89889-0.80167-1.9677-0.80167z"
            style="
              font-feature-settings: normal;
              font-variant-caps: normal;
              font-variant-ligatures: normal;
              font-variant-numeric: normal;
            "
          />
          <path
            d="m82.109 65.449-7.4337-13.459q-0.92313-1.6519 0.17006-3.3767 1.0446-1.6519 2.9394-1.6519h0.38869q2.3564 0 3.231 2.235 2.2593 5.6117 4.6157 10.859l4.6643-10.859q0.94746-2.235 3.231-2.235h0.04857q1.9677 0 3.0123 1.7006 1.0446 1.7248 0.09717 3.3525l-7.6766 13.167v8.9157q0 1.7977-1.0689 2.8666-1.0446 1.0689-2.5265 1.0689h-0.09717q-1.4819 0-2.5265-1.0689-1.0689-1.0446-1.0689-2.8666z"
            style="
              font-feature-settings: normal;
              font-variant-caps: normal;
              font-variant-ligatures: normal;
              font-variant-numeric: normal;
            "
          />
          <path
            d="m107.64 55.464 5.3202 18.657q0.46157 1.6033 1.822 2.6723 1.3847 1.0446 3.0609 1.0446h0.0972q1.6277 0 3.1095-1.0446 1.3847-1.0204 1.8463-2.6723l5.2716-18.657-0.43728 19.192q-0.0243 1.3118 0.94746 2.2593 0.94746 0.92313 2.2835 0.92313h0.0486q1.7005 0 2.7208-0.9717 0.9717-0.92313 0.9717-2.2106v-21.305q0-2.5022-1.7734-4.227-1.7248-1.7248-4.1784-1.7248h-0.0729q-1.992 0-3.5954 1.1904-1.579 1.2146-2.1378 3.1095l-5.0044 17.515-5.0529-17.564q-0.55874-1.9192-2.1378-3.061-1.579-1.1904-3.5468-1.1904h-0.0729q-2.5022 0-4.227 1.7248t-1.7248 4.227v21.305q0 1.2389 0.9717 2.2106t2.2106 0.9717h0.53444q1.3604 0 2.3079-0.9717 0.92313-0.8988 0.89889-2.2106z"
            style="
              font-feature-settings: normal;
              font-variant-caps: normal;
              font-variant-ligatures: normal;
              font-variant-numeric: normal;
            "
          />
        </g>
        <g :fill="color">
          <path
            d="m26.154 127.23c-5.5972-0.52294-10.433-1.8549-15.182-4.1811-3.6263-1.7764-5.8537-3.6714-7.1302-6.0663-1.713-3.2139-1.1033-5.7608 2.1503-8.9831 2.7646-2.738 6.6539-4.6839 12.063-6.0354 3.376-0.84355 5.7994-1.1574 11.732-1.5191l4.7163-0.28744 40.987-18.665 29.676 0.1406-6.3348 3.9052c-21.926 13.517-32.999 20.536-36.832 23.348l-1.7938 1.3159 0.13648 2.3939c0.15452 2.7098-0.1241 3.8818-1.3492 5.6749-4.1378 6.0563-19.388 10.217-32.84 8.96zm22.294-86.788c-8.7996-4.3775-10.851-5.25-12.345-5.2518-0.70651-8.4e-4 -2.527 0.14214-4.0455 0.31786-6.6879 0.77362-15.803-1.3286-19.488-4.4945-1.2522-1.0758-2.2578-2.8935-2.2578-4.0809 0-1.1654 0.9984-2.9993 2.1865-4.0163 1.488-1.2737 4.258-2.5592 7.2783-3.3777 2.427-0.65775 5.7273-0.83945 8.613-0.88314 2.9801-0.04721 7.1147 0.24495 8.9182 0.64212 1.8674 0.41123 2.4891 0.4406 3.9265 0.18463 2.561-0.45634 7.2947-1.6731 16.466-4.2328 11.689-3.2624 24.363-6.7603 25.316-6.9869 0.99732-0.23708 1.2118-0.55458 1.2171-1.8019 0.01574-3.754 6.8809-6.5692 14.898-6.1094 6.7203 0.38552 11.496 2.825 11.496 5.8722 0 3.9266-8.306 6.9837-16.189 5.9586-4.9932-0.64931-5.0714-0.64716-8.3397 0.22922-3.1096 0.83378-11.934 3.6091-29.414 9.2509l-9.5454 3.0808v1.5776c0 0.86766-0.1828 2.0151-0.40619 2.5497-0.22339 0.5347-0.40619 1.1854-0.40619 1.4461 0 0.52242 4.2345 2.5787 18.414 8.9406 4.3936 1.9713 8.1041 3.691 8.2456 3.8215 0.1477 0.13638-3.7919 0.23708-9.2526 0.23708h-9.5099z"
            stroke-width=".27079"
          />
        </g>
      </svg>
    </template>
    <span>{{ description }}</span>
  </v-tooltip>
</template>

<script>
export default {
  name: "IconLogo",
  props: {
    iconName: {
      type: String,
      default: "DjEYM",
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
    viewBox: [0, 0, 138.78, 128.79],
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
