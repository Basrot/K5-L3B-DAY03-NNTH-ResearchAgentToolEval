---
name: deduplicate_sources
track: core
kind: local_formatter
requires_env: []
inputs: [urls]
outputs: [urls, duplicate_count, invalid_count]
side_effect: false
---
# deduplicate_sources

Removes duplicate HTTP(S) source URLs while preserving the first occurrence and input order. URL fragments and trailing slashes are ignored when detecting duplicates; query strings are kept because they can identify distinct resources.
