# The Success Code: stick-figure reel style guide

Every reel must follow this look so the page feels like one brand.

## Format
- 1080x1920 vertical, 30 fps, H.264 + AAC, 18-30 seconds, under 15 MB.
- `engine/example_stairs.py` is the reference implementation. Copy it and change the story,
  scene drawing, captions and timeline. Keep the helpers (`line`, `man`, `caption`, `mix`,
  `seg`, `wob`) and the music generator.

## Look
- Paper background (244,239,230) with fixed grain. Ink (28,28,30). Gold accent (212,154,31). Grey (140,136,130) for the "other" or "quitter" figure.
- Hand-drawn stick figures with the 4-frame "boil" wobble, 8 px round strokes, and a hollow head.
- Brand tag "THE SUCCESS CODE" with a gold underline at the top of every scene.
- Captions: Inter ExtraBold 64 px, uppercase, 1-2 lines, key words in gold, fade and slide in.
- Speech/thought bubbles: white rounded box, Lora Italic.
- End card on plain paper: the big lesson line (Inter ExtraBold 78, last line gold), then "— The Success Code" and "Follow for daily wisdom" (Lora Italic).

## Story rules
- One clear lesson per reel, told visually in 3-5 beats: setup, struggle, turning point, payoff, lesson card.
- Vary the visual metaphor: stairs, a road with forks, a mountain, digging for gold, planting a tree,
  two paths, a race, a bridge, a boxing ring, a chess board, a coin jar growing, a door, etc.
  Don't reuse the same metaphor within 7 days (check `posted-log.md`).
- Themes: success, growth, discipline, leadership, money habits / building wealth, mindset, failure, patience.
- Quotes from real people must be verified with a web search. Attribute them exactly, or say
  "often attributed to" when the attribution is disputed. Never invent quotes. Don't give specific
  financial advice; money content should be about habits and mindset.
- Never draw known cartoon characters, logos or brands.

## Music
- Generated in code, piano-like arpeggios. Vary the key, chord progression and tempo per reel
  (for example I–V–vi–IV, vi–IV–I–V, I–vi–IV–V; 80-110 bpm). Add a lift at the payoff.
