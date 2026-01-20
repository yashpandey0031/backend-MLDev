## HTTP

**Summary:** The base protocol used for communication between client (browser/app) and server. Uses methods like **GET, POST, PUT, DELETE** and status codes like **200, 404, 500**.
**Applications:** Web apps, APIs, fetching data from servers, form submissions, authentication requests.

---

## REST

**Summary:** A style of designing APIs where everything is treated as a **resource** (like `/users`, `/products`). Uses HTTP methods properly and returns structured data (usually JSON).
**Applications:** Building scalable backend APIs for web/mobile apps, CRUD systems, microservices.

---

## Auth: JWT + Sessions

**JWT (Token-based auth):**
**Summary:** Server issues a signed token. Client sends it in every request (usually via `Authorization` header). Stateless.
**Applications:** Mobile apps, SPAs (React), microservices, distributed systems.

**Sessions (Cookie-based auth):**
**Summary:** Server stores session data, client stores only a session id cookie. Stateful.
**Applications:** Traditional websites, dashboards, safer logout control, user login systems.

---

## Middleware

**Summary:** Functions that run **between request and response**. Can modify request, verify auth, validate input, log requests, etc.
**Applications:** Auth checking, rate limiting, request logging, input parsing, error handling.

---

## Env / Secrets

**Summary:** Sensitive config values stored outside code (like database URL, API keys). Usually managed through `.env` or secret managers.
**Applications:** Prevent leaking keys on GitHub, switching configs between dev/prod, secure deployments.

---

## PostgreSQL

**Summary:** A powerful relational SQL database. Supports tables, joins, constraints, indexing, transactions.
**Applications:** User data storage, ecommerce, finance apps, analytics, anything needing structured + reliable data.

---

## ORM (Prisma)

**Summary:** ORM lets you interact with database using code instead of raw SQL. Prisma generates typesafe queries and schema-based database models.
**Applications:** Faster backend development, type-safe DB operations in Node/TS projects, easier migrations.

---

## Error handling + Logging

**Summary:** Error handling ensures failures don’t crash the system and responses are meaningful. Logging records events for debugging and monitoring.
**Applications:** Debugging production bugs, audit trails, tracking failed requests, monitoring app health (Sentry/Logtail/ELK).

---

## Validation (Zod)

**Summary:** Zod validates and parses request data (body/query/params) and ensures it matches the expected schema.
**Applications:** Prevent bad input, reduce runtime errors, secure APIs, enforce correct types in Express/Next.js backends.
