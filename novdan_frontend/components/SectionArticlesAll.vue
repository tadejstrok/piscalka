<template>
  <section class="background-black articles">
    <div class="container">
      <div>
        <div>
          <div class="filters">
            <button
              v-for="filter in filters"
              :key="filter"
              type="button"
              :class="{ active: activeFilter === filter }"
              @click="toggleFilter(filter)"
            >
              {{ filter }}
            </button>
          </div>
          <div class="date-articles">
            <div class="article-list">
              <div
                v-for="article in articlesWithFirstNewDate"
                :key="article.id"
              >
                <div
                  :class="{
                    'date-line': true,
                    'only-line': !article.firstNewDate,
                  }"
                >
                  <span class="date">{{
                    article.firstNewDate
                      ? formatLongDate(article.published_at)
                      : "&nbsp;"
                  }}</span>
                  <hr />
                </div>
                <a :href="article.url" target="_blank" class="article">
                  <div class="medium-and-date">
                    <p>
                      <img
                        :src="article.medium.icon_url"
                        :alt="article.medium.name"
                        class="favicon"
                      />
                      <span>{{ article.medium.name }}</span>
                    </p>
                    <small :title="article.published_at">{{
                      formatRelativeTime(article.published_at)
                    }}</small>
                  </div>
                  <PreferHttpsImage
                    :src="article.image_url"
                    :alt="`Image for ${article.title}`"
                  />
                  <h5>{{ article.title }}</h5>
                  <p class="line-clamp-4">
                    {{ article.description }}
                  </p>
                </a>
              </div>
            </div>
          </div>
          <div v-if="articles?.next" class="more-articles">
            <button type="button" @click="$emit('load-more')">
              <span>Več →</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import PreferHttpsImage from "./PreferHttpsImage.vue";

export default {
  name: "SectionArticlesAll",
  components: {
    PreferHttpsImage,
  },
  props: {
    articles: {
      type: Object,
      required: true,
    },
  },
  emits: ["load-more"],
  data() {
    return {
      filters: [
        "Petkova Propagandna Poročila",
        "Posebni Propagandni Pogovori",
        "Kratke vsebine",
      ],
      activeFilter: null,
    };
  },
  computed: {
    filteredResults() {
      const results = this.articles?.results || [];
      if (!this.activeFilter) {
        return results;
      }
      return results.filter(
        (article) => this.categorize(article) === this.activeFilter,
      );
    },
    articlesWithFirstNewDate() {
      let lastDate = null;
      return this.filteredResults.map((article) => {
        const date = new Date(article.published_at).toISOString().split("T")[0];
        if (date !== lastDate) {
          lastDate = date;
          return {
            ...article,
            firstNewDate: true,
          };
        }
        return article;
      });
    },
  },
  methods: {
    toggleFilter(filter) {
      this.activeFilter = this.activeFilter === filter ? null : filter;
    },
    categorize(article) {
      const title = article.title || "";
      if (/^PPP\s*#/i.test(title)) {
        return "Petkova Propagandna Poročila";
      }
      if (/^Poseben propagandni pogovor/i.test(title)) {
        return "Posebni Propagandni Pogovori";
      }
      return "Kratke vsebine";
    },
    formatDate(date) {
      return Intl.DateTimeFormat("sl-SI", {
        year: "numeric",
        month: "long",
        day: "numeric",
      }).format(new Date(date));
    },
    formatLongDate(date) {
      return Intl.DateTimeFormat("sl-SI", {
        year: "numeric",
        month: "long",
        day: "numeric",
        weekday: "long",
      }).format(new Date(date));
    },
    formatRelativeTime(date) {
      const now = new Date().getTime();
      const then = new Date(date).getTime();
      const diff = now - then;

      const formatter = new Intl.RelativeTimeFormat("sl-SI", {
        numeric: "auto",
      });

      const UNITS = {
        second: 1000,
        minute: 1000 * 60,
        hour: 1000 * 60 * 60,
        day: 1000 * 60 * 60 * 24,
        week: 1000 * 60 * 60 * 24 * 7,
        month: 1000 * 60 * 60 * 24 * 30,
        year: 1000 * 60 * 60 * 24 * 365,
      };
      const UNIT_KEYS = Object.keys(UNITS);

      for (let i = 0; i < UNIT_KEYS.length; i++) {
        const unit = UNIT_KEYS[i];
        const nextUnit = UNIT_KEYS[i + 1];
        if (!nextUnit || diff < UNITS[nextUnit]) {
          const amount = Math.floor(diff / UNITS[unit]);
          return formatter.format(-amount, unit);
        }
      }
    },
  },
};
</script>

