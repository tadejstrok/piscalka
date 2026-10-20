<template>
  <footer class="footer">
    <div class="container">
      <div class="columns">
        <div class="brand">
          <NuxtLink to="/" aria-label="Piščalka">
            <img class="logo" src="~assets/images/LOGO.png" alt="Piščalka" />
          </NuxtLink>
          <p class="tagline">Medijska platforma <br />na ljudski pogon</p>
        </div>
        <div class="column">
          <p class="label">Projekt</p>
          <p>
            Razvija
            <a
              href="https://danesjenovdan.si/"
              target="_blank"
              rel="noopener noreferrer"
              >Danes je nov dan</a
            >
          </p>
          <a href="mailto:novdan@danesjenovdan.si">novdan@danesjenovdan.si</a>
        </div>
        <div class="column">
          <p class="label">Podpora</p>
          <NuxtLink class="cta" to="/#podpora">Postani podpornik</NuxtLink>
          <a href="#" @click.prevent="cancelSupport"
            >Že podpornik? Upravljaj podporo</a
          >
        </div>
      </div>
      <div class="ornament-row">
        <svg
          class="ornament"
          viewBox="0 0 90 64"
          width="36"
          height="26"
          aria-hidden="true"
        >
          <g
            stroke="currentColor"
            stroke-width="9"
            stroke-linecap="round"
            fill="none"
          >
            <path d="M26 50 L10 22" />
            <path d="M45 48 L42 10" />
            <path d="M64 50 L76 18" />
          </g>
        </svg>
        <span class="rule"></span>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  methods: {
    cancelSupport() {
      // eslint-disable-next-line no-alert
      prompt("Prosimo kontaktirajte nas na e-naslovu:", "novdan@djnd.si");
    },
  },
};
</script>

<style scoped lang="scss">
.footer {
  margin-top: 6rem;
  padding: 3.5rem 1rem 3rem;
  display: flex;
  justify-content: center;
  background: var(--ink);
  color: var(--paper);

  a {
    color: var(--paper);
    font-weight: 700;
  }

  p {
    margin: 0;
  }

  .columns {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 2.5rem;

    @media (min-width: 768px) {
      grid-template-columns: 1.4fr 1fr 1fr;
      gap: 3rem;
    }
  }

  .brand {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .logo {
    height: 6rem;
    width: auto;
  }

  .tagline {
    font-stretch: 62%;
    font-size: 1.5rem;
    font-weight: 700;
    line-height: 1.1;
    color: var(--ground);
  }

  .column {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
    font-size: 1.0625rem;
    line-height: 1.5;
  }

  .label {
    color: var(--ground);
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }

  .cta {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    background: var(--red-text);
    border: 2px solid var(--paper);
    border-radius: 12px;
    font-size: 1.125rem;
    font-weight: 800;
    text-decoration: none;

    &:hover {
      background: var(--red);
      color: var(--ink);
    }

    &:focus-visible {
      outline: 3px solid var(--paper);
      outline-offset: 3px;
    }
  }

  .ornament-row {
    margin-top: 2.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;

    .ornament {
      flex-shrink: 0;
      color: var(--red);
    }

    .rule {
      flex: 1;
      height: 1px;
      background: var(--paper);
      opacity: 0.25;
    }
  }
}
</style>
