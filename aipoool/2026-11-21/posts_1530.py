FOOT = ("Follow AIPOOOL to stay ahead in the race of Tech & AI.\n"
        "Subscribe to our newsletter on LinkedIn: https://lnkd.in/gnUKzght")
BASE = "#tech #innovation #AI #AIautomation #ArtificialIntelligence"

POSTS = [
    {
        "id": "d1121mid", "when": "2026-11-21T15:30:00", "kind": "image",
        "tag": "AI MODELS",
        "title": "Google's Gemini 4 Neon\njoins the top three",
        "points": [
            ("#3", "On the Artificial Analysis\nIntelligence Index (61)"),
            ("$3", "Per million input tokens,\n$15 per million output"),
            ("1M", "Token context window,\nfour thinking levels"),
            ("#1", "On the AA Coding Agent\nIndex at 58.6"),
        ],
        "body": """Google has a new model in the top three, and it is not its biggest one.

Gemini 4 Neon, released on 18 November, sits between Gemini 4 Hydrogen and Gemini 4 Carbon in the Gemini 4 family. It is built for deeper analysis, coding and long-running agent tasks.

The key numbers:
- Scores 61 on the Artificial Analysis Intelligence Index at its highest thinking level, third overall behind Claude Fable 5.2 and GPT-6.2 Astra, and one point ahead of Gemini 4 Carbon
- Ranks first on the Artificial Analysis Coding Agent Index at 58.6
- Priced at $3 per million input tokens and $15 per million output tokens, with cached input at $0.15
- 1 million token context window and four thinking levels, from low to extra high
- Available in the paid Gemini API, AI Studio, Antigravity and the Gemini app for Pro and Ultra subscribers

One trade-off to know: at its highest setting, Neon takes longer per task than many similar models.

What this means for businesses: a mid-priced model now competes with the very top. Before paying for the biggest model, test whether a cheaper one does the job just as well for your tasks.""",
        "tags": "#Gemini #GoogleAI #AIModels #LLM #GenerativeAI",
    },
    {
        "id": "d1122mid", "when": "2026-11-22T15:30:00", "kind": "image",
        "tag": "AI AGENTS",
        "title": "Banks: your AI agent,\nyour responsibility",
        "points": [
            ("Citi", "Customers liable for third-\nparty AI agent activity"),
            ("Hacked", "Still the customer's risk if\nan agent leaks a login"),
            ("PNC", "Changed its terms on\n18 November"),
            ("Read", "Read-only open banking\naccess still allowed"),
        ],
        "body": """If you let an AI agent into your bank account, the bank now says the risk is yours.

Citi has updated its Online User Agreement with a new section on third-party AI agents. Customers who give an outside AI agent access to their accounts are responsible for what that agent does, TechCrunch reported on 18 November.

What the new rules say:
- Access and transactions by an AI agent are treated as authorised by the customer
- If an agent leaks or shares your login, or is hacked, what happens next is also on you
- Citi cautions customers against using third-party agents to log in or make transactions
- PNC changed its terms on 18 November, and Citizens has emailed customers a similar warning
- JPMorgan and Bank of America announced similar policies earlier; read-only access through regulated open banking providers is still allowed

Banks are not against AI agents. Citi is building its own on an internal platform called Arc. The concern is outside agents holding customer passwords.

What this means for businesses: before any AI agent touches money or customer accounts, check the terms, use official connections instead of shared passwords, and keep a human approval step for payments.""",
        "tags": "#AIAgents #Banking #FinTech #CyberSecurity #AIGovernance",
    },
]

def caption(p):
    return f"{p['body']}\n\n{FOOT}\n\n{BASE} {p['tags']}"
