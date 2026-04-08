# FIDgate — Questions and Answers Only

---

### ABOUT YOU

**"Tell me about yourself."**

> "I come from an entrepreneurial background. I studied mechanical engineering in Brazil, focusing on renewable energy, and during that time I co-founded a business and later worked as a project manager in a family business. That shaped how I think — I always look at both the technical and business sides.
>
> I then moved to Germany to pursue a Master's in Software Engineering, where I built a SaaS product called Odys from scratch. It's live and helps freelancers manage bookings and reduce no-shows through automated communication, via a self-hosted WhatsApp API.
>
> I built the entire system myself — backend, frontend, payments, and infrastructure — so I'm used to owning both product and engineering decisions.
>
> What attracted me to FIDgate is the combination of three things that rarely come together: renewable energy, which was my original field, founding-level ownership, and real AI engineering. It's not a common opportunity."

---

**"Why do you want to work with us?"**

> "There are three things that rarely come together for me.
>
> First, the domain. I originally studied renewable energy during my mechanical engineering degree, and I always wanted to work on meaningful problems in that space, but I didn't find the right opportunity before moving into software.
>
> Second, the level of ownership. I'm not looking for a role where I just implement tickets. I want to own real problems end to end, and that's exactly what this position offers.
>
> Third, the problem itself. Critical energy decisions are still made using static models. Building a system that continuously optimizes those decisions in real time is both technically challenging and has real-world impact.
>
> That combination is what makes this opportunity very compelling to me."

---

**"Why are you transitioning from project management to engineering?"**

> "It's less of a transition and more of a completion. As a project manager I was always the person closest to the technical decisions without making them. At some point I realized I was the bottleneck — I understood the problem but needed someone else to build the solution. So I went back to study and then built Odys to prove I could do it alone. The combination is what makes me useful: I think like a product person and I can execute like an engineer."

---

**"You have a mechanical engineering degree — why software?"**

> "Mechanical engineering gave me systems thinking. I was always more interested in how things work together than in the physical components. Software is the same problem at a different layer. And honestly, in software you can ship something in weeks that would take years in physical engineering. The leverage is completely different."

---

**"You co-founded a business before — what happened to it?"**

> "It's still running. My family members run it now in Brazil. I'm in Germany so I can't be involved in the day-to-day operations, but it's active. That experience is what gave me the founder mindset — understanding that a business only works if you care about the user's actual problem, not just the product you want to build."

---

### ABOUT ODYS

**"Tell me more about Odys — what problem does it solve and what was the hardest part?"**

> "Odys is focused on Brazilian freelancers like psychologists and personal trainers who still manage everything manually through WhatsApp — scheduling, confirmations, and payments.
>
> The core idea was to let clients book in a self-service way, while professionals receive automated WhatsApp messages sent from their own number, not from a generic bot.
>
> The main technical challenge was making that integration reliable. I had to self-host a WhatsApp API (Evolution API) inside a Docker container and deal with unstable connections, since WhatsApp sessions can drop at any time.
>
> To handle that, I built a watchdog system to monitor the connection and automatically restart it, along with scheduled jobs for reminders and robust webhook handling for payments.
>
> Since I was the only one building it, I had to treat reliability as a core requirement from the start."

---

**"How many users does Odys have?"**

> "It's live in production, but I haven't focused on distribution yet, so I don't have meaningful user traction to claim.
>
> My priority so far was building the product and validating the core workflows technically before pushing for growth."

---

**"You built it alone — what would break first if you had 10x the users?"**

> "Probably the WhatsApp connection layer. I'm using a self-hosted Evolution API — it works reliably for the current load but hasn't been stress-tested at scale. The database and API layer I'm not worried about — Supabase with proper indexing handles that. But the WebSocket connections to WhatsApp would need proper load balancing and potentially multiple instances."

---

**"What would you improve in your own system if you had 3 more months?"**

> "Honestly, the first priority would be real user validation. The system is functional, but I haven't yet validated it with paying customers, so I'd focus on onboarding users and collecting feedback as quickly as possible.
>
> Based on that, I'd prioritize two areas.
>
> First, the WhatsApp integration at scale. Right now it runs on a single Evolution API instance, which is a risk. I'd move toward multiple instances with proper load balancing and monitoring to handle unstable connections reliably.
>
> Second, I'd simplify the product. I overbuilt some features early on — like recurring bookings and financial reports — without strong validation. I'd remove or reduce what's not being used and focus only on what actually reduces friction for the user.
>
> So the focus would be validation, reliability, and simplification."

---

**"What would you have built differently?"**

