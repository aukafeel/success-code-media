FOOT = ("Follow AIPOOOL to stay ahead in the race of Tech & AI.\n"
        "Subscribe to our newsletter on LinkedIn: https://lnkd.in/gnUKzght")
BASE = "#tech #innovation #AI #AIautomation #ArtificialIntelligence"

POSTS = [
    {
        "id": "d1126am", "when": "2026-11-26T08:30:00", "kind": "video",
        "tag": "ROBOTICS",
        "title": "Ant Group bets $100M\non a humanoid maker",
        "points": [
            ("$100M", "Pre-Series A round\nled by Ant Group"),
            ("$1.6B", "Valuation, says co-founder\nWang Kai"),
            ("iX", "New wheeled humanoid\nunveiled on 23 November"),
            ("Tencent", "Existing investors Tencent,\nHongShan and Lanchi joined"),
        ],
        "voiceover": [
            "Ant Group is betting big on Chinese humanoid robot maker Simplexity Robotics.",
            "It is leading a one hundred million dollar pre-Series A funding round.",
            "Co-founder Wang Kai says that values the company at one point six billion dollars.",
            "This week Simplexity unveiled iX, a wheeled humanoid that serves drinks and guides visitors.",
            "Existing backers Tencent, HongShan and Lanchi Ventures also joined the round.",
            "outro",
        ],
        "body": """Ant Group is leading a $100 million bet on one of China's youngest humanoid robot makers.

Simplexity Robotics has raised $100 million in a pre-Series A round led by Ant Group, valuing the company at $1.6 billion, chairman and co-founder Wang Kai told Bloomberg. Existing investors Tencent, HongShan and Lanchi Ventures also took part, TechNode reported on 23 November.

The key facts:
- Simplexity was founded in July 2025 by former executives of Chinese EV maker Li Auto: CEO Jia Peng, chairman Wang Kai and COO Wang Jiajia
- It is based in Hangzhou
- By March 2026 it had already raised about 2 billion yuan (around $289 million) across five rounds in less than six months, Yicai reported, passing a $1 billion valuation
- On 23 November it unveiled iX, a wheeled humanoid shown preparing and delivering drinks, fetching objects and guiding visitors
- The company builds its own hardware and AI models, and plans to start in closed settings such as factories, supermarkets and logistics

What makes it stand out is the team's car-industry background: building complex machines at scale is exactly the skill humanoid makers now need.

What this means for businesses: service humanoids are attracting serious money from China's biggest tech groups. Expect more robots aimed at reception, guiding and fetch-and-carry tasks, and judge them on uptime and cost per task rather than on launch demos.""",
        "tags": "#Robotics #HumanoidRobots #PhysicalAI #Startups #VentureCapital",
    },
    {
        "id": "d1126mid", "when": "2026-11-26T15:30:00", "kind": "image",
        "tag": "AI TOOLS",
        "title": "AWS's DevOps agent\ncan now take action",
        "points": [
            ("5", "Services it can now act in,\nincl. GitHub and GitLab"),
            ("PRs", "Opens and updates pull\nrequests, issues, branches"),
            ("Undo", "Can retry pipelines and\nroll back deployments"),
            ("Sandbox", "Custom agents can now run\ncode in isolated sandboxes"),
        ],
        "body": """Amazon's AI agent for IT operations has moved from suggesting fixes to carrying them out.

On 20 November, AWS updated AWS DevOps Agent so customers can let it take write actions in five outside services, according to the product's official release notes.

What it can now do:
- GitHub and GitLab: create and update pull requests and merge requests, comments, issues and branches, retry workflows and pipelines, and roll back deployments
- Azure DevOps: pull requests, branches and work items, retry build stages and roll back deployments
- ServiceNow and PagerDuty: create and update incidents and add notes

More updates landed the same week:
- 21 November: custom agents can now write and run code in a sandbox, with each run in its own temporary environment and read-only AWS access
- 21 November: the sandbox is available in all commercial AWS Regions
- 19 November: teams can connect all or part of an AWS Organization to the agent, and new accounts in a covered unit are included automatically

The common thread is that the agent no longer stops at a diagnosis. It can open the fix, update the ticket and roll back a bad release.

What this means for businesses: AI agents are getting the keys to production systems. Before switching write actions on, decide which actions are allowed, who approves them and how every change is logged.""",
        "tags": "#AITools #AIAgents #AWS #DevOps #CloudComputing",
    },
    {
        "id": "d1126pm", "when": "2026-11-26T18:30:00", "kind": "image",
        "tag": "AI AGENTS",
        "title": "AI agents designed\na new CPU",
        "points": [
            ("4.59x", "Performance per watt, across\n25 test workloads"),
            ("3.83x", "On 15 workloads not used\nfor tuning the design"),
            ("7nm", "Process used for the\npre-silicon design"),
            ("None", "Physical chips built yet;\nresults are simulated"),
        ],
        "body": """A startup says swarms of AI agents have designed a new kind of computer processor, almost from scratch.

On 18 November, Architect Labs presented Frostbite, a CPU with its own instruction set and a different way of running work in parallel. The company says its AI agents worked across the whole stack, from the compiler and instruction set down to the circuit layout and verification.

The numbers the company reported:
- 4.59x better performance per watt across 25 workloads, compared with a conventional in-order CPU core of similar size
- 3.83x on the 15 workloads that were held back and not used to tune the design
- Designed for a 7-nanometre process

The important caveats:
- These are pre-silicon results from simulation and design tools. No physical chip has been built
- The comparison core has not been publicly named
- Better efficiency is not the same as a faster chip
- The design files have not been released, and no independent tests have been published yet

Even so, it shows how far AI agents have moved: from writing code to proposing, building and checking an entire hardware design.

What this means for businesses: AI agents are starting to take on complex engineering work. The value will come from pairing them with strict testing and independent checks, so bold claims are proven before money is spent.""",
        "tags": "#AIAgents #Semiconductors #Chips #Engineering #Hardware",
    },
]

def caption(p):
    return f"{p['body']}\n\n{FOOT}\n\n{BASE} {p['tags']}"
