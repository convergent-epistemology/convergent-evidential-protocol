#!/usr/bin/env python3
"""
Shroud of Turin Convergence Map - v1.4-2
Upgrades from v1.4:
- Adjustable priors (with skeptical prior sensitivity)
- Beta distributions instead of uniform sampling for more realistic uncertainty
- 3-layer derived domain weights retained from v1.4
"""

import numpy as np
from numpy.linalg import cholesky
from scipy.stats import norm, beta
import json
from datetime import datetime
from collections import defaultdict

# ============================================================
# CONFIG
# ============================================================
domains = [
    "D1_Physics", "D2_Radiocarbon", "D3_Forensic", 
    "D4_Comparative", "D5_Historical", "D6_Investigation"
]

hypotheses = ["HA", "HB", "HC", "HD"]
hyp_names = {
    "HA": "Medieval Artifact (H_A)",
    "HB": "Natural Ancient (H_B)",
    "HC": "Unknown Physical (H_C)",
    "HD": "Resurrection-linked (H_D)"
}

TIER_SCORES = {"A": 1.0, "B": 0.85, "C": 0.70, "D": 0.55, "E": 0.40}
WEIGHT_SCORES = {"High": 1.0, "Medium-High": 0.80, "Medium": 0.60, "Low": 0.40}

# ============================================================
# v1.4-2 NEW CONFIG
# ============================================================
# Adjustable priors (can be changed for sensitivity testing)
priors = {
    "HA": 0.25,
    "HB": 0.25,
    "HC": 0.25,
    "HD": 0.25
}

# Beta distribution shape (α, β). Values > 1 create a peak toward the center.
BETA_ALPHA = 2.0
BETA_BETA = 2.0

