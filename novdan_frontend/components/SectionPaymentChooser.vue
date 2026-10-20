<template>
  <section id="podpora" class="chooser">
    <div class="container">
      <div>
        <div class="head">
          <h2>Postani podpornik</h2>
          <div class="toggle" role="group" aria-label="Pogostost podpore">
            <NuxtLink
              class="toggle-option"
              :class="{ active: type === 'recurring' }"
              :aria-current="type === 'recurring' ? 'true' : undefined"
              to="?enkratno=false"
              >Mesečno</NuxtLink
            >
            <NuxtLink
              class="toggle-option"
              :class="{ active: type === 'one_time' }"
              :aria-current="type === 'one_time' ? 'true' : undefined"
              to="?enkratno=true"
              >Enkratno</NuxtLink
            >
          </div>
        </div>
        <div class="amount-buttons">
          <template v-for="da in donationAmounts">
            <button
              v-if="Number(da.amount) > 0"
              :key="da.id"
              type="button"
              @click.prevent="
                $router.push(`/${medium.slug}/podpri?${queryString(da.amount)}`)
              "
            >
              <img v-if="da.image" class="tier-image" :src="da.image" alt="" />
              <span v-if="da.name" class="name">{{ da.name }}</span>
              <span class="amount">{{ Number(da.amount) }}&nbsp;€</span>
              <span v-if="type === 'recurring'" class="period">na mesec</span>
            </button>
            <div
              v-else-if="Number(da.amount) === -1"
              :key="`custom-${da.id}`"
              class="button"
              @click.prevent="focusInput"
            >
              <span class="name">{{ da.name || "Poljubni znesek" }}</span>
              <form class="amount" @submit.prevent="continueWithCustomAmount">
                <input v-model="customAmount" type="number" />&nbsp;€
              </form>
            </div>
          </template>
        </div>
        <p class="disclaimer">
          Redna finančna podpora pokriva stroške programske in druge opreme,
          predvsem pa prinaša motivacijo za nadaljnje ustvarjanje vsebin in
          razvoj platforme. Za spletno doniranje trenutno skrbi
          <a
            href="https://danesjenovdan.si"
            target="_blank"
            rel="noopener noreferrer"
            >Danes je nov dan</a
          >.
        </p>
        <div v-if="customAmount && customAmount > 0" class="continue-button">
          <button
            type="button"
            :disabled="!customAmount || customAmount <= 0"
            @click.prevent="continueWithCustomAmount"
          >
            Nadaljuj
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "SectionPaymentChooser",
  props: {
    medium: {
      type: Object,
      required: true,
    },
    type: {
      type: String,
      default: "recurring",
    },
  },
  data() {
    return {
      customAmount: "",
    };
  },
  computed: {
    donationAmounts() {
      return this.medium.donation_amounts
        .filter((da) => da[this.type])
        .sort((a, b) => {
          if (Number(a.amount) === -1) {
            return 1;
          }
          if (Number(b.amount) === -1) {
            return -1;
          }
          return Number(a.amount) - Number(b.amount);
        });
    },
  },
  methods: {
    queryString(amount) {
      const params = new URLSearchParams();
      if (this.type === "one_time") {
        params.append("enkratno", "true");
      }
      params.append("znesek", amount);
      return params.toString();
    },
    focusInput() {
      const input = this.$el.querySelector(".amount-buttons .button input");
      if (input) {
        input.focus();
      }
    },
    continueWithCustomAmount() {
      if (this.customAmount && this.customAmount > 0) {
        this.$router.push(
          `/${this.medium.slug}/podpri?${this.queryString(this.customAmount)}`,
        );
      }
    },
  },
};
</script>

