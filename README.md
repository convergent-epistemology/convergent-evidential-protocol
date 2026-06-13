**Note on Implementation Update (June 2026)**  
The accompanying Python script (`shroud_mc_v1.4_weighted.py`) has been corrected to fully implement the Gaussian copula correlation and dynamic metrics as originally described in this v1.4 framework. These were implementation fixes only — **they do not change the underlying methodology, evidence tiers, domain weights, or overall conclusions** of the CEP. A minor update to the main PDF (CEP_v1.4_Shroud_Demonstration.pdf) is pending to reflect the corrected results and implementation notes.


# Convergent Evidential Protocol (CEP) v1.4

**First Full-Scale Demonstration: Shroud of Turin**

A structured, quantitative, and fully auditable framework for evaluating complex, multi-domain evidence under uncertainty.

**Author:** Tyler Leroux  
**Date:** June 2026  
**Version:** 1.4


## Overview

The **Convergent Evidential Protocol (CEP)** is a generalizable methodology for assessing competing hypotheses when evidence comes from multiple domains, varies in quality and directness, and contains real interdependencies and uncertainty.

Rather than relying on informal narrative synthesis or single-discipline analysis, the CEP provides a transparent, traceable process that:

- Derives domain-level likelihoods bottom-up from explicitly tiered and weighted individual criteria
- Models correlations between lines of evidence using a Gaussian copula
- Propagates uncertainty via Monte Carlo simulation with Beta distribution sampling
- Applies derived multi-layer domain weights (Evidence Strength × Diagnosticity × Independence)
- Includes built-in sensitivity testing, parsimony assessment, and a pre-specified Operational Falsification & Updating Protocol

The framework is designed to be usable by researchers across disciplines. The main PDF contains the complete analysis with expert consensus tracking. No programming knowledge is required to understand the methodology or conclusions.


## What Makes the CEP Distinctive

- **Bottom-up, auditable aggregation** — Domain likelihood ranges are mathematically derived from individual criteria using locked Evidence Tier and Weight Category scores.
- **Three-layer domain weighting** — Each domain’s influence is determined by Evidence Strength, Diagnosticity, and Independence (to reduce double-counting).
- **Correlation-aware Monte Carlo synthesis** — Uses a Gaussian copula combined with Beta distribution sampling for realistic joint distributions.
- **Adversarial sensitivity testing** — Includes base case, Skeptical Vector, Hyper-Skeptical scenarios, and adjustable priors.
- **Stability across versions** — Core rankings have remained directionally consistent through v1.0–v1.4.
- **Epistemic sandbox philosophy** — Inputs are locked for traceability but explicitly designed to be varied and stress-tested by others.


## This Repository

This repository contains the first full-scale application of the CEP, using the Shroud of Turin as the test case. The Shroud was chosen because it requires rigorous integration of physical, chemical, forensic, historical, and radiocarbon evidence while navigating deep tensions between domains.

While the Shroud serves as the demonstration, the CEP itself is a general-purpose framework applicable to historical controversies, scientific disputes, and other complex evidential problems.


## Key Findings (Base Case, v1.4)

In the base-case analysis with flat priors:

| Hypothesis                        | Mean Posterior | Notes                          |
|-----------------------------------|----------------|--------------------------------|
| Resurrection-linked (H_D)         | ≈ 0.597        | Highest support                |
| Unknown Physical (H_C)            | ≈ 0.324        | Second highest                 |
| Natural Ancient (H_B)             | ≈ 0.060        | Limited support                |
| Medieval Artifact (H_A)           | ≈ 0.019        | Lowest support                 |

These results are not presented as definitive conclusions. The framework is explicitly designed to remain sensitive to alternative assumptions. Readers are encouraged to examine the model and test different parameterizations.

The directional ranking **H_D > H_C > H_B > H_A** has remained stable across multiple sensitivity tests and version iterations.

Full posterior distributions, Bayes factors, domain weights, layer scores, and sensitivity results are available in the PDF and `shroud_mc_v1.4_results.json`.

**Note on Hypothesis Framing**

H_D (Resurrection-linked Mechanism) is not treated as an unconstrained miracle hypothesis. The model imposes real physical, forensic, and historical constraints on H_D. It must still align with the observed evidence (such as extreme superficiality, 3D encoding, blood flow patterns, anatomical accuracy, and historical provenance). This prevents H_D from functioning as an explanatory wildcard that can accommodate any observation.

## Repository Contents

| File                                      | Description |
|-------------------------------------------|-------------|
| `CEP_v1.4_Shroud_Demonstration.pdf`      | Complete methodology document + full Shroud demonstration |
| `shroud_mc_v1.4_weighted.py`             | Python implementation of the Monte Carlo engine |
| `shroud_mc_v1.4_results.json`            | Posterior summaries, Bayes factors, domain weights, and layer scores |
| `README.md`                              | This file |


## How to Engage with This Work

**General readers & researchers** — Start with the PDF. It contains the complete, self-contained analysis with expert consensus tracking. No programming knowledge is required.

**Transparency & modification** — Use the Python script and JSON results to:
- Reproduce the published results
- Test alternative likelihood ranges or domain weights
- Vary the correlation matrix (especially between Radiocarbon and Historical domains)
- Run your own sensitivity analyses or Skeptical Vector scenarios

The code is intentionally modular. All key inputs (likelihood ranges, tier/weight scores, correlation matrix, priors, and Beta shape parameters) are clearly defined at the top of the script and can be edited directly.

**Researchers wanting to adapt the framework** — The CEP structure (criterion registry, weighted aggregation, 3-layer domain weighting, and copula Monte Carlo engine) is designed to be reusable. You can replace the Shroud criteria with evidence from another problem while retaining the surrounding methodology.

The goal of this repository is to function as a transparent **epistemic sandbox** — a system for exploring how complex, multi-domain evidence interacts under different assumptions rather than delivering a fixed verdict.


## Citation

If you use or reference this work, please cite:
Leroux, T. (2026). Convergent Evidential Protocol (CEP) v1.4 – First Demonstration: Shroud of Turin. https://github.com/convergent-epistemology/convergent-evidential-protocol


## License

This work is released under the **MIT License**.


## Contact & Future Development

This is Version 1.4 and the first public release of the full framework.

Feedback, questions, proposed alternative parameter sets, and suggestions for additional case studies are welcome.

Planned future directions include:
- Additional real-world case studies
- Expanded sensitivity testing and interactive visualizations
- Further methodological refinements
- Tooling to make the protocol easier to apply to new problems

Open an issue or contact the author to discuss collaboration or extensions.