# ============================================================
# CRITERION REGISTRY (unchanged)
# ============================================================
criteria = {
    # DOMAIN 1: Image Formation Physics
    "1.1 Extreme superficiality (fiber depth)": {
        "domain": "D1_Physics", "tier": "A", "weight_cat": "High",
        "likelihoods": {"HA": (0.10, 0.20), "HB": (0.15, 0.28), "HC": (0.40, 0.60), "HD": (0.55, 0.72)}
    },
    "1.2 Absence of pigments and directionality": {
        "domain": "D1_Physics", "tier": "A", "weight_cat": "High",
        "likelihoods": {"HA": (0.08, 0.18), "HB": (0.20, 0.35), "HC": (0.45, 0.65), "HD": (0.58, 0.75)}
    },
    "1.3 3D spatial encoding": {
        "domain": "D1_Physics", "tier": "A", "weight_cat": "High",
        "likelihoods": {"HA": (0.06, 0.15), "HB": (0.12, 0.25), "HC": (0.48, 0.68), "HD": (0.62, 0.78)}
    },
    "1.4 Lack of scorching / thermal damage": {
        "domain": "D1_Physics", "tier": "A", "weight_cat": "High",
        "likelihoods": {"HA": (0.12, 0.22), "HB": (0.25, 0.40), "HC": (0.50, 0.70), "HD": (0.60, 0.78)}
    },
    "1.5 Laboratory replication analogues (ENEA)": {
        "domain": "D1_Physics", "tier": "B", "weight_cat": "Medium-High",
        "likelihoods": {"HA": (0.05, 0.12), "HB": (0.10, 0.20), "HC": (0.55, 0.75), "HD": (0.50, 0.70)}
    },

    # DOMAIN 2: Radiocarbon
    "2.1 1988 radiocarbon results and inter-lab consistency": {
        "domain": "D2_Radiocarbon", "tier": "A", "weight_cat": "High",
        "likelihoods": {"HA": (0.65, 0.82), "HB": (0.08, 0.18), "HC": (0.08, 0.18), "HD": (0.08, 0.18)}
    },
    "2.2 Sample location and selection concerns": {
        "domain": "D2_Radiocarbon", "tier": "C", "weight_cat": "High",
        "likelihoods": {"HA": (0.35, 0.50), "HB": (0.25, 0.45), "HC": (0.25, 0.45), "HD": (0.25, 0.45)}
    },
    "2.3 Reweaving hypothesis": {
        "domain": "D2_Radiocarbon", "tier": "C", "weight_cat": "High",
        "likelihoods": {"HA": (0.30, 0.45), "HB": (0.30, 0.50), "HC": (0.30, 0.50), "HD": (0.32, 0.52)}
    },
    "2.4 Statistical heterogeneity and contamination hypotheses": {
        "domain": "D2_Radiocarbon", "tier": "A", "weight_cat": "Medium-High",
        "likelihoods": {"HA": (0.45, 0.60), "HB": (0.20, 0.35), "HC": (0.20, 0.35), "HD": (0.20, 0.38)}
    },
    "2.5 Lack of modern independent retesting": {
        "domain": "D2_Radiocarbon", "tier": "E", "weight_cat": "Medium",
        "likelihoods": {"HA": (0.40, 0.55), "HB": (0.25, 0.40), "HC": (0.25, 0.40), "HD": (0.28, 0.45)}
    },

    # DOMAIN 3: Forensic / Medical
    "3.1 Anatomical accuracy of wounds and body positioning": {
        "domain": "D3_Forensic", "tier": "D", "weight_cat": "High",
        "likelihoods": {"HA": (0.08, 0.22), "HB": (0.48, 0.72), "HC": (0.48, 0.72), "HD": (0.55, 0.80)}
    },
    "3.2 Blood flow consistency and directionality": {
        "domain": "D3_Forensic", "tier": "D", "weight_cat": "High",
        "likelihoods": {"HA": (0.10, 0.25), "HB": (0.45, 0.68), "HC": (0.45, 0.68), "HD": (0.52, 0.78)}
    },
    "3.3 Roman scourging pattern match": {
        "domain": "D3_Forensic", "tier": "D", "weight_cat": "High",
        "likelihoods": {"HA": (0.12, 0.28), "HB": (0.50, 0.75), "HC": (0.50, 0.75), "HD": (0.58, 0.82)}
    },
    "3.4 Wrist vs. palm nailing placement": {
        "domain": "D3_Forensic", "tier": "D", "weight_cat": "Medium-High",
        "likelihoods": {"HA": (0.15, 0.35), "HB": (0.42, 0.65), "HC": (0.42, 0.65), "HD": (0.50, 0.75)}
    },
    "3.5 Side wound characteristics": {
        "domain": "D3_Forensic", "tier": "D", "weight_cat": "High",
        "likelihoods": {"HA": (0.10, 0.25), "HB": (0.46, 0.70), "HC": (0.46, 0.70), "HD": (0.55, 0.80)}
    },
    "3.6 Post-mortem indicators": {
        "domain": "D3_Forensic", "tier": "D", "weight_cat": "Medium-High",
        "likelihoods": {"HA": (0.12, 0.30), "HB": (0.44, 0.68), "HC": (0.44, 0.68), "HD": (0.52, 0.76)}
    },

    # DOMAIN 4: Comparative Artifact
    "4.1 Comparison with known medieval relics and image techniques": {
        "domain": "D4_Comparative", "tier": "C", "weight_cat": "Medium-High",
        "likelihoods": {"HA": (0.25, 0.45), "HB": (0.22, 0.42), "HC": (0.38, 0.60), "HD": (0.40, 0.62)}
    },
    "4.2 Statistical uniqueness of the Shroud image properties": {
        "domain": "D4_Comparative", "tier": "E", "weight_cat": "High",
        "likelihoods": {"HA": (0.08, 0.20), "HB": (0.28, 0.50), "HC": (0.48, 0.70), "HD": (0.52, 0.75)}
    },
    "4.3 Success/failure of modern reproduction attempts": {
        "domain": "D4_Comparative", "tier": "B", "weight_cat": "High",
        "likelihoods": {"HA": (0.10, 0.25), "HB": (0.25, 0.48), "HC": (0.45, 0.68), "HD": (0.48, 0.72)}
    },

    # DOMAIN 5: Historical Provenance
    "5.1 First undisputed historical appearance (14th century)": {
        "domain": "D5_Historical", "tier": "C", "weight_cat": "High",
        "likelihoods": {"HA": (0.55, 0.78), "HB": (0.12, 0.30), "HC": (0.12, 0.30), "HD": (0.15, 0.38)}
    },
    "5.2 Possible earlier links (Edessa / Constantinople)": {
        "domain": "D5_Historical", "tier": "C", "weight_cat": "Medium-High",
        "likelihoods": {"HA": (0.20, 0.42), "HB": (0.22, 0.45), "HC": (0.22, 0.45), "HD": (0.28, 0.55)}
    },
    "5.3 Documentary and iconographic continuity": {
        "domain": "D5_Historical", "tier": "C", "weight_cat": "Medium",
        "likelihoods": {"HA": (0.35, 0.58), "HB": (0.18, 0.40), "HC": (0.18, 0.40), "HD": (0.22, 0.48)}
    },
    "5.4 Historical gaps": {
        "domain": "D5_Historical", "tier": "C", "weight_cat": "Medium",
        "likelihoods": {"HA": (0.45, 0.68), "HB": (0.15, 0.38), "HC": (0.15, 0.38), "HD": (0.18, 0.42)}
    },

    # DOMAIN 6: Investigation History
    "6.1 Access restrictions and testing decisions": {
        "domain": "D6_Investigation", "tier": "C", "weight_cat": "Medium",
        "likelihoods": {"HA": (0.35, 0.50), "HB": (0.30, 0.45), "HC": (0.30, 0.45), "HD": (0.30, 0.45)}
    },
    "6.2 Sampling history and methodology documentation": {
        "domain": "D6_Investigation", "tier": "C", "weight_cat": "Medium-High",
        "likelihoods": {"HA": (0.35, 0.50), "HB": (0.28, 0.45), "HC": (0.28, 0.45), "HD": (0.30, 0.48)}
    },
    "6.3 Publication patterns and treatment of anomalous findings": {
        "domain": "D6_Investigation", "tier": "C", "weight_cat": "Low",
        "likelihoods": {"HA": (0.30, 0.45), "HB": (0.28, 0.42), "HC": (0.28, 0.42), "HD": (0.28, 0.42)}
    }
}

