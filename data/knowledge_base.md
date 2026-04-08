# Tiago Fortunato — Technical Knowledge Base

> This document is the authoritative source of truth for Tiago Fortunato's professional profile. It is used by the RAG chatbot to answer recruiter questions with accurate, technical depth.

---

## About Tiago

Tiago Fortunato is a **Full-Stack Developer and Founder** based in **Berlin, Germany**. He is currently completing an **MSc in Software Engineering** at the University of Europe for Applied Sciences (graduating 2026), with a background in Mechanical Engineering (BSc, UERJ, Brazil).

He is the **sole founder and developer of Odys** (odys.com.br) — a live, production WhatsApp-first scheduling SaaS for freelance professionals in Brazil, built entirely from architecture to deployment.

His technical focus spans **AI application engineering** (RAG pipelines, computer vision, ML), **backend API development** (Python/FastAPI), and **full-stack SaaS product development** (Next.js/TypeScript/Supabase).

**Contact:**
- Email: tifortunato.eng@gmail.com
- Phone: +49 172 238 9909
- Portfolio: tiagorcfortunato.vercel.app
- GitHub: github.com/tiagorcfortunato
- LinkedIn: linkedin.com/in/tiagorcfortunato

**Languages:** Portuguese (native), English (fluent), German (B2.2, actively improving)

**Available for:** Full-Stack or Backend Developer roles in Berlin or remote. Actively pursuing the Founding Product & AI Engineer role at FIDgate.

---

## Why FIDgate

FIDgate is building autonomous optimization systems to replace manual, Excel-based energy decisions. This problem resonates directly with Tiago's work: his MSc thesis was architecturally identical — replacing manual road inspection and maintenance decisions with a hybrid ML + rule-based expert system. The pattern is the same: perception/detection layer → reasoning/prioritization layer → automated, traceable decisions. He has built this from scratch.

**What Tiago brings to FIDgate specifically:**
- Can turn an existing Python API into a clean, developer-facing platform — demonstrated with the Inspection Management API (JWT auth, filtering, pagination, sorting, full OpenAPI docs)
- Has shipped AI/LLM features in production — RAG chatbot with full pipeline (embeddings, vector search, conversation history, source attribution)
- Has founding-team experience — built and launched Odys entirely solo, from market research to production
- Python + TypeScript across the full stack
- High autonomy — does not need to be managed, figures out what matters and builds it
- Based in Berlin, aligned with FIDgate's HQ location

---

## Academic Excellence

### MSc Thesis Overview

Tiago's MSc thesis is titled *"Expert System for Road Surface Hazard Detection: A Deep Learning-Based Detection and Maintenance Prioritization Pipeline"*, submitted in February 2026 at the University of Europe for Applied Sciences, Berlin. It presents a modular two-component pipeline: a YOLOv8 object detection model identifies road surface defects (potholes, cracks) from monocular images, and a deterministic rule-based expert system assigns maintenance priority levels (Low / Medium / High) based on defect type, confidence scores, and detection count. Best result: mAP50 of 0.663 with YOLOv8s, with post-processing reducing noisy detections by 31.2%. The architecture separates perception from reasoning, allowing decision logic to be updated without retraining the model. This is directly analogous to FIDgate's autonomous optimization system — replacing manual judgment with automated, traceable reasoning on top of a detection/modelling layer.

### MSc Thesis — Expert System for Road Surface Hazard Detection

**Full Title:** *Expert System for Road Surface Hazard Detection: A Deep Learning-Based Detection and Maintenance Prioritization Pipeline*

**Institution:** University of Europe for Applied Sciences, Berlin
**Submitted:** 15 February 2026
**Supervisors:** Prof. Dr. Raja Hashim (first), Prof. Dr. Shan Faiz (second)

#### Problem Statement

