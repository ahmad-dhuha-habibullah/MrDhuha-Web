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

  // Topics Collection (from Markdown files instead of tag extraction)
  eleventyConfig.addCollection("topics", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/content/topics/**/*.md").sort((a, b) => a.data.title.localeCompare(b.data.title));
  });

  // Resolve an itemList from CMS into actual Eleventy items
  eleventyConfig.addFilter("getResolvedList", function(itemList, collections) {
    if (!itemList || !Array.isArray(itemList)) return [];
    
    return itemList.map(entry => {
      if (entry.type === 'article' && collections.articles) {
        return collections.articles.find(a => a.data.title === entry.item);
      } else if (entry.type === 'video' && collections.videos) {
        return collections.videos.find(v => v.data.title === entry.item);
      }
      return null;
    }).filter(item => item !== null);
  });

  // Find which series an article/video belongs to based on its title
  eleventyConfig.addFilter("getSeriesForTitle", function(title, collections) {
    if (!title || !collections.series) return null;
    return collections.series.find(series => {
      if (!series.data.itemList || !Array.isArray(series.data.itemList)) return false;
      return series.data.itemList.some(entry => entry.item === title);
    });
  });

  // Find which topic an article/video belongs to based on its title
  eleventyConfig.addFilter("getTopicForTitle", function(title, collections) {
    if (!title || !collections.topics) return null;
    return collections.topics.find(topic => {
      if (!topic.data.itemList || !Array.isArray(topic.data.itemList)) return false;
      return topic.data.itemList.some(entry => entry.item === title);
    });
  });

  // Get adjacent items from an itemList array
  eleventyConfig.addFilter("getAdjacentItem", function(itemList, currentTitle, direction, collections) {
    if (!itemList || !Array.isArray(itemList) || !currentTitle) return null;
    const currentIndex = itemList.findIndex(entry => entry.item === currentTitle);
    if (currentIndex === -1) return null;
    
    const adjacentIndex = direction === 'next' ? currentIndex + 1 : currentIndex - 1;
    if (adjacentIndex >= 0 && adjacentIndex < itemList.length) {
      const entry = itemList[adjacentIndex];
      if (entry.type === 'article' && collections.articles) {
        return collections.articles.find(a => a.data.title === entry.item);
      } else if (entry.type === 'video' && collections.videos) {
        return collections.videos.find(v => v.data.title === entry.item);
      }
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
