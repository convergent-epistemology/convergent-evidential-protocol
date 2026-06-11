# Convergent Evidential Protocol (CEP) v1.4
**First Full-Scale Demonstration: Shroud of Turin Convergence Mapping**

**Author:** Tyler Leroux  
**Date:** June 2026  
**Version:** 1.4

This repository presents the **Convergent Evidential Protocol (CEP)** — a structured, quantitative, and fully auditable framework for evaluating complex, heterogeneous, multi-disciplinary evidence under uncertainty — together with its first complete demonstration on the Shroud of Turin.

---

## What is the Convergent Evidential Protocol?

The CEP is a generalizable methodology for assessing competing hypotheses when evidence comes from multiple domains, varies widely in quality and directness, and contains real interdependencies and uncertainty.

Instead of informal narrative synthesis or single-discipline analysis, the CEP delivers a transparent, traceable process that:

- Derives domain-level likelihoods bottom-up from explicitly tiered and weighted individual criteria
- Models correlations between lines of evidence using a Gaussian copula
- Propagates uncertainty via Monte Carlo simulation with Beta distribution sampling
- Applies derived multi-layer domain weights (Evidence Strength × Diagnosticity × Independence)
- Includes built-in sensitivity testing, parsimony assessment, and a pre-specified Operational Falsification & Updating Protocol

The framework is designed to be usable by researchers across disciplines and levels of expertise. The main PDF presents the full analysis in readable form with expert consensus tracking. No programming knowledge is required to understand the methodology or conclusions. The accompanying code and results files allow technical users to inspect, replicate, modify, or extend the model.

---

## What Makes the CEP Distinctive

- **Bottom-up, auditable aggregation** — Domain likelihood ranges are mathematically derived from individual criteria using locked Evidence Tier and Weight Category scores rather than holistic expert judgment.
- **Three-layer domain weighting** — Each domain’s influence is determined by Evidence Strength, Diagnosticity (how well it separates hypotheses), and Independence (to reduce double-counting).
- **Correlation-aware Monte Carlo synthesis** — A Gaussian copula combined with Beta sampling produces realistic joint distributions while respecting bounded likelihood ranges.
- **Adversarial sensitivity testing** — Includes base case, Skeptical Vector, and Hyper-Skeptical scenarios plus adjustable priors.
- **Stability across versions** — Core rankings have remained directionally consistent through iterative refinements to weighting, sampling, and prior handling (v1.0–v1.4).
- **Epistemic sandbox philosophy** — Inputs are locked for traceability but explicitly designed to be varied and stress-tested by others.

The CEP was developed because no existing single method fully addresses the challenges of highly contested, multi-domain problems where evidence is incomplete, interdependent, and subject to long-standing interpretive disagreement.

---

## This Repository: First Full Demonstration

The Shroud of Turin was chosen as the initial test case because it demands rigorous integration of physical, chemical, forensic, historical, and radiocarbon evidence while navigating deep tensions between domains. While the Shroud serves as the demonstration, the CEP itself is a general-purpose framework applicable to any complex evidential problem (historical controversies, scientific disputes with heterogeneous data, anomalous phenomena, etc.).

Future work may include additional case studies, expanded visualizations, and tooling to make the protocol easier to apply to new questions.

---

## Key Findings (Base Case, v1.4)

In the base-case analysis with flat priors:

- **Resurrection-linked Mechanism (H_D)** receives the highest posterior support (mean ≈ 0.597).
- **Unknown Physical Mechanism (H_C)** is the second most supported (mean ≈ 0.324).
- **Natural Ancient Mechanism (H_B)** receives limited support (mean ≈ 0.060).
- **Medieval Artifact (H_A)** receives the lowest support (mean ≈ 0.019).

These results are **not** presented as definitive proof of any hypothesis. The CEP is explicitly designed to remain sensitive to alternative assumptions. Readers are encouraged to examine the model, adjust parameters (especially radiocarbon-related criteria or domain correlations), and explore strongly skeptical scenarios.

The directional ranking **H_D > H_C > H_B > H_A** has remained stable across multiple sensitivity tests and version iterations. Full posterior distributions, Bayes factors, domain weights, layer scores, and sensitivity results are available in the accompanying PDF and `shroud_mc_v1.4_results.json`.

---

## Repository Contents

| File                                      | Description |
|-------------------------------------------|-------------|
| `CEP_v1.4_Shroud_Demonstration.pdf`      | Complete methodology document + full Shroud demonstration (all domains, criterion-level analysis, expert consensus tracking, and final synthesis) |
| `shroud_mc_v1.4_weighted.py`             | Python implementation of the Monte Carlo engine (weighted aggregation, 3-layer domain weighting, Gaussian copula correlations, Beta sampling, adjustable priors) |
| `shroud_mc_v1.4_results.json`            | Structured output: posterior summaries, Bayes factors, aggregated likelihood ranges, domain weights, layer scores, and metadata |
| `README.md`                              | This file |

---

## How to Engage with This Work

**General readers & researchers** — Start with the PDF. It contains the complete, self-contained analysis with no programming required.

**Transparency & modification** — Use the Python script and JSON results to:
- Reproduce the published results
- Test alternative likelihood ranges or domain weights
- Vary the correlation matrix (especially between Radiocarbon and Historical domains)
- Run your own sensitivity analyses or Skeptical Vector scenarios

The code is intentionally modular. All key inputs (likelihood ranges, tier/weight scores, correlation matrix, priors, Beta shape parameters) are clearly defined at the top of the script and can be edited directly.

**Researchers wanting to adapt the framework** — The CEP structure (criterion registry, weighted aggregation, 3-layer domain weighting, copula Monte Carlo engine) is designed to be reusable. You can replace the Shroud criteria with evidence from another problem while retaining the surrounding machinery.

The goal of this repository is to function as a transparent **epistemic sandbox** — a system for exploring how complex, multi-domain evidence interacts under different assumptions rather than delivering a fixed verdict.

---

## Citation

If you use or reference this work, please cite:

> Leroux, T. (2026). *Convergent Evidential Protocol (CEP) v1.4 – First Demonstration: Shroud of Turin Convergence Mapping*. https://github.com/convergent-epistemology/convergent-evidential-protocol

---

## License

This work is released under an open license with attribution. The methodology, documentation, code, and results may be freely used, modified, and adapted provided appropriate credit is given.

---

## Contact & Future Development

This is Version 1.4 and the first public release of the full framework. Feedback, questions, proposed alternative parameter sets, and suggestions for additional case studies are welcome.

Planned future directions include:
- Additional real-world case studies
- Expanded sensitivity testing and interactive visualizations
- Further methodological refinements
- Tooling to lower the barrier for applying the CEP to new problems

Open an issue or contact the author to discuss collaboration or extensions.
