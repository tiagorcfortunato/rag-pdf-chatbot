# Odys — Technical Deep Dive

> Technical knowledge base for Odys, Tiago Fortunato's WhatsApp-first scheduling SaaS for Brazilian independent professionals. Live at [odys.com.br](https://odys.com.br). Built solo by Tiago, in production.

---

## Overview

Odys is a scheduling and customer-management SaaS for Brazilian independent professionals (psychologists, personal trainers, nutritionists, beauticians, coaches, therapists — about 30 professions across 6 verticals). The key differentiator is WhatsApp automation that sends from the professional's real phone number, using a self-hosted Evolution API. The common thread across users: independent operators who run everything through WhatsApp manually today.

---

## Codebase Scale (Concrete Numbers)

- **112** TypeScript files in `src/` (`.ts` + `.tsx`)
- **20** API route handlers (`src/app/api/**/route.ts`)
- **19** reusable React components in `src/components/`
- **10** PostgreSQL tables managed by Drizzle ORM
- **19** WhatsApp message templates as named functions (not inline strings)

---

## Stack Versions

- **Next.js 16.2.1** (App Router)
- **React 19.2.4**
- **TypeScript 5**
- **Tailwind CSS v4** + shadcn/ui + Base UI
- **Drizzle ORM 0.45.2** on **postgres-js** driver
- **Stripe 21.0.1**
- **Groq SDK 1.1.2** — model `llama-3.3-70b-versatile`
- **Supabase SSR 0.9.0**
- **Zod 4** for request validation
- **date-fns 4** for all date arithmetic
- **Upstash Redis** for rate limiting
- **Sentry** for error monitoring
- **PostHog** for product analytics
- **Resend** for transactional email
- **Evolution API v2** (self-hosted on Railway) for WhatsApp

---

## Database Schema — The 10 Tables

