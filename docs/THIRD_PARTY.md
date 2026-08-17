# Third-Party Asset Provenance

This repository is primarily first-party MIT-licensed work. A small set of file-header SVGs were originally derived from a public-domain source and are tracked separately here so the MIT license for this repository stays clear.

## Upstream Source

| Field | Details |
| --- | --- |
| Source repository | <https://github.com/OstinUA/Promt-AI-Helper> |
| Upstream license | The Unlicense |
| License type | Public domain dedication |
| Attribution required | No |
| Redistribution allowed | Yes |
| Modification allowed | Yes |

The Unlicense allows use, modification, redistribution, and relicensing without attribution requirements. This project still documents the source for transparency.

## Known Derived Assets

The following file-header assets were originally picked up from the upstream source and then normalized for this kit:

| Asset | Local path | Status | Notes |
| --- | --- | --- | --- |
| Code of Conduct green header | [`assets/file_headers/code_of_conduct_green.svg`](../assets/file_headers/code_of_conduct_green.svg) | Modified derivative | Normalized to the repo file-header sizing and SVG quality expectations. |
| Code of Conduct red header | [`assets/file_headers/code_of_conduct_red.svg`](../assets/file_headers/code_of_conduct_red.svg) | Modified derivative | Normalized to the repo file-header sizing and SVG quality expectations. |
| Code of Conduct white header | [`assets/file_headers/code_of_conduct_white.svg`](../assets/file_headers/code_of_conduct_white.svg) | Modified derivative | Normalized to the repo file-header sizing and SVG quality expectations. |
| Contributing green header | [`assets/file_headers/contributing_green.svg`](../assets/file_headers/contributing_green.svg) | Modified derivative | Normalized to the repo file-header sizing and SVG quality expectations. |
| Contributing red header | [`assets/file_headers/contributing_red.svg`](../assets/file_headers/contributing_red.svg) | Modified derivative | Normalized to the repo file-header sizing and SVG quality expectations. |
| Contributing white header | [`assets/file_headers/contributing_white.svg`](../assets/file_headers/contributing_white.svg) | Modified derivative | Normalized to the repo file-header sizing and SVG quality expectations. |
| Security green header | [`assets/file_headers/security_green.svg`](../assets/file_headers/security_green.svg) | Modified derivative | Normalized to the repo file-header sizing and SVG quality expectations. |
| Security red header | [`assets/file_headers/security_red.svg`](../assets/file_headers/security_red.svg) | Modified derivative | Normalized to the repo file-header sizing and SVG quality expectations. |
| Security white header | [`assets/file_headers/security_white.svg`](../assets/file_headers/security_white.svg) | Modified derivative | Normalized to the repo file-header sizing and SVG quality expectations. |

## First-Party File Header Assets

The rest of the current `assets/file_headers/` category is treated as first-party work in this repository unless this document is updated with a new provenance entry.

Current first-party file-header examples include:

- [`accessibility_audit.svg`](../assets/file_headers/accessibility_audit.svg)
- [`api_reference_grid.svg`](../assets/file_headers/api_reference_grid.svg)
- [`architecture_circuit.svg`](../assets/file_headers/architecture_circuit.svg)
- [`benchmark_racing_line.svg`](../assets/file_headers/benchmark_racing_line.svg)
- [`ci_cd_pipeline.svg`](../assets/file_headers/ci_cd_pipeline.svg)
- [`database_schema_map.svg`](../assets/file_headers/database_schema_map.svg)
- [`deployment_flow.svg`](../assets/file_headers/deployment_flow.svg)
- [`docker_compose_stack.svg`](../assets/file_headers/docker_compose_stack.svg)
- [`environment_variables_panel.svg`](../assets/file_headers/environment_variables_panel.svg)
- [`funding_sponsors.svg`](../assets/file_headers/funding_sponsors.svg)
- [`governance_charter.svg`](../assets/file_headers/governance_charter.svg)
- [`observability_dashboard.svg`](../assets/file_headers/observability_dashboard.svg)
- [`performance_budget.svg`](../assets/file_headers/performance_budget.svg)
- [`readme_neon_scan.svg`](../assets/file_headers/readme_neon_scan.svg)
- [`support_signal.svg`](../assets/file_headers/support_signal.svg)
- [`testing_matrix.svg`](../assets/file_headers/testing_matrix.svg)

## Separation From Project License

The repository license in [`LICENSE`](../LICENSE) covers the project as distributed here. This provenance file exists to make clear that:

- first-party assets and documentation are maintained under this repository's MIT license;
- the known derived file-header assets came from an upstream public-domain source;
- the derived assets may be redistributed as part of this project because the upstream license permits it;
- this document should be updated whenever another external asset source is added.

## Review Rules For Future Third-Party Assets

Before adding a third-party asset, confirm:

- The source license allows redistribution in this repository.
- The source license allows modification if the asset is edited.
- The asset does not require attribution that conflicts with README usage.
- The source URL, license, local files, and modification status are added to this document.
- The asset passes `npm run check:svg`.
- Generated previews are regenerated when the asset is added.

Do not add assets from sources with unclear licensing, non-commercial restrictions, no-derivatives restrictions, or attribution terms that would be hard for downstream README users to preserve.

## Provenance Entry Template

Use this format for future sources:

```markdown
## Source Name

| Field | Details |
| --- | --- |
| Source repository or page | URL |
| Upstream license | License name |
| Attribution required | Yes or no |
| Redistribution allowed | Yes or no |
| Modification allowed | Yes or no |

| Asset | Local path | Status | Notes |
| --- | --- | --- | --- |
| Human-readable name | `assets/.../file.svg` | Original or modified derivative | What changed, if anything. |
```