Traditional road inspection is manual, costly, slow, and subjectively inconsistent. Existing deep-learning approaches for road damage detection focus solely on maximizing detection accuracy on benchmark datasets — they treat damage detection as an isolated perception task without addressing how detected defects should be **prioritized for maintenance planning**. This gap between visual inspection and actionable infrastructure management decisions was the central motivation for the thesis.

#### Proposed Solution — Hybrid Pipeline

Tiago designed a **modular two-component pipeline** that separates perception from reasoning:

1. **Detection Component (YOLOv8):** A YOLO-based object detection model identifies and localizes road surface defects from monocular RGB images under real-world, unconstrained environmental conditions.

2. **Expert System (Rule-Based Prioritization):** A deterministic, rule-based decision-support system processes the structured detection outputs (bounding boxes, class labels, confidence scores) and assigns maintenance priority levels (Low / Medium / High) based on:
   - Defect type (e.g., pothole, longitudinal crack, transverse crack, alligator crack)
   - Detection confidence score (configurable thresholds)
   - Number of detections per image (aggregation)
   - Contextual operational criteria

The interface between both components is: `P = f(D)`, where `f(·)` is the non-probabilistic rule function and `D` is the structured detector output. This separation allows decision logic to be modified without retraining the perception model.

#### Dataset

**RDD2022** (Road Damage Dataset 2022) — a large-scale benchmark containing annotated road images from multiple countries with varied lighting, weather, and surface conditions. Key challenge: class imbalance and small-defect detection.

#### Experimental Design (EXP1–EXP4)

Controlled experiments varying one factor at a time:

| Experiment | Model | Main Modification |
|---|---|---|
| EXP1 | YOLOv8n | Baseline configuration |
| EXP2 | YOLOv8n | Training epochs: 50 → 100 |
| EXP3 | YOLOv8n | Image size: 640 → 800 |
| EXP4 | YOLOv8s | Higher-capacity model (best config) |

#### Results

**Best configuration (EXP4 — YOLOv8s):**
- **mAP50: 0.663**
- **Precision: 0.694**
- **Recall: 0.604**
- Post-processing (quantile-based prioritization + deterministic filtering) **reduced noisy detections by 31.2%**
- Every prioritization decision is traceable to explicit rules — no black-box decisions

#### Key Technical Contributions

- Demonstrated that combining deep learning with explicit rule-based reasoning improves both performance and **operational interpretability**
- Modular architecture allows independent testing of perception and decision-making components
- Reproducible benchmarking: fixed random seeds, pinned library versions, held-out test set never touched during training
- Post-processing aggregation stabilizes prioritization across confidence threshold variations

#### Tech Stack (Thesis)

Python, PyTorch, YOLOv8 (Ultralytics), Scikit-learn, Pandas, Linux, GPU-accelerated training

---

## Full-Stack & AI Projects

### Projects Overview

Tiago has built three main projects: (1) RAG Career Chatbot — AI career assistant with streaming SSE, LangChain, ChromaDB, Groq, deployed on Render. (2) Inspection Management API — REST API with AI-powered damage classification using Groq Llama 3.2 11B Vision, JWT auth, admin roles, 31 Pytest tests. (3) Odys — WhatsApp-first scheduling SaaS built entirely solo, live at odys.com.br, with Stripe payments and self-hosted WhatsApp API.

### 1. RAG Career Chatbot (2026)

**Repository:** github.com/tiagorcfortunato/rag-pdf-chatbot
**Live Demo:** rag-pdf-chatbot-0w9z.onrender.com

A production-deployed AI Career Assistant built as a Retrieval-Augmented Generation (RAG) application. It serves as Tiago's interactive professional profile — recruiters and hiring managers can ask natural-language questions about his experience, projects, skills, and motivations, and receive accurate, sourced answers in real time with streaming responses.

Originally built as a general-purpose PDF chatbot, Tiago evolved it into a career-focused product with a recruiter persona, streaming UI, and optimized deployment for memory-constrained environments.

