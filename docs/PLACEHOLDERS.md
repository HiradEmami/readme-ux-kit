# Placeholders

Use uppercase snake-case placeholders so generated and copied Markdown can be checked reliably. Placeholders are intentionally loud: if a user pastes a template and forgets to replace one, it should be obvious during review.

## Rules

- Use `UPPERCASE_SNAKE_CASE`.
- Keep placeholders factual and replaceable.
- Prefer one precise placeholder over a sentence fragment.
- Put placeholders in code spans when they appear inside prose or tables.
- Do not use angle placeholders such as `<project name>` in stable templates.
- Remove sections whose placeholders cannot be filled honestly.

## Core Project Placeholders

| Placeholder | Meaning |
| --- | --- |
| `PROJECT_NAME` | Public project name. |
| `PACKAGE_NAME` | Package, binary, image, or module name. |
| `SERVICE_NAME` | Service name when a backend or internal system has a service boundary. |
| `TARGET_USER` | Primary reader or user segment. |
| `PRIMARY_OUTCOME` | Main outcome the project helps readers achieve. |
| `PRIMARY_DOMAIN` | Product, data, research, or operational domain. |
| `PRIMARY_PROBLEM` | Problem the package or project solves. |
| `COMMON_PAIN_POINT` | Pain point avoided by the project. |
| `COMMON_WORKAROUND` | Existing workaround the project replaces. |
| `SCALING_OR_MAINTENANCE_ISSUE` | Reason the old approach breaks down. |
| `PACKAGE_ECOSYSTEM` | npm, PyPI, Docker, GitHub Action, or another distribution ecosystem. |
| `LICENSE` | License identifier or link target. |

## Repository And Link Placeholders

| Placeholder | Meaning |
| --- | --- |
| `OWNER` | Repository owner or organization. |
| `REPO` | Repository name. |
| `DOCS_URL` | Documentation URL. |
| `EXAMPLES_URL` | Example gallery, examples folder, or demo URL. |
| `ISSUES_URL` | Issue tracker URL. |
| `SUPPORT_URL` | Support, discussion, or help URL. |
| `SECURITY_CONTACT` | Private vulnerability report path. |
| `CONTRIBUTING_URL` | Contribution guide URL or relative path. |
| `FUNDING_URL` | Sponsorship, funding, or sustainability URL. |
| `MAINTAINER_HANDLE` | GitHub handle or team alias responsible for maintenance. |
| `STATUS_URL` | Public status page or internal status dashboard. |
| `STAGING_URL` | Staging environment URL. |
| `PRODUCTION_URL` | Production environment URL. |

## Command Placeholders

| Placeholder | Meaning |
| --- | --- |
| `INSTALL_COMMAND` | Primary install command. |
| `RUN_COMMAND` | Primary local run command. |
| `TEST_COMMAND` | Required test command. |
| `LINT_COMMAND` | Lint or static-analysis command. |
| `BUILD_COMMAND` | Build command. |
| `DEPLOY_COMMAND` | Deployment command. |
| `START_DEPENDENCIES_COMMAND` | Local dependency startup command. |
| `UNIT_TEST_COMMAND` | Unit test command. |
| `INTEGRATION_TEST_COMMAND` | Integration test command. |

## Technical Placeholders

| Placeholder | Meaning |
| --- | --- |
| `API_BASE_URL` | Base URL for API examples. |
| `API_TOKEN` | API token or secret name used in examples. |
| `PRIMARY_API` | Main API or exported surface. |
| `CONFIG_FILE` | Main configuration file path. |
| `DATABASE_URL` | Database connection string. |
| `QUEUE_URL` | Queue or broker connection string. |
| `DATABASE_NAME` | Database product or logical database name. |
| `QUEUE_NAME` | Queue or broker product name. |
| `LANGUAGE_FRAMEWORK` | Runtime language and framework. |
| `OBSERVABILITY_STACK` | Logging, metrics, traces, and alerting stack. |
| `NODE_VERSION` | Supported Node.js version. |
| `PYTHON_VERSION` | Supported Python version. |
| `BROWSER_SUPPORT` | Browser support statement. |
| `PROJECT_ENV` | Runtime environment variable. |
| `PROJECT_LOG_LEVEL` | Logging level variable. |
| `PROJECT_OUTPUT_DIR` | Output directory variable. |
| `LOG_LEVEL` | Log verbosity variable. |

## Operations And Release Placeholders

| Placeholder | Meaning |
| --- | --- |
| `BUSINESS_CAPABILITY` | Capability owned by a service. |
| `CLIENT_SYSTEMS` | Clients, services, or systems consuming an API. |
| `PRIMARY_DATA` | Data owned or processed by a service. |
| `STORAGE_LAYER` | Storage layer used by the project. |
| `CORE_RESPONSIBILITY` | Core responsibility handled by a service. |
| `RESPONSIBILITY_ONE` | First concrete responsibility. |
| `RESPONSIBILITY_TWO` | Second concrete responsibility. |
| `RESPONSIBILITY_THREE` | Third concrete responsibility. |
| `EXPLICIT_NON_GOAL_ONE` | First explicit non-goal. |
| `EXPLICIT_NON_GOAL_TWO` | Second explicit non-goal. |
| `P95_LATENCY_TARGET` | Latency target for operational docs. |
| `ERROR_RATE_TARGET` | Error-rate target for operational docs. |
| `QUEUE_LAG_TARGET` | Queue lag target for operational docs. |
| `FEATURE_NAME` | Feature or capability name. |
| `VERSION` | Release version. |
| `OLD_VERSION` | Previous version in an upgrade guide. |
| `NEW_VERSION` | Target version in an upgrade guide. |
| `REMOVAL_VERSION` | Version where a deprecated feature is removed. |
| `MODEL_NAME` | Model name in ML or AI templates. |
| `DATASET_VERSION` | Dataset version or frozen snapshot. |
| `TASK_NAME` | Task name for ML or automation templates. |
| `TEAM_NAME` | Team or owner group. |
| `BOUNDARY` | Security, ownership, or system boundary. |

Run `npm run check:placeholders` before publishing template or component updates.
