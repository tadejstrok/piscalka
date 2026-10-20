<template>
  <div class="content">
    <ArticleHeadlineMedium
      :medium="medium"
      :supporter-amount="supporterAmount"
    />
    <SectionArticlesAll :articles="articles" />
    <ArticlesFooter />
  </div>
</template>

<script setup>
import { ref } from "vue";
import ArticleHeadlineMedium from "../components/ArticleHeadlineMedium.vue";
import SectionArticlesAll from "../components/SectionArticlesAll.vue";
import ArticlesFooter from "../components/ArticlesFooter.vue";

const SLUG = "ppporocila";

const config = useRuntimeConfig();
const apiBase = import.meta.server ? config.apiBase : config.public?.apiBase;

const { data: medium, error: mediumError } = await useAsyncData(
  `${SLUG}-medium`,
  () =>
    $fetch(`/articles/medium/${SLUG}/`, {
      baseURL: apiBase,
    }),
);

const { data: initialArticles, error: articlesError } = await useAsyncData(
  `${SLUG}-articles`,
  () => fetchAllArticles(apiBase, SLUG),
);

if (
  mediumError.value ||
  articlesError.value ||
  !medium.value ||
  !medium.value.donation_campaign_slug
) {
  throw createError({ statusCode: 404, message: "Medium not found" });
}

const articles = ref(initialArticles.value);

const supporterAmount = ref(0);
try {
  const podpriData = await $fetch(
    `https://podpri.djnd.si/api/donation-campaign/${medium.value.donation_campaign_slug}/`,
  );
  supporterAmount.value = podpriData?.active_monthly_subscriptions || 0;
} catch {
  // ignore errors
}
</script>
