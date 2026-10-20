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
  </section>
</template>

<script>
export default {};
</script>

<style scoped lang="scss">
.headline {
  padding: 1rem;

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
      color: #dc4d35;
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