#### Architecture

```
Knowledge base (Markdown) → section-aware chunking → fastembed (BAAI/bge-small-en-v1.5, local)
    ↓
ChromaDB (persistent vector store, pre-ingested at Docker build time)

──────────────────────────────────────

User question (via chat UI or API)
    ↓
History-enriched search query (last 2 exchanges prepended)
    ↓
Similarity search → top-10 most relevant chunks
    ↓
LangChain prompt: system instructions + conversation history + context + question
    ↓
Groq LLM (Llama 3.1 8B Instant) → streaming SSE tokens
    ↓
Frontend: real-time markdown rendering + source attribution
```

#### Key Technical Details

- **Streaming SSE responses:** Backend yields Server-Sent Events via `POST /api/query/stream`. Frontend consumes the stream with Fetch API ReadableStream, rendering markdown incrementally as tokens arrive. Feels like ChatGPT — text appears word by word.
- **Pre-build Docker ingestion:** The knowledge base is embedded and indexed at Docker build time (`RUN python -c "ingest_markdown(...)"`), not at runtime. This avoids the memory spike from loading fastembed + ChromaDB + ingesting 100+ chunks simultaneously — critical for fitting within Render's 512MB free tier.
- **Section-aware chunking:** For PDFs, uses PyMuPDF to extract font sizes across all spans, computes median font size, flags text 15%+ larger as headings. For Markdown, splits by ATX headings. Keeps small sections whole; uses `RecursiveCharacterTextSplitter` (chunk_size=500, overlap=50) only for large sections. Each sub-chunk is prefixed with its section title for retrieval coherence.
- **History-enriched retrieval:** Enriches search queries with the last 2 conversation exchanges, enabling natural follow-up questions ("tell me more about the first one").
- **Suggested question chips:** Interactive clickable questions shown after each response. Tracks which questions have been asked and shows only remaining suggestions — guides the conversation naturally without requiring the user to think of questions.
- **Markdown rendering:** Uses marked.js to render tables, bullet points, code blocks, bold text, and headers within chat bubbles.
- **Keep-alive mechanism:** Background async task pings `/health` every 10 minutes to prevent Render free tier spin-down (which otherwise adds 50+ seconds cold start delay).
- **Source attribution:** Every answer shows the knowledge base sections that were retrieved, so users can see which parts of Tiago's profile informed the response.
- **Recruiter persona system prompt:** Configured as a Professional Talent Assistant with instructions to answer from context, never hallucinate, and always try to give thorough answers from available information.
- **REST API:** Full OpenAPI/Swagger docs at `/docs`. Both non-streaming (`POST /api/query`) and streaming (`POST /api/query/stream`) endpoints available.

#### Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI 0.115 |
| PDF Parsing | PyMuPDF (fitz) 1.24 |
| Embeddings | BAAI/bge-small-en-v1.5 via fastembed 0.3.1 (local, ~80MB) |
| Vector DB | ChromaDB 0.5 (persistent) |
| LLM | Llama 3.1 8B Instant via Groq API |
| Orchestration | LangChain 0.3 + langchain-groq 0.2 |
| Frontend | Vanilla HTML/CSS/JS + marked.js (served by FastAPI) |
| Deployment | Docker, Render (free tier, 512MB) |
| Testing | Pytest + GitHub Actions CI/CD |
| Streaming | Server-Sent Events (SSE) via FastAPI StreamingResponse |

#### Challenges and Solutions

- **Challenge:** Generic chunking loses section context, causing poor retrieval.
  **Solution:** Built custom font-size-based heading detection with PyMuPDF for PDFs and ATX heading splitting for Markdown — no external dependencies, works on any document.

- **Challenge:** Follow-up questions fail vector search when they lack explicit keywords.
  **Solution:** History-enriched query construction prepends recent conversation context before embedding the search query.

