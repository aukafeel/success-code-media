import sys, json
sys.path.insert(0, "/home/claude/success-code-media/aipoool/tools")
import make_posts as M
SEGS = [
 "How does a robot actually work? Every robot follows the same three steps: sense, think, and act.",
 "First, it senses. Cameras see, microphones hear, and touch sensors feel. A balance sensor tells it which way is up.",
 "Then it thinks. A computer, often running A.I. models, works out what it is seeing, and plans the next move.",
 "Then it acts. Electric motors in each joint move its arms, hands and legs.",
 "And it repeats this loop many times every second, checking and correcting as it goes.",
 "That is how a humanoid keeps its balance, or picks up a cup without crushing it.",
 "Newer robots use a single A.I. model that turns what they see and hear straight into actions.",
 "So, sensors are its senses, the computer is its brain, and the motors are its muscles.",
 "outro"]
r = M.voiceover(SEGS, "vo.mp3")
json.dump({"starts": r[1], "dur": M.duration("vo.mp3")}, open("cues.json", "w"))
print(r[1], M.duration("vo.mp3"))
