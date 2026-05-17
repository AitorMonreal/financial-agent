# Satellite Portfolio AI Engine - Implementation Roadmap

This roadmap defines the sequential phases for building the autonomous financial multi-agent system.

## Phase 0: Project Specification (Completed)
*   Define technical specifications (`specs.md`) covering architectural decisions and discarded alternatives.
*   Establish the project roadmap (`roadmap.md`).

## Phase 1: Infrastructure and Deterministic Bridges
*   **Focus:** Secure data ingestion and typing without AI logic.
*   **Deliverables:**
    *   Secure credential vault setup (`.env`).
    *   Interactive Brokers integration via `py-ibkr`.
    *   Market data integration via `yfinance` and FMP.
    *   Comprehensive `unittest` suite with mocked API responses.

## Phase 2: The Mathematical Core
*   **Focus:** Deterministic financial algorithms.
*   **Deliverables:**
    *   Python-based DCF and Monte Carlo simulation models.
    *   Commodity macro-regime mapping functions.
    *   Strict TDD validation to ensure computational accuracy and edge-case handling.

## Phase 3: The Pydantic AI Agent Layer
*   **Focus:** Safe LLM integration.
*   **Deliverables:**
    *   Definition of strict Pydantic output schemas (`ThesisExtraction`, `SummaryReport`).
    *   Implementation of the Analyst, Critic, and Controller agents.
    *   Mocking framework via dependency injection for testing agent logic.

## Phase 4: LangGraph Orchestration
*   **Focus:** Multi-agent state machine.
*   **Deliverables:**
    *   Definition of the strict `AgentState` object.
    *   Construction of the LangGraph nodes (Router, Analysts, Critic) and conditional edges (Feedback loops, Approvals).

## Phase 5: Automation and Synthesis
*   **Focus:** UI and scheduling.
*   **Deliverables:**
    *   Responsive Jinja2 HTML email template.
    *   SMTP delivery logic via Gmail App Password.
    *   Final `main.py` orchestrator script prepared for cron execution.