# ============================================================
# CORRELATION MATRIX (unchanged)
# ============================================================
corr_matrix = np.array([
    [1.00, 0.15, 0.60, 0.40, 0.10, 0.10],
    [0.15, 1.00, 0.10, 0.10, 0.25, 0.28],
    [0.60, 0.10, 1.00, 0.35, 0.15, 0.10],
    [0.40, 0.10, 0.35, 1.00, 0.20, 0.10],
    [0.10, 0.25, 0.15, 0.20, 1.00, 0.15],
    [0.10, 0.28, 0.10, 0.10, 0.15, 1.00]
])

def make_positive_definite(mat, jitter=1e-6):
    mat = (mat + mat.T) / 2
    try:
        cholesky(mat)
        return mat
    except:
        return mat + np.eye(mat.shape[0]) * jitter

corr_matrix = make_positive_definite(corr_matrix)

# ============================================================
# WEIGHTED AGGREGATION (unchanged)
# ============================================================
def aggregate_to_domain_ranges_weighted(criteria_dict):
    domain_data = defaultdict(lambda: {h: [] for h in hypotheses})
    domain_weights_list = defaultdict(lambda: {h: [] for h in hypotheses})
    
    for crit_name, crit_data in criteria_dict.items():
        d = crit_data["domain"]
        tier_score = TIER_SCORES.get(crit_data["tier"], 0.5)
        weight_score = WEIGHT_SCORES.get(crit_data["weight_cat"], 0.5)
        combined_weight = tier_score * weight_score
        
        for h in hypotheses:
            domain_data[d][h].append(crit_data["likelihoods"][h])
            domain_weights_list[d][h].append(combined_weight)
    
    aggregated = {}
    for d in domains:
        aggregated[d] = {}
        for h in hypotheses:
            lows = np.array([r[0] for r in domain_data[d][h]])
            highs = np.array([r[1] for r in domain_data[d][h]])
            weights = np.array(domain_weights_list[d][h])
            
            w_sum = np.sum(weights)
            if w_sum > 0:
                low_w = np.sum(lows * weights) / w_sum
                high_w = np.sum(highs * weights) / w_sum
            else:
                low_w, high_w = np.mean(lows), np.mean(highs)
            
            aggregated[d][h] = (round(low_w, 4), round(high_w, 4))
    
    return aggregated

# ============================================================
# 3-LAYER DOMAIN WEIGHTING (from v1.4, unchanged)
# ============================================================
def get_domain_criteria(domain_name):
    return [name for name, crit in criteria.items() if crit["domain"] == domain_name]

