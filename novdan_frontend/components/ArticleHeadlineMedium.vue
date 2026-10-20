<template>
  <section class="headline">
    <div class="container">
      <div class="title">
        <h1>
          <NuxtLink to="/" aria-label="Piščalka">
            <img class="logo" src="~assets/images/LOGO.png" alt="Piščalka" />
          </NuxtLink>
        </h1>
        <p>Medijska platforma <br />na ljudski pogon</p>
        <a v-if="showButtons" class="support-link" href="#podpora">Podpri</a>
      </div>
    </div>
    <div v-if="showButtons" class="container">
      <SectionMission />
    </div>
    <div v-if="showButtons" class="container">
      <SectionPaymentChooser :medium="medium" :type="paymentType" />
    </div>
  </section>
</template>

<script>
import SectionMission from "./SectionMission.vue";
import SectionPaymentChooser from "./SectionPaymentChooser.vue";

export default {
  components: {
    SectionMission,
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
    margin: 0.5rem 0;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem 1.75rem;

    h1 {
      margin: 0;

      a {
        display: block;
      }
    }

    p {
      font-family: "Archivo", sans-serif;
      font-stretch: 62%;
      font-size: 1.5rem;
      line-height: 1.1;
      font-weight: 700;
      text-align: left;
      color: var(--ink);
      margin: 0;

      @media (min-width: 768px) {
        font-size: 1.875rem;
      }
    }
  }

  .support-link {
    margin-left: auto;
    display: inline-block;
    padding: 0.875rem 1.75rem;
    background: var(--red-text);
    color: var(--paper);
    border: 2px solid var(--ink);
    border-radius: 12px;
    box-shadow: 4px 4px 0 var(--ink);
    font-size: 1.1875rem;
    font-weight: 800;
    text-decoration: none;
    transition:
      transform 0.12s ease,
      box-shadow 0.12s ease;

    &:hover,
    &:focus-visible {
      transform: translate(-2px, -2px);
      box-shadow: 6px 6px 0 var(--ink);
    }

    &:focus-visible {
      outline: 3px solid var(--ink);
      outline-offset: 3px;
    }

    @media (prefers-reduced-motion: reduce) {
      transition: none;
    }
  }

  .logo {
    height: 5.5rem;
    width: auto;

    @media (min-width: 768px) {
      height: 7rem;
    }
  }
}
</style>
