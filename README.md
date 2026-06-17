# PaySecure Gateway DR Architecture

This project contains a complete multi-region disaster recovery architecture for PaySecure Gateway Private Limited, a fictional mid-tier payment aggregator processing 3.2 million daily transactions worth INR 500 crore across 45,000 merchants.

## What is included

- `ARCHITECTURE.md` — full AWS multi-region design covering active-active and active-passive patterns
- `COMPLIANCE_MAPPING.md` — crosswalk of design decisions to RBI, PCI-DSS v4.0, NPCI UPI, and India data localisation
- `BC_REVIEW_BOARD_PRESENTATION.md` — board-ready summary for a simulated Business Continuity Review Board of five stakeholders
- `RUNBOOKS/` — 12 production-quality disaster recovery runbooks for key failure scenarios
- `docs/` — static site content to publish the architecture as a live link via GitHub Pages

## Project goals

- Achieve 99.99% uptime by Q3 2026
- Meet regulatory RPO < 1 minute and RTO < 5 minutes
- Keep all payment-related data within Indian AWS regions
- Support resilient recovery across AWS Mumbai and Hyderabad

## How to use the project in your repository

1. Copy the entire `paysecure-dr-architecture` directory into your repository root.
2. Commit the folder and its contents using Git.
3. If you want a live preview, publish the `docs/` folder as GitHub Pages.

## Publish as a live link

1. Push the repository to GitHub.
2. In GitHub Repository settings, enable GitHub Pages from the `docs/` folder on the default branch.
3. Use the generated URL shown in GitHub Pages settings. Example: `https://<your-username>.github.io/<repo-name>/`

> Note: The project contains a static site in `docs/` that can be used for a live documentation link.

## Recommended repository structure

```
<repo-root>/paysecure-dr-architecture/
  README.md
  ARCHITECTURE.md
  COMPLIANCE_MAPPING.md
  BC_REVIEW_BOARD_PRESENTATION.md
  RUNBOOKS/
  docs/
```

## Next steps after adding files

- Review compliance mapping and update references to your organization name
- Customize runbooks for your real AWS account names and service identifiers
- Deploy the static `docs/index.html` through GitHub Pages or a similar static host
