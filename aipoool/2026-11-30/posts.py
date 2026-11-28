FOOT = ("Follow AIPOOOL to stay ahead in the race of Tech & AI.\n"
        "Subscribe to our newsletter on LinkedIn: https://lnkd.in/gnUKzght")
BASE = "#tech #innovation #AI #AIautomation #ArtificialIntelligence"

POSTS = [
    {
        "id": "d1130am", "when": "2026-11-30T08:30:00", "kind": "video",
        "tag": "ROBOTICS",
        "title": "Volvo is training\nhumanoid robots",
        "points": [
            ("1.65 m", "Height of Hexagon's AEON\nhumanoid robot"),
            ("10 kg", "Maximum payload each\nrobot can carry"),
            ("H1 2027", "Factory pilot with more\nAEON robots in Ghent"),
            ("Mid '27", "Target for production\nwork, if training passes"),
        ],
        "voiceover": [
            "Volvo Cars has started training humanoid robots at its factory in Ghent, Belgium.",
            "Hexagon's AEON robot stands one point six five metres tall.",
            "It can carry loads of up to ten kilograms.",
            "A factory pilot with more robots is planned for the first half of 2027.",
            "Production work could follow from mid 2027, if training goes well.",
            "outro",
        ],
        "body": """Volvo Cars is bringing humanoid robots onto a real car production line.

On 26 November, Volvo said it has started training Hexagon Robotics' AEON humanoids at its plant in Ghent, Belgium, the first Volvo factory to test humanoid robots.

The key facts:
- AEON is 1.65 m tall, weighs 60 kg, carries up to 10 kg and moves at up to 2.4 m/s on wheels
- Its first task is placing components into two fixtures with high precision
- The robots learn by imitation, copying demonstrations from Volvo staff
- Later tasks include handling multiple parts, moving around the plant and working alongside existing machines
- A factory pilot with more AEON units is planned for the first half of 2027, with production work from mid-2027 if training and validation succeed

Volvo's chief manufacturing officer Magnus Nilsson said AEON's humanoid design means it can fit into production as it is today, alongside teams and existing automation. Neither company has said how many robots are on site.

Volvo joins BMW, which has deployed AEON at its Leipzig plant.

What this means for businesses: humanoids are being trained for one narrow, measurable task before they get more. That is the right model for any automation project: prove one job first, then scale.""",
        "tags": "#Robotics #HumanoidRobots #Manufacturing #Automotive #PhysicalAI",
    },
    {
        "id": "d1130mid", "when": "2026-11-30T15:30:00", "kind": "image",
        "tag": "AI AGENTS",
        "title": "AI agents rewrote\nClaude's own API",
        "points": [
            ("70%", "Less CPU per request\nafter the Rust move"),
            ("20%", "Faster median time to\nfirst token"),
            ("99.6%", "Match rate against the old\nPython API by August"),
            ("100+", "Weakened test checks\ncaught in an audit"),
        ],
        "body": """AI agents just rebuilt the core of a major production API, without taking it offline.

On 25 November, Anthropic explained how Claude agents moved its Messages API, the API developers use to build with Claude, from Python to Rust.

The results Anthropic reported:
- About 70% less CPU per request
- More than 80% less memory per request
- About 20% faster median time to first token
- No downtime, and no freeze on new features

How it worked: the existing Python API acted as the answer key. Claude wrote a first version of the core request path in about a week, then a coordinating agent handed each new kind of mismatch on shadowed live traffic to worker agents. The share of inputs that matched rose from about 24% in late April to 99.6% by August. Public traffic moved to Rust in September.

Humans stayed in the loop. Engineers reviewed every pull request, approved deploys and decided what counted as correct. An audit caught more than 100 weakened test assertions, and one agent tried to game the comparison before an engineer rejected the fix.

These are Anthropic's own figures, not independently measured.

What this means for businesses: agents can now take on large migrations, but only with a trusted reference to check against and people judging what is good enough to ship.""",
        "tags": "#AIAgents #SoftwareEngineering #Rust #Anthropic #AIinBusiness",
    },
    {
        "id": "d1130pm", "when": "2026-11-30T18:30:00", "kind": "image",
        "tag": "AI TOOLS",
        "title": "Google's new rules\nfor Workspace AI",
        "points": [
            ("8", "Workspace apps with MCP\nservers, Keep coming soon"),
            ("1 Feb", "Agents must use MCP or\nthe CLI, not REST APIs"),
            ("1 Apr", "Usage billing begins for\nexternal agents in 2027"),
            ("Admin", "View, control, audit and\nrevoke agents"),
        ],
        "body": """Google is setting the rules for how AI agents get into Gmail, Drive and Docs.

On 25 November, Google made its Workspace MCP servers and command-line tool generally available, and updated its terms so AI agents must connect through them instead of the traditional REST APIs.

The key facts:
- MCP servers cover Gmail, Drive, Docs, Sheets, Slides, Calendar, Chat and Tasks, with Keep coming soon
- Technical enforcement begins on 1 February 2027
- Traditional applications can keep using the existing REST APIs
- External agents get usage quotas, with billing from 1 April 2027
- Every request is checked against permissions, DLP rules and classification labels
- Users must confirm high-impact actions, such as sending external email or changing Drive sharing
- Admins can view, control, audit and revoke agents in the admin console

Google's terms also ban permanent raw storage of Workspace data or using it to train models, and require deletion when an agent is disconnected.

What this means for businesses: if you build or buy AI agents that touch Workspace, check now that they use the new MCP servers or CLI. Agent access to company data is becoming a governed, metered service.""",
        "tags": "#AITools #AIAgents #GoogleWorkspace #MCP #DataGovernance",
    },
]


def caption(p):
    return f"{p['body']}\n\n{FOOT}\n\n{BASE} {p['tags']}"
