FOOT = ("Follow AIPOOOL to stay ahead in the race of Tech & AI.\n"
        "Subscribe to our newsletter on LinkedIn: https://lnkd.in/gnUKzght")
BASE = "#tech #innovation #AI #AIautomation #ArtificialIntelligence"

POSTS = [
    {
        "id": "d1124am", "when": "2026-11-24T08:30:00", "kind": "video",
        "tag": "ROBOTICS",
        "title": "Humanoids sort\nmail in 8 cities",
        "points": [
            ("11", "Postal hubs across\nGuangdong province"),
            ("8", "Cities, from Guangzhou\nto Shenzhen"),
            ("1,500+", "Parcels per hour, the\naverage induction rate"),
            ("March", "Month the pilot began\nin Guangzhou"),
        ],
        "voiceover": [
            "Humanoid robots are now sorting parcels for China Post in eight cities.",
            "ROBOTERA's robots are working at eleven postal hubs across Guangdong province.",
            "The eight cities include Guangzhou, Shenzhen and Dongguan.",
            "They average more than fifteen hundred parcels an hour, comparable to experienced workers.",
            "It all started with a single pilot in Guangzhou in March.",
            "outro",
        ],
        "body": """Humanoid robots have moved from one pilot site to a province-wide postal network.

On 17 November, Chinese robotics company ROBOTERA announced that its humanoid robots now work at 11 China Post hubs in eight cities across Guangdong, China's largest province by express parcel volume.

The key facts:
- The cities are Guangzhou, Shenzhen, Dongguan, Jiangmen, Shantou, Shanwei, Jieyang and Heyuan
- The robots load parcels onto sorting lines, a job known as induction
- They achieved an average induction rate of more than 1,500 parcels per hour, which ROBOTERA says is comparable to experienced human workers
- They use the company's own five-finger dexterous hands, with irregular-item rejection and adaptive speed control to reduce jams and missed items
- It all began with a pilot at the Guangzhou Postal District Center in March 2026

Parcel induction is repetitive, physically demanding and runs around the clock during peak seasons, which makes it one of the clearest early jobs for humanoids.

What this means for businesses: the real signal is not a single demo but a rollout from one site to eleven. Logistics leaders should watch for deployments like this that scale across a network, because that is where cost, uptime and reliability get proven.""",
        "tags": "#Robotics #HumanoidRobots #Logistics #Automation #PhysicalAI",
    },
    {
        "id": "d1124mid", "when": "2026-11-24T15:30:00", "kind": "image",
        "tag": "AI TOOLS",
        "title": "ChatGPT now helps\nclose the books",
        "points": [
            ("Nov 18", "ChatGPT for Accounting\nlaunched by OpenAI"),
            ("8", "Finance app plugins, incl.\nQuickBooks, Xero, NetSuite"),
            ("Close", "Reconciliation, reports,\ndata entry and audit prep"),
            ("Human", "Final entries still need\na person's approval"),
        ],
        "body": """AI is moving into the accounting department, and it now plugs straight into the ledger.

On 18 November, OpenAI launched ChatGPT for Accounting, an accounting plugin with connections to the finance software many teams already use.

What it covers:
- Eight partner plugins, including Intuit QuickBooks, Xero, Oracle NetSuite, BILL, FreshBooks, Rillet and Campfire
- Tasks such as invoice processing, bank reconciliation, month-end reports, data entry and audit preparation
- Templates and review checks can be saved and reused for recurring work
- Final accounting entries still require human approval before changes are applied

Access is not the same everywhere. Some connections can create or update records, while others are read-only. FreshBooks, for example, says its plugin can look at your data but cannot make changes. Each user connects their own account, and the connector works within that user's permissions.

What this means for businesses: the routine parts of the month-end close are becoming AI work. Before switching it on, decide who reviews and approves AI-drafted entries, keep that separate from who prepares them, and check exactly what each connected app is allowed to change.""",
        "tags": "#AITools #Accounting #Finance #ChatGPT #Automation",
    },
    {
        "id": "d1124pm", "when": "2026-11-24T18:30:00", "kind": "image",
        "tag": "AI AGENTS",
        "title": "AT&T runs nearly 500\nAI agent workflows",
        "points": [
            ("~500", "Agentic workflows already\nin production"),
            ("45B", "AI tokens processed\nacross AT&T every day"),
            ("1M+", "Transactions handled by\nthe platform each month"),
            ("3x", "Target: triple the\nworkflows next year"),
        ],
        "body": """AT&T is not adding AI on top of old processes. It is rebuilding the processes around AI agents.

Speaking at an Amazon Web Services event in Boston, Luke Corbin, assistant vice president of digital transformation and AI at AT&T Business, shared how far the telecom giant has gone, SiliconANGLE reported on 14 November.

The numbers:
- Nearly 500 agentic workflows are already in production
- About 45 billion AI tokens are processed daily across the company
- The agentic AI platform handles more than 1 million transactions a month
- AT&T plans to triple the number of workflows next year

Real examples include fiber installation order changes, sales prospecting and provisioning. AT&T halved the time needed to provision dedicated internet in buildings that already had fiber.

The safety rule is simple. Every production workflow starts with human oversight, and agents only run on their own once accuracy reaches the mid- to high-90% range within an acceptable risk profile. Workflows that affect customers must pass security, privacy and compliance reviews through AT&T's Business Agent Foundry.

What this means for businesses: scale comes from discipline, not from more chatbots. Redesign the process first, keep people in the loop until the accuracy is proven, and put customer-facing agents through a single review path.""",
        "tags": "#AIAgents #AgenticAI #EnterpriseAI #Telecom #DigitalTransformation",
    },
]


def caption(p):
    return f"{p['body']}\n\n{FOOT}\n\n{BASE} {p['tags']}"
