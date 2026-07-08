---
title: Lumina Video Architect
emoji: 🔮
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 4.16.0
app_file: app.py
pinned: false
---

# 🔮 Lumina Video Architect - OS Frontend Core v2.3 (Toast Engine)

**Transform video data streams into custom, automated PowerPoint presentations with fine-tuned user controls, high-intensity inline parsing, and zero-leak thread management.**

---

## 📸 Production Workspace Preview

![Lumina OS UI Interface Desktop View](image_1e64ba.png)

The production workspace centers on three primary controls that drive the compilation pipeline:

- **Target Slide Count Slider** — lets the user dial the output deck between 3 and 15 slides, directly shaping how aggressively the summarization stage compresses source content.
- **Audience Depth Dropdown** — sets the tone and technical density of generated bullets (e.g. *Advanced Engineering*), so the same source video can be turned into a beginner overview or a specialist briefing.
- **Async Stream Terminal** — surfaces real-time pipeline telemetry (fetch → summarize → schema → assemble) as the request is processed, giving the user visibility into long-running jobs without blocking the UI thread.

Together, these controls feed a single `Trigger Lumina Engine` action that kicks off the backend compilation job and returns a downloadable `.pptx` artifact on completion.

---

## ⚙️ System Core Engineering Pillars

Three backend optimizations underpin the compiler's stability and performance:

**Decoupled Task Offloading**
A persistent `ThreadPoolExecutor(max_workers=4)` isolates heavy binary processing (video fetch, transcript parsing, slide assembly) away from the client-facing event loop, keeping the UI fluid and responsive while compilation runs in the background.

**Memory Leak Auditing & OXML Tree Pruning**
On completion of each compile job, sub-level OpenXML elements are explicitly cleared via `shapes._spTree.clear()`, followed by a manual `gc.collect()` cycle to deallocate unreachable cyclic node references left behind by `python-pptx` object graphs.

**Secure Sandbox Log Masking**
A transparent `sys.stdout` interceptor, wrapped around structured regular expressions, filters real-time telemetry logs and replaces any live credentials with `[SECURE_MASK_LOCKED]` before they ever reach the terminal or log file.

---

## 📊 Sample Output Showcase

A recent production run compiling a TED talk into a corporate-style slide deck:

| Field | Value |
|---|---|
| **Input Query URL** | `https://youtu.be/RcGyVTAoXEU?si=k-CCWgQUd7yQ-FZy` |
| **Context Topic** | How to Make Stress Your Friend (TED Session Analysis) |
| **Execution Mode** | Generative AI Fallback Engine *(upstream scraper firewall restrictions)* |
| **Total Process Time** | 44.84 seconds |
| **Cyclic Memory Nodes Flushed** | 15,967 unreachable references |

**Performance Profiler — Phase Latency**

```
Phase 1  Fetch      25.12s
Phase 2  Summary    10.10s
Phase 3  Schema      9.40s
Phase 4  Assembly    0.20s
─────────────────────────────
Total                44.84s
```

---

## 📂 Generated Presentation Payload — 7-Slide Corporate Matrix

Each slide follows a **Three-Zone Layout Alignment Grid**: Zone 1 (visual context), Zone 2 (Column A focus), Zone 3 (Column B focus).

<details>
<summary><strong>Slide 01 — Executive Overview: Reframing Stress</strong></summary>

**Zone 1:** EXECUTIVE OVERVIEW: REFRAMING STRESS

**Zone 2**
- Stress is often misperceived as purely negative, hindering growth and connection.
- Scientific analysis redefines stress as a potential catalyst for positive outcomes.

**Zone 3**
- Strategic shift from stress avoidance to leveraging its biological responses.
- Cognitive reframing and active social engagement are key to harnessing stress.
</details>

<details>
<summary><strong>Slide 02 — Core Pillars of Stress Transformation</strong></summary>

**Zone 1:** CORE PILLARS OF STRESS TRANSFORMATION

**Zone 2**
- This section outlines fundamental concepts for understanding and managing stress effectively.
- Focus on stress reframe, cognitive appraisal, psychological resilience, and oxytocin dynamics.

**Zone 3**
- Highlights the critical role of human connection in stress mitigation and thriving.
- Provides a structured approach to leveraging stress for personal and collective benefit.
</details>

<details>
<summary><strong>Slide 03 — Stress Reframe: Challenge vs. Threat Response</strong></summary>

**Zone 1:** STRESS REFRAME: CHALLENGE VS. THREAT RESPONSE

**Zone 2**
- View stress not as debilitating, but as the body's natural physiological response to challenge.
- Shift from outright stress elimination to consciously utilizing adaptive responses.

**Zone 3**
- Promote a 'challenge response' for increased cardiovascular efficiency and enhanced focus.
- Avoid the 'threat response' characterized by fear and physiological constriction for better performance.
</details>

<details>
<summary><strong>Slide 04 — Cognitive Appraisal Theory: Interpreting Stressors</strong></summary>

**Zone 1:** COGNITIVE APPRAISAL THEORY: INTERPRETING STRESSORS

**Zone 2**
- This theory is central to understanding the individual stress response mechanism.
- The interpretation or 'appraisal' of a stressor critically dictates subsequent outcomes.

**Zone 3**
- Appraise situations as manageable challenges versus overwhelming threats for better outcomes.
- Fosters a proactive mindset in managing perceptions of demanding situations to cultivate beneficial responses.
</details>

<details>
<summary><strong>Slide 05 — Building Psychological Resilience</strong></summary>

**Zone 1:** BUILDING PSYCHOLOGICAL RESILIENCE

**Zone 2**
- Resilience explores the innate human capacity to adapt, recover, and even thrive amidst adversity.
- Linked to the successful activation of a 'challenge response' and effective coping strategies.

**Zone 3**
- Actively built through developing self-efficacy and practicing emotional regulation techniques.
- Leveraging robust social support systems is crucial for fostering resilience, not an absence of stress.
</details>

<details>
<summary><strong>Slide 06 — Oxytocin: The Social Bonding Hormone</strong></summary>

**Zone 1:** OXYTOCIN: THE SOCIAL BONDING HORMONE

**Zone 2**
- Oxytocin plays a crucial role as a neuro-hormone that reduces fear and promotes pro-social behaviors.
- Notably released during stressful periods when individuals seek or offer social support and connection.

**Zone 3**
- Acts as a natural antidote to the typical 'fight-or-flight' response, encouraging 'tend-and-befriend'.
- Aids in healing, fostering courage, and strengthening social connection during times of heightened stress.
</details>

<details>
<summary><strong>Slide 07 — Human Connection & Thriving with Stress</strong></summary>

**Zone 1:** HUMAN CONNECTION & THRIVING WITH STRESS

**Zone 2**
- Active human connection and robust social support networks are critical for effective stress management.
- Engaging with others, offering help, or seeking connection during stress activates the 'tend and befriend' response.

**Zone 3**
- This mechanism, primarily facilitated by oxytocin, significantly enhances individual and collective well-being.
- Reshape our relationship with stress to build profound resilience, foster empathy, and ultimately thrive in life.
</details>

---

## 🚀 Local Runtime Initialization

**1. Activate the virtual environment**
```powershell
.\.env_workspace\Scripts\activate
```

**2. Install dependencies**
```powershell
pip install -r requirements.txt
```

**3. Launch the application**
```powershell
python app.py
```

The app will boot a local Gradio server (default `http://127.0.0.1:7860/`), from which the Production Workspace shown above becomes accessible.

---

*Built with Gradio · Powered by the Lumina OS multi-agent architecture.*