<style scoped lang="scss">
.articles {
  padding: 0 1rem 2rem;

  > .container {
    border-top: 2px solid #dc4d35;
    padding-top: 2rem;
  }

  @media (min-width: 576px) {
    padding-inline: 2rem;
  }

  @media (min-width: 1200px) {
    padding-inline: 0;
  }

  h1 {
    font-size: 2rem;
    font-weight: 800;
    margin-top: 2rem;
    margin-bottom: 2rem;
    color: #ff5ccb;

    @media (min-width: 992px) {
      font-size: 6rem;
    }

    @media (min-width: 1200px) {
      font-size: 8rem;
    }
  }

  h4 {
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
    font-weight: 800;
    color: #000;

    @media (min-width: 992px) {
      font-size: 2rem;
    }

    a {
      color: inherit;
      text-decoration: none;

      &:hover {
        text-decoration: underline;
      }
    }
  }

  hr {
    background-color: #dc4d35;
    border-color: #dc4d35;
    width: 8rem;
    margin: 0;
  }

  .filters {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 1.5rem;

    button {
      background-color: transparent;
      border: 2px solid #dc4d35;
      border-radius: 999px;
      padding: 0.4rem 1.25rem;
      font-size: 1rem;
      font-weight: 600;
      color: #dc4d35;
      cursor: pointer;
      transition: all 0.2s ease-in-out;

      &:hover {
        background-color: rgba(220, 77, 53, 0.1);
      }

      &.active {
        background-color: #dc4d35;
        color: #fff;
      }
    }
  }

  .date-articles {
    overflow: hidden;
  }

  .date-line {
    display: flex;
    gap: 1.5rem;
    align-items: center;
    color: #dc4d35;
    margin-inline: -2rem;

    .date {
      margin-left: 0.5rem;
      padding-left: 1.5rem;
      background: #dbe3ef;
      font-size: 1rem;
      font-weight: 500;
    }

    @media (min-width: 576px) {
      .date {
        font-size: 1.25rem;
      }
    }

    hr {
      flex: 1;
    }

    &.only-line {
      gap: 0;

      .date {
        margin-left: 0;
        text-indent: -999px;
        background: transparent;
      }
    }
  }

  .article-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(300px, 100%), 1fr));
    gap: 2rem 1.5rem;
    margin-top: 1rem;

    .article {
      display: block;
      margin-top: 1rem;
      text-decoration: none;
      color: #000;

      &:hover {
        h5 {
          text-decoration: underline;
        }
      }

      img {
        box-sizing: border-box;
        display: block;
        aspect-ratio: 16/9;
        width: 100%;
        height: auto;
        object-fit: cover;
        background-color: #fff;
        border: 1px solid #dc4d35;
        border-radius: 4px;
      }

      small {
        display: block;
        font-size: 0.8rem;
        font-style: italic;
        opacity: 0.8;
        margin-block: 0.5em;
      }

      h5 {
        font-size: 1.2rem;
        font-weight: 500;
        margin-block: 0.7em;
      }

      p {
        font-size: 1rem;
        margin-block: 0.7rem;
      }

      .line-clamp-4 {
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 4;
        line-clamp: 4;
        overflow: hidden;
      }

      .medium-and-date {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.4rem;

        p {
          display: flex;
          gap: 0.33rem;
          align-items: center;
          margin: 0;

          .favicon {
            display: block;
            overflow: hidden;
            width: 22px;
            aspect-ratio: 1/1;
            background: #fff;
            border: 1px solid #fff;
            border-radius: 0;
          }
        }
      }
    }
  }

  .more-articles {
    margin-top: 2rem;
    text-align: center;

    button {
      background-color: #dc4d35;
      border: none;
      border-radius: 4px;
      padding: 0.5rem 2rem;
      font-size: 1.25rem;
      font-weight: 600;
      color: #000;
      cursor: pointer;
      transition: background-color 0.2s ease-in-out;

      &:hover {
        background-color: #ff5ccb;
      }
    }
  }
}
</style>
