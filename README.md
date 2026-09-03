# Develop Coaching landing page

A standalone, mobile-first HTML landing page combining the Scale Session booking flow with the core Develop Mastermind offer.

## Preview locally

```bash
python3 -m http.server 4174
```

Then open `http://127.0.0.1:4174`.

## Booking integration

The booking panel in `index.html` is intentionally a visual placeholder. Replace `.calendar-placeholder` with the final scheduling embed when it is approved.

## Content and assets

The page combines the approved Develop Coaching booking-page content with the programme positioning, fit criteria, five-pillar method, toolkit, first 90 days, member results, founder section and FAQ from the Develop Mastermind page.

The Mastermind poster and testimonial images are local production assets. The main programme video streams from the existing Develop Coaching media URL to avoid adding a 33 MB video file to the repository.

The only authored conversion action is “Book a Call”; all CTA links return to the booking section. The footer contains only the requested legal links.

## Verification

```bash
python3 tests.py
npx --yes html-validate index.html
```
