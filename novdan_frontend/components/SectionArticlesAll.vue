<template>
  <section class="background-black articles">
    <div class="container">
      <h2>Vsebine</h2>
      <div class="filters" role="group" aria-label="Filter vsebin">
        <button
          type="button"
          :class="{ active: activeFilter === null }"
          :aria-pressed="activeFilter === null"
          @click="setFilter(null)"
        >
          Vse
        </button>
        <button
          v-for="filter in filters"
          :key="filter"
          type="button"
          :class="{ active: activeFilter === filter }"
          :aria-pressed="activeFilter === filter"
          @click="setFilter(filter)"
        >
          {{ filter }}
        </button>
      </div>
      <div class="article-list">
        <article v-for="article in items" :key="article.id" class="card">
          <div class="kicker" :class="{ 'is-spacer': !article.firstNewDate }">
            <svg
              v-if="article.isNewest"
              class="ornament"
              viewBox="0 0 90 64"
              width="26"
              height="18"
              aria-hidden="true"
            >
              <g
                stroke="currentColor"
                stroke-width="10"
                stroke-linecap="round"
                fill="none"
              >
                <path d="M26 50 L10 22" />
                <path d="M45 48 L42 10" />
                <path d="M64 50 L76 18" />
              </g>
            </svg>
            <span class="date">{{
              article.firstNewDate
                ? formatLongDate(article.published_at)
                : "&nbsp;"
            }}</span>
            <span class="rule"></span>
          </div>
          <a
            :href="article.url"
            target="_blank"
            rel="noopener noreferrer"
            class="card-link"
          >
            <div class="thumb">
              <template v-if="article.shortImage">
                <img
                  class="thumb-bg"
                  :src="article.shortImage"
                  alt=""
                  @error="onShortError(article.id)"
                />
                <img
                  class="thumb-portrait"
                  :src="article.shortImage"
                  :alt="`Sličica: ${article.title}`"
                  @error="onShortError(article.id)"
                />
              </template>
              <PreferHttpsImage
                v-else
                class="thumb-img"
                :src="article.image_url"
                :alt="`Sličica: ${article.title}`"
              />
              <span class="tag" :class="`tag-${article.categoryKey}`">{{
                article.tagLabel
              }}</span>
              <span v-if="article.isNew" class="tag tag-new">Novo</span>
            </div>
            <h3>{{ article.title }}</h3>
            <p v-if="article.excerpt" class="excerpt">{{ article.excerpt }}</p>
            <p class="meta">
              <span :title="article.published_at">{{
                formatRelativeTime(article.published_at)
              }}</span>
              <template v-if="article.source"> · {{ article.source }}</template>
            </p>
          </a>
        </article>
      </div>
      <div v-if="hasMore" class="more-articles">
        <button type="button" @click="visibleCount += PAGE_SIZE">Več</button>
      </div>
    </div>
  </section>
</template>

<script>
import PreferHttpsImage from "./PreferHttpsImage.vue";