- **Challenge:** Free embedding APIs add latency and cost at scale.
  **Solution:** Runs BAAI/bge-small-en-v1.5 locally via fastembed — downloaded once (~80MB), zero API cost.

- **Challenge:** Render free tier has only 512MB RAM; loading fastembed + ChromaDB + ingesting 100+ chunks at startup causes OOM crash.
  **Solution:** Pre-ingest the knowledge base during Docker build. The vector store is baked into the image — runtime startup only loads FastAPI + reads the pre-built ChromaDB, fitting comfortably in 512MB.

- **Challenge:** Render free tier spins down after inactivity, causing 50+ second cold starts.
  **Solution:** Background async keep-alive task pings the health endpoint every 10 minutes.

---

### 2. Inspection Management API (2026)

**Repository:** github.com/tiagorcfortunato/inspection-management-api
**Live API:** inspection-management-api.onrender.com
**Live Dashboard:** inspection-dashboard.vercel.app
**API Docs:** inspection-management-api.onrender.com/docs

A production-grade REST API for infrastructure inspection management with **AI-powered damage classification**, role-based access control, and a companion React dashboard. Demonstrates clean layered backend architecture, comprehensive test coverage, and real AI integration.

#### Key Features

- **AI-Powered Classification:** When an inspection is created, a background task sends the notes and/or uploaded image to **Groq Llama 3.2 11B Vision** (multimodal LLM) which classifies the damage type (pothole, crack, rutting, surface_wear) and severity (low, medium, high, critical) with a human-readable rationale. Uses LangChain structured output for type-safe classification results.
- **Multimodal Image Analysis:** Users can upload base64-encoded images of road damage. The AI service processes both text notes and images together for classification — this is real multimodal AI in production, not just text.
- **Role-Based Access Control:** Two roles (user, admin). Regular users can only CRUD their own inspections. Admins have a separate `/admin` endpoint group that can view all inspections across all users (with user_email), update, and delete any inspection.
- **JWT Authentication:** Registration, login, protected routes via FastAPI dependency injection (python-jose + bcrypt).
- **Per-user data isolation:** Each user only sees their own records. Enforced at the query level.
- **Status lifecycle:** `reported` → `verified` → `scheduled` → `repaired`
- **Filtering:** By `severity`, `status`, `damage_type`
- **Pagination:** `limit` + `offset` with total count
- **Sorting:** By `reported_at`, `severity`, `status`, `damage_type`, `location_code` (asc/desc)
- **Rate Limiting:** slowapi to prevent abuse
- **Background AI Processing:** AI classification runs as a FastAPI BackgroundTask — the API responds immediately to the client while AI processes asynchronously.

#### API Endpoints

```
POST /auth/register
POST /auth/login

GET    /inspections                    (user's own, filtered/paginated/sorted)
POST   /inspections                    (creates + triggers background AI classification)
GET    /inspections/{id}
PUT    /inspections/{id}
DELETE /inspections/{id}

GET    /admin/inspections              (all users, includes user_email)
PUT    /admin/inspections/{id}
DELETE /admin/inspections/{id}
```

#### Architecture (Layered)

| Layer | Responsibility |
|---|---|
| Routers | HTTP handlers (auth, inspections, users, admin) |
| Services | Business logic (inspection_service, ai_service, auth_service) |
| Models | SQLAlchemy ORM entities (User, Inspection) |
| Schemas | Pydantic request/response validation |
| Core | Config, security, dependencies, enums, rate limiter |
| Database | PostgreSQL with Alembic migrations |

#### Database Migrations (Alembic)

4 sequential migrations showing the evolution of the schema:
1. `initial_schema` — users + inspections tables
2. `add_role_to_users` — admin/user role field
3. `add_ai_fields_to_inspections` — ai_rationale, is_ai_processed columns
4. `add_image_data_to_inspections` — base64 image storage

#### Testing & CI/CD

