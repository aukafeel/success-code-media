FOOT = ("Follow AIPOOOL to stay ahead in the race of Tech & AI.\n"
        "Subscribe to our newsletter on LinkedIn: https://lnkd.in/gnUKzght")
BASE = "#tech #innovation #AI #AIautomation #ArtificialIntelligence"

POSTS = [
    {
        "id": "d1123am", "when": "2026-11-23T08:30:00", "kind": "video",
        "tag": "ROBOTICS",
        "title": "Atlas robot heads\ninto chip factories",
        "points": [
            ("2027", "Atlas testing begins at\nGlobalFoundries sites"),
            ("1st", "Atlas customer outside\nthe car industry"),
            ("4", "Spot sites: New York,\nVermont, Dresden, Singapore"),
            ("99%", "Spot mission success in\nSingapore, 90,000+ checks"),
        ],
        "voiceover": [
            "Boston Dynamics' Atlas humanoid is heading into chip factories.",
            "GlobalFoundries will start testing Atlas at its sites in early twenty twenty-seven.",
            "It is the first Atlas customer outside the car industry.",
            "GlobalFoundries is also expanding Spot robots to four sites, from New York to Singapore.",
            "In Singapore, Spot has run more than ninety thousand inspections, with ninety-nine percent mission success.",
            "outro",
        ],
        "body": """Boston Dynamics' Atlas humanoid is about to leave the car plant and walk into a chip factory.

On 17 November, Boston Dynamics and GlobalFoundries announced that the chipmaker will begin testing Atlas at its facilities in early 2027. GlobalFoundries becomes the first customer outside the automotive industry to test Atlas, through Boston Dynamics' early adopter program and skills development workshop.

What was announced:
- The workshop will evaluate humanoid use cases, check integration needs and start training Atlas on specific tasks
- The exact tasks and the number of robots have not been disclosed
- GlobalFoundries is expanding Spot, the four-legged robot dog, to Malta (New York), Burlington (Vermont), Dresden and Singapore
- In Singapore, two Spot robots have travelled nearly 900 km since April, run more than 90,000 inspections and reached a 99% mission success rate

GlobalFoundries says Spot has moved its maintenance from reactive to predictive, and it has a road map to more than double its inspection work.

What this means for businesses: the path to humanoids runs through proven robots first. Companies that already collect data and measure results with simpler automation are the ones now first in line to trial the next generation.""",
        "tags": "#Robotics #HumanoidRobots #BostonDynamics #Semiconductors #Manufacturing",
    },
    {
        "id": "d1123mid", "when": "2026-11-23T15:30:00", "kind": "image",
        "tag": "AI MODELS",
        "title": "A 20GB AI model that\nruns on a laptop",
        "points": [
            ("26.4B", "Total parameters, with\n3.4B active per token"),
            ("~20GB", "Memory footprint, small\nenough for a laptop"),
            ("20.1", "Intelligence Index score,\nlevel with Qwen3.8-27B"),
            ("~6x", "Cheaper per test task than\nQwen3.8-27B, says AA"),
        ],
        "body": """Mira Murati's Thinking Machines Lab has released a small open model that punches well above its size.

Inkling 2 Mini, released on 20 November, is an open-weights model under the Apache 2.0 licence. Its trick is a "looped" design: of its 24 layers, the middle 12 run three times for every token, so the model gets more thinking from the same weights.

The key facts:
- 26.4 billion total parameters, with 3.4 billion active per token
- About 20GB in total, small enough to run on consumer laptops and desktop AI computers
- Text and image input, with a context window of up to 1 million tokens
- Scores 20.1 on the Artificial Analysis Intelligence Index, level with Qwen3.8-27B
- Artificial Analysis found it about 6x cheaper and 4x faster per index task than Qwen3.8-27B
- Thinking Machines' own pricing is $0.15 per million input tokens and $0.50 per million output tokens
- Weights are on Hugging Face, with support in Ollama, vLLM and SGLang

The lab says it leads open models under 100 billion parameters on coding benchmarks such as DeepSWE, though it still trails Qwen3.8-27B on multi-turn chat and complex instructions.

What this means for businesses: capable AI no longer needs a data centre. Small open models can run privately on your own hardware, which keeps sensitive data in-house and cuts per-task costs.""",
        "tags": "#AIModels #OpenSource #LLM #EdgeAI #GenerativeAI",
    },
]


def caption(p):
    return f"{p['body']}\n\n{FOOT}\n\n{BASE} {p['tags']}"