const CATEGORY_PPP = "Petkova Propagandna Poročila";
const CATEGORY_TALK = "Poseben Propagandni Pogovor";
const CATEGORY_SHORT = "Kratke vsebine";
const PAGE_SIZE = 12;
const NEW_WINDOW_MS = 1000 * 60 * 60 * 48;

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
  data() {
    return {
      filters: [CATEGORY_PPP, CATEGORY_TALK, CATEGORY_SHORT],
      activeFilter: null,
      failedShorts: {},
      visibleCount: PAGE_SIZE,
      PAGE_SIZE,
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
    hasMore() {
      return this.filteredResults.length > this.visibleCount;
    },
    items() {
      let lastDate = null;
      const now = Date.now();
      return this.filteredResults
        .slice(0, this.visibleCount)
        .map((article, index) => {
          const date = new Date(article.published_at)
            .toISOString()
            .split("T")[0];
          const firstNewDate = date !== lastDate;
          lastDate = date;
          const category = this.categorize(article);
          return {
            ...article,
            firstNewDate,
            isNewest: index === 0,
            isNew:
              now - new Date(article.published_at).getTime() < NEW_WINDOW_MS,
            categoryKey: this.categoryKey(category),
            tagLabel: this.tagLabel(article, category),
            shortImage: this.shortImage(article),
            excerpt: this.excerpt(article),
            source: this.source(article),
          };
        });
    },
  },
  methods: {
    setFilter(filter) {
      this.activeFilter = filter;
      this.visibleCount = PAGE_SIZE;
    },
    categorize(article) {
      const title = article.title || "";
      if (/^PPP\s*#/i.test(title)) {
        return CATEGORY_PPP;
      }
      if (/^Poseben propagandni pogovor/i.test(title)) {
        return CATEGORY_TALK;
      }
      return CATEGORY_SHORT;
    },
    categoryKey(category) {
      if (category === CATEGORY_PPP) {
        return "ppp";
      }
      if (category === CATEGORY_TALK) {
        return "talk";
      }
      return "short";
    },
    tagLabel(article, category) {
      if (category === CATEGORY_PPP) {
        const match = (article.title || "").match(/^PPP\s*#\s*(\d+)/i);
        return match ? `PPP #${match[1]}` : "PPP";
      }
      if (category === CATEGORY_TALK) {
        return "Pogovor";
      }
      return "Kratko";
    },
    shortImage(article) {
      if (this.failedShorts[article.id]) {
        return null;
      }
      const match = (article.url || "").match(/\/shorts\/([\w-]+)/);
      return match ? `https://i.ytimg.com/vi/${match[1]}/oar2.jpg` : null;
    },
    onShortError(id) {
      this.failedShorts = { ...this.failedShorts, [id]: true };
    },
    excerpt(article) {
      const text = (article.description || "")
        .split("-------")[0]
        .replace(/https?:\/\/(www\.)?/gi, "")
        .replace(/\s+/g, " ")
        .trim();
      if (!text || text === (article.title || "").trim()) {
        return "";
      }
      return text;
    },
    source(article) {
      try {
        return new URL(article.url).hostname.replace(/^www\./, "");
      } catch {
        return "";
      }
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
  padding: 4.5rem 1rem 2rem;

  @media (min-width: 576px) {
    padding-inline: 2rem;
  }

  @media (min-width: 1200px) {
    padding-inline: 0;
  }

  h2 {
    margin: 0 0 1.5rem;
    font-weight: 900;
    font-size: 3rem;
    line-height: 0.92;
    text-transform: uppercase;

    @media (min-width: 768px) {
      font-size: 4.5rem;
    }
  }

  .filters {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 2.5rem;

    button {
      padding: 0.5rem 1.25rem;
      background: transparent;
      border: 2px solid var(--ink);
      border-radius: 999px;
      color: var(--ink);
      font: inherit;
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
      transition: background-color 0.15s ease;

      &:hover {
        background: var(--red-tint);
      }

      &.active {
        background: var(--ink);
        color: var(--paper);
      }

      &:focus-visible {
        outline: 3px solid var(--ink);
        outline-offset: 2px;
      }

      @media (prefers-reduced-motion: reduce) {
        transition: none;
      }
    }
  }

  .article-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(300px, 100%), 1fr));
    gap: 2.5rem 1.75rem;
  }

  .card {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .kicker {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    color: var(--red-text);
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;

    .ornament {
      flex-shrink: 0;
      color: var(--red);
    }

    .rule {
      flex: 1;
      height: 1px;
      background: var(--ink);
      opacity: 0.25;
    }

    &.is-spacer .date {
      visibility: hidden;
    }
  }

  .card-link {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    color: var(--ink);
    text-decoration: none;

    &:hover h3 {
      text-decoration: underline;
      text-decoration-color: var(--red-text);
      text-decoration-thickness: 2px;
    }

    &:focus-visible {
      outline: 3px solid var(--ink);
      outline-offset: 4px;
      border-radius: 12px;
    }
  }

  .thumb {
    position: relative;
    aspect-ratio: 16 / 9;
    overflow: hidden;
    background: var(--ink);
    border: 2px solid var(--ink);
    border-radius: 12px;
    box-sizing: border-box;

    .thumb-img {
      display: block;
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .thumb-bg {
      position: absolute;
      inset: -10%;
      width: 120%;
      height: 120%;
      object-fit: cover;
      filter: blur(14px);
      opacity: 0.85;
    }

    .thumb-portrait {
      position: absolute;
      left: 50%;
      top: 0;
      height: 100%;
      width: auto;
      transform: translateX(-50%);
    }
  }

  .tag {
    position: absolute;
    top: 0.6rem;
    left: 0.6rem;
    padding: 3px 10px;
    border: 2px solid transparent;
    border-radius: 999px;
    font-size: 0.8125rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .tag-ppp {
    background: var(--ink);
    border-color: var(--paper);
    color: var(--paper);
  }

  .tag-talk {
    background: var(--red-text);
    border-color: var(--paper);
    color: var(--paper);
  }

  .tag-short {
    background: var(--paper);
    border-color: var(--ink);
    color: var(--ink);
  }

  .tag-new {
    left: auto;
    right: 0.6rem;
    background: var(--red-text);
    border-color: var(--paper);
    color: var(--paper);
  }

  h3 {
    margin: 0.25rem 0 0;
    font-weight: 700;
    font-size: 1.75rem;
    line-height: 1.05;
  }

  .excerpt {
    margin: 0;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    overflow: hidden;
    color: var(--ink-soft);
    font-size: 0.9375rem;
    line-height: 1.5;
  }

  .meta {
    margin: 0;
    color: var(--ink-soft);
    font-size: 0.875rem;
  }

  .more-articles {
    margin-top: 3rem;
    text-align: center;

    button {
      padding: 0.875rem 2.5rem;
      background: var(--red-text);
      border: 2px solid var(--ink);
      border-radius: 12px;
      box-shadow: 4px 4px 0 var(--ink);
      color: var(--paper);
      font: inherit;
      font-size: 1.1875rem;
      font-weight: 800;
      cursor: pointer;
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
  }
}
</style>
