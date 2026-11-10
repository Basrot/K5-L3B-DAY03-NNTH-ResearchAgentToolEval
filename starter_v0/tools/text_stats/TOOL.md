---
name: text_stats
track: core
kind: local_formatter
requires_env: []
inputs: [text, wpm]
outputs: [word_count, char_count, sentence_count, paragraph_count, reading_time_minutes]
side_effect: false
---
# text_stats

Computes descriptive statistics for a given text, including word count, character count, sentence count, paragraph count, and estimated reading time in minutes based on words-per-minute (WPM).