> "I would have done less upfront. I built the full tiered subscription system, recurring appointments, financial reports — features that real users might not even need first. I should have shipped the core booking flow and gotten real feedback before building everything else. Classic mistake."

---

**"How would you integrate AI or LLMs into Odys to improve the product?"**

> "The most natural place is the booking flow. Right now, freelancers still receive messages like 'can I book something this week?' directly on WhatsApp.
>
> I would use an LLM to turn those messages into structured actions — parse intent, extract constraints like date or service, and then connect that to the availability system to either suggest slots or confirm a booking automatically.
>
> Architecturally, this would sit as a layer between the WhatsApp input and the booking backend, with validation to avoid wrong actions and fallback to manual confirmation when needed.
>
> The second use case is for the professional side. Instead of navigating dashboards, they could query the system in natural language — like 'who cancelled this week?' or 'what's my revenue this month?' — and get immediate answers.
>
> So it's essentially adding a conversational interface on top of existing workflows, reducing friction without changing the core system."

---

### ABOUT THE RAG PIPELINE

**"Tell me about the RAG pipeline — what did you actually build?"**

> "I built a RAG pipeline over PDF documents, focusing specifically on improving retrieval quality.
>
> One of the main issues with typical RAG systems is naive chunking. Fixed-size chunks often break semantic structure — splitting sections mid-sentence or mixing headers with body text — which hurts retrieval.
>
> To address that, I implemented a custom chunking strategy based on font size, distinguishing headers from body text and preserving logical sections. That significantly improved the relevance of retrieved context.
>
> I also added history-aware retrieval. Before querying the vector store, I reformulate the user's query based on previous messages, which helps maintain context across multi-turn interactions.
>
> The stack included FastAPI, ChromaDB, and an LLM backend, but the main focus was on improving retrieval quality rather than just assembling components."

---

**"Explain the RAG pipeline to a non-technical person."**

> "It's a system that lets an AI answer questions based on specific documents, instead of relying only on general knowledge.
>
> When a question comes in, the system first searches for the most relevant parts of the documents. Then it uses that information to generate a more accurate and grounded answer.
>
> The main challenge is making sure the right content gets retrieved — if the wrong pieces are selected, the answer fails regardless of how good the model is."

---

**"What are the limitations of RAG systems?"**

> "There are four main ones.
>
> First, retrieval quality. If the relevant context isn't retrieved, the answer fails regardless of the model. That's why I focused on chunking — it's the root cause of most retrieval failures.
>
> Second, hallucinations. Even with the right context, the model can still generate incorrect or overconfident responses.
>
> Third, latency and cost. Combining retrieval and generation adds overhead — it can become slow and expensive at scale.
>
> Fourth, evaluation is hard. It's not always obvious how to measure whether retrieval is actually improving, especially without labeled ground truth data."

---

**"How does the RAG work apply to what FIDgate is building?"**

> "FIDgate's engine produces results — optimal configurations, revenue projections, dispatch strategies. But the energy professional needs to understand why a specific configuration is optimal before committing millions of euros to it. That's the same problem I worked on: making complex model outputs trustworthy and interpretable. I'd build an AI layer that explains the engine's reasoning in plain language — not just 'this configuration has the highest IRR' but 'this configuration outperforms because of these specific market conditions and site constraints.'"

---

### ABOUT TECHNICAL SKILLS

**"Where are you with Python and TypeScript?"**

> "Python is where I'm strongest — FastAPI, SQLAlchemy, LangChain, Pytest, Docker. I built the RAG pipeline and the Inspection Management API entirely in Python.
>
> TypeScript I use through Next.js — Odys is built with it, full App Router, server components, API routes. My TypeScript is more frontend-focused.
>
> On the backend I'm stronger in Python, but I've shipped production code with TypeScript and I'm comfortable working across both when needed."

---

**"How would you handle scale — queues, async, retries?"**

> "For any workflow that involves external systems — like calling the decision engine or sending notifications — I'd introduce background job queues for async processing and make all external interactions idempotent. That way failures can be retried safely without side effects. For observability I'd add structured logging and metrics on queue depth and failure rates from the start."

---

**"Have you worked with optimization algorithms or numerical methods?"**

> "Not directly in production. My mechanical engineering background covered numerical methods and optimization theory, and my thesis involved modelling. But I haven't built parametric optimization systems in software. What I can do is work closely with your modelling team and build the platform layer that makes their engine accessible — that's the engineering problem, not the domain science problem."

---

**"What does your testing and deployment workflow look like?"**