1. **professionals** — core account (userId, slug, plan, pricing, Stripe IDs, payment type, PIX key, trial, welcomeMessage, autoConfirm)
2. **availability** — weekly working hours per day-of-week
3. **clients** — client records per professional (userId nullable — clients don't need an account to be booked)
4. **client_notes** — private notes pros keep on clients (Pro plan)
5. **recurring_schedules** — weekly / biweekly / twice_weekly patterns
6. **appointments** — bookings with status + payment status + reminder flags
7. **messages** — in-app chat (text/link/pdf) with readAt
8. **follows** — user follows professional
9. **reviews** — 1–5 stars + comment, unique per appointment
10. **notifications** — in-app bell, typed (booking_request, booking_confirmed, reminder_24h, etc.)

### Indexes Created
- `availability_professional_id_idx`
- `clients_professional_id_idx`, `clients_user_id_idx`
- `appointments_professional_id_idx`, `appointments_client_id_idx`, `appointments_starts_at_idx`, `appointments_status_idx`
- `messages_professional_client_idx` (composite)
- `follows_professional_id_idx`, `follows_user_id_idx`
- `reviews_professional_id_idx`
- `notifications_recipient_id_idx`

### State Machines
**Appointment status:**
`pending_confirmation → confirmed | rejected`
`confirmed → completed | cancelled | no_show`

**Payment status:**
`none → authorized → captured | refunded`

---

## Plans & Pricing (Monthly BRL)

| Plan | Price | Clients | Appts/mo | Reminders | Recurring | Messages | Notes | Reports | AI |
|------|------:|--------:|---------:|:---------:|:---------:|:--------:|:-----:|:-------:|:--:|
| Free | R$0 | 10 | 20 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Basic | R$39 | ∞ | ∞ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Pro | R$79 | ∞ | ∞ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Premium | R$149 | ∞ | ∞ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

- **14-day Pro trial** for new signups (constant `TRIAL_DAYS`)
- Premium differentiator: **multiple professionals per account** (coming soon)
- `effectivePlan(plan, trialEndsAt)` returns "pro" while trial is active
- Plan changes are webhook-driven — client can never escalate plan

---

## Rate Limits (Upstash Redis, Sliding Window)

- **Booking:** 5 requests per IP per 10 minutes (`rl:booking`)
- **Generic API:** 60/minute per IP (`rl:api`)
- **Onboarding:** 3/hour per IP (`rl:onboarding`)

Three distinct limiters with distinct Redis key prefixes so they don't collide and can be changed independently. IP extracted from `x-forwarded-for` header. Returns 429 on exceed.

---

## Cron Jobs (`vercel.json`)

- **08:00 daily** — `/api/cron/reminders` (24h and 1h reminder sends + trial expiry emails)
- **09:00 daily** — `/api/cron/whatsapp-watchdog` (reconnects WhatsApp session if dropped overnight)

### Reminder Windows (Defensive)
- **24h window:** `[now+23h, now+25h]` — any confirmed appointment in this range gets a reminder
- **1h window:** `[now+50min, now+70min]`

The 2-hour window ensures idempotency via flags while also being resilient to missed cron runs. If the cron fails one day, the next run still catches the same appointments.

---

## Booking Flow (The Golden Path)

**Endpoint:** `GET /api/booking?slug=...&date=...` returns `{ professional, rules, existingAppointments }`. The client renders available slots via `generateSlots()` in `src/lib/slots.ts`, which:
1. Picks the rule matching `date.getDay()`
2. Iterates from start time to end time in `sessionDuration` steps
3. Skips slots in the past
4. Skips slots overlapping any existing appointment
5. Returns array of `"HH:mm"` strings

**Endpoint:** `POST /api/booking` validated with Zod. Does **seven** things in order:
1. **Rate limit** — 5 per 10 min per IP
2. **Load professional** by slug
3. **Plan limits** — if plan caps apply, count clients and monthly appointments, reject over limit (existing clients can re-book even at cap)
4. **Overlap check** — `lt(startsAt, endDate) AND gt(endsAt, startDate)`, excluding rejected/cancelled, returns 409 if conflict
5. **Upsert client** — look up by professionalId + (phone OR email); if found with empty email and email now provided, update it
6. **Insert appointment** — status is `confirmed` if `professional.autoConfirm`, else `pending_confirmation`
7. **Fire side-effects** — in-app notification (awaited DB insert), WhatsApp to pro (fire-and-forget `.catch`), Resend email to pro (fire-and-forget `.catch`)

Side-effects that can fail (WhatsApp, email) are fire-and-forget so they don't block the response. The notification insert IS awaited because in-app notifications are the SLA-sensitive surface. Validation and limits happen BEFORE DB mutations.

---

## Appointment Lifecycle (`PATCH /api/appointments/[id]`)

Single endpoint handles every status transition. Actions: `confirm`, `reject`, `cancel`, `paid`, `complete`, `no_show`.

- **Auth:** loads user, appointment, professional, client. Determines `isProfessional` or `isClient` by matching `userId`
- **Cancel:** allowed if `pending_confirmation` or `confirmed`; both sides can cancel; different WhatsApp templates for "client cancelled → notify pro" vs "pro cancelled → notify client"
- **Paid / Complete / No-show:** professional only (`forbidden` otherwise)
- **Confirm / Reject:** professional only; sets status AND payment status (`authorized`/`refunded`); creates a notification for the client if they have an account; sends tailored WhatsApp + email; if the client has no account, the confirmation message appends `msgRegistrationInvite()` with a pre-filled register URL — that's the user-growth hook

---

## The AI Assistant (`POST /api/ai/chat`)

File: `src/app/api/ai/chat/route.ts` (244 lines). Flow:

1. `getUser()` / `getProfessional()` — else 401
2. `canUseFeature(plan, "assistant", trialEndsAt)` — else 403
3. Read messages array from body — Zod validation
4. Build `[system, ...userMessages]`
5. `Groq.chat.completions.create({ tools: TOOLS, tool_choice: "auto" })`
6. If no tool_calls → return content directly
7. Else: execute each tool_call
   - `get_stats` → queries appointments for last 6 months, builds per-month and global summaries
   - `get_upcoming` → joins appointments × clients for next 7 days, limit 20
   - `get_no_show_clients` → SQL count-filter aggregation, top 10 groups, filters zero-no-shows client-side
8. Append tool results to messages as `role:"tool"` with `tool_call_id`
9. Second Groq call (no tools) for the final answer
10. Return `{ reply }`

### AI Guardrails (Four Layers)
1. **Plan check** happens BEFORE the Groq client is even initialized — 403 if not Pro, saves money on unauthorized traffic
2. **Tenant scoping at SQL layer** — every tool query is scoped to `professional.id` from the server-authenticated session, never trusted to the model
3. **Deterministic math** — revenue is computed by the tool (`completed_count × sessionPrice`), not by the model. The model doesn't multiply numbers.
4. **System prompt rules** — "always use tools, never invent numbers, format BRL, respond in Portuguese, follow this output structure". Unknown tool names return an error object instead of throwing.

The system prompt shape is one of those cases where prompt engineering is design: "TAXA DE NO-SHOW → use get_stats" vs "QUAIS clientes faltam mais → use get_no_show_clients" explicitly disambiguates two similar intents.

---

## The Reminder Cron (`GET /api/cron/reminders`)

Triggered daily at 08:00. Three stages in one endpoint:

1. **24h reminders** — joins appointments × clients × professionals, filters `status = confirmed`, `reminder_sent_24h = false`, and `startsAt ∈ [now+23h, now+25h]`. For each, re-checks plan feature (in case the pro downgraded between cron runs), sends WhatsApp, collects IDs of successfully-sent, then bulk updates `reminder_sent_24h = true`.
2. **1h reminders** — same pattern, window `[now+50min, now+70min]`.
3. **Trial expiry emails** — scans professionals with a `trialEndsAt`, computes `trialDaysLeft()`, sends Resend email when `daysLeft === 3` or `daysLeft === 1`.

**Auth:** `x-cron-secret` header OR `Authorization: Bearer <CRON_SECRET>` — supports both Vercel's native cron header and manual debug calls.

---

## The WhatsApp Watchdog (`GET /api/cron/whatsapp-watchdog`)

Daily at 09:00. Flow:

1. Auth check (same dual scheme)
2. `GET /instance/fetchInstances` on Evolution API → check connection status
3. If `status === "open"` → return `{ ok: true }`
4. Otherwise → hit `/instance/connect/{instance}` to force re-init
5. Sleep 10 seconds
6. Re-check status
7. Return the before/after statuses

This is the "invisible" reliability feature. If the Evolution API's WhatsApp Web session drops overnight, it's reconnected before the first reminder goes out.

---

## Stripe Billing (`POST /api/stripe/checkout` + `POST /api/stripe/webhook`)

### Checkout Creation
- Creates a Stripe Checkout Session in `subscription` mode
- Metadata carries `professionalId` and `plan` so the webhook can map back
- **Trial-aware:** if the pro is currently in the 14-day Pro trial and is buying Pro, `trial_end` is set to their existing trial end, and `payment_method_collection: "if_required"` — meaning they don't have to enter a card mid-trial
- Locale forced to `pt-BR`

### Webhook
- Verifies signature with `stripe.webhooks.constructEvent`
- Handles three events:
  - `checkout.session.completed` → update `plan`, `stripeCustomerId`, `stripeSubscriptionId` on the professional
  - `customer.subscription.updated` (active) → look up plan by `priceId`, update `plan` (upgrade/downgrade via portal)
  - `customer.subscription.deleted` → reset `plan = "free"`, null the subscription ID

**Security callout:** plan updates happen ONLY via webhook. There's no client-trusted path to escalate plan. Stripe signs the event, Tiago verifies, then updates.

---

## Auth (Supabase)

- SSR via `@supabase/ssr`'s `createServerClient`
- Cookie bridge through `next/headers` `cookies()`
- `getUser()` in `lib/api.ts` is the choke point — every protected route calls it
- `getProfessional(userId)` is the companion — most routes also want the professional row
- Email/password + Google OAuth, handled by Supabase

### Authorization
Per-route checks. For the appointment PATCH endpoint, loads the appointment, the professional, and the client, then derives `isProfessional = professional.userId === user.id` and `isClient = client.userId === user.id`. Each action gates on one of those — cancel allows both, paid/complete/no-show is pro-only, confirm/reject is pro-only. It's explicit, not magic.

---

## Recurring Schedules

- Stored as "patterns" (`weekly`, `biweekly`, `twice_weekly`)
- On creation, generates **concrete appointments** for the next 8 weeks (`RECURRING_WEEKS_AHEAD`), inserted as `status: "confirmed"`
- On delete, the schedule is marked `active: false` but existing future appointments are not deleted — users can still cancel them individually

Trade-off: pre-generation means recurring clients always know their next 2 months of appointments in the UI without lazy-generating on every page load, and the overlap check "just works" without special-casing recurring.

---

## PIX QR Code (`lib/pix.ts`)

Hand-rolled payment protocol code — Tiago implemented the PIX QR standard from scratch rather than using a library:

- Implements EMV BR Code generation per Banco Central's spec (Manual de Padrões para Iniciação do Pix)
- TLV encoder (`field(id, value)`)
- CRC16/CCITT-FALSE for the 4-char checksum at the end
- Merchant name/city normalized (NFD, strip accents, uppercase, length-capped)
- Optional amount field — if set, produces a fixed-amount QR; otherwise static

Reason for not using a library: "the spec is small, the libraries I found pulled too much, and I wanted to understand what I was generating."

---

## Infrastructure & Deployment

- **Hosting:** Vercel (app + cron jobs)
- **Database:** Supabase PostgreSQL with PgBouncer pooler
- **WhatsApp API:** Evolution API v2, self-hosted on Railway (Docker)
- **Rate limiting:** Upstash Redis
- **Error monitoring:** Sentry
- **Analytics:** PostHog
- **Transactional email:** Resend
- **CI/CD:** GitHub Actions (tsc, eslint, build) → auto-deploy via Vercel

### The `prepare: false` Decision
Required for PgBouncer transaction mode (Supabase's pooler). Prepared statements are per-connection state, so they break when PgBouncer rotates server connections between clients. Turning off prepared statements is the documented workaround.

---

## Technical Decisions — The "Why" Behind Every Choice

| Decision | Reasoning |
|---|---|
| **Next.js 16 App Router** | SSR for SEO on public booking pages and API routes in the same codebase — solo dev, no separate backend to own |
| **Drizzle over Prisma** | Lighter, fully typed at query level, schema changes surface as type errors across the codebase; less generated code to reason about |
| **Supabase over self-hosted Postgres** | Managed auth + Postgres + storage from one vendor, pooled connection string works from serverless |
| **`prepare: false` on postgres-js** | Required for PgBouncer transaction mode — prepared statements span connections and break |
| **Evolution API (self-hosted) over WhatsApp Business API** | Messages send from the professional's real phone via WhatsApp Web — the actual product differentiator, and 10× cheaper |
| **Groq for the AI assistant** | Latency. llama-3.3-70b inference is fast enough that tool-calling chat feels instant; on OpenAI it wouldn't |
| **Tool-calling with scoped SQL over embedding search** | Answers must cite real numbers for a financial tool. Structured queries over structured data win over RAG here |
| **Upstash Redis for rate limiting** | Serverless-friendly (fetch-based, no connection pool), cheap, three isolated limiters |
| **Zod for request validation** | Parse-don't-validate — TypeScript type is derived from schema, runtime and compile-time checks can't drift |
| **Stripe webhooks as the only plan-update path** | Client-trusted plan upgrades are a security smell. Stripe signs the event, Tiago verifies, then updates |
| **Vercel cron over Inngest/Trigger.dev** | Two jobs, daily, no fan-out — don't need the complexity |
| **Sentry + PostHog separately** | Sentry for errors, PostHog for product funnels. Different failure modes, different tools |
| **Self-hosted postgres-js driver over @supabase/supabase-js** | Direct Drizzle queries with full type inference, not the PostgREST layer |
| **Resend over SendGrid/Postmark** | DX-first: TypeScript SDK, React Email compatibility, free tier fits solo launch |
| **shadcn/ui + Tailwind v4** | Copy-paste components Tiago owns (can modify), not a dependency he's stuck with |
| **Fire-and-forget side-effects for WhatsApp/email** | User clicked "confirm booking" — they need a 200 back fast; a WhatsApp send taking 2s shouldn't block |
| **19 WhatsApp templates as named functions** | Single source of truth, no typos, searchable, testable, copy changes are one file |

---

## Odys Q&A — Product Questions

**Q: What does Odys actually do, in one sentence?**
A: Scheduling and customer-management SaaS for Brazilian independent professionals, with WhatsApp automation that sends from the professional's real phone number.

**Q: Who are the users?**
A: About 30 professions across 6 verticals — psychologists, personal trainers, nutritionists, beauticians, coaches, therapists. The common thread: independent operators who run everything through WhatsApp manually today.

**Q: How do users pay?**
A: Stripe subscriptions, four tiers — Free, R$39, R$79, R$149. 14-day Pro trial on signup. Plan changes are webhook-driven so the client can never escalate plan on its own.

**Q: Why Brazil specifically?**
A: Three reasons. One, WhatsApp penetration is the highest in the world there (~95%+) — the WhatsApp-first assumption is correct for every user. Two, PIX is the instant-payment rail, so the PIX QR integration works and every user already knows what to do with it. Three, existing tools there are complex and don't have real WhatsApp integration.

**Q: Who are the competitors?**
A: Calendly and Simples Agenda globally/locally. Calendly doesn't fit because Brazilian clients don't book through email — they book through WhatsApp threads. Simples Agenda is closer but doesn't do WhatsApp from the real number.

**Q: What's the moat?**
A: Not a moat in the defensibility sense — a bigger player could copy this. It's an execution moat: the self-hosted Evolution API + watchdog + 19 templated touch points + professional-number authentication is a lot of invisible plumbing that most people won't build because it's not glamorous.

**Q: What metrics does Odys track?**
A: No-show rate (month-by-month), completed sessions, revenue per professional, trial conversion rate. The AI assistant's main job is reporting on these.

**Q: What feature is Tiago proudest of?**
A: The AI assistant. It was his first time building a tool-calling agent against production data, and he had to get the guardrails right — plan check before the Groq call, scoped SQL per tenant, deterministic revenue math instead of trusting the model to multiply. The other candidate is the WhatsApp-from-real-number setup with the watchdog.

**Q: What was the hardest product decision?**
A: Whether clients should need an account to book. Tiago said no — booking is self-serve, account-optional, and the confirmation message includes a register-with-pre-filled-data link. More code (nullable user_id on the client table, upsert-on-booking logic) but it's the right call because friction kills booking conversion.

---

## Odys Q&A — Technical Questions

**Q: How does Odys prevent double-booking?**
A: Pre-insert overlap check: query for any appointment on that professional where `startsAt < proposedEnd` AND `endsAt > proposedStart`, excluding rejected and cancelled. If a row comes back, return 409. It's not transactionally bulletproof — under enough concurrent load two parallel requests could both see empty results and both insert. For current traffic it's the right trade-off. For hard correctness, Tiago would wrap the read+insert in a serializable transaction or add a Postgres exclusion constraint (`EXCLUDE USING gist`) on the tstzrange of the appointment.

**Q: How does auth work in Odys?**
A: Supabase Auth via `@supabase/ssr`. The choke point is `getUser()` in `lib/api.ts` — every protected API route calls it first. It reads cookies, asks Supabase for the user, returns user or null. Companion `getProfessional(userId)` fetches the professional row. Email/password + Google OAuth configured in Supabase's dashboard.

**Q: How is rate limiting done?**
A: Upstash Redis with `@upstash/ratelimit`'s sliding window. Three separate limiters — booking (5 per 10 min/IP), general API (60/min), onboarding (3/hour). Distinct Redis prefixes so they don't collide. IP from `x-forwarded-for`. Returns 429 on exceed.

**Q: What happens if WhatsApp sending fails?**
A: `sendWhatsApp()` never throws — it catches, logs to `console.error`, and returns `false`. Callers treat it as fire-and-forget with `.catch(console.warn)` so a WhatsApp failure never breaks the user's flow. WhatsApp delivery is never on the critical path of the app's response — the in-app notification is. If every WhatsApp fails, the user still sees their confirmed appointment in the dashboard.

**Q: What happens if the Evolution API server goes down?**
A: The watchdog catches most disconnections — polls every morning, reconnects if `status !== "open"`. For sends during downtime, they fail-soft. A retry queue for critical messages is on the "would add" list.

**Q: How does the AI assistant prevent leaking one professional's data to another?**
A: The tools accept `professionalId` as an argument (from the server-authenticated session, not from the model), and every SQL query inside the tool is `WHERE professional_id = $1`. The model never sees another professional's data, because the model never calls anything but the three tools, and the three tools never join across tenants. Tenant isolation is enforced BENEATH the model, at the SQL layer.

**Q: What are the AI guardrails?**
A: Four layers. (1) Plan check before the Groq client is even initialized — 403 if not Pro. (2) Tenant scoping at the SQL layer. (3) Deterministic math — revenue is computed by the tool, not by the model. (4) System prompt rules — "always use tools, never invent numbers, format BRL, respond in Portuguese." Unknown tool names return an error object instead of throwing.

**Q: Why Groq specifically?**
A: Inference latency. Groq's LPU architecture gets llama-3.3-70b responses back in under a second for short contexts. For a chat UI where the user is staring at an input, that's the difference between feeling instant and feeling sluggish. OpenAI's 4o is closer in quality but slower for this shape of workload, and for an internal analytics tool 70b is enough.

**Q: How does Odys handle Stripe webhooks?**
A: Three events — `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`. Signature verification via `stripe.webhooks.constructEvent` first — if that fails, 400. Session metadata carries `professionalId` and `plan`. Subscription updates look up plan by `priceId`. Deletes reset to "free". **All plan changes happen here and nowhere else** — the client can never POST its way to a paid plan.

**Q: What's the failure mode if a Stripe webhook is missed?**
A: Stripe retries webhooks on non-2xx responses for up to 3 days. If still down, the professional's plan drifts out of sync. Mitigation not yet built: a nightly reconciler that asks Stripe for the current subscription state of every professional and updates drift.

**Q: Why `prepare: false` on postgres-js?**
A: Supabase's pooled connection string uses PgBouncer in transaction mode, which rotates server connections between clients. Prepared statements are per-connection state, so they break when PgBouncer hands a next query to a different underlying connection. Turning off prepared statements is the documented workaround.

**Q: How is Vercel cron secured?**
A: Vercel hits `GET` on the path at the scheduled time with an `Authorization: Bearer <CRON_SECRET>` header. Handlers check EITHER that header or a `x-cron-secret` header — dual scheme for manual debug triggers. Returns 401 if neither matches.

**Q: Why the 2-hour reminder window instead of "24 hours exactly"?**
A: Two reasons. One: cron runs once a day, so "exactly 24 hours" would miss most appointments — any appointment whose 24h mark is between crons wouldn't get notified. The ±1h window guarantees every confirmed appointment falls into exactly one daily run. Two: resilience to missed runs. If the cron fails one day, the window plus the `reminder_sent_24h` flag means the next run catches most of the backlog.

**Q: How is production monitored?**
A: Sentry for errors (exceptions, stack traces with source maps). PostHog for product analytics and funnels. Vercel's own logs for HTTP. The watchdog cron is a daily "is this alive?" probe. For a team setting, Tiago would add more — uptime monitoring, alert rules, structured log aggregation.

**Q: What about test coverage?**
A: Honest answer: very light test coverage. For a team setting, Tiago would introduce unit tests for `lib/slots.ts` and `lib/pix.ts` (pure functions), contract tests for the API routes (Vitest + supertest), and an eval suite for the AI assistant. Currently relies on TypeScript + manual QA, which is the trade-off that stops working the moment a second person touches the code.

**Q: What's the most complex query in the codebase?**
A: The `get_no_show_clients` aggregation in the AI route. Left join of appointments and clients, filtered by professional and last 6 months, grouped by client, selects both `count(*)` (total sessions) and `count(*) filter (where status = 'no_show')` (no-shows). Uses raw SQL via `sql\`\`` in Drizzle for the Postgres filter-clause aggregation.

**Q: How would pagination work with 100,000 appointment rows?**
A: Cursor pagination using `startsAt + id` as the cursor key: `WHERE (starts_at, id) > ($cursor_time, $cursor_id) ORDER BY starts_at, id LIMIT $n`. Offset pagination gets quadratically slow at high offsets. The `appointments_starts_at_idx` index already covers the ordering half; for full coverage, add a composite `(starts_at, id)` index.

---

## Specific Subsystem Details

**Appointment status machine:** Six states. `pending_confirmation` is the initial state on booking (unless autoConfirm is on → `confirmed`). From `pending_confirmation`, the pro can confirm → `confirmed` or reject → `rejected`. From `confirmed`, three terminal transitions: `complete` → `completed`, `no_show` → `no_show`, or either side can cancel → `cancelled`. Rejected and cancelled appointments are excluded from the overlap check so their time slots become available again. Payment status is a separate orthogonal machine that tracks independently.

**Autoconfirm toggle:** Flag on the professional row. In the booking POST, appointment status is set to `confirmed` instead of `pending_confirmation` if `autoConfirm` is true. Used by pros with open calendars who don't need to manually approve every booking. Off by default because most professionals want the screening step.

**Recurring schedules after week 9:** Currently the pre-generated 8 weeks expires. Known issue. Options considered: extend generation on every login for professionals with active recurring schedules (cheap but not clean), or a nightly cron that tops up to 8 weeks from now (cleaner, another moving part).

**Fire-and-forget for side-effects rationale:** (1) User's response time should reflect the core operation (the DB insert), not the secondary ones (WhatsApp, email). A 2-second delay on booking POST is terrible UX. (2) WhatsApp and email have their own reliability profiles — WhatsApp can be down, Resend can throttle — and neither should turn a successful booking into a failed one.

---

## Future Improvements (Known Gaps)

- **Formal AI evals** — currently manual regression tests, not a formal eval suite. For production: pairs of (user question, expected tool called, expected answer shape) run on each deploy.
- **Stripe webhook reconciler** — nightly job that asks Stripe for current subscription state and fixes drift.
- **Stricter state machine enforcement** — extract transitions into a map and let a single function validate any transition, plus audit log.
- **Retry queue for critical WhatsApp messages** — confirmation message, 24h reminder.
- **Caching layer** — for public booking page (per-slug with revalidation) and `/explore` discovery page (stale-while-revalidate).
- **Test coverage** — unit tests for pure functions, contract tests for API routes, AI eval suite.
- **Recurring schedule auto-extension** — nightly cron to maintain the 8-week rolling window.

---

## Professions Catalog

Odys supports ~30 professions across 6 verticals: psychologists, personal trainers, nutritionists, beauticians (cabeleireiros, esteticistas, manicures), coaches, and therapists. The common thread: independent operators who manage appointments manually through WhatsApp today.
