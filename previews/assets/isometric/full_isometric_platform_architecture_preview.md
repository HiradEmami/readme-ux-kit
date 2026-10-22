# Full Platform Architecture Preview

3D isometric software architecture patterns for hexagonal ports, CQRS splits, saga orchestrators, multi-tenant cells, and modular monoliths.

Generated from `assets/`. Do not edit this page directly; run `npm run generate:previews` after asset changes.

[Back to Isometric](../isometric.md)

## Metadata

- Category: `isometric`
- Group: `platform-architecture`
- Asset count: 15
- Best for: 3D isometric software architecture patterns for hexagonal ports, CQRS splits, saga orchestrators, multi-tenant cells, and modular monoliths.
- Group tags: `architecture`, `isometric`, `system`

## Compact index

Top tags: `3d` (15), `architecture` (15), `isometric` (15), `system` (15), `animated` (9), `motion` (9), `static` (6), `data` (2), `code` (1), `testing` (1)

| Asset | Type | Tags | Preview | Source | Raw |
| --- | --- | --- | --- | --- | --- |
| `isometric_cqrs_command_query_segregation` | Animated | `3d`, `animated`, `architecture`, `code`, `isometric`, `motion`, `system` | [Jump](#isometric-cqrs-command-query-segregation) | [Source](../../../assets/isometric/platform-architecture/isometric_cqrs_command_query_segregation.svg) | [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_cqrs_command_query_segregation.svg) |
| `isometric_durable_execution_workflow_hub` | Animated | `3d`, `animated`, `architecture`, `isometric`, `motion`, `system` | [Jump](#isometric-durable-execution-workflow-hub) | [Source](../../../assets/isometric/platform-architecture/isometric_durable_execution_workflow_hub.svg) | [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_durable_execution_workflow_hub.svg) |
| `isometric_feature_flag_targeting_matrix` | Animated | `3d`, `animated`, `architecture`, `data`, `isometric`, `motion`, `system`, `testing` | [Jump](#isometric-feature-flag-targeting-matrix) | [Source](../../../assets/isometric/platform-architecture/isometric_feature_flag_targeting_matrix.svg) | [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_feature_flag_targeting_matrix.svg) |
| `isometric_hexagonal_ports_adapters` | Static or subtle motion | `3d`, `architecture`, `isometric`, `static`, `system` | [Jump](#isometric-hexagonal-ports-adapters) | [Source](../../../assets/isometric/platform-architecture/isometric_hexagonal_ports_adapters.svg) | [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_hexagonal_ports_adapters.svg) |
| `isometric_idempotent_payment_ledger_pipe` | Animated | `3d`, `animated`, `architecture`, `isometric`, `motion`, `system` | [Jump](#isometric-idempotent-payment-ledger-pipe) | [Source](../../../assets/isometric/platform-architecture/isometric_idempotent_payment_ledger_pipe.svg) | [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_idempotent_payment_ledger_pipe.svg) |
| `isometric_modular_monolith_bounded_contexts` | Static or subtle motion | `3d`, `architecture`, `isometric`, `static`, `system` | [Jump](#isometric-modular-monolith-bounded-contexts) | [Source](../../../assets/isometric/platform-architecture/isometric_modular_monolith_bounded_contexts.svg) | [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_modular_monolith_bounded_contexts.svg) |
| `isometric_multi_region_cell_routing_terraces` | Animated | `3d`, `animated`, `architecture`, `isometric`, `motion`, `system` | [Jump](#isometric-multi-region-cell-routing-terraces) | [Source](../../../assets/isometric/platform-architecture/isometric_multi_region_cell_routing_terraces.svg) | [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_multi_region_cell_routing_terraces.svg) |
| `isometric_multi_tenant_cell_isolation` | Static or subtle motion | `3d`, `architecture`, `isometric`, `static`, `system` | [Jump](#isometric-multi-tenant-cell-isolation) | [Source](../../../assets/isometric/platform-architecture/isometric_multi_tenant_cell_isolation.svg) | [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_multi_tenant_cell_isolation.svg) |
| `isometric_plugin_microkernel_extensibility` | Static or subtle motion | `3d`, `architecture`, `isometric`, `static`, `system` | [Jump](#isometric-plugin-microkernel-extensibility) | [Source](../../../assets/isometric/platform-architecture/isometric_plugin_microkernel_extensibility.svg) | [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_plugin_microkernel_extensibility.svg) |
| `isometric_policy_driven_data_residency_stack` | Animated | `3d`, `animated`, `architecture`, `data`, `infrastructure`, `isometric`, `motion`, `security`, `system` | [Jump](#isometric-policy-driven-data-residency-stack) | [Source](../../../assets/isometric/platform-architecture/isometric_policy_driven_data_residency_stack.svg) | [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_policy_driven_data_residency_stack.svg) |
| `isometric_saga_orchestration_compensator` | Animated | `3d`, `animated`, `architecture`, `isometric`, `motion`, `system` | [Jump](#isometric-saga-orchestration-compensator) | [Source](../../../assets/isometric/platform-architecture/isometric_saga_orchestration_compensator.svg) | [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_saga_orchestration_compensator.svg) |
| `isometric_schema_first_contract_broker` | Animated | `3d`, `animated`, `architecture`, `isometric`, `motion`, `system` | [Jump](#isometric-schema-first-contract-broker) | [Source](../../../assets/isometric/platform-architecture/isometric_schema_first_contract_broker.svg) | [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_schema_first_contract_broker.svg) |
| `isometric_transactional_outbox_relay` | Animated | `3d`, `animated`, `architecture`, `isometric`, `motion`, `system` | [Jump](#isometric-transactional-outbox-relay) | [Source](../../../assets/isometric/platform-architecture/isometric_transactional_outbox_relay.svg) | [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_transactional_outbox_relay.svg) |
| `isometric_usage_metering_aggregation_pipe` | Static or subtle motion | `3d`, `architecture`, `docs`, `isometric`, `static`, `system` | [Jump](#isometric-usage-metering-aggregation-pipe) | [Source](../../../assets/isometric/platform-architecture/isometric_usage_metering_aggregation_pipe.svg) | [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_usage_metering_aggregation_pipe.svg) |
| `isometric_webhook_delivery_retry_ladder` | Static or subtle motion | `3d`, `architecture`, `isometric`, `static`, `system` | [Jump](#isometric-webhook-delivery-retry-ladder) | [Source](../../../assets/isometric/platform-architecture/isometric_webhook_delivery_retry_ladder.svg) | [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_webhook_delivery_retry_ladder.svg) |

## Visual previews

<a id="isometric-cqrs-command-query-segregation"></a>

## isometric_cqrs_command_query_segregation

[![isometric_cqrs_command_query_segregation](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_cqrs_command_query_segregation.svg)](https://github.com/HiradEmami)

### Copy this asset

<details>
<summary>Markdown</summary>

```markdown
[![isometric_cqrs_command_query_segregation](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_cqrs_command_query_segregation.svg)](https://github.com/HiradEmami)
```

</details>

<details>
<summary>HTML</summary>

```html
<a href="https://github.com/HiradEmami">
  <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_cqrs_command_query_segregation.svg" alt="isometric_cqrs_command_query_segregation" />
</a>
```

</details>

### Details

- Type: Animated
- Tags: `3d`, `animated`, `architecture`, `code`, `isometric`, `motion`, `system`
- Anchor: `#isometric-cqrs-command-query-segregation`
- [Source file](../../../assets/isometric/platform-architecture/isometric_cqrs_command_query_segregation.svg)
- [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_cqrs_command_query_segregation.svg)

<a id="isometric-durable-execution-workflow-hub"></a>

## isometric_durable_execution_workflow_hub

[![isometric_durable_execution_workflow_hub](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_durable_execution_workflow_hub.svg)](https://github.com/HiradEmami)

### Copy this asset

<details>
<summary>Markdown</summary>

```markdown
[![isometric_durable_execution_workflow_hub](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_durable_execution_workflow_hub.svg)](https://github.com/HiradEmami)
```

</details>

<details>
<summary>HTML</summary>

```html
<a href="https://github.com/HiradEmami">
  <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_durable_execution_workflow_hub.svg" alt="isometric_durable_execution_workflow_hub" />
</a>
```

</details>

### Details

- Type: Animated
- Tags: `3d`, `animated`, `architecture`, `isometric`, `motion`, `system`
- Anchor: `#isometric-durable-execution-workflow-hub`
- [Source file](../../../assets/isometric/platform-architecture/isometric_durable_execution_workflow_hub.svg)
- [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_durable_execution_workflow_hub.svg)

<a id="isometric-feature-flag-targeting-matrix"></a>

## isometric_feature_flag_targeting_matrix

[![isometric_feature_flag_targeting_matrix](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_feature_flag_targeting_matrix.svg)](https://github.com/HiradEmami)

### Copy this asset

<details>
<summary>Markdown</summary>

```markdown
[![isometric_feature_flag_targeting_matrix](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_feature_flag_targeting_matrix.svg)](https://github.com/HiradEmami)
```

</details>

<details>
<summary>HTML</summary>

```html
<a href="https://github.com/HiradEmami">
  <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_feature_flag_targeting_matrix.svg" alt="isometric_feature_flag_targeting_matrix" />
</a>
```

</details>

### Details

- Type: Animated
- Tags: `3d`, `animated`, `architecture`, `data`, `isometric`, `motion`, `system`, `testing`
- Anchor: `#isometric-feature-flag-targeting-matrix`
- [Source file](../../../assets/isometric/platform-architecture/isometric_feature_flag_targeting_matrix.svg)
- [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_feature_flag_targeting_matrix.svg)

<a id="isometric-hexagonal-ports-adapters"></a>

## isometric_hexagonal_ports_adapters

[![isometric_hexagonal_ports_adapters](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_hexagonal_ports_adapters.svg)](https://github.com/HiradEmami)

### Copy this asset

<details>
<summary>Markdown</summary>

```markdown
[![isometric_hexagonal_ports_adapters](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_hexagonal_ports_adapters.svg)](https://github.com/HiradEmami)
```

</details>

<details>
<summary>HTML</summary>

```html
<a href="https://github.com/HiradEmami">
  <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_hexagonal_ports_adapters.svg" alt="isometric_hexagonal_ports_adapters" />
</a>
```

</details>

### Details

- Type: Static or subtle motion
- Tags: `3d`, `architecture`, `isometric`, `static`, `system`
- Anchor: `#isometric-hexagonal-ports-adapters`
- [Source file](../../../assets/isometric/platform-architecture/isometric_hexagonal_ports_adapters.svg)
- [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_hexagonal_ports_adapters.svg)

<a id="isometric-idempotent-payment-ledger-pipe"></a>

## isometric_idempotent_payment_ledger_pipe

[![isometric_idempotent_payment_ledger_pipe](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_idempotent_payment_ledger_pipe.svg)](https://github.com/HiradEmami)

### Copy this asset

<details>
<summary>Markdown</summary>

```markdown
[![isometric_idempotent_payment_ledger_pipe](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_idempotent_payment_ledger_pipe.svg)](https://github.com/HiradEmami)
```

</details>

<details>
<summary>HTML</summary>

```html
<a href="https://github.com/HiradEmami">
  <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_idempotent_payment_ledger_pipe.svg" alt="isometric_idempotent_payment_ledger_pipe" />
</a>
```

</details>

### Details

- Type: Animated
- Tags: `3d`, `animated`, `architecture`, `isometric`, `motion`, `system`
- Anchor: `#isometric-idempotent-payment-ledger-pipe`
- [Source file](../../../assets/isometric/platform-architecture/isometric_idempotent_payment_ledger_pipe.svg)
- [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_idempotent_payment_ledger_pipe.svg)

<a id="isometric-modular-monolith-bounded-contexts"></a>

## isometric_modular_monolith_bounded_contexts

[![isometric_modular_monolith_bounded_contexts](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_modular_monolith_bounded_contexts.svg)](https://github.com/HiradEmami)

### Copy this asset

<details>
<summary>Markdown</summary>

```markdown
[![isometric_modular_monolith_bounded_contexts](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_modular_monolith_bounded_contexts.svg)](https://github.com/HiradEmami)
```

</details>

<details>
<summary>HTML</summary>

```html
<a href="https://github.com/HiradEmami">
  <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_modular_monolith_bounded_contexts.svg" alt="isometric_modular_monolith_bounded_contexts" />
</a>
```

</details>

### Details

- Type: Static or subtle motion
- Tags: `3d`, `architecture`, `isometric`, `static`, `system`
- Anchor: `#isometric-modular-monolith-bounded-contexts`
- [Source file](../../../assets/isometric/platform-architecture/isometric_modular_monolith_bounded_contexts.svg)
- [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_modular_monolith_bounded_contexts.svg)

<a id="isometric-multi-region-cell-routing-terraces"></a>

## isometric_multi_region_cell_routing_terraces

[![isometric_multi_region_cell_routing_terraces](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_multi_region_cell_routing_terraces.svg)](https://github.com/HiradEmami)

### Copy this asset

<details>
<summary>Markdown</summary>

```markdown
[![isometric_multi_region_cell_routing_terraces](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_multi_region_cell_routing_terraces.svg)](https://github.com/HiradEmami)
```

</details>

<details>
<summary>HTML</summary>

```html
<a href="https://github.com/HiradEmami">
  <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_multi_region_cell_routing_terraces.svg" alt="isometric_multi_region_cell_routing_terraces" />
</a>
```

</details>

### Details

- Type: Animated
- Tags: `3d`, `animated`, `architecture`, `isometric`, `motion`, `system`
- Anchor: `#isometric-multi-region-cell-routing-terraces`
- [Source file](../../../assets/isometric/platform-architecture/isometric_multi_region_cell_routing_terraces.svg)
- [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_multi_region_cell_routing_terraces.svg)

<a id="isometric-multi-tenant-cell-isolation"></a>

## isometric_multi_tenant_cell_isolation

[![isometric_multi_tenant_cell_isolation](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_multi_tenant_cell_isolation.svg)](https://github.com/HiradEmami)

### Copy this asset

<details>
<summary>Markdown</summary>

```markdown
[![isometric_multi_tenant_cell_isolation](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_multi_tenant_cell_isolation.svg)](https://github.com/HiradEmami)
```

</details>

<details>
<summary>HTML</summary>

```html
<a href="https://github.com/HiradEmami">
  <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_multi_tenant_cell_isolation.svg" alt="isometric_multi_tenant_cell_isolation" />
</a>
```

</details>

### Details

- Type: Static or subtle motion
- Tags: `3d`, `architecture`, `isometric`, `static`, `system`
- Anchor: `#isometric-multi-tenant-cell-isolation`
- [Source file](../../../assets/isometric/platform-architecture/isometric_multi_tenant_cell_isolation.svg)
- [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_multi_tenant_cell_isolation.svg)

<a id="isometric-plugin-microkernel-extensibility"></a>

## isometric_plugin_microkernel_extensibility

[![isometric_plugin_microkernel_extensibility](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_plugin_microkernel_extensibility.svg)](https://github.com/HiradEmami)

### Copy this asset

<details>
<summary>Markdown</summary>

```markdown
[![isometric_plugin_microkernel_extensibility](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_plugin_microkernel_extensibility.svg)](https://github.com/HiradEmami)
```

</details>

<details>
<summary>HTML</summary>

```html
<a href="https://github.com/HiradEmami">
  <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_plugin_microkernel_extensibility.svg" alt="isometric_plugin_microkernel_extensibility" />
</a>
```

</details>

### Details

- Type: Static or subtle motion
- Tags: `3d`, `architecture`, `isometric`, `static`, `system`
- Anchor: `#isometric-plugin-microkernel-extensibility`
- [Source file](../../../assets/isometric/platform-architecture/isometric_plugin_microkernel_extensibility.svg)
- [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_plugin_microkernel_extensibility.svg)

<a id="isometric-policy-driven-data-residency-stack"></a>

## isometric_policy_driven_data_residency_stack

[![isometric_policy_driven_data_residency_stack](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_policy_driven_data_residency_stack.svg)](https://github.com/HiradEmami)

### Copy this asset

<details>
<summary>Markdown</summary>

```markdown
[![isometric_policy_driven_data_residency_stack](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_policy_driven_data_residency_stack.svg)](https://github.com/HiradEmami)
```

</details>

<details>
<summary>HTML</summary>

```html
<a href="https://github.com/HiradEmami">
  <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_policy_driven_data_residency_stack.svg" alt="isometric_policy_driven_data_residency_stack" />
</a>
```

</details>

### Details

- Type: Animated
- Tags: `3d`, `animated`, `architecture`, `data`, `infrastructure`, `isometric`, `motion`, `security`, `system`
- Anchor: `#isometric-policy-driven-data-residency-stack`
- [Source file](../../../assets/isometric/platform-architecture/isometric_policy_driven_data_residency_stack.svg)
- [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_policy_driven_data_residency_stack.svg)

<a id="isometric-saga-orchestration-compensator"></a>

## isometric_saga_orchestration_compensator

[![isometric_saga_orchestration_compensator](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_saga_orchestration_compensator.svg)](https://github.com/HiradEmami)

### Copy this asset

<details>
<summary>Markdown</summary>

```markdown
[![isometric_saga_orchestration_compensator](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_saga_orchestration_compensator.svg)](https://github.com/HiradEmami)
```

</details>

<details>
<summary>HTML</summary>

```html
<a href="https://github.com/HiradEmami">
  <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_saga_orchestration_compensator.svg" alt="isometric_saga_orchestration_compensator" />
</a>
```

</details>

### Details

- Type: Animated
- Tags: `3d`, `animated`, `architecture`, `isometric`, `motion`, `system`
- Anchor: `#isometric-saga-orchestration-compensator`
- [Source file](../../../assets/isometric/platform-architecture/isometric_saga_orchestration_compensator.svg)
- [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_saga_orchestration_compensator.svg)

<a id="isometric-schema-first-contract-broker"></a>

## isometric_schema_first_contract_broker

[![isometric_schema_first_contract_broker](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_schema_first_contract_broker.svg)](https://github.com/HiradEmami)

### Copy this asset

<details>
<summary>Markdown</summary>

```markdown
[![isometric_schema_first_contract_broker](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_schema_first_contract_broker.svg)](https://github.com/HiradEmami)
```

</details>

<details>
<summary>HTML</summary>

```html
<a href="https://github.com/HiradEmami">
  <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_schema_first_contract_broker.svg" alt="isometric_schema_first_contract_broker" />
</a>
```

</details>

### Details

- Type: Animated
- Tags: `3d`, `animated`, `architecture`, `isometric`, `motion`, `system`
- Anchor: `#isometric-schema-first-contract-broker`
- [Source file](../../../assets/isometric/platform-architecture/isometric_schema_first_contract_broker.svg)
- [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_schema_first_contract_broker.svg)

<a id="isometric-transactional-outbox-relay"></a>

## isometric_transactional_outbox_relay

[![isometric_transactional_outbox_relay](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_transactional_outbox_relay.svg)](https://github.com/HiradEmami)

### Copy this asset

<details>
<summary>Markdown</summary>

```markdown
[![isometric_transactional_outbox_relay](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_transactional_outbox_relay.svg)](https://github.com/HiradEmami)
```

</details>

<details>
<summary>HTML</summary>

```html
<a href="https://github.com/HiradEmami">
  <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_transactional_outbox_relay.svg" alt="isometric_transactional_outbox_relay" />
</a>
```

</details>

### Details

- Type: Animated
- Tags: `3d`, `animated`, `architecture`, `isometric`, `motion`, `system`
- Anchor: `#isometric-transactional-outbox-relay`
- [Source file](../../../assets/isometric/platform-architecture/isometric_transactional_outbox_relay.svg)
- [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_transactional_outbox_relay.svg)

<a id="isometric-usage-metering-aggregation-pipe"></a>

## isometric_usage_metering_aggregation_pipe

[![isometric_usage_metering_aggregation_pipe](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_usage_metering_aggregation_pipe.svg)](https://github.com/HiradEmami)

### Copy this asset

<details>
<summary>Markdown</summary>

```markdown
[![isometric_usage_metering_aggregation_pipe](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_usage_metering_aggregation_pipe.svg)](https://github.com/HiradEmami)
```

</details>

<details>
<summary>HTML</summary>

```html
<a href="https://github.com/HiradEmami">
  <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_usage_metering_aggregation_pipe.svg" alt="isometric_usage_metering_aggregation_pipe" />
</a>
```

</details>

### Details

- Type: Static or subtle motion
- Tags: `3d`, `architecture`, `docs`, `isometric`, `static`, `system`
- Anchor: `#isometric-usage-metering-aggregation-pipe`
- [Source file](../../../assets/isometric/platform-architecture/isometric_usage_metering_aggregation_pipe.svg)
- [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_usage_metering_aggregation_pipe.svg)

<a id="isometric-webhook-delivery-retry-ladder"></a>

## isometric_webhook_delivery_retry_ladder

[![isometric_webhook_delivery_retry_ladder](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_webhook_delivery_retry_ladder.svg)](https://github.com/HiradEmami)

### Copy this asset

<details>
<summary>Markdown</summary>

```markdown
[![isometric_webhook_delivery_retry_ladder](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_webhook_delivery_retry_ladder.svg)](https://github.com/HiradEmami)
```

</details>

<details>
<summary>HTML</summary>

```html
<a href="https://github.com/HiradEmami">
  <img src="https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_webhook_delivery_retry_ladder.svg" alt="isometric_webhook_delivery_retry_ladder" />
</a>
```

</details>

### Details

- Type: Static or subtle motion
- Tags: `3d`, `architecture`, `isometric`, `static`, `system`
- Anchor: `#isometric-webhook-delivery-retry-ladder`
- [Source file](../../../assets/isometric/platform-architecture/isometric_webhook_delivery_retry_ladder.svg)
- [Raw SVG](https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/isometric/platform-architecture/isometric_webhook_delivery_retry_ladder.svg)
