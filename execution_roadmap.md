# EcoBuck Smart Compost Monitoring System
## 6-Week Connectivity & Backend Execution Roadmap (Assignment C)

**Author:** Toqeer Ahmed  
**Role:** Principal IoT Systems & Backend Architect  
**Date:** July 8, 2026  
**Status:** PROPOSED (Roadmap Review Stage)  

---

## Week 1: Requirements Locking, Cloud Path Selection & Baseline Project Init

### Day 1: Project Setup and Local Environment Provisioning
*   **Objective:** Set up python environment, dependency management tools, local Git configurations, and initial repository scaffolding.
*   **Expected Output:** Functioning local environment running Python 3.10+, virtual environment active, and baseline dependencies installed.
*   **Dependencies:** None.
*   **Skills Required:** Git version control, Python package management (`pip`, `venv`).
*   **Resources to Learn:** [Python virtual environments guide](https://docs.python.org/3/library/venv.html).
*   **Deliverables:** Main project directory structure with `.gitignore`, `requirements.txt`, and virtual environment directory.
*   **Potential Risks:** Local dependency version mismatches with other team members.
*   **Acceptance Criteria:** A command `python -m pip list` runs successfully and version control tracks initial structure.
*   **Collaboration Required:** Aligning Git branching guidelines with Firmware (Team B) and Mobile (Team D) leads.

### Day 2: Cloud Platform Comparative Analysis & Architecture Selection
*   **Objective:** Document and decide between PostgreSQL/TimescaleDB, Firestore NoSQL, and MQTT setups.
*   **Expected Output:** Signed-off Architecture Decision Record (ADR-001) outlining final database choice (Firestore).
*   **Dependencies:** Day 1 local environment configuration.
*   **Skills Required:** Technology stack evaluation, cost estimation, system design analysis.
*   **Resources to Learn:** [Firestore pricing and performance limits](https://firebase.google.com/docs/firestore).
*   **Deliverables:** `docs/adr/001-cloud-database-selection.md` in repository.
*   **Potential Risks:** Picking a database structure that is too complex for 6-week prototyping.
*   **Acceptance Criteria:** The ADR is written, detailing costs, query speeds, complexity tradeoffs, and mobile integration speeds.
*   **Collaboration Required:** Approval from Product Lead and Assignment D (Mobile App) owner.

### Day 3: Finalizing Ingestion Schema Contracts
*   **Objective:** Define the exact telemetry JSON payload schema that the ESP32 firmware will send.
*   **Expected Output:** API contract document specifying exact variable names, types, units, and boundaries.
*   **Dependencies:** Day 2 database choice selection.
*   **Skills Required:** JSON schema layout, data contracting.
*   **Resources to Learn:** [JSON Schema standards](https://json-schema.org/).
*   **Deliverables:** `docs/schemas/telemetry_schema.json` documenting the JSON contract.
*   **Potential Risks:** Firmware team sending fields not supported by the backend parsing models.
*   **Acceptance Criteria:** Signed-off schema definition containing `device_id`, timestamp, readings (raw/filtered/trend), status, quality flags, and battery level.
*   **Collaboration Required:** Joint session with Team B (Firmware) to freeze key names.

### Day 4: Core Project Structure Scaffolding
*   **Objective:** Implement folder structures matching the clean architecture design (app, api, services, schemas, repositories, core).
*   **Expected Output:** Empty Python files initialized with imports and structure templates.
*   **Dependencies:** Day 1 & Day 3 contract freezes.
*   **Skills Required:** FastAPI structure layouts, clean architecture paradigms.
*   **Resources to Learn:** [FastAPI Bigger Applications Project Layout](https://fastapi.tiangolo.com/tutorial/bigger-applications/).
*   **Deliverables:** Folders `/app`, `/app/api`, `/app/schemas`, `/app/services`, `/app/repositories`, `/app/db`.
*   **Potential Risks:** Circular imports due to poor scaffolding configurations.
*   **Acceptance Criteria:** Command `uvicorn app.main:app` successfully runs an empty API server on port 8000 without warnings.
*   **Collaboration Required:** Internal alignment only.

### Day 5: Milestone 1 Review: Scope Signoff and ADR Locking
*   **Objective:** Review scope, check constraints, and lock requirements for Milestone 1 (M1).
*   **Expected Output:** Signed milestone agreement and updated project board backlog.
*   **Dependencies:** Days 1-4 deliverables completed.
*   **Skills Required:** Project management, task planning.
*   **Resources to Learn:** [Agile sprint retrospective formats](https://www.atlassian.com/agile/scrum/retrospectives).
*   **Deliverables:** Milestone 1 evidence log.
*   **Potential Risks:** Undetected scope creep stretching the 6-week timeframe.
*   **Acceptance Criteria:** Product lead approves scope notes and decision log.
*   **Collaboration Required:** All Assignment owners (A, B, C, D) and Product Lead must sign off.

---

## Week 2: Authentication & Ingestion Baseline Prototype

### Day 6: Device Authentication System Implementation
*   **Objective:** Build token validation logic to secure the device ingestion path.
*   **Expected Output:** Core security helper verifying API keys from `X-Device-Token` header.
*   **Dependencies:** Core folder scaffolding.
*   **Skills Required:** Symmetric encryption, hashing algorithms, API design.
*   **Resources to Learn:** [FastAPI Security Helpers](https://fastapi.tiangolo.com/tutorial/security/).
*   **Deliverables:** `app/core/security.py` containing token generation and hash verification helper scripts.
*   **Potential Risks:** Hardcoding secrets in git repo histories.
*   **Acceptance Criteria:** Passing security test checks showing valid tokens bypass routing but invalid tokens fail.
*   **Collaboration Required:** Alignment with Team B to coordinate how tokens are stored in the device's flash memory.

### Day 7: Mobile Authentication Setup
*   **Objective:** Set up standard user OAuth2 token exchanges using JWTs.
*   **Expected Output:** Endpoint router generating JWT access tokens from email/password verify.
*   **Dependencies:** Day 6 security helpers.
*   **Skills Required:** JSON Web Tokens (JWT), password hashing (`passlib`, `bcrypt`).
*   **Resources to Learn:** [OAuth2 with Password and Bearer](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/).
*   **Deliverables:** `/app/api/v1/endpoints/auth.py` registering endpoints and `/app/schemas/auth.py` validation rules.
*   **Potential Risks:** Using weak signing keys or insecure validation mechanisms.
*   **Acceptance Criteria:** Postman requests to `/api/v1/auth/login` successfully yield JWT strings expiring in 60 minutes.
*   **Collaboration Required:** Assignment D (Mobile App) team to align JWT handling protocols.

### Day 8: Ingestion Endpoint Prototype Creation
*   **Objective:** Program the initial ingestion route `/api/v1/telemetry`.
*   **Expected Output:** API handler receiving incoming JSON body and print logging contents.
*   **Dependencies:** Day 3 schema lock, Day 6 device auth.
*   **Skills Required:** FastAPI router methods, request body parsing.
*   **Resources to Learn:** [FastAPI path parameters and body payloads](https://fastapi.tiangolo.com/tutorial/body/).
*   **Deliverables:** `/app/api/v1/endpoints/telemetry.py` containing the POST endpoint.
*   **Potential Risks:** Processing payloads with incorrect Content-Types.
*   **Acceptance Criteria:** An HTTP client sending valid telemetry payload receives HTTP 202 Accepted.
*   **Collaboration Required:** Internal developer tests.

### Day 9: Payload Validation Logic Mapping
*   **Objective:** Bind the telemetry Pydantic schemas to the ingestion route, validating inputs at runtime.
*   **Expected Output:** Schema filters checking payload parameters (timestamps, float boundaries, array lengths).
*   **Dependencies:** Day 8 endpoint prototype.
*   **Skills Required:** Pydantic validation decorators, constraint bindings.
*   **Resources to Learn:** [Pydantic V2 validation types](https://docs.pydantic.dev/latest/concepts/validators/).
*   **Deliverables:** `/app/schemas/telemetry.py` mapping structure and properties.
*   **Potential Risks:** Over-validating values causing normal sensor fluctuations to get rejected.
*   **Acceptance Criteria:** Telemetry posts containing missing fields yield clear validation error structures (HTTP 422).
*   **Collaboration Required:** Review with Team B to ensure firmware limits match validation thresholds.

### Day 10: Milestone 2 Review: Local Mock Ingestion Demo
*   **Objective:** Present a working demonstration of Milestone 2 (M2) core ingestion function.
*   **Expected Output:** Terminal demonstrations showcasing telemetry ingest pipelines.
*   **Dependencies:** Days 6-9 deliverables.
*   **Skills Required:** Technical presentation, testing pipelines.
*   **Resources to Learn:** [Designing software demos](https://www.ycombinator.com/library/4q-how-to-demo).
*   **Deliverables:** Ingestion prototype demonstration logs.
*   **Potential Risks:** Network configuration errors during demonstration.
*   **Acceptance Criteria:** Demonstration runs without errors, showing a mock payload successfully authenticated and validated.
*   **Collaboration Required:** Relevant owners (B, D) and Product Lead must attend.

---

## Week 3: Firestore/PostgreSQL Database Schema & Caching Layer

### Day 11: Database Registry & CRUD Scaffolding
*   **Objective:** Setup database clients and base CRUD repositories.
*   **Expected Output:** Singleton database connections initialized on server startup.
*   **Dependencies:** Cloud configuration parameters.
*   **Skills Required:** Firebase SDK configuration, NoSQL clients.
*   **Resources to Learn:** [Firebase Admin SDK for Python setup](https://firebase.google.com/docs/admin/setup).
*   **Deliverables:** `/app/db/firestore.py` database connection file and `/app/repositories/base.py` CRUD interfaces.
*   **Potential Risks:** Connection timeouts or improper client initializations.
*   **Acceptance Criteria:** The application connects to database successfully without throwing credential errors.
*   **Collaboration Required:** Product Lead to provision cloud credentials.

### Day 12: Time-Series Telemetry Persistance Implementation
*   **Objective:** Write incoming telemetry data points into the telemetry storage.
*   **Expected Output:** Telemetry payloads written to database collections.
*   **Dependencies:** Day 11 database setup, Day 9 validation logic.
*   **Skills Required:** Database writes, document layouts.
*   **Resources to Learn:** [Firestore write operations](https://firebase.google.com/docs/firestore/manage-data/add-data).
*   **Deliverables:** `/app/repositories/telemetry.py` repository class.
*   **Potential Risks:** High storage utilization due to unnecessary fields (e.g., redundant text strings).
*   **Acceptance Criteria:** Database records are created containing exact timestamp mappings and sensor values.
*   **Collaboration Required:** Internal tests.

### Day 13: Caching Latest Status
*   **Objective:** Implement latest status write-duplication caching pattern.
*   **Expected Output:** Ingestion pipeline updates single status document upon writing time-series log.
*   **Dependencies:** Day 12 telemetry repository.
*   **Skills Required:** Cache strategy design, database transaction executions.
*   **Resources to Learn:** [Firestore Transactions and Batched Writes](https://firebase.google.com/docs/firestore/manage-data/transactions).
*   **Deliverables:** Add latest status updating functions inside `/app/repositories/device.py`.
*   **Potential Risks:** Race conditions causing latest status to desynchronize from time-series logs.
*   **Acceptance Criteria:** Every telemetry write results in updating `/devices/{id}/latest/status` document with current state.
*   **Collaboration Required:** Align details with Mobile App Team D.

### Day 14: Historical Queries & Pagination
*   **Objective:** Create historical data fetching routines with limits and ordering filters.
*   **Expected Output:** Retrieve paginated arrays of telemetry points sorted by timestamp.
*   **Dependencies:** Day 12 telemetry database storage.
*   **Skills Required:** NoSQL query construction, date filters.
*   **Resources to Learn:** [Querying data in Firestore](https://firebase.google.com/docs/firestore/query-data/queries).
*   **Deliverables:** Query filters in `/app/repositories/telemetry.py`.
*   **Potential Risks:** High latency queries if indexes are missing.
*   **Acceptance Criteria:** Running the queries returns data points ordered by timestamp within requested window.
*   **Collaboration Required:** Mobile Team D to design chart API pagination parameters.

### Day 15: Database Access Rules and Indexing Rules Setup
*   **Objective:** Secure collections and build database indexes for ordering constraints.
*   **Expected Output:** Security configuration rules deployed to cloud console.
*   **Dependencies:** Database collections setup.
*   **Skills Required:** Database access control, index provision.
*   **Resources to Learn:** [Firestore Security Rules syntax](https://firebase.google.com/docs/firestore/security/get-started).
*   **Deliverables:** `firestore.rules` file containing security specifications.
*   **Potential Risks:** Over-restrictive database rules blocking legitimate requests.
*   **Acceptance Criteria:** Unauthenticated reads to user data are rejected; search queries requiring compound sort run without index errors.
*   **Collaboration Required:** Security lead review if applicable.

---

## Week 4: Alert Rules Engine & Notifications Hooking

### Day 16: Alert Engine Core Logic Setup
*   **Objective:** Scaffold the rules evaluator processing data during ingestion.
*   **Expected Output:** Execution pipeline routing telemetry data into checking steps.
*   **Dependencies:** Week 3 database storage.
*   **Skills Required:** Event processing systems, modular programming.
*   **Resources to Learn:** [Designing rules engines](https://martinfowler.com/articles/rules-engines.html).
*   **Deliverables:** `/app/alert_engine/processor.py` base script.
*   **Potential Risks:** Lag in ingestion pipelines if alert analysis is slow.
*   **Acceptance Criteria:** Processing test payload invokes the check routines.
*   **Collaboration Required:** Internal tests.

### Day 17: Rule Boundaries Implementation
*   **Objective:** Program logic checks (high heat threshold, extreme moisture limits, error flags).
*   **Expected Output:** Functions evaluating telemetry values and flagging true/false states.
*   **Dependencies:** Day 16 engine core.
*   **Skills Required:** Conditional evaluations, domain math.
*   **Resources to Learn:** [Composting guidelines for temperature and moisture limits](https://cwmi.css.cornell.edu/composting.htm).
*   **Deliverables:** `/app/alert_engine/rules.py` file with bounds evaluations.
*   **Potential Risks:** High rate of false positives on noisy inputs.
*   **Acceptance Criteria:** Readings with moisture < 20% or temp > 65°C successfully trigger flag changes.
*   **Collaboration Required:** Check thresholds with Assignment A (Sensors/Calibration) team.

### Day 18: Heartbeat/Offline Monitor Setup
*   **Objective:** Create background scheduler to flag devices that stop reporting.
*   **Expected Output:** A routine running checks on the last seen timestamp of all devices.
*   **Dependencies:** Day 17 rules engine.
*   **Skills Required:** Background task execution, cron jobs.
*   **Resources to Learn:** [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/).
*   **Deliverables:** Heartbeat checking schedule in `/app/alert_engine/processor.py`.
*   **Potential Risks:** Server resources saturated by constant scanning loops.
*   **Acceptance Criteria:** Setting device timestamp back 20 minutes triggers an offline status and alerts.
*   **Collaboration Required:** Internal developers testing.

### Day 19: Firebase Cloud Messaging Integration
*   **Objective:** Set up push notifications to forward alerts to mobile devices.
*   **Expected Output:** FCM client connection dispatching push envelopes.
*   **Dependencies:** Day 17 rules engine, Firebase project config.
*   **Skills Required:** Push notification APIs, FCM integration.
*   **Resources to Learn:** [FCM Python SDK documentation](https://firebase.google.com/docs/cloud-messaging/send-message).
*   **Deliverables:** `/app/services/notification.py` integrations.
*   **Potential Risks:** Network blockages or device token invalidations.
*   **Acceptance Criteria:** Calling dispatch helper yields success message from Google servers.
*   **Collaboration Required:** Mobile Team D to register mobile device registration tokens.

### Day 20: Milestone 3 Review: Integration Schema Freeze
*   **Objective:** Freeze data schemas, status names, and routes for Milestone 3 (M3).
*   **Expected Output:** Complete API contracts frozen and published.
*   **Dependencies:** Days 11-19 completed.
*   **Skills Required:** Quality assurance, API freeze checkpoints.
*   **Resources to Learn:** [API Versioning best practices](https://restfulapi.net/versioning/).
*   **Deliverables:** Versioned API schema contract log.
*   **Potential Risks:** Retrospective schema changes breaking build files.
*   **Acceptance Criteria:** Developers B, C, D sign agreement on frozen variables and routes.
*   **Collaboration Required:** All Assignment Owners (A, B, C, D) must attend.

---

## Week 5: Logging, System Monitoring & Mock Simulator

### Day 21: Logging and Request Tracing Setup
*   **Objective:** Create standardized logs for server actions and error states.
*   **Expected Output:** Middleware tagging incoming API calls and writing structured logs.
*   **Dependencies:** Core configuration utilities.
*   **Skills Required:** Log formats, tracing, HTTP middlewares.
*   **Resources to Learn:** [Python logging module](https://docs.python.org/3/library/logging.html).
*   **Deliverables:** `/app/utils/logger.py` format configuration.
*   **Potential Risks:** Verbose logs filling server disk spaces.
*   **Acceptance Criteria:** Every HTTP call yields formatted logger output displaying elapsed time.
*   **Collaboration Required:** Internal tests.

### Day 22: Analytics and Metric Counters
*   **Objective:** Collect system performance metrics (number of successful uploads, alert frequencies).
*   **Expected Output:** Endpoint returning system metrics and counters.
*   **Dependencies:** Week 3 database storage.
*   **Skills Required:** Aggregate queries, dashboard metrics.
*   **Resources to Learn:** [REST API analytics design](https://blog.ndepend.com/rest-api-analytics/).
*   **Deliverables:** `/api/v1/endpoints/alerts.py` summary charts endpoints.
*   **Potential Risks:** High database overhead for tracking metrics.
*   **Acceptance Criteria:** Calling metric endpoint returns current upload counts and alert logs.
*   **Collaboration Required:** Coordinate with Mobile App Team D.

### Day 23: Complete Mock Device Simulator Script
*   **Objective:** Write simulator script generating realistic sensor data curves.
*   **Expected Output:** Python simulator utility pushing telemetry updates via HTTP POST requests.
*   **Dependencies:** Ingestion routes deployed.
*   **Skills Required:** Telemetry simulation, HTTP client tools (`requests`, `httpx`).
*   **Resources to Learn:** [Building HTTP mock clients in Python](https://www.python-httpx.org/).
*   **Deliverables:** `/simulator/run_simulation.py` script.
*   **Potential Risks:** Simulator flooding server if loop intervals fail.
*   **Acceptance Criteria:** Simulator script runs, logging successful 202 responses from the ingestion endpoint.
*   **Collaboration Required:** Deliver script to Mobile Team D to unblock client tests.

### Day 24: Integration Test Suite Execution
*   **Objective:** Run tests validating endpoints, database transactions, and rules evaluations.
*   **Expected Output:** Pytest output showing all test cases successfully pass.
*   **Dependencies:** All core modules deployed.
*   **Skills Required:** Unit testing, mock techniques.
*   **Resources to Learn:** [Testing FastAPI applications with Pytest](https://fastapi.tiangolo.com/advanced/testing-database/).
*   **Deliverables:** `/tests/` collection scripts.
*   **Potential Risks:** Fragile tests generating false failures.
*   **Acceptance Criteria:** Execution of `pytest` displays success code across all tests.
*   **Collaboration Required:** Review test coverage with Quality Lead.

### Day 25: Milestone 4 Review: Security Auditing & Bench Testing
*   **Objective:** Review security and execute bench testing validation for Milestone 4 (M4).
*   **Expected Output:** Vulnerability logs and verified proof-of-concept tests.
*   **Dependencies:** Week 5 deliverables.
*   **Skills Required:** Security audit, hardware-in-the-loop validation.
*   **Resources to Learn:** [OWASP IoT Top 10 Security checks](https://owasp.org/www-pdf-archive/OWASP-IoT-Top-10-Template-2018.pdf).
*   **Deliverables:** Milestone 4 test report.
*   **Potential Risks:** Security issues requiring redesign of authorization paths.
*   **Acceptance Criteria:** Zero critical issues, authentication rules pass validation.
*   **Collaboration Required:** Assignment B (Firmware) and A (Sensors) leads must participate.

---

## Week 6: Full End-to-End Integration, Handover & Demo Readiness

### Day 26: Cross-Team Integration Testing
*   **Objective:** Perform tests verifying hardware-to-cloud-to-mobile communications.
*   **Expected Output:** Live data uploads from physical ESP32 boards displaying on the mobile app.
*   **Dependencies:** Milestone 3 freezes, Mobile app integration.
*   **Skills Required:** End-to-end integration testing, wireless networks debugging.
*   **Resources to Learn:** [Cross-platform end-to-end testing systems](https://martinfowler.com/articles/practical-test-pyramid.html).
*   **Deliverables:** Integration verification log.
*   **Potential Risks:** High latency or message loss on physical wireless networks.
*   **Acceptance Criteria:** Physical device status change updates mobile screen in under 5 seconds.
*   **Collaboration Required:** Joint session with Team B (Firmware) and Team D (Mobile App).

### Day 27: Manual Validation Endpoint Verification
*   **Objective:** Verify manual compost validation flows.
*   **Expected Output:** Validation command from mobile transitions status inside database and synced back to device config.
*   **Dependencies:** Day 26 integration.
*   **Skills Required:** Transaction systems, configuration synchronization.
*   **Resources to Learn:** [Design of commands and events in REST APIs](https://microservices.io/patterns/data/cqrs.html).
*   **Deliverables:** Integration checks for `/validate` route.
*   **Potential Risks:** Race conditions during reset transitions.
*   **Acceptance Criteria:** Triggering validation transitions state to `ready_confirmed` and changes status on physical device during next sync.
*   **Collaboration Required:** Teams B and D.

### Day 28: Deployment Packaging
*   **Objective:** Package application inside Docker containers.
*   **Expected Output:** Built docker image running FastAPI service locally.
*   **Dependencies:** Full codebase complete.
*   **Skills Required:** Docker builds, deployment environments setup.
*   **Resources to Learn:** [Dockerizing FastAPI applications](https://fastapi.tiangolo.com/deployment/docker/).
*   **Deliverables:** `/deploy/Dockerfile` and `deploy/docker-compose.yml`.
*   **Potential Risks:** Oversized Docker images slow to deploy.
*   **Acceptance Criteria:** Running `docker-compose up` runs the app and database emulator.
*   **Collaboration Required:** DevOps engineer alignment.

### Day 29: Handover Documentation Compilation
*   **Objective:** Assemble onboarding guides, API docs, and environment instructions.
*   **Expected Output:** Clean, versioned documentation repository.
*   **Dependencies:** Deployed project structures.
*   **Skills Required:** Technical writing, markdown layout.
*   **Resources to Learn:** [How to write a developer-friendly README](https://www.makeareadme.com/).
*   **Deliverables:** Final root `README.md` and API specifications PDF.
*   **Potential Risks:** Outdated specs mismatching current code.
*   **Acceptance Criteria:** A new developer can run the app using README steps in under 15 minutes.
*   **Collaboration Required:** Review documents with all team members.

### Day 30: Milestone 5 Review: Final Presentation & Code Freeze
*   **Objective:** Final presentation and code freeze for Milestone 5 (M5).
*   **Expected Output:** Live demonstration to EcoZindagi leads and repository code tag.
*   **Dependencies:** Days 26-29 completed.
*   **Skills Required:** Public speaking, git branch tag.
*   **Resources to Learn:** [Delivering successful software presentations](https://www.atlassian.com/blog/inside-atlassian/master-the-art-of-the-presentation).
*   **Deliverables:** Tagged release (e.g. `v1.0.0-mvp`) and slide deck.
*   **Potential Risks:** Technical hitches during live demo.
*   **Acceptance Criteria:** Product Lead accepts project handover.
*   **Collaboration Required:** Entire internship cohort (A, B, C, D) and EcoZindagi panel.

---

## 3. Gantt-Style Execution Table

| Week | Phase / Task Area | Mon (Day 1/6/11/16/21/26) | Tue (Day 2/7/12/17/22/27) | Wed (Day 3/8/13/18/23/28) | Thu (Day 4/9/14/19/24/29) | Fri (Day 5/10/15/20/25/30) | Milestones / Checkpoints |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **W1** | **Locking & Setup** | Project setup & env | ADR comparative analysis | Ingestion schema drafts | Scaffold clean architecture | Scope & ADR lock | **M1: Requirements Locked** |
| **W2** | **Ingestion Auth** | Device Auth (HMAC) | User Auth (JWT setup) | Telemetry route baseline | Schema Pydantic rules | Mock Ingestion Demo | **M2: Ingestion Prototype** |
| **W3** | **Data & Storage** | DB connection pool | Telemetry persistence | Latest Status cache | Query logic & page | Access rules & indexes | **Database Configured** |
| **W4** | **Rules & Alerts** | Engine core setup | Hazard checks rules | Heartbeat monitors | FCM Cloud messaging | Schema freeze meeting | **M3: Integration-Ready** |
| **W5** | **Logs & Mocking** | Mid-wear log traces | Metrics endpoints | Complete Mock Sim | Pytest execution | Security auditing | **M4: Tested & Documented** |
| **W6** | **E2E & Handover** | Hardware/Cloud/App test| Validate command checks | Deploy (Docker setup) | Handover docs compile | Final presentation demo | **M5: Demo-Ready (Release)** |
