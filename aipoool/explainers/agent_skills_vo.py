import sys, json
sys.path.insert(0, "/home/claude/success-code-media/aipoool/tools")
import make_posts as M
SEGS = [
 "What are agent skills? Think of them as training manuals that an A.I. agent picks up when it needs them.",
 "A skill is just a folder. Inside is a file called skill dot M D, with a name, a short description, and step-by-step instructions.",
 "It can also hold scripts, templates and reference files.",
 "At the start, the agent only reads each skill's name and description. So it can keep many skills ready, without slowing down.",
 "When a task matches, like, make a sales report in Excel, it opens that skill, and follows the full instructions.",
 "Extra files are only opened when they are needed.",
 "And you can write your own skills, for your company's way of working, like your brand style, or your reporting process.",
 "So, the model is the brain. Skills are the know-how it picks up for each job.",
 "outro"]
r = M.voiceover(SEGS, "vo.mp3")
json.dump({"starts": r[1], "dur": M.duration("vo.mp3")}, open("cues.json", "w"))
print(r[1], M.duration("vo.mp3"))
