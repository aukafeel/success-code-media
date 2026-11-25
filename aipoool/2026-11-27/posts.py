FOOT = ("Follow AIPOOOL to stay ahead in the race of Tech & AI.\n"
        "Subscribe to our newsletter on LinkedIn: https://lnkd.in/gnUKzght")
BASE = "#tech #innovation #AI #AIautomation #ArtificialIntelligence"

POSTS = [
    {
        "id": "d1127am", "when": "2026-11-27T08:30:00", "kind": "video",
        "tag": "AI SCIENCE",
        "title": "OpenAI's GPT-6 is\ndesigning proteins",
        "points": [
            ("10.9%", "Of 322 lab-made designs\nbound their target protein"),
            ("5 of 5", "Targets had at least one\nworking designed binder"),
            ("70%", "Of 182 redesigned antibody\nloops still bound IL-4Ra"),
            ("13.1%", "Hit rate on three shapes\nnever published before"),
        ],
        "voiceover": [
            "OpenAI says G.P.T. six can design brand new proteins.",
            "Of three hundred twenty-two lab-made designs, ten point nine percent bound their target.",
            "At least one design worked for all five target proteins.",
            "Seventy percent of one hundred eighty-two redesigned antibody loops still bound.",
            "On three never-published shapes, the hit rate was thirteen percent.",
            "outro",
        ],
        "body": """OpenAI says its general-purpose models can design working proteins, with no specialist biology model doing the creative part.

On 24 November, OpenAI published results from a protein design campaign run with wet-lab partner Onava. GPT-6.2 generated the protein shapes, and the designs were then physically made and tested for binding.

The results OpenAI reported:
- 35 of 322 designed minibinders, or 10.9%, bound their intended target
- At least one design worked for each of the five human targets: PD-L1, IL-7Ra, TrkA, VEGF-A and IL-17A
- 128 of 182 redesigned antibody grip loops, or 70%, still bound IL-4Ra in the lab
- 14 of 107 designs, or 13.1%, bound when built on three shapes the model generated that have never been published

The honest limits, stated by OpenAI itself: specialist tools including Boltz-2, ESMFold2 and SolubleMPNN still supplied sequences and filtered candidates, so this is not an end-to-end result. Binding is only the first step, with specificity, stability and safety untested. Whole-protein structure prediction remains a weak point. These are company results, not yet peer reviewed.

What this means for businesses: general reasoning models are starting to do real work inside specialist scientific fields. The pattern worth watching is a general model paired with trusted domain tools and physical validation, rather than either one on its own.""",
        "tags": "#AIinScience #ProteinDesign #OpenAI #Biotech #DrugDiscovery",
    },
    {
        "id": "d1127mid", "when": "2026-11-27T15:30:00", "kind": "image",
        "tag": "AI TOOLS",
        "title": "AWS open-sources\ntiny decision models",
        "points": [
            ("5", "Open-weight models, from\nE2B up to a 31B dense one"),
            ("17.5M", "Decision examples used\nto train the family"),
            ("$500", "Cost per million tickets,\ndown from about $22,200"),
            ("897ms", "Per-call latency, down\nfrom 4,215ms (v1 test)"),
        ],
        "body": """Not every AI decision needs a frontier model.

On 23 November, AWS released Strands Decider v2, a family of open-weight models built for one job: picking an answer from a known set of options, and saying how confident it is.

What is in it:
- Five models, from E2B and E4B through 12B and a 26B mixture-of-experts up to a 31B dense model
- Each starts from the matching Gemma 4 instruction-tuned model
- Trained on about 17.5 million decision examples
- Released under the Apache 2.0 licence

The cost case comes from AWS's own internal use of the earlier v1 model. An Amazon ticketing team replaced Claude Sonnet 4.6 with Decider for ticket labelling and reported cost falling from roughly $22,200 to about $500 per million tickets, with per-call latency dropping from 4,215 milliseconds to 897 milliseconds.

AWS is candid about the limits. The benchmarks are its own, the 31B model trails rivals on three of six of them, no accuracy figures were published alongside the cost win, and Decider only suits decisions with a fixed set of possible answers. It is not on Amazon Bedrock yet.

What this means for businesses: the cheapest win in AI right now is routing. Classify, label and triage with a small specialised model, and save the expensive frontier model for the work that genuinely needs it.""",
        "tags": "#AITools #OpenSourceAI #AWS #MLOps #Automation",
    },
    {
        "id": "d1127pm", "when": "2026-11-27T18:30:00", "kind": "image",
        "tag": "AI BUSINESS",
        "title": "Dell's AI backlog\nhits $132.3 billion",
        "points": [
            ("$54.9B", "Record quarterly revenue,\nup 103% year on year"),
            ("$22.0B", "AI-optimised server\nrevenue, up 291%"),
            ("$132.3B", "AI backlog at the end\nof the quarter"),
            ("$202B", "Full-year FY27 revenue\nguidance, up 78%"),
        ],
        "body": """The AI infrastructure boom now shows up as one of the biggest revenue jumps in enterprise computing.

On 24 November, Dell Technologies reported third-quarter results for its 2027 fiscal year.

The numbers Dell reported:
- Record revenue of $54.9 billion, up 103% year on year, against analyst expectations of about $49.3 billion
- Record AI-optimised server revenue of $22.0 billion, up 291% year on year
- A record $132.3 billion AI backlog at the end of the quarter, after booking $60.2 billion of orders
- Full-year FY27 revenue guidance raised to $202.0 billion, up 78%, from $192.0 billion
- The AI-optimised server revenue outlook for the year raised to $78.0 billion, up 216%, from $74.0 billion
- A $25 billion share buyback authorisation

Two things are worth keeping straight. Backlog is orders not yet recognised as revenue, so it measures demand rather than money earned. And Dell's own filing warns that results could differ materially, naming AI demand, supplier relationships and macroeconomic conditions as risks.

What this means for businesses: compute demand is still running well ahead of supply, and that shapes what everyone else pays and waits for. If your plans depend on GPU capacity next year, lock in lead times early, and design systems that can run on whatever hardware you can actually get.""",
        "tags": "#AIinBusiness #AIInfrastructure #Dell #DataCenters #Earnings",
    },
]

def caption(p):
    return f"{p['body']}\n\n{FOOT}\n\n{BASE} {p['tags']}"
