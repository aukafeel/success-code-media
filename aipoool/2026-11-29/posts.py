FOOT = ("Follow AIPOOOL to stay ahead in the race of Tech & AI.\n"
        "Subscribe to our newsletter on LinkedIn: https://lnkd.in/gnUKzght")
BASE = "#tech #innovation #AI #AIautomation #ArtificialIntelligence"

POSTS = [
    {
        "id": "d1129am", "when": "2026-11-29T08:30:00", "kind": "video",
        "tag": "ROBOTAXIS",
        "title": "Uber robotaxis drop\ntheir safety drivers",
        "points": [
            ("100+", "Lucid Gravity robotaxis\ndelivered for the program"),
            ("4", "Bay Area cities in the first\ndriverless tests"),
            ("35,000", "Lucid vehicles Uber has\ncommitted to buy"),
            ("Q1 2027", "Public launch target in\nthe San Francisco Bay Area"),
        ],
        "voiceover": [
            "Uber, Nuro and Lucid have started testing robotaxis with no one behind the wheel.",
            "Lucid has delivered a fleet of more than one hundred Gravity vehicles.",
            "Driverless testing has begun in four Bay Area cities, including Palo Alto.",
            "Uber has committed to buy at least thirty-five thousand Lucid vehicles.",
            "The public launch is planned for the first quarter of twenty twenty-seven.",
            "outro",
        ],
        "body": """Uber's next robotaxi has nobody in the driver's seat.

On 24 November, Nuro, Lucid and Uber said they have started fully driverless testing on public roads in the San Francisco Bay Area, ahead of a public launch planned for the first quarter of 2027.

The key facts:
- Testing runs in Palo Alto, Mountain View, Los Altos and Sunnyvale, with more Bay Area cities to follow next year
- Lucid has delivered a fleet of more than 100 Gravity SUVs for the program
- Each vehicle carries a redundant sensor suite of cameras, lidar and radar, with a roof-mounted halo
- Nuro supplies the Level 4 self-driving system, Lucid builds the vehicles, and Uber will own and operate the fleet with partners
- Uber has committed to buy at least 35,000 Lucid vehicles equipped with the Nuro Driver
- Nuro holds a California DMV driverless testing permit, one of six companies allowed to test with no one behind the wheel

The next step is driverless rides for employees, which the companies say will start soon. Paying riders come later.

What this means for businesses: autonomy is becoming a partnership model, with one company for the software, one for the vehicle and one for the customer. Expect the same split in other areas of physical AI, from delivery to logistics.""",
        "tags": "#Robotaxi #AutonomousVehicles #PhysicalAI #Uber #SelfDriving",
    },
    {
        "id": "d1129mid", "when": "2026-11-29T15:30:00", "kind": "image",
        "tag": "AI TOOLS",
        "title": "AI agents can now\napprove code changes",
        "points": [
            ("3", "Agents: Code Review, PR\nSteward, Claude Approvals"),
            ("Policy", "Teams write approval rules\nas a file in the repo"),
            ("Human", "Changes marked for review\ngo to a person to decide"),
            ("Beta", "Team and Enterprise plans,\nfor GitHub repositories"),
        ],
        "body": """AI coding agents are moving from writing code to deciding what is ready to merge.

On 23 November, Anthropic launched Claude Ship, a set of three AI agents that take a pull request through review, fixes and an approval decision.

How it works:
- Code Review, already generally available, reviews proposed changes and flags problems
- PR Steward, in beta, handles failing CI checks, merge conflicts and review feedback, and comments after every push on what it changed and how to roll it back
- Claude Approvals, in beta, applies an approval policy the team writes in plain language as a file in the repository
- Changes that pass the policy are approved, and changes the team marks for escalation go to a human

The controls:
- Teams choose where it runs and the review depth: Quick, Standard or Deep
- Monthly spending limits can be set
- Anthropic suggests starting with approvals in observe-only mode, and teams can begin with a single repository

Claude Ship is rolling out to Claude Team and Enterprise plans for repositories on GitHub. Anthropic has not published usage figures for it yet.

What this means for businesses: the bottleneck in software is shifting from writing code to reviewing it. Before handing approval to an agent, write down which changes are routine, which always need a person, and how every decision is logged.""",
        "tags": "#AITools #AIAgents #SoftwareDevelopment #DevOps #Anthropic",
    },
    {
        "id": "d1129pm", "when": "2026-11-29T18:30:00", "kind": "image",
        "tag": "AI MODELS",
        "title": "Open AI translation\nfor 102 languages",
        "points": [
            ("102", "Languages covered, up\nfrom 38 in Hy-MT2"),
            ("3", "Model sizes: 1.8B, 7B\nand 30B-A3B"),
            ("-74%", "Fewer outputs with missing\nor added text vs Hy-MT2"),
            ("Apache", "Open weights under the\nApache 2.0 licence"),
        ],
        "body": """Machine translation for 102 languages is now available as open weights.

On 24 November, Tencent released Hy-MT3, the third generation of its open-source Hunyuan translation models.

The key facts:
- Three sizes: 1.8B and 7B dense models, and a 30B mixture-of-experts model with about 3B active parameters
- Language coverage grows from 38 to 102
- Weights are on Hugging Face under the Apache 2.0 licence, with standard, FP8 and GGUF builds, so the smaller models can run locally
- On real-world test data, the share of outputs with omitted or added text fell from 21.2% to 5.5% compared with Hy-MT2, a relative cut of about 74%
- Built with the Honor of Kings game team for game localisation, with an open toolchain for Unity and Unreal

The limits: the benchmarks are Tencent's own and use a scoring method it built. The 30B model leads its rivals only when they run without "thinking" mode. There are no per-language scores for the 64 new languages, Google Translate and DeepL are not in the comparison, and the context window is 8,192 tokens.

What this means for businesses: high-quality translation no longer has to leave your own servers. For product, support and game content, an open model you can test, fine-tune and run in-house is a real option, so test it on your own languages first.""",
        "tags": "#AIModels #OpenSourceAI #Translation #Localization #Tencent",
    },
]


def caption(p):
    return f"{p['body']}\n\n{FOOT}\n\n{BASE} {p['tags']}"