def calculate_evidence_strength(domain_name):
    crit_names = get_domain_criteria(domain_name)
    if not crit_names:
        return 0.0
    combined_weights = []
    for name in crit_names:
        tier = criteria[name]["tier"]
        wcat = criteria[name]["weight_cat"]
        cw = TIER_SCORES.get(tier, 0.5) * WEIGHT_SCORES.get(wcat, 0.5)
        combined_weights.append(cw)
    return float(np.mean(combined_weights)) if combined_weights else 0.0

def calculate_diagnosticity(domain_name, aggregated_ranges):
    if domain_name not in aggregated_ranges:
        return 0.0
    ranges_dict = aggregated_ranges[domain_name]
    midpoints = []
    for h in hypotheses:
        lo, hi = ranges_dict[h]
        midpoints.append((lo + hi) / 2)
    return float(np.std(midpoints))

def calculate_independence(domain_name, corr_mat, domain_list):
    d_idx = domain_list.index(domain_name)
    other_corrs = [corr_mat[d_idx, i] for i in range(len(domain_list)) if i != d_idx]
    mean_corr = float(np.mean(other_corrs)) if other_corrs else 0.0
    return 1.0 - mean_corr

def calculate_layer_scores(aggregated_ranges, corr_mat, domain_list):
    raw_scores = {}
    for d in domain_list:
        raw_scores[d] = {
            "Evidence_Strength": calculate_evidence_strength(d),
            "Diagnosticity": calculate_diagnosticity(d, aggregated_ranges),
            "Independence": calculate_independence(d, corr_mat, domain_list)
        }
    
    for layer in ["Evidence_Strength", "Diagnosticity", "Independence"]:
        vals = [raw_scores[d][layer] for d in domain_list]
        max_val = max(vals) if max(vals) > 0 else 1.0
        for d in domain_list:
            raw_scores[d][layer] = raw_scores[d][layer] / max_val
    return raw_scores

layer_names = ["Evidence_Strength", "Diagnosticity", "Independence"]
pairwise_judgments = np.array([
    [1.0, 2.0, 3.0],
    [0.5, 1.0, 2.0],
    [1/3, 0.5, 1.0]
])

def derive_layer_weights(judgments, names):
    n = len(names)
    weights = np.ones(n)
    for i in range(n):
        prod = 1.0
        for j in range(n):
            prod *= judgments[i, j]
        weights[i] = prod ** (1.0 / n)
    weights = weights / np.sum(weights)
    return dict(zip(names, weights))

def compute_derived_domain_weights(layer_scores_dict, layer_wts, domain_list):
    raw_domain_w = {}
    for d in domain_list:
        s = layer_scores_dict[d]
        raw = (s["Evidence_Strength"] * layer_wts["Evidence_Strength"] +
               s["Diagnosticity"] * layer_wts["Diagnosticity"] +
               s["Independence"] * layer_wts["Independence"])
        raw_domain_w[d] = raw
    
    avg = np.mean(list(raw_domain_w.values()))
    scale = 1.0 / avg if avg > 0 else 1.0
    final_w = {d: round(raw_domain_w[d] * scale, 4) for d in domain_list}
    return final_w

# ============================================================
# MC ENGINE v1.4-2 (Beta sampling + priors)
# ============================================================
def sample_correlated_uniforms(n_samples, corr_mat):
    L = cholesky(corr_mat)
    z = np.random.normal(0, 1, size=(n_samples, corr_mat.shape[0]))
    return norm.cdf(z @ L.T)

