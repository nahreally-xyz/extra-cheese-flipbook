# Project Context & Collaboration History

## The Album

**Title:** Extra Cheese
**Artist:** NAHreally (real name: Michael Judd)
**Label:** Three Dollar Pistol Music LLC, Philadelphia PA
**Year:** 2026
**Catalog #:** TDP-021
**Format:** Physical album with booklet/zine

**Credits:**
- All songs produced, written, recorded by NAHreally
- Mixed by ialive at The Order of Infinite Ideas
- Mastered by Steel Tipped Dove
- Artwork by Michael Stone
- Proofread by Katie Choi

**Track Listing:**
1. 1010 WINS
2. Moderately Well
3. Umpteen
4. Kick in the Pants
5. FUKWITME 2
6. I Need a Hobby
7. You've Got a Friend Type Beat
8. Too Many Cooks
9. How We Always Gotta Be
10. Find Our Way
11. Human Error

**Essayists in the booklet:**
- Thomas Mattera — cheesemaker, Oaklands Farm, Gardiner ME; radio host
- Nate LeBlanc — music writer, record collector, San Jose CA; host of Dad Bod Rap Pod podcast
- NAHreally — rapper, beatmaker, rap show organizer, from Holliston MA, based in Jersey City NJ

**NAHreally Discography (from booklet):**
- TAPE (2016), TAPE 2 (2017), TAPE 3 (2018), TAPE 4 (2019), TAPE 5 (2020)
- Loose Around The Edges (2021), HACKINAWAY (2022)
- BLIP with The Expert (2024), Secret Pancake (2025), Extra Cheese (2026)

**About the "Extra Cheese" name:**
Originated from a lyric in "Shoutout To Me" on TAPE 4 (2019):
*"If I were making a pizza, I'd add some extra cheese"*
It was retroactively applied as the label imprint name to all self-released work since 2018.

---

## Collaboration History (This Chat)

### What Was Uploaded
- `extra_cheese_cover.pdf` — one landscape page, 1787×1278px
- `Extra_Cheese_interior.pdf` — 38 portrait pages, 912×1278px each

### Iteration 1 — Initial Build
**Request:** "i want to make an interactive PDF that turns pages"

Built a self-contained HTML flipbook with:
- Cover PDF shown as a full-width landscape spread
- Interior pages shown two-at-a-time
- Thumbnail strip, keyboard nav, click-to-turn

**Problem:** Cover was a single landscape image, not integrated as proper book pages.

### Iteration 2 — Proper Book Structure
**Request:** "Can you put the front cover on the left side with the page 1 page on the right then put the back cover at the back?"

Solution:
- Cropped cover PDF into two portrait halves
- Built 40-page sequence: front cover + 38 interior + back cover = 20 clean spreads
- **Error made:** Left half of cover was assigned as front cover — wrong

### Iteration 3 — Cover Swap Fix
**Request:** "ah the one with the green should be the back cover. please swap"

Fix:
- Right half of landscape cover = front cover (cheese still life, white+red bg)
- Left half of landscape cover = back cover (green bg, man + dog + cheese prop)
- Re-encoded data, injected into existing HTML without full rebuild

### Iteration 4 — Memory Log
**Request:** Comprehensive conversation memory log capturing project context, solutions, working style, etc.

Delivered as `extra_cheese_memory_log.md` (in outputs).

### Iteration 5 — Claude Code Docs (current)
**Request:** "Create a claude.md file and any appropriate docs that will capture all of the relevant context from this chat for me to use in a new claude code project repo so I can pick up in claude code where we left off"

Delivered this doc set.

---

## User's Working Style

- **Concise instructions** — short, direct, no lengthy preamble
- **Visual descriptions** — "the one with the green" not "the left half of the landscape image"
- **Iterative** — comfortable making small corrections, not over-specifying upfront
- **Trusts execution** — doesn't need to approve the approach before Claude proceeds
- **Low ceremony** — skip confirmations, just make the change and show the result
- **Expects interpretation** — Claude should figure out ambiguity and act, not ask

---

## What Was Learned About the Source Material

The cover PDF layout (left = back cover, right = front cover) is the **opposite** of typical Western book convention where the front cover would naturally be on the left when the book is closed and viewed flat. This is worth noting because it's counterintuitive and caused the initial crop error.

The interior PDF pages are in correct reading order (000 = title page, 037 = other works/discography).

The booklet's design aesthetic: bold use of green, red, and yellow; illustrations throughout the essays; clean serif typography (italic caps for essay titles); printed in the tradition of hip-hop album booklets.
