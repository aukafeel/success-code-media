import sys, json
sys.path.insert(0, "/home/claude/success-code-media/aipoool/tools")
import make_posts as M
SEGS = [
 "How does Claude actually work? And what makes Claude Code different?",
 "Claude is a large language model. First, your words are split into small pieces called tokens.",
 "A neural network, trained on huge amounts of text, looks at all of them, and predicts the next token. One at a time, it builds the answer.",
 "In the Claude app, you chat. You ask, Claude answers, and you copy the result into your work.",
 "Claude Code uses the same Claude models, but gives them tools.",
 "It reads your project files, plans the change, edits the code, runs the tests, checks the result, and repeats until the job is done.",
 "And you stay in control, approving changes along the way.",
 "So, Claude thinks and writes. Claude Code thinks, writes, and acts.",
 "outro"]
r = M.voiceover(SEGS, "vo.mp3")
json.dump({"starts": r[1], "dur": M.duration("vo.mp3")}, open("cues.json", "w"))
print(r[1], M.duration("vo.mp3"))