- **31 Pytest tests** covering:
  - Auth: register, login, duplicate email, wrong password, unauthenticated access
  - CRUD: create, list, get by ID, update, delete
  - Data isolation: user A cannot see/update/delete user B's inspections
  - Filtering: by severity, damage_type, status
  - Pagination: limit, offset, total count, page boundary correctness
  - Sorting: by severity asc/desc
  - Admin: admin can list all (with user_email), update any, delete any; regular users get 403 on admin endpoints
  - Validation: invalid severity, invalid damage_type, missing required fields → 422
- **GitHub Actions CI:** tests run automatically on every push
- **Docker Compose:** isolated PostgreSQL test environment

#### Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI 0.135 |
| Database | PostgreSQL + SQLAlchemy 2.0 |
| Migrations | Alembic |
| AI Classification | Groq Llama 3.2 11B Vision (multimodal) via LangChain structured output |
| Auth | JWT (python-jose) + bcrypt |
| Validation | Pydantic 2.12 |
| Rate Limiting | slowapi |
| Testing | Pytest (31 tests) |
| CI/CD | GitHub Actions |
| Deployment | Docker, Render |
| Dashboard | React (Vercel) |

---

### 3. Odys — Scheduling SaaS for Freelance Professionals (2026–present)

**Live Product:** odys.com.br

A WhatsApp-first SaaS platform built entirely solo — from architecture to production — targeting Brazilian freelance professionals (psychologists, personal trainers, beauty professionals, etc.) who manage appointments manually via WhatsApp.

#### Problem It Solves

Brazilian freelance professionals lose time and revenue managing bookings manually via WhatsApp: confirming appointments one by one, tracking payments in spreadsheets, and experiencing frequent no-shows due to lack of automated reminders. Existing tools are too complex or lack real WhatsApp integration.

#### Key Features

**For professionals:**
- Public booking page at `/p/[slug]` with real-time availability calendar
- Dashboard with daily agenda and upcoming appointments
- Confirm, reject, and cancel bookings
- Automatic WhatsApp reminders sent 24h before appointments
- Payment tracking per session
- Configurable availability and payment policies
- Guided onboarding
- Real-time notifications

**For clients:**
- Self-service booking via the professional's public page
- Client area with appointment history (`/meus-agendamentos`)
- WhatsApp confirmation and reminders

#### Technical Architecture

**Multi-tenant architecture:** Each professional gets an isolated public booking page at `/p/[slug]`. Data is fully isolated per tenant.

**WhatsApp-native reminders:** Self-hosted **Evolution API v2** running on Railway (Docker image: `tiagorcfortunato/evolution-api-odys`). Reminders are triggered by **Supabase pg_cron** — a PostgreSQL-native cron job that periodically calls `/api/cron/reminders`, which queries upcoming appointments and sends WhatsApp messages via Evolution API. This is NOT a third-party bot — the message appears from the professional's own WhatsApp number.

**Payments:** Stripe subscriptions + PIX with webhook handling. Resolved PgBouncer transaction mode compatibility issue with Drizzle ORM (required `pgbouncer=true&connection_limit=1` in connection string).

**Rate limiting:** Upstash Redis with `@upstash/ratelimit` on API routes.

**Error monitoring:** Sentry (edge + server configs).

**Transactional email:** Resend for booking confirmations and notifications.

#### Tech Stack

| Layer | Technology |
|---|---|
| Framework | Next.js 16 (App Router) + TypeScript |
| Styling | Tailwind CSS v4 + shadcn/ui |
| Database | Supabase (PostgreSQL) |
| ORM | Drizzle ORM |
| Auth | Supabase Auth (email/password) |
| WhatsApp | Evolution API v2 (self-hosted, Railway) |
| Payments | Stripe (subscriptions + PIX) |
| Email | Resend |
| Rate limiting | Upstash Redis |
| Monitoring | Sentry |
| Scheduled tasks | Supabase pg_cron |
| App deployment | Vercel |
| WhatsApp API deployment | Railway |

