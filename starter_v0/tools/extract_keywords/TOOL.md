---
name: extract_keywords
track: core
kind: local_formatter
requires_env: []
inputs: [text, top_k]
outputs: [keywords, total_words, unique_words]
side_effect: false
---
# extract_keywords

Extracts the most frequent and meaningful keywords from a given research or article text. It filters out common stop words and returns the top_k keywords with their occurrence counts.

