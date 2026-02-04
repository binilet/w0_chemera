## key insigths

- LLMs that aren’t just generating text, but planning actions, calling external tools, and carrying out tasks across multiple domains with minimal human oversight.

 - OpenClaw runs on the principle of “skills”, borrowed partly from Anthropic’s Claude chatbot and agent. Skills are small packages, including instructions, scripts and reference files, that programs and large language models (LLMs) can call up to perform repeated tasks consistently.

 -github-spec (sdd impl) -> built with clear specifications first and then use AI agents to turn those specs into working code. It helps you build AI‑driven apps faster by making your specifications executable, reducing miscommunication, and letting AI generate and extend implementations directly from your intent

- tradition approach Code first → fix later → tech debt → chaos
- sdd approach : Design first → test expectations → control AI behavior → then implement

-sdd comprises of 
    - Specs -> Write what system must do
    - Skills -> Break AI into modular abilities
    - Tests -> Prove behavior works
    - Governance -> Prevent unsafe AI behavior

## Arcitectural Approach