> "For the Inspection Management API I have 31 automated Pytest tests covering the full status lifecycle, running in a GitHub Actions CI/CD pipeline on every push. Docker containerized, PostgreSQL database. For Odys the deployment is on Vercel with Railway for the self-hosted WhatsApp server. I use Sentry for error monitoring and PostHog for analytics. I don't push without understanding what I'm shipping."

---

**"How do you use AI in your engineering workflow?"**

> "My daily setup is Claude Code and Gemini inside Cursor. I write deliberate prompts, review every suggestion critically, and only ship what I actually understand. I don't use AI to generate code I can't explain. It lets me move at founder speed without sacrificing quality — but the architectural decisions are always mine."

---

### ABOUT THE ROLE

**"You have no energy industry experience. How do you see yourself contributing without that background?"**

> "That's true, I don't have direct experience in the energy industry yet.
>
> But I see my role as bringing strong engineering and product thinking to make the system usable, reliable, and scalable. That part is somewhat domain-agnostic.
>
> At the same time, I'd close the domain gap quickly by working closely with the modelling team and early users, understanding how decisions are made and what actually matters in practice.
>
> In early-stage environments, I think the ability to learn fast and translate domain knowledge into working systems is more important than coming in with all the answers upfront.
>
> My mechanical engineering background in renewable energy gives me a starting point — I'm not learning the domain from zero. But the real value I bring is on the engineering and product side, and that's where I'd focus first."

---

**"You're early in your software career. Why should I trust you to own the platform end to end?"**

> "That's fair, I am early in my software career.
>
> But I'm not early in ownership. Before software, I co-founded a business and worked as a project manager, so I'm used to being responsible for outcomes, not just tasks.
>
> In software, I've already applied that mindset. I built a full SaaS product end to end — backend, frontend, payments, infrastructure, and external integrations. I had to make decisions across the entire system and deal with real-world issues like reliability and failure handling.
>
> I don't claim to know everything, but I'm comfortable operating in uncertainty, breaking problems down, and figuring things out quickly.
>
> What you get from me is high ownership, fast iteration, and someone who treats the system as a product, not just code."

---

**"Where do you see yourself in this role in 2 years?"**

> "In two years, I see myself having taken full ownership of key parts of the platform — from API design to infrastructure and reliability.
>
> I'd expect to be deeply familiar with both the technical system and how it's used in real decision-making, contributing not just to implementation but to shaping how the product evolves.
>
> If things go well, I'd naturally grow into a more strategic role, helping define architecture decisions and guiding how the platform scales.
>
> The title itself is less important to me than the level of responsibility and impact I can have."

---

**"How would you turn our decision engine into a platform developers want to use?"**

> "The first thing I'd do is talk to early adopters to understand how they're actually using the engine and where the current API creates friction. I wouldn't assume the interface upfront.
>
> From there, I'd focus on three areas.
>
> First, the API design: clear versioning, predictable response structures, and meaningful error handling. Developers stop using APIs when behavior is inconsistent.
>
> Second, developer experience: documentation based on real workflows — not just endpoints, but showing how to go from inputs to actual decisions step by step.
>
> Third, reliability: rate limiting, monitoring, and clear expectations around latency and uptime, especially since these are high-stakes decisions.
>
> On top of that, I'd add an AI layer focused on interpretability — helping users understand why the engine suggests a given configuration, not just the output. That's key for building trust in decisions tied to real assets."

---

**"What would you do in your first 30 days here?"**

> "In the first 30 days, my focus would be understanding before building, but not passively.
>
> I'd start by going deep into the system: the decision engine, the current API, and how it's being used. I'd run it locally, explore edge cases, and try to break it from a developer's perspective.
>
> In parallel, I'd talk to early adopters to understand what decisions they're trying to make, where the current interface creates friction, and what they don't trust yet.
>
> Based on that, I'd identify one or two high-impact improvements and start implementing them before the end of the first month.
>
> The goal is to make sure the first things I ship are grounded in real usage and immediately useful."

---

**"How would you approach the first 90 days?"**

> "In the first 90 days, I'd focus on three things: understanding the system deeply, reducing the biggest points of friction for early users, and shipping improvements that make the platform easier to trust and build on.
>
> That starts with the decision engine and the current API — running it, exploring edge cases, and understanding how it's actually being used.
>
> In parallel, I'd talk to early adopters to identify where the interface or outputs create confusion or friction.
>
> From there, I'd prioritize improvements around API clarity, documentation based on real workflows, and reliability.
>
> Once that foundation is solid, I'd move into building the AI explanation layer, based on what users actually struggle to interpret."

---

**"How do you handle working without management or clear requirements?"**

