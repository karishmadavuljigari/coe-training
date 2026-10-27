# Overview

> Audience: FDE trainees, developers, and reviewers working on this service.

## Who this is for (audience).

This service is a starting point for FDE trainees to learn how to build, test, and maintain a secure API service.

## What the service does in two sentences.

The service provides health and readiness endpoints to report whether the application is alive and whether its declared dependencies are ready. It also provides a `/ask` endpoint that accepts a question and currently returns a safe placeholder response until source retrieval and answer generation are implemented.

## Who uses it and what they can do.

Developers and trainees can use the health endpoints to check service status and use the `/ask` endpoint to submit a question. The current version does not yet retrieve knowledge sources or generate source-grounded answers.

## Main limits and known issues.

The readiness check does not yet verify external dependencies, and the answering service does not yet retrieve sources or call a model provider. These capabilities are planned for later training tasks.
