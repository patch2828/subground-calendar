# subground-calendar

SubGround Collective's static site pages.

- `index.html` — **Upcoming**: the public show calendar (shows, pop-ups, content nights).
- `community.html` — **Common Ground**: the community space. Every artist in the Valley — day one to headliner — one room.
  - **The Door** — what it is, how it works, house rules, resident ticker.
  - **The Floor** — express wall. First posts, tracks, art, questions, wins, keeping it real. Anonymous allowed.
  - **The Circle** — big teaches small. "I can teach" / "I want to learn" boards with automatic link-up matching.
  - **The Fam** — artist directory. Name, crafts, stage (day one → veteran), mentor flags, links.

Both pages are fully self-contained (no build step, no dependencies). Deploy by uploading the folder as-is.

Note: Common Ground currently stores entries in each visitor's browser (localStorage). A shared backend is the next step to make posts visible across everyone.