#### Challenges and Solutions

- **Challenge:** PgBouncer transaction mode breaks Drizzle ORM's connection pooling.
  **Solution:** Added `pgbouncer=true&connection_limit=1` to the DATABASE_URL — resolved without switching away from PgBouncer.

- **Challenge:** WhatsApp reminders must come from the professional's own number (not a generic bot).
  **Solution:** Self-hosted Evolution API v2 on Railway; the professional scans a QR code once to connect their number; reminders are then sent natively.

- **Challenge:** Cron jobs in serverless environments are unreliable.
  **Solution:** Used Supabase `pg_cron` (PostgreSQL-native) which runs inside the database layer — independent of the Next.js serverless functions.

---

## Core Skills

### Backend Engineering
- **Python** — primary language; production-grade codebases
- **FastAPI** — REST APIs, dependency injection, Pydantic validation, OpenAPI docs
- **PostgreSQL** — schema design, migrations (Alembic, Drizzle), query optimization
- **SQLAlchemy** — ORM, session management, relationships
- **Drizzle ORM** — TypeScript-native ORM on PostgreSQL/Supabase
- **Pydantic** — data validation and settings management
- **Alembic** — database migration management
- **JWT** — auth flows, token-based security
- **Pytest** — unit and integration testing, fixtures, coverage

### AI & Machine Learning
- **RAG (Retrieval-Augmented Generation)** — end-to-end pipeline design and implementation
- **LangChain** — orchestration, prompt templates, message history, chains
- **ChromaDB** — vector store, persistent embeddings, metadata filtering
- **Vector Search** — embedding-based similarity retrieval, query enrichment strategies
- **fastembed** — local embedding model inference (BAAI/bge-small-en-v1.5)
- **Groq API** — LLM inference (Llama 3.1 8B)
- **YOLOv8 (Ultralytics)** — object detection, training, evaluation (mAP, precision, recall)
- **PyTorch** — model training, GPU-accelerated inference
- **Scikit-learn** — classical ML, evaluation metrics
- **Pandas** — data manipulation and analysis
- **PyMuPDF (fitz)** — PDF parsing, font-size-based document analysis
- **Claude Code** — AI-assisted development workflow

### Full-Stack & SaaS
- **TypeScript** — type-safe full-stack development
- **Next.js 16** (App Router) — SSR, API routes, dynamic routing, server components
- **Supabase** — PostgreSQL-as-a-service, Auth, pg_cron, real-time
- **Stripe** — subscription billing, PIX payments, webhook handling
- **Resend** — transactional email
- **Upstash Redis** — serverless rate limiting
- **Evolution API v2** — self-hosted WhatsApp messaging integration
- **Tailwind CSS + shadcn/ui** — component-based UI development

### DevOps & Infrastructure
- **Docker** — containerization, multi-service Docker Compose setups
- **GitHub Actions** — CI/CD pipelines, automated test runs
- **Vercel** — Next.js deployments, environment management
- **Railway** — Docker-based service deployments (Evolution API)
- **Render** — FastAPI/Python service deployments
- **Git** — version control, branching strategies

### Methodologies & Practices
- Clean layered architecture (Routers → Services → Models → Schemas)
- Test-driven development with automated CI
- Multi-tenant SaaS architecture
- Modular ML pipeline design (perception/reasoning separation)
- Production monitoring and error tracking (Sentry)
- Reproducible ML experiments (fixed seeds, controlled ablations, held-out test sets)

---

## Professional Experience

### Odys — Founder & Full-Stack Developer (2026–present, Berlin)
Built and launched a live SaaS product from zero — market research, product design, technical architecture, implementation, and production deployment — as sole developer.

### Fortunato Joias — Project Manager (2019–2024, Brazil)
End-to-end ownership of production planning, supplier relationships, and delivery cycles for a jewelry manufacturing business. Five years of operational management.

