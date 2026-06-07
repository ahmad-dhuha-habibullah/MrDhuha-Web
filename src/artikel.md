---
layout: layouts/artikel_page.njk
title: Artikel - Mr Dhuha
page_heading: "Semua Artikel"
page_description: "Kumpulan artikel sains, teknologi, dan data yang menjelaskan dunia dengan cara sederhana."
pagination:
  data: collections.articles
  size: 6
  alias: articles
  reverse: true
permalink: "artikel/{% if pagination.pageNumber > 0 %}{{ pagination.pageNumber + 1 }}/{% endif %}index.html"
---