> "That's how I prefer to work. At Odys there was no product manager, no designer, no one to tell me what to build next. I talked to potential users, identified the highest-friction point, and built that. Then repeated. The risk of working without management is building the wrong thing — the solution is staying close to the user, not waiting for someone to write a spec."

---

**"What does founder-level ownership mean to you?"**

> "For me, founder-level ownership means not waiting to be told where the problem is.
>
> It means understanding the user, identifying what matters most, making decisions with incomplete information, and taking responsibility for the outcome — not just the implementation.
>
> It's thinking beyond the code and treating the product as something you are fully accountable for."

---

### ABOUT SALARY

**"What are your salary expectations?"**

> "I initially put 43k in the application, but I see this as a different kind of role given the level of ownership and the equity component.
>
> I'm definitely open to revisiting that depending on the full compensation structure.
>
> How are you thinking about compensation for this position?"

*(Let him anchor first. If he pushes back: "Given the founding-level ownership and equity, I'd expect something in the 60-70k range plus meaningful equity.")*

---

**"What do you think about equity vs salary?"**

> "For a role like this, equity matters. If FIDgate becomes what it could be in this market, I want to have been there from the beginning and have that reflected in my stake. I'm not expecting a large salary at founding stage — I understand how this works. But the equity needs to be meaningful."

---

### PRACTICAL / LOGISTICAL QUESTIONS

**"Are you currently employed? When can you start?"**

> "I'm not currently employed — I've been focused on my master's, building Odys, and applying for the right opportunity. I can start relatively quickly, within a few weeks if needed."

---

**"Do you have the right to work in Germany?"**

> "Yes, I have a permanent residence permit and full work authorization in Germany."

---

**"Have you ever worked in a team or only solo?"**

> "Both. During my master's I worked in team projects and during my project management years I coordinated cross-functional teams. Odys I built alone, which taught me a different kind of discipline. I'm comfortable in both modes, but I prefer working closely with a small, high-trust team where ownership is clear."

---

**"What's one thing you're not good at yet?"**

> "Distributed systems at scale. I've built reliable systems for current load levels, but I haven't operated infrastructure at the scale of thousands of concurrent users. That's a gap I'm aware of and actively working on. What I do well is identifying when a system is approaching that limit and designing for it before it becomes a problem."

---

**"Why did you apply to FIDgate — how did you find us?"**

> "I came across the role while searching for founding-level AI engineering positions in Berlin. The combination of renewable energy, real decision-making systems, and the CTO path stood out immediately. Most roles at this level are either too corporate or too shallow technically. This one wasn't."

---

**"Can you show me something you built?"**

> "Yes — I can show you Odys live at odys.com.br, the portfolio at tiagorcfortunato.vercel.app, and the GitHub repositories for the Inspection Management API and RAG pipeline. Happy to walk through any of them."

---

### CURVEBALL QUESTIONS

**"What do you think we're doing wrong?"**

> "From the outside, the platform flow makes sense — simulate, optimize, decide. But I'd want to know how energy professionals actually interpret the results. My guess is the outputs are technically correct but not immediately actionable. If someone gets a result saying 'this configuration has 12% IRR with a 15-year payback' — do they trust it? Do they understand which assumptions drove it? That's the gap I'd want to close first."

---

**"Why should we hire you over someone more experienced?"**

> "In an early-stage environment, ownership, speed, and clarity matter as much as years of experience.
>
> I've already shown that I can build real systems end to end, make product and engineering decisions myself, and operate without waiting for structure.
>
> I may have fewer years in software, but I've already built and shipped real systems alone, made product and engineering decisions without supervision, and operated in exactly the kind of environment this role requires."

---

**"What would you do if you disagreed with a technical decision I made?"**

> "I'd say it directly. I'd explain my reasoning and what I think the risk is. If you heard it and still wanted to proceed, I'd execute it — you have context I might not have. But I wouldn't stay quiet about it. A founding engineer who doesn't push back is not useful."

---

**"Do you have other interviews ongoing?"**

> "I have a few applications in process. But this is the one I've prepared for most specifically — the combination of renewable energy, founding-level ownership, and a real product is not common."

---

## Your Questions to Ask Him

Ask 2 or 3 naturally — don't read them:

1. "The Python API is already live — what's the biggest gap between what it does today and what a developer would need to actually build on it?"
2. "Who are the first adopters you're targeting for the platform? Other developers, or energy analysts directly?"
3. "The AI-assisted features you mentioned — do you have something specific in mind, or is that still open?"
4. "When you say CTO path — is that a formal milestone or more of a natural evolution as the company grows?"
5. "What's the biggest risk to platform adoption in the next 12 months?"
6. "What would success look like for this role in the first 6 months?"
