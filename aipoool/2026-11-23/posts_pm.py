FOOT = ("Follow AIPOOOL to stay ahead in the race of Tech & AI.\n"
        "Subscribe to our newsletter on LinkedIn: https://lnkd.in/gnUKzght")
BASE = "#tech #innovation #AI #AIautomation #ArtificialIntelligence"

POSTS = [
    {
        "id": "d1123pm", "when": "2026-11-23T18:30:00", "kind": "image",
        "tag": "AI AGENTS",
        "title": "Every banker gets\nan AI agent",
        "points": [
            ("$250M", "Series B co-led by General\nAtlantic and QED Investors"),
            ("$1.5B", "Valuation, 18 months after\nleaving stealth"),
            ("12x", "Year-on-year growth in\nannual recurring revenue"),
            ("2%", "Of frontier model cost for\nits own tuned models"),
        ],
        "body": """AI agents for finance just got a $1.5 billion vote of confidence.

London-based Model ML has raised $250 million in Series B funding at a $1.5 billion valuation, 18 months after launching from stealth. The round was co-led by General Atlantic and QED Investors, bringing total funding to $350 million.

What Model ML builds is simple to describe: a personal AI agent for every banker, consultant and investor. The agent learns the user's clients, live deals and preferred formats, runs on the firm's own systems and data, and turns new information into analysis in minutes rather than days.

The numbers the company shared:
- Annual recurring revenue grew 12x year on year in Q3 2026
- Daily active users grew 26x over the same period
- Its own fine-tuned open-source models run at 2% of the cost of frontier models, and in most cases five times faster, the company says
- It is not tied to one AI provider and routes each task to the model that fits best
- Customer data is never used to train AI models

The new money will expand research and engineering teams in London and New York.

What this means for businesses: the next wave of AI agents is specialised. Agents built for one profession, with its own data, formats and security rules, are winning budgets that general chatbots could not.""",
        "tags": "#AIAgents #FinTech #AgenticAI #Banking #Startups",
    },
]


def caption(p):
    return f"{p['body']}\n\n{FOOT}\n\n{BASE} {p['tags']}"
