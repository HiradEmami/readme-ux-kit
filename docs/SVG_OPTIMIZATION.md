# SVG Optimization

This repository uses a conservative Python optimizer for SVG assets:

```bash
npm run optimize:svg
```

To see whether files would change without writing them:

```bash
npm run check:svg:optimize
```

## Why Not Aggressive SVGO By Default

Many assets in this kit are animated and rely on readable IDs, gradients, masks, filters, SMIL animation, and CSS keyframes. Aggressive SVG optimization can accidentally break those details.

SVGO is useful for final compression, but it should be introduced with a reviewed config before it rewrites the library. Until then, the built-in optimizer applies only a safe profile.

## Safe Profile

The optimizer may:

- Normalize line endings to LF.
- Remove XML declarations.
- Remove XML comments.
- Trim trailing whitespace.
- Collapse repeated blank lines.
- Ensure files end with one newline.

The optimizer must not:

- Rename IDs, classes, gradients, filters, masks, or clip paths.
- Remove `<defs>`, `<style>`, `<animate>`, or `<animateTransform>`.
- Rewrite path data.
- Merge or remove groups.
- Change colors, opacity, transforms, dimensions, or `viewBox`.
- Add external references.

Every optimized candidate is parsed before writing. The tool rejects rewrites that would produce invalid XML, change the root SVG element, change the `viewBox`, introduce `<script>`, or introduce external `href`/`src` references.

## Recommended Workflow

After adding or editing SVG assets:

```bash
npm run optimize:svg
npm run generate:previews
npm run check:all
```

Use `npm run check:svg:optimize` in focused cleanup PRs when you want a non-writing report for optimization drift. It is intentionally separate from `npm run check:all` so normal asset work is not blocked by broad formatting churn.
