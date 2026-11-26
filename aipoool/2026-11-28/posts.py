FOOT = ("Follow AIPOOOL to stay ahead in the race of Tech & AI.\n"
        "Subscribe to our newsletter on LinkedIn: https://lnkd.in/gnUKzght")
BASE = "#tech #innovation #AI #AIautomation #ArtificialIntelligence"

POSTS = [
    {
        "id": "d1128am", "when": "2026-11-28T08:30:00", "kind": "video",
        "tag": "ROBOTICS",
        "title": "XPENG's IRON robot\ngoes to production",
        "points": [
            ("2027", "Mass production of IRON\nhardware from January"),
            ("76", "Degrees of freedom\nacross the whole body"),
            ("2,250", "TOPS from three in-house\nTuring AI chips"),
            ("2.5", "Minutes to build one IRON\nat full line capacity"),
        ],
        "voiceover": [
            "Chinese carmaker XPENG is taking its IRON humanoid robot into mass production.",
            "Hardware production is scheduled to begin in January 2027.",
            "The robot has seventy-six degrees of freedom across its body.",
            "Three in-house Turing chips give it two thousand two hundred and fifty TOPS of computing power.",
            "At full capacity, the line can build one robot every two and a half minutes.",
            "outro",
        ],
        "body": """XPENG is taking its humanoid robot from the stage to the production line.

At XPENG AI Day 2026 in Guangzhou on 25 November, the Chinese EV maker showed the new version of IRON and said mass production of the hardware is scheduled to begin in January 2027.

The key facts:
- 170 cm tall and 62 kg, with 76 degrees of freedom across the body
- Dexterous hands with 21 degrees of freedom each, and more than 1,500 tactile sensing points
- Three in-house Turing AI chips with 2,250 TOPS of computing power
- A solid-state battery pack: about 1.5 hours of work from a 20-minute charge
- At full capacity, the production line can build one IRON every 2.5 minutes

The rollout is cautious. IRON will first be trained as a sales assistant in XPENG's own retail stores from the first quarter of 2027, with a wider commercial release planned for the second quarter. Early roles include reception, store guidance and exhibition hosting, not homes.

Chairman He Xiaopeng said humanoid robotics must "move beyond demonstrations", and described himself as optimistic in the long term but cautious in the short term.

What this means for businesses: carmakers are bringing factory-scale manufacturing to humanoids. The first real use cases are front-of-house roles, so judge them on reliability and cost per task rather than on launch-day demos.""",
        "tags": "#Robotics #HumanoidRobots #PhysicalAI #XPENG #Manufacturing",
    },
    {
        "id": "d1128mid", "when": "2026-11-28T15:30:00", "kind": "image",
        "tag": "AI MODELS",
        "title": "A 27B AI model that\nfits in 5.9 GB",
        "points": [
            ("5.9 GB", "Model size, against 53.8 GB\nfor the full FP16 version"),
            ("75.6", "SWE-bench Verified score,\nup from 60.8 in Bonsai 2"),
            ("204/s", "Tokens per second on one\nRTX 4090 graphics card"),
            ("Apache", "Open weights under the\nApache 2.0 licence"),
        ],
        "body": """A capable AI coding agent no longer needs a data centre.

On 24 November, PrismML released Ternary Bonsai 2.5 27B, an open-weight model built on Qwen3.8 27B and compressed so each weight is stored as -1, 0 or +1.

The key facts:
- 5.93 GB on disk at 1.76 bits per weight, against 53.8 GB for the full FP16 model
- SWE-bench Verified: 75.6, up from 60.8 for Bonsai 2 and close to 80.6 for the full model
- AppWorld agent benchmark: 90.5, against 93.2 for the full model
- 204 tokens per second on a single RTX 4090 graphics card, and 291 on an NVIDIA H100, using multi-token prediction
- Runs on NVIDIA and Intel GPUs through llama.cpp, and on Mac, iPhone and iPad through MLX
- Weights released under the Apache 2.0 licence

The limits: these are PrismML's own benchmarks, and the compressed model still trails the full version on most tests, most clearly on Terminal-Bench 2.1 (60.1 against 70.8).

PrismML is aiming it at coding assistants for private code, document analysis and desktop assistants, where data stays on the device.

What this means for businesses: agent workloads that once needed a cloud API can now run on a single workstation. For sensitive code and documents, a local model is becoming a serious option.""",
        "tags": "#AIModels #OpenSourceAI #EdgeAI #AIAgents #LocalAI",
    },
    {
        "id": "d1128pm", "when": "2026-11-28T18:30:00", "kind": "image",
        "tag": "AI AGENTS",
        "title": "AI agents now shop\nBlack Friday deals",
        "points": [
            ("Nov 24", "Walmart opens Black Friday\ndeals to Meta's Muse"),
            ("Gateway", "Walmart's own systems pick\nthe matching products"),
            ("Limits", "Shoppers set spending caps\nand can require approval"),
            ("5,000+", "Gopuff products Muse can\nnow order for delivery"),
        ],
        "body": """This Black Friday, some shoppers will not visit a store or a website at all. Their AI agent will.

On 24 November, Walmart said customers can now shop its Black Friday deals directly through Muse, Meta's AI agent. Muse connects to Walmart's Agent Gateway instead of browsing Walmart.com like a person.

How it works:
- The shopper asks Muse for something, for example a TV deal or a gift under a set budget
- Walmart's own systems find the matching products and return them to Muse
- The shopper signs in to their Walmart account and sets up an Agent Profile with a spending limit
- Orders can require approval, checkout uses a card saved in the Walmart account, and agent orders are marked in purchase history
- Walmart.com prices, membership benefits and the normal return policy still apply

Walmart is not alone. On the same day, Gopuff launched a Muse connector covering more than 5,000 products at the nearest Gopuff, with delivery in as little as 15 minutes.

Walmart has not shared any figures yet on how many customers use the feature.

What this means for businesses: retailers are deciding how AI agents get into their store. Building your own agent gateway keeps control of products, prices, customer data and approvals, rather than letting outside bots scrape your site.""",
        "tags": "#AIAgents #AgenticCommerce #Retail #Ecommerce #BlackFriday",
    },
]

def caption(p):
    return f"{p['body']}\n\n{FOOT}\n\n{BASE} {p['tags']}"