<style scoped lang="scss">
.chooser {
  padding-top: 3rem;
  margin-bottom: 2rem;
  scroll-margin-top: 1rem;

  a {
    color: inherit;
  }

  .head {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: flex-end;
    gap: 1rem 2rem;

    h2 {
      margin: 0;
      font-weight: 900;
      font-size: 3rem;
      line-height: 0.92;
      text-transform: uppercase;

      @media (min-width: 768px) {
        font-size: 4.5rem;
      }
    }
  }

  .toggle {
    display: flex;
    border: 2px solid var(--ink);
    border-radius: 12px;
    overflow: hidden;
    background: var(--paper);

    .toggle-option {
      padding: 0.75rem 1.5rem;
      color: var(--ink);
      font-size: 1.0625rem;
      font-weight: 700;
      text-decoration: none;

      &.active {
        background: var(--ink);
        color: var(--paper);
      }

      &:focus-visible {
        box-shadow: inset 0 0 0 3px var(--red);
      }
    }
  }

  .amount-buttons {
    margin-block: 1.75rem 2.25rem;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1.25rem;

    @media (min-width: 768px) {
      gap: 1.5rem;
    }

    @media (min-width: 992px) {
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    }

    button,
    .button {
      background: var(--paper);
      border: 2px solid var(--ink);
      border-radius: 16px;
      box-shadow: 6px 6px 0 var(--ink);
      color: var(--ink);
      font: inherit;
      padding: 1.5rem 1.25rem 1.25rem;
      text-align: center;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 0.25rem;
      transition:
        transform 0.12s ease,
        box-shadow 0.12s ease,
        background-color 0.12s ease;

      &:hover,
      &:focus-visible {
        background: var(--red-tint);
        transform: translate(-3px, -3px);
        box-shadow: 9px 9px 0 var(--red);
      }

      &:focus-visible {
        outline: 3px solid var(--ink);
        outline-offset: 3px;
      }

      &:active {
        transform: translate(0, 0);
        box-shadow: 3px 3px 0 var(--ink);
      }

      @media (prefers-reduced-motion: reduce) {
        transition: none;
      }

      .tier-image {
        height: 5.5rem;
        width: auto;
        max-width: 100%;
        object-fit: contain;
      }

      .name {
        margin-top: 0.5rem;
        font-size: 1.125rem;
        font-weight: 700;
      }

      .amount {
        display: flex;
        align-items: center;
        justify-content: center;
        font-stretch: 62%;
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1;

        @media (min-width: 768px) {
          font-size: 4.5rem;
        }

        input::-webkit-outer-spin-button,
        input::-webkit-inner-spin-button {
          -webkit-appearance: none;
          margin: 0;
        }

        input[type="number"] {
          -moz-appearance: textfield;
          appearance: textfield;
        }

        input {
          flex: 1;
          width: 100%;
          margin-top: 0.5rem;
          padding: 0.25rem;
          font: inherit;
          font-size: inherit;
          font-weight: 700;
          color: var(--ink);
          background: #fff;
          border: 2px solid var(--ink);
          border-radius: 0.5rem;
          text-align: center;

          &:focus-visible {
            outline: 3px solid var(--red);
          }
        }
      }

      .period {
        font-size: 0.9375rem;
        color: var(--ink-soft);
      }
    }
  }

  .disclaimer {
    margin: 0;
    max-width: 780px;
    font-size: 1rem;
    line-height: 1.55;
    color: var(--ink-soft);

    a {
      color: var(--red-text);
      font-weight: 700;
    }
  }

  .continue-button {
    margin-top: 2rem;
    text-align: center;

    button {
      padding: 0.875rem 2.5rem;
      background: var(--red-text);
      color: var(--paper);
      border: 2px solid var(--ink);
      border-radius: 12px;
      box-shadow: 4px 4px 0 var(--ink);
      font: inherit;
      font-size: 1.1875rem;
      font-weight: 800;
      cursor: pointer;

      &:focus-visible {
        outline: 3px solid var(--ink);
        outline-offset: 3px;
      }

      &:disabled {
        background: #ccc;
        color: var(--ink);
        cursor: not-allowed;
      }
    }
  }
}
</style>
