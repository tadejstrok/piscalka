const OG_TITLE = "Piščalka – medijska platforma na ljudski pogon";
const OG_DESCRIPTION =
  "Ustvarjamo informativne vsebine z upanjem v boljši svet. Gradimo neodvisno alternativo obstoječemu medijskemu ekosistemu. Našo neodvisnost zagotavljate podporniki.";
const OG_IMAGE = "https://piscalka.si/og.png";

export default defineNuxtConfig({
  compatibilityDate: "2026-07-15",
  app: {
    baseURL: process.env.NUXT_APP_BASE_URL || "/",
    head: {
      htmlAttrs: {
        lang: "sl",
      },
      title: OG_TITLE,
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { name: "format-detection", content: "telephone=no" },

        { property: "og:site_name", content: OG_TITLE },
        { property: "og:type", content: "website" },
        { name: "author", content: "Danes je nov dan" },
        { name: "twitter:creator", content: "@danesjenovdan" },
        { name: "twitter:card", content: "summary_large_image" },
        {
          hid: "og-title",
          property: "og:title",
          content: OG_TITLE,
        },
        {
          hid: "twitter-title",
          name: "twitter:title",
          content: OG_TITLE,
        },
        {
          hid: "description",
          name: "description",
          content: OG_DESCRIPTION,
        },
        {
          hid: "og-description",
          property: "og:description",
          content: OG_DESCRIPTION,
        },
        {
          hid: "twitter-description",
          name: "twitter:description",
          content: OG_DESCRIPTION,
        },
        {
          hid: "og-image",
          property: "og:image",
          content: OG_IMAGE,
        },
        {
          hid: "twitter-image",
          name: "twitter:image",
          content: OG_IMAGE,
        },
      ],
      link: [
        { rel: "icon", href: "/favicon.ico", sizes: "any" },
        {
          rel: "icon",
          type: "image/png",
          sizes: "192x192",
          href: "/icon-192.png",
        },
        { rel: "apple-touch-icon", href: "/apple-touch-icon.png" },
        { rel: "stylesheet", href: "/fonts/selfhosted.css" },
        {
          rel: "alternate",
          type: "application/rss+xml",
          title: "RSS feed",
          href: "https://denarnica.novdan.si/articles/feed/rss/",
        },
        {
          rel: "alternate",
          type: "application/atom+xml",
          title: "Atom feed",
          href: "https://denarnica.novdan.si/articles/feed/atom/",
        },
      ],
      script: [
        {
          src: "https://plausible.lb.djnd.si/js/plausible.js",
          async: true,
          defer: true,
          "data-domain": "novdan.si",
        },
      ],
    },
  },
  css: ["~/assets/main.scss"],
  modules: ["@nuxt/eslint"],
  experimental: {
    appManifest: false,
  },
  runtimeConfig: {
    apiBase: process.env.NUXT_API_BASE,
    public: {
      apiBase: process.env.NUXT_API_BASE_BROWSER || process.env.NUXT_API_BASE,
    },
  },
});
