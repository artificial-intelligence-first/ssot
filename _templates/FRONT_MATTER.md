---
title: Topic Name
slug: topic-name
summary: "Short doc label (<20 chars)."
document_type: one of [spec, guide, reference, policy, concept]
tags: [tag1, tag2, tag3]
last_updated: YYYY-MM-DD
---
## Usage Rules

- Apply this front matter to every "official document" (AGENTS, SSOT, PLANS, SKILL, specs, designs, procedures, AI reference topics, etc.).
- Every md under `/docs` or `/knowledge` must include it; `/drafts`, `/notes`, `/scratch`, and similar work logs are exempt.
- The repository root `README.md` is the lone exception even if it is official.
- Skip it for transient notes or drafts where title/slug/tags/summary would be meaningless noise.
- Keep `summary` ultra concise (<=20 characters) and focused on the doc's label.
- Always include `document_type` using one of: `spec`, `guide`, `reference`, `policy`, `concept`.
- Close the front matter and immediately begin the first heading/content with no blank line in between.
