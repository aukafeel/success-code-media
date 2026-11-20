import sys, json
sys.path.insert(0, "/home/claude/success-code-media/aipoool/tools")
import make_posts as M
SEGS = [
 "Who is winning the A.I. race right now? The answer depends on how you measure it.",
 "Artificial Analysis runs the same tough tests on every model, and combines them into one score.",
 "On that index, Anthropic's Claude Fable five point two leads, with about sixty-five points.",
 "OpenAI's new G.P.T. six point two Astra is second at sixty-two, and Google's brand-new Gemini four Neon is third at sixty-one.",
 "But on Arena, where people vote on blind answers, Google holds the top two spots.",
 "And the race is speeding up. The last two top models launched just eight days apart.",
 "Open models that anyone can download are close behind, now just a few points from the very top.",
 "So right now, Anthropic leads the tests, Google wins the vote, and OpenAI is closing in fast.",
 "outro"]
r = M.voiceover(SEGS, "vo.mp3")
json.dump({"starts": r[1], "dur": M.duration("vo.mp3")}, open("cues.json", "w"))
print(r[1], M.duration("vo.mp3"))
