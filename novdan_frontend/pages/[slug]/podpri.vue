<template>
  <div class="content">
    <ArticleHeadlineMedium
      :medium="medium"
      :supporter-amount="supporterAmount"
      :show-buttons="false"
    />
    <SectionPaymentEmbed
      :campaign-slug="medium.donation_campaign_slug"
      :type="paymentType"
      :amount="amount"
    />
    <ArticlesFooter />
  </div>
</template>

<script setup>
import { ref } from "vue";
import ArticleHeadlineMedium from "../../components/ArticleHeadlineMedium.vue";
import SectionPaymentEmbed from "../../components/SectionPaymentEmbed.vue";
import ArticlesFooter from "../../components/ArticlesFooter.vue";

const config = useRuntimeConfig();
const apiBase = import.meta.server ? config.apiBase : config.public?.apiBase;
const route = useRoute();

const slug = encodeURIComponent(String(route.params.slug || ""));
const paymentType = route.query.enkratno === "true" ? "one_time" : "recurring";
const amount = route.query.znesek ? parseInt(route.query.znesek, 10) : null;

const { data: medium, error: mediumError } = await useAsyncData(
  `${slug}-medium`,
  () =>
    $fetch(`/articles/medium/${slug}/`, {
      baseURL: apiBase,
    }),
);

if (
  mediumError.value ||
  !medium.value ||
  !medium.value.donation_campaign_slug
) {
  throw createError({ statusCode: 404, message: "Medium not found" });
}

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
