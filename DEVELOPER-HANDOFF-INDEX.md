# Developer Handoff: index.html — Answer Lead Rewrite

## Priority: HIGH
## Target: Homepage hero section / first visible paragraph

---

## What to Change

The homepage (index.html) needs an "Answer Lead" — a plain-language sentence in the first visible paragraph that Google's AI Overviews and featured snippets can extract directly.

### Current State
The hero section likely uses brand-voice copy without a direct factual statement about what Crawford Brothers is.

### Recommended First Paragraph (on-brand)
Add this as the first visible `<p>` element after the hero, or as a subtitle within the hero:

> Crawford Brothers Steakhouse is a chef-driven steakhouse in the Fenton district of Cary, NC, featuring an in-house dry-aging program, a 300-bottle sommelier-curated wine list, and private dining in the Gangster Room. Open daily for dinner, 5–10pm.

### Why This Matters
- Google AI Overviews pull from the first clear factual statement on a page
- "What is Crawford Brothers" and "best steakhouse Cary NC" queries need a direct answer to extract
- Without an Answer Lead, Google pulls from third-party sites (Yelp, TripAdvisor) instead of your own site

### Implementation Notes
- Keep the brand voice in the hero H1 — don't touch the headline
- Add the Answer Lead as the first `<p>` in a `text-section` immediately below the hero
- Use `<strong>` on "Crawford Brothers Steakhouse" for emphasis signal
- Do NOT wrap it in an `<h2>` — keep it as body copy so it reads naturally

### Additional index.html Recommendations
1. Add Restaurant schema (same block as blog posts — already templated)
2. Add FAQPage schema with 3-4 questions:
   - "What kind of restaurant is Crawford Brothers?"
   - "Where is Crawford Brothers located?"
   - "Does Crawford Brothers take reservations?"
   - "What is the dress code at Crawford Brothers?"
3. Ensure canonical URL matches the live domain

---

*Generated from Gemini + Claude audit synthesis, March 2026*
