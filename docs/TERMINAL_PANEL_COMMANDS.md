# Terminal Panel Command Reference

Every command shown in `assets/terminal_panels/` is repeated here as copyable Markdown text. Values such as `PACKAGE_NAME`, `TARGET`, and `RESOURCE_ID` are explicit placeholders; the panels do not claim a real project result.

## Install

### npm Package Install

Asset: `assets/terminal_panels/install/terminal_npm_package_install.svg`

```bash
npm install PACKAGE_NAME
```

### Python Environment Setup

Asset: `assets/terminal_panels/install/terminal_python_environment_setup.svg`

```bash
python -m venv .venv
```

### Container Image Pull

Asset: `assets/terminal_panels/install/terminal_container_image_pull.svg`

```bash
docker pull IMAGE_NAME:TAG
```

### Binary Archive Install

Asset: `assets/terminal_panels/install/terminal_binary_archive_install.svg`

```bash
tool install ./PACKAGE_ARCHIVE
```

### System Package Install

Asset: `assets/terminal_panels/install/terminal_system_package_install.svg`

```bash
pkg-manager install PACKAGE_NAME
```

### Source Checkout Install

Asset: `assets/terminal_panels/install/terminal_source_checkout_install.svg`

```bash
git clone REPOSITORY_URL
```

### Workspace Bootstrap

Asset: `assets/terminal_panels/install/terminal_workspace_bootstrap.svg`

```bash
tool bootstrap --workspace .
```

## Commands

### Cli Help Overview

Asset: `assets/terminal_panels/commands/terminal_cli_help_overview.svg`

```bash
tool --help
```

### Configuration Inspect

Asset: `assets/terminal_panels/commands/terminal_configuration_inspect.svg`

```bash
tool config show
```

### Asset Generation

Asset: `assets/terminal_panels/commands/terminal_asset_generation.svg`

```bash
tool generate --input INPUT_PATH
```

### Project Validation

Asset: `assets/terminal_panels/commands/terminal_project_validation.svg`

```bash
tool validate --all
```

### Schema Migration

Asset: `assets/terminal_panels/commands/terminal_schema_migration.svg`

```bash
tool migrate --plan
```

### Artifact Export

Asset: `assets/terminal_panels/commands/terminal_artifact_export.svg`

```bash
tool export --format FORMAT
```

### Preview Server

Asset: `assets/terminal_panels/commands/terminal_preview_server.svg`

```bash
tool preview --host 127.0.0.1
```

## Build

### Source Compile

Asset: `assets/terminal_panels/build/terminal_source_compile.svg`

```bash
tool compile --target TARGET
```

### Frontend Bundle

Asset: `assets/terminal_panels/build/terminal_frontend_bundle.svg`

```bash
tool bundle --mode production
```

### Package Archive

Asset: `assets/terminal_panels/build/terminal_package_archive.svg`

```bash
tool package --output OUTPUT_DIR
```

### Artifact Manifest

Asset: `assets/terminal_panels/build/terminal_artifact_manifest.svg`

```bash
tool artifact manifest
```

### Cache Restore

Asset: `assets/terminal_panels/build/terminal_cache_restore.svg`

```bash
tool cache restore CACHE_KEY
```

### Multi Stage Build

Asset: `assets/terminal_panels/build/terminal_multi_stage_build.svg`

```bash
tool build --stage final
```

## Tests

### Unit Suite

Asset: `assets/terminal_panels/tests/terminal_unit_suite.svg`

```bash
tool test --unit
```

### Integration Suite

Asset: `assets/terminal_panels/tests/terminal_integration_suite.svg`

```bash
tool test --integration
```

### End To End Suite

Asset: `assets/terminal_panels/tests/terminal_end_to_end_suite.svg`

```bash
tool test --e2e
```

### Accessibility Audit

Asset: `assets/terminal_panels/tests/terminal_accessibility_audit.svg`

```bash
tool audit --accessibility
```

### Performance Check

Asset: `assets/terminal_panels/tests/terminal_performance_check.svg`

```bash
tool check --performance
```

### Platform Matrix

Asset: `assets/terminal_panels/tests/terminal_platform_matrix.svg`

```bash
tool test --matrix
```

## Deploy

### Preview Deploy

Asset: `assets/terminal_panels/deploy/terminal_preview_deploy.svg`

```bash
tool deploy --preview
```

### Staging Deploy

Asset: `assets/terminal_panels/deploy/terminal_staging_deploy.svg`

```bash
tool deploy --environment staging
```

### Production Plan

Asset: `assets/terminal_panels/deploy/terminal_production_plan.svg`

```bash
tool deploy --plan production
```

### Rollback Release

Asset: `assets/terminal_panels/deploy/terminal_rollback_release.svg`

```bash
tool rollback RELEASE_ID
```

### Static Site Publish

Asset: `assets/terminal_panels/deploy/terminal_static_site_publish.svg`

```bash
tool publish --static OUTPUT_DIR
```

### Container Rollout

Asset: `assets/terminal_panels/deploy/terminal_container_rollout.svg`

```bash
tool deploy --container IMAGE_TAG
```

### Infrastructure Apply

Asset: `assets/terminal_panels/deploy/terminal_infrastructure_apply.svg`

```bash
tool infra apply PLAN_FILE
```

## Logs

### Structured Events

Asset: `assets/terminal_panels/logs/terminal_structured_events.svg`

```bash
tool logs --format json
```

### Trace Span

Asset: `assets/terminal_panels/logs/terminal_trace_span.svg`

```bash
tool trace TRACE_ID
```

### Queue Consumer

Asset: `assets/terminal_panels/logs/terminal_queue_consumer.svg`

```bash
tool queue inspect QUEUE_NAME
```

### Request Lifecycle

Asset: `assets/terminal_panels/logs/terminal_request_lifecycle.svg`

```bash
tool request inspect REQUEST_ID
```

### Background Job

Asset: `assets/terminal_panels/logs/terminal_background_job.svg`

```bash
tool job inspect JOB_ID
```

### Health Observability

Asset: `assets/terminal_panels/logs/terminal_health_observability.svg`

```bash
tool health --verbose
```

## Errors

### Validation Failure

Asset: `assets/terminal_panels/errors/terminal_validation_failure.svg`

```bash
tool validate CONFIG_PATH
```

### Configuration Missing

Asset: `assets/terminal_panels/errors/terminal_configuration_missing.svg`

```bash
tool config require SETTING_NAME
```

### Permission Denied

Asset: `assets/terminal_panels/errors/terminal_permission_denied.svg`

```bash
tool access check RESOURCE_ID
```

### Network Timeout

Asset: `assets/terminal_panels/errors/terminal_network_timeout.svg`

```bash
tool network retry ENDPOINT_URL
```

### Dependency Conflict

Asset: `assets/terminal_panels/errors/terminal_dependency_conflict.svg`

```bash
tool dependencies resolve
```

### Recovery Steps

Asset: `assets/terminal_panels/errors/terminal_recovery_steps.svg`

```bash
tool recover --dry-run
```