### Metalúrgica Besser — Engineering Intern, Logistics & Operations (2018–2019, Rio de Janeiro)
Supported logistics routines and production planning; reduced delays through structured problem solving.

### Guide Idiomas — Co-Founder & German Teacher (2016–2018, Rio de Janeiro)
Co-founded a German language school; developed structured curricula and managed operations.

---

## Education

| Degree | Institution | Location | Year |
|---|---|---|---|
| MSc Software Engineering | University of Europe for Applied Sciences | Berlin, Germany | 2024–2026 |
| Exchange — Mechanical Engineering | Hochschule Wismar | Germany | 2014–2016 |
| BSc Mechanical Engineering | UERJ | Rio de Janeiro, Brazil | 2013–2018 |

**MSc Thesis:** *Expert System for Road Surface Hazard Detection* — YOLOv8 pipeline with rule-based maintenance prioritization (RDD2022 dataset)

---

## Interview Q&A — Tiago in His Own Words

### About Tiago's Background

**"Tell me about yourself."**

Tiago comes from an entrepreneurial background. He studied mechanical engineering in Brazil with a focus on renewable energy, co-founded a business, and later worked as a project manager in a family business. This shaped how he thinks — he always looks at both the technical and business sides. He then moved to Germany to pursue a Master's in Software Engineering, where he built a SaaS product called Odys from scratch. It's live and helps freelancers manage bookings and reduce no-shows through automated communication via a self-hosted WhatsApp API. He built the entire system himself — backend, frontend, payments, and infrastructure — so he's used to owning both product and engineering decisions.

**"Why the transition from project management to engineering?"**

It's less of a transition and more of a completion. As a project manager Tiago was always the person closest to the technical decisions without making them. At some point he realized he was the bottleneck — he understood the problem but needed someone else to build the solution. So he went back to study and then built Odys to prove he could do it alone. The combination is what makes him useful: he thinks like a product person and executes like an engineer.

**"Mechanical engineering degree — why software?"**

Mechanical engineering gave Tiago systems thinking. He was always more interested in how things work together than in the physical components. Software is the same problem at a different layer. And in software you can ship something in weeks that would take years in physical engineering. The leverage is completely different.

### Why FIDgate

**"Why do you want to work at FIDgate?"**

Three things that rarely come together. First, the domain — Tiago originally studied renewable energy during his mechanical engineering degree, and always wanted to work on meaningful problems in that space. Second, the level of ownership — he's not looking for a role where he just implements tickets, he wants to own real problems end to end. Third, the problem itself — critical energy decisions are still made using static models, and building a system that continuously optimizes those decisions in real time is both technically challenging and has real-world impact. That combination is what makes this opportunity very compelling.

**"You have no energy industry experience. How would you contribute?"**

Tiago's role is to bring strong engineering and product thinking to make the system usable, reliable, and scalable — that part is domain-agnostic. He would close the domain gap quickly by working closely with the modelling team and early users. His mechanical engineering background in renewable energy gives him a starting point — he's not learning the domain from zero. But the real value he brings is on the engineering and product side.

### About Odys in Depth

**"What was the hardest part of building Odys?"**

The main technical challenge was making the WhatsApp integration reliable. Tiago had to self-host a WhatsApp API (Evolution API) inside a Docker container and deal with unstable connections, since WhatsApp sessions can drop at any time. To handle that, he built a watchdog system to monitor the connection and automatically restart it, along with scheduled jobs for reminders and robust webhook handling for payments. Since he was the only one building it, he had to treat reliability as a core requirement from the start.

**"What would break first at 10x users?"**

Probably the WhatsApp connection layer. The self-hosted Evolution API works reliably for current load but hasn't been stress-tested at scale. The database and API layer aren't a concern — Supabase with proper indexing handles that. But the WebSocket connections to WhatsApp would need proper load balancing and potentially multiple instances.