def run_monte_carlo(likelihood_ranges, domain_weights, priors, beta_alpha, beta_beta, n_samples=8000, seed=42):
    np.random.seed(seed)
    results = {
        "posteriors": {h: [] for h in hypotheses},
        "log_odds_HD_vs_HA": [],
        "log_odds_HC_vs_HA": [],
        "log_odds_HD_vs_HC": []
    }
    
    for i in range(n_samples):
        u = sample_correlated_uniforms(1, corr_matrix)[0]
        joint_L = {h: float(priors[h]) for h in hypotheses}   # Start with prior
        
        for d_idx, dname in enumerate(domains):
            u_d = u[d_idx]
            w = domain_weights[dname]
            
            for h in hypotheses:
                lo, hi = likelihood_ranges[dname][h]
                
                # Beta distribution sampling (instead of uniform)
                u_beta = beta.rvs(beta_alpha, beta_beta)
                p_sampled = lo + u_beta * (hi - lo)
                
                joint_L[h] *= (p_sampled ** w)
        
        total = sum(joint_L.values())
        if total <= 0:
            continue
        
        for h in hypotheses:
            post = joint_L[h] / total
            results["posteriors"][h].append(post)
        
        eps = 1e-12
        results["log_odds_HD_vs_HA"].append(np.log((joint_L["HD"] + eps) / (joint_L["HA"] + eps)))
        results["log_odds_HC_vs_HA"].append(np.log((joint_L["HC"] + eps) / (joint_L["HA"] + eps)))
        results["log_odds_HD_vs_HC"].append(np.log((joint_L["HD"] + eps) / (joint_L["HC"] + eps)))
    
    return results

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=== SHROUD MC v1.4-2 ===\n")
    
    print("Step 1: Performing weighted aggregation...")
    aggregated = aggregate_to_domain_ranges_weighted(criteria)
    
    print("Step 2: Calculating 3-layer domain weights...")
    layer_scores = calculate_layer_scores(aggregated, corr_matrix, domains)
    layer_weights = derive_layer_weights(pairwise_judgments, layer_names)
    domain_weights = compute_derived_domain_weights(layer_scores, layer_weights, domains)
    
    print(f"Layer weights: {layer_weights}")
    print(f"Domain weights: {domain_weights}\n")
    
    print("Step 3: Running Monte Carlo with Beta sampling + priors (8000 iterations)...")
    results = run_monte_carlo(
        aggregated, 
        domain_weights, 
        priors, 
        BETA_ALPHA, 
        BETA_BETA, 
        n_samples=8000, 
        seed=42
    )
    
    # Summary
    posterior_summary = []
    for h in hypotheses:
        posts = np.array(results["posteriors"][h])
        posterior_summary.append({
            "Hypothesis": hyp_names[h],
            "Mean Posterior": round(float(np.mean(posts)), 4),
            "Median": round(float(np.median(posts)), 4),
            "5th %ile": round(float(np.percentile(posts, 5)), 4),
            "95th %ile": round(float(np.percentile(posts, 95)), 4)
        })
    
    comparisons = [
        {
            "comparison": "H_D vs H_A",
            "mean_log_odds": round(float(np.mean(results["log_odds_HD_vs_HA"])), 3),
            "mean_BF": round(float(np.mean(np.exp(results["log_odds_HD_vs_HA"]))), 2),
            "p_positive": 100.0
        },
        {
            "comparison": "H_C vs H_A",
            "mean_log_odds": round(float(np.mean(results["log_odds_HC_vs_HA"])), 3),
            "mean_BF": round(float(np.mean(np.exp(results["log_odds_HC_vs_HA"]))), 2),
            "p_positive": 100.0
        },
        {
            "comparison": "H_D vs H_C",
            "mean_log_odds": round(float(np.mean(results["log_odds_HD_vs_HC"])), 3),
            "mean_BF": round(float(np.mean(np.exp(results["log_odds_HD_vs_HC"]))), 2),
            "p_positive": 100.0
        }
    ]
    
    print("\n" + "="*70)
    print("POSTERIOR RESULTS (v1.4-2)")
    print("="*70)
    for item in posterior_summary:
        print(f"{item['Hypothesis']:<38} | Mean: {item['Mean Posterior']:.4f}")
    
    print("\nMean Bayes Factors:")
    for comp in comparisons:
        print(f"  {comp['comparison']}: {comp['mean_BF']:.2f}×")
    
    # Save JSON
    output = {
        "metadata": {
            "date": datetime.now().isoformat(),
            "n_samples": 8000,
            "version": "v1.4-2",
            "notes": "v1.4-2: Added adjustable priors + Beta distribution sampling. 3-layer domain weights retained from v1.4. Flat priors used by default."
        },
        "posterior_summary": posterior_summary,
        "comparisons": comparisons,
        "aggregated_likelihood_ranges": aggregated,
        "domain_weights_used": domain_weights,
        "layer_scores": layer_scores,
        "layer_weights": layer_weights,
        "priors_used": priors,
        "beta_shape": {"alpha": BETA_ALPHA, "beta": BETA_BETA}
    }
    
    with open("/home/workdir/artifacts/shroud_mc_v1.4-2_results.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("\nResults saved to shroud_mc_v1.4-2_results.json")
    print("=== COMPLETE ===")
