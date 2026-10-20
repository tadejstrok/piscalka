const PAGE_SIZE = 50;

// Loads every page of articles for a medium in one go. The static build has
// no API available in the browser, so "Več" only reveals what is embedded.
export async function fetchAllArticles(apiBase, slug) {
  const first = await $fetch("/articles/", {
    baseURL: apiBase,
    query: { medium__slug: slug, limit: PAGE_SIZE },
  });
  const results = [...first.results];
  let next = first.next;
  while (next && results.length < first.count) {
    const url = new URL(next);
    const page = await $fetch(`${url.pathname}${url.search}`, {
      baseURL: apiBase,
    });
    if (!page.results.length) {
      break;
    }
    results.push(...page.results);
    next = page.next;
  }
  return { ...first, results, next: null };
}