**"How would you integrate AI/LLMs into Odys?"**

The most natural place is the booking flow. Freelancers receive messages like "can I book something this week?" directly on WhatsApp. An LLM could parse intent, extract constraints like date or service, and connect that to the availability system to either suggest slots or confirm a booking automatically. The second use case is the professional side: querying the system in natural language — "who cancelled this week?" — instead of navigating dashboards.

### About the RAG Pipeline

**"How does the RAG work apply to FIDgate?"**

FIDgate's engine produces results — optimal configurations, revenue projections, dispatch strategies. But the energy professional needs to understand why a specific configuration is optimal before committing millions of euros to it. That's the same problem Tiago worked on: making complex model outputs trustworthy and interpretable. He would build an AI layer that explains the engine's reasoning in plain language — not just "this configuration has the highest IRR" but "this configuration outperforms because of these specific market conditions and site constraints."

**"What are the limitations of RAG systems?"**

Four main ones: (1) Retrieval quality — if the relevant context isn't retrieved, the answer fails regardless of the model; (2) Hallucinations — even with the right context, the model can generate incorrect responses; (3) Latency and cost — combining retrieval and generation adds overhead at scale; (4) Evaluation is hard — it's not always obvious how to measure whether retrieval is improving.

### Technical Depth

**"How would you handle scale — queues, async, retries?"**

For any workflow involving external systems, Tiago would introduce background job queues for async processing and make all external interactions idempotent. That way failures can be retried safely without side effects. For observability he'd add structured logging and metrics on queue depth and failure rates from the start.

**"How do you use AI in your engineering workflow?"**

His daily setup is Claude Code and Gemini inside Cursor. He writes deliberate prompts, reviews every suggestion critically, and only ships what he actually understands. He doesn't use AI to generate code he can't explain. It lets him move at founder speed without sacrificing quality — but the architectural decisions are always his.

### About the FIDgate Role Specifically

**"How would you turn the decision engine into a platform developers want to use?"**

First, talk to early adopters to understand how they're actually using the engine and where the current API creates friction. Then focus on three areas: (1) API design — clear versioning, predictable response structures, meaningful error handling; (2) Developer experience — documentation based on real workflows, not just endpoints; (3) Reliability — rate limiting, monitoring, clear latency/uptime expectations. On top of that, an AI layer focused on interpretability — helping users understand why the engine suggests a given configuration.

**"What would you do in your first 30 days?"**

Understanding before building, but not passively. Go deep into the decision engine, the current API, and how it's being used — run it locally, explore edge cases, try to break it from a developer's perspective. In parallel, talk to early adopters to understand what decisions they're trying to make and where the interface creates friction. Then identify one or two high-impact improvements and start implementing them before the end of the first month.

**"What does founder-level ownership mean to you?"**

It means not waiting to be told where the problem is. Understanding the user, identifying what matters most, making decisions with incomplete information, and taking responsibility for the outcome — not just the implementation. Thinking beyond the code and treating the product as something you are fully accountable for.

### Working Style and Availability

**"How do you handle working without management or clear requirements?"**

That's how Tiago prefers to work. At Odys there was no product manager, no designer, no one to tell him what to build next. He talked to potential users, identified the highest-friction point, and built that. Then repeated. The risk of working without management is building the wrong thing — the solution is staying close to the user, not waiting for someone to write a spec.

**"Are you currently employed? When can you start?"**

Tiago is not currently employed. He's been focused on his master's, building Odys, and applying for the right opportunity. He can start within a few weeks.

**"Do you have the right to work in Germany?"**

Yes. Tiago has a permanent residence permit and full work authorization in Germany.

**"What's one thing you're not good at yet?"**

Distributed systems at scale. He's built reliable systems for current load levels, but hasn't operated infrastructure at the scale of thousands of concurrent users. What he does well is identifying when a system is approaching that limit and designing for it before it becomes a problem.
