# Asset Deprecation Policy

Raw GitHub URLs are part of this kit's public surface. Renaming or removing an asset can break READMEs that already embed it.

Use this policy before deleting, renaming, or replacing assets.

## When to Deprecate

Deprecate instead of deleting when an asset:

- has a typo in the filename but may already be used
- has a better replacement
- no longer matches the quality bar
- has licensing or provenance concerns that need a safer alternative
- is visually redundant but still functional

## When to Rename

Rename only when the benefit clearly outweighs the compatibility cost.

Good reasons:

- serious typo in a newly added asset
- misleading category or name
- duplicate asset name causing confusion
- asset has not been released or used publicly yet

Avoid renaming long-standing assets without a migration note.

## Deprecation Process

1. Add or identify the replacement asset.
2. Regenerate previews.
3. Document the old and new paths in the pull request.
4. Keep the old asset for at least one release cycle when practical.
5. Mention the deprecation in release notes.

Example:

```text
Deprecated:
assets/banners/energy/banner_energy_cloude.svg

Replacement:
assets/banners/energy/banner_energy_cloud.svg
```

## Removal Process

Only remove an asset when:

- it is unsafe
- it violates licensing expectations
- it is broken beyond reasonable repair
- it was added by mistake and has not been released

If an asset is removed, explain why in the pull request and release notes.

## Compatibility Notes

Raw GitHub links usually look like this:

```text
https://raw.githubusercontent.com/HiradEmami/readme-ux-kit/master/assets/...
```

Changing the file path breaks that URL. Prefer adding replacements over renaming or deleting established files.

## Preview Updates

After deprecating, replacing, renaming, or removing an asset:

```bash
npm run generate:previews
npm run check:all
```

Generated previews should reflect the final asset tree.
