const { DateTime } = require("luxon");

module.exports = function(eleventyConfig) {
  // Passthrough copy for images and CSS
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/favicon.ico");
  eleventyConfig.addPassthroughCopy("src/admin");
  
  // Colocate images in content directories
  eleventyConfig.addPassthroughCopy("src/content/**/*.{jpg,jpeg,png,gif,svg}");

  // Figure shortcode for images with captions
  eleventyConfig.addShortcode("figure", function(src, alt, caption) {
    return `<figure class="my-8">
      <img src="${src}" alt="${alt}" class="w-full rounded-xl shadow-md border border-border">
      <figcaption class="text-center text-sm text-textLight mt-3 italic">${caption}</figcaption>
    </figure>`;
  });

  // Custom filter for resolving colocated assets
  eleventyConfig.addFilter("resolveAsset", function(assetPath, inputPath) {
    if (!assetPath) return "";
    
    // If the path is already absolute or a URL, return as is
    if (assetPath.startsWith("/") || assetPath.startsWith("http")) {
      return encodeURI(assetPath);
    }
    
    // Otherwise, it's a relative path (e.g. from Sveltia CMS)
    // Sveltia saves the image alongside the markdown file.
    // Example inputPath: "./src/content/articles/slug/index.md"
    // We want the output to be: "/content/articles/slug/image.jpg"
    
    let dir = inputPath.replace(/^\.\/src/, ""); // Remove ./src
    dir = dir.substring(0, dir.lastIndexOf("/") + 1); // Get directory part
    
    let cleanAssetPath = assetPath.replace(/^\.\//, ""); // Remove leading ./ from asset
    
    return encodeURI(dir + cleanAssetPath);
  });

  // Custom filter for readable dates (e.g. "12 Juni 2024")
  // Since PRD asks for Indonesian audience, we format dates in Indonesian.
  // The mockup had relative dates, but static sites generate absolute dates better unless done client-side.
  eleventyConfig.addFilter("readableDate", (dateObj) => {
    return DateTime.fromJSDate(dateObj, { zone: 'utc' }).setLocale('id').toFormat("dd MMMM yyyy");
  });

  // Create collections based on directories
  eleventyConfig.addCollection("articles", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/content/articles/**/*.md").sort((a, b) => b.date - a.date);
  });

  eleventyConfig.addCollection("videos", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/content/videos/**/*.md").sort((a, b) => b.date - a.date);
  });

  eleventyConfig.addCollection("series", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/content/series/**/*.md").sort((a, b) => b.date - a.date);
  });

  eleventyConfig.addCollection("explorations", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/content/explorations/**/*.md").sort((a, b) => b.date - a.date);
  });

  // Extract unique topics from articles and videos
  eleventyConfig.addCollection("topics", function(collectionApi) {
    let topicSet = new Set();
    const items = collectionApi.getFilteredByGlob(["src/content/articles/**/*.md", "src/content/videos/**/*.md"]);
    items.forEach(item => {
      if ('topic' in item.data) {
        topicSet.add(item.data.topic);
      }
    });
    return [...topicSet].sort();
  });

  // Custom filters to get previous and next items in a series
  eleventyConfig.addFilter("getPreviousInSeries", function(currentItem, collections) {
    if (!currentItem.data.series) return null;
    const series = currentItem.data.series;
    
    // Combine both articles and videos, then filter by series
    const allItems = [...(collections.articles || []), ...(collections.videos || [])];
    const seriesItems = allItems.filter(item => item.data.series === series);
    
    // Sort chronologically (oldest first) so that "Next" means a newer post.
    // Wait, the collections.articles is sorted b.date - a.date (newest first).
    // So we need to reverse it to chronological order for series step progression.
    seriesItems.sort((a, b) => a.date - b.date);
    
    const currentIndex = seriesItems.findIndex(item => item.url === currentItem.url);
    if (currentIndex > 0) {
      return seriesItems[currentIndex - 1];
    }
    return null;
  });

  eleventyConfig.addFilter("getNextInSeries", function(currentItem, collections) {
    if (!currentItem.data.series) return null;
    const series = currentItem.data.series;
    
    const allItems = [...(collections.articles || []), ...(collections.videos || [])];
    const seriesItems = allItems.filter(item => item.data.series === series);
    
    seriesItems.sort((a, b) => a.date - b.date);
    
    const currentIndex = seriesItems.findIndex(item => item.url === currentItem.url);
    if (currentIndex !== -1 && currentIndex < seriesItems.length - 1) {
      return seriesItems[currentIndex + 1];
    }
    return null;
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data"
    },
    templateFormats: ["md", "njk", "html"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    dataTemplateEngine: "njk"
  };
};
