---
layout: layouts/video_page.njk
title: Video - Mr Dhuha
page_heading: "Semua Video"
page_description: "Kumpulan video penjelasan sains dan data untuk memudahkan pemahaman Anda."
pagination:
  data: collections.videos
  size: 6
  alias: videos
  reverse: true
permalink: "video/{% if pagination.pageNumber > 0 %}{{ pagination.pageNumber + 1 }}/{% endif %}index.html"
---
