<template>
  <section class="background-gif headline">
    <div class="container">
      <div class="title">
        <h1>
          <NuxtLink to="/" aria-label="Piščalka">
            <img class="logo" src="~assets/images/LOGO.png" alt="Piščalka" />
          </NuxtLink>
        </h1>
        <p>Medijska platforma <br />na ljudski pogon</p>
      </div>
    </div>
    <div class="container">
      <SectionPaymentChooser
        v-if="showButtons"
        :medium="medium"
        :type="paymentType"
      />
    </div>
  </section>
</template>

<script>
import SectionPaymentChooser from "./SectionPaymentChooser.vue";

export default {
  components: {
    SectionPaymentChooser,
  },
  props: {
    medium: {
      type: Object,
      required: true,
    },
    showButtons: {
      type: Boolean,
      default: true,
    },
    supporterAmount: {
      type: Number,
      default: 0,
    },
  },
  data() {
    const query = this.$route.query;

    return {
      paymentType: query.enkratno === "true" ? "one_time" : "recurring",
    };
  },
  watch: {
    "$route.query.enkratno"(value) {
      this.paymentType = value === "true" ? "one_time" : "recurring";
    },
  },
};
</script>

<style scoped lang="scss">
.headline {
  padding: 1rem;
  padding-bottom: 0;

  .container:nth-of-type(1) {
    position: relative;
    z-index: 2;
  }

  .title {
    margin: 1rem 0;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem 1.5rem;

    h1 {
      margin: 0;

      a {
        display: block;
      }
    }

    p {
      font-family: 'wf-archivo-extracondensed', sans-serif;
      font-size: 1.5rem;
      line-height: 1.2;
      font-weight: 700;
      text-align: left;
      margin: 0;

      @media (min-width: 768px) {
        font-size: 2rem;
      }
    }
  }

  .logo {
    height: 6.5rem;
    width: auto;

    @media (min-width: 768px) {
      height: 9.1rem;
    }
  }
}
</style>
