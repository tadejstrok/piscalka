<template>
  <section class="mission">
    <div class="beats">
      <p class="beat">
        <span class="verb">Ustvarjamo</span>
        informativne vsebine z upanjem v boljši svet.
      </p>
      <p class="beat">
        <span class="verb">Gradimo</span>
        neodvisno alternativo obstoječemu medijskemu ekosistemu.
      </p>
      <a class="beat beat-cta" href="#podpora">
        <span class="lead-in">Našo neodvisnost</span>
        <span class="verb">zagotavljate</span>
        <span class="who">
          podporniki.
          <svg
            class="arrow"
            viewBox="0 0 44 44"
            width="44"
            height="44"
            aria-hidden="true"
          >
            <circle
              cx="22"
              cy="22"
              r="20"
              fill="none"
              stroke="currentColor"
              stroke-width="2.5"
            />
            <path
              d="M22 12 V30 M14 23 L22 31 L30 23"
              fill="none"
              stroke="currentColor"
              stroke-width="3"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </span>
      </a>
    </div>
  </section>
</template>

<style scoped lang="scss">
.mission {
  padding-top: 1.5rem;
}

.beats {
  width: 100%;
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  border: 2px solid var(--ink);
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 6px 6px 0 var(--ink);

  @media (min-width: 768px) {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.beat {
  margin: 0;
  padding: 1.5rem 1.5rem 1.75rem;
  background: var(--paper);
  color: var(--ink);
  font-size: 1.3rem;
  font-weight: 500;
  line-height: 1.4;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  text-decoration: none;

  & + & {
    border-top: 2px solid var(--ink);

    @media (min-width: 768px) {
      border-top: 0;
      border-left: 2px solid var(--ink);
    }
  }
}

.verb {
  display: block;
  font-stretch: 62%;
  font-weight: 900;
  font-size: 2.75rem;
  line-height: 0.95;
  text-transform: uppercase;

  @media (min-width: 768px) {
    font-size: 2rem;
  }

  @media (min-width: 992px) {
    font-size: 2.7rem;
  }

  @media (min-width: 1200px) {
    font-size: 3.4rem;
  }
}

.beat-cta {
  background: var(--red);
  gap: 0.5rem;

  .lead-in {
    font-size: 1.2rem;
    font-weight: 800;
    line-height: 1.2;
  }

  .who {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    font-stretch: 62%;
    font-weight: 900;
    font-size: 2.2rem;
    line-height: 1;
    text-transform: uppercase;
  }

  .arrow {
    flex-shrink: 0;
    transition: transform 0.15s ease;
  }

  &:hover .arrow,
  &:focus-visible .arrow {
    transform: translateY(4px);
  }

  &:focus-visible {
    outline: 3px solid var(--ink);
    outline-offset: -8px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .beat-cta .arrow {
    transition: none;
  }
}
</style>
