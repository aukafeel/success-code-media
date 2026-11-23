FOOT = ("Follow AIPOOOL to stay ahead in the race of Tech & AI.\n"
        "Subscribe to our newsletter on LinkedIn: https://lnkd.in/gnUKzght")
BASE = "#tech #innovation #AI #AIautomation #ArtificialIntelligence"

POSTS = [
    {
        "id": "d1125am", "when": "2026-11-25T08:30:00", "kind": "video",
        "tag": "WORLD MODELS",
        "title": "Google's AI now\nbuilds live worlds",
        "points": [
            ("720p", "Worlds generated live\nat 24 frames per second"),
            ("Audio", "Native sound, from ambient\nnoise to dialogue"),
            ("Live", "Change weather, light or\nevents while you play"),
            ("API", "Open to developers in\nthe Gemini API, Nov 19"),
        ],
        "voiceover": [
            "Google's Genie 4 turns a simple prompt into a live world you can explore.",
            "It generates worlds in seven-twenty p, at twenty-four frames per second.",
            "Each world comes with its own sound, from ambient noise to dialogue.",
            "You can change the weather, the lighting or events while you explore.",
            "Since November nineteenth, developers can build with it through the Gemini A.P.I.",
            "outro",
        ],
        "body": """Google's AI can now build a world you can walk around in, live, from a single prompt.

On 19 November, Google made Genie 4, its Google DeepMind world model, available to developers through the Gemini API and Google AI Studio. A day earlier it began rolling out to eligible Google AI Ultra subscribers through Project Genie.

What Genie 4 does:
- Starts from a text prompt, a reference image, or both
- Generates continuous 720p worlds at 24 frames per second
- Adds synchronised native audio, from ambient sound and effects to character dialogue
- Lets you move with keyboard controls and type live prompts to change the weather, lighting, objects or events
- Uses Gemini to keep the world consistent as it changes
- Marks every output with an invisible SynthID watermark

Google first showed Genie 4 as a research preview on 27 October. TechCrunch reported it can keep a scene consistent for up to two minutes, and that details can still drift the longer a simulation runs.

Google lists prototyping interactive experiences, visualising spatial concepts and training robots and AI agents as key uses.

What this means for businesses: interactive 3D environments used to take a game studio. Product demos, training simulations and virtual walkthroughs can now be prototyped in minutes, which makes it cheap to test an idea before investing in a full build.""",
        "tags": "#WorldModels #GoogleDeepMind #GenerativeAI #Simulation #Gemini",
    },
    {
        "id": "d1125mid", "when": "2026-11-25T15:30:00", "kind": "image",
        "tag": "AI AGENTS",
        "title": "AI agent swarms\nwith a budget cap",
        "points": [
            ("Goal", "You set the outcome and\nthe success criteria"),
            ("Budget", "A spending cap for the\nwhole mission"),
            ("$3,000", "Budget for a monitoring\nplatform built in 2 days"),
            ("19x", "NumPy speed-up with 32\nagents, Replit's own test"),
        ],
        "body": """Replit wants you to hand AI agents a goal and a budget, not a list of prompts.

On 17 November, Replit launched Missions. Instead of guiding one coding agent step by step, you agree a "mission" up front and Replit coordinates a swarm of agents that plan, build, test and iterate until the goal is met or the budget runs out.

How a mission works:
- You set the goal, the approach and clear success criteria
- You set a spending cap for Replit AI usage on the whole mission
- You set boundaries, such as actions that need your approval first
- Agents work in parallel, each in its own isolated cloud environment
- An independent AI judge checks the result against the agreed criteria before it comes back to you

Replit's own examples: a swarm of agents built a monitoring platform with dashboards, alerts and application tracing in two days within a $3,000 budget. On 13 NumPy performance tasks, a single agent reached speed-ups of up to 4x, while a 32-agent swarm reached 19x. These are Replit's own tests.

Replit is also clear about the limits: work already running can go slightly over budget before it stops, and an automated sign-off does not guarantee the result is correct.

What this means for businesses: managing AI is starting to look like managing a project. Clear goals, a fixed budget, approval points and a final human review are what keep agent work useful and under control.""",
        "tags": "#AIAgents #AgenticAI #Replit #SoftwareDevelopment #Automation",
    },
    {
        "id": "d1125pm", "when": "2026-11-25T18:30:00", "kind": "image",
        "tag": "AI BUSINESS",
        "title": "Palo Alto bets $4.5B\non open AI models",
        "points": [
            ("$4.5B", "All-stock deal for\nApplied Compute"),
            ("Open", "Platform to train and run\nopen-weight AI models"),
            ("Nov 18", "Deal announced with\nPalo Alto's Q1 results"),
            ("Q3 FY27", "Expected close, subject\nto regulatory clearance"),
        ],
        "body": """One of the world's largest cybersecurity companies is buying its way into AI model training.

On 18 November, Palo Alto Networks announced it will acquire Applied Compute in an all-stock deal valued at $4.5 billion, subject to adjustments. The deal is expected to close in Palo Alto Networks' fiscal third quarter of 2027, subject to regulatory clearance.

The key facts:
- Applied Compute runs a platform for post-training and inference of open-weight AI models
- It takes open models, such as Qwen, Kimi, GLM and DeepSeek, and trains them on a company's own data and workflows
- It was founded in 2025 by former OpenAI researchers
- CEO and co-founder Yash Patil will become Palo Alto Networks' Co-Chief AI Officer
- Palo Alto plans to let enterprises train, adapt and deploy open-weight models in public cloud or sovereign environments

CEO Nikesh Arora said: "Every enterprise is going to run a mix of open and closed models, and every one of those models needs to be secured."

Not everyone is convinced. Greyhound Research analyst Sanchit Vir Gogia told CSO Online that a supervisor trained by the same party it supervises is "a colleague, not a check."

What this means for businesses: custom AI models built on open weights are going mainstream. Security, data control and independent oversight should be part of that plan from day one, not added afterwards.""",
        "tags": "#AIinBusiness #CyberSecurity #OpenSourceAI #EnterpriseAI #MergersAndAcquisitions",
    },
]


def caption(p):
    return f"{p['body']}\n\n{FOOT}\n\n{BASE} {p['tags']}"
