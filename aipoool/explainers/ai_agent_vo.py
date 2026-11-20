import sys, json
sys.path.insert(0, "/home/claude/success-code-media/aipoool/tools")
import make_posts as M
SEGS = [
 "What is an A.I. agent? And how is it different from a chatbot?",
 "A chatbot answers your question, and then it waits for you.",
 "An agent is given a goal, and works out the steps to reach it by itself.",
 "It is built from four parts: a model that thinks, tools to take action, memory to keep track, and a loop that keeps it going.",
 "Ask it to thank your top three customers. It checks your sales data, finds the top three, and drafts each email.",
 "After every step, it looks at the result, and decides what to do next.",
 "And it can pause to ask you before anything important, like sending those emails.",
 "So, a chatbot gives you answers. An agent gets the job done.",
 "outro"]
r = M.voiceover(SEGS, "vo.mp3")
json.dump({"starts": r[1], "dur": M.duration("vo.mp3")}, open("cues.json", "w"))
print(r[1], M.duration("vo.mp3"))
