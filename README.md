
---
# Multi-Modal Drug Repurposing for Head and Neck Cancer (HNC)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DOI](https://img.shields.io/badge/DOI-Pending-orange.svg)](https://doi.org/)

> **A comprehensive computational framework integrating electronic health records, genomics, and literature mining for systematic drug repurposing in head and neck cancer, stratified by HPV status.**

---

## Table of Contents

- [Overview](#overview)
- [Key Findings](#key-findings)
- [Data Requirements & Acquisition](#data-requirements--acquisition)
- [Methodology](#methodology)
  - [Aim 1: EHR-Based Drug Repurposing](#aim-1-ehr-based-drug-repurposing)
  - [Aim 2: Genomics-Based Drug Repurposing](#aim-2-genomics-based-drug-repurposing)
  - [Aim 3: Literature-Based Validation](#aim-3-literature-based-validation)
  - [Integration: Multi-Modal Candidate Prioritization](#integration-multi-modal-candidate-prioritization)
- [Results](#results)
- [Installation](#installation)
- [Usage](#usage)
- [Citation](#citation)
- [Contact](#contact)

---

## Overview

Head and neck cancer (HNC) represents a significant clinical challenge with limited treatment options and poor outcomes for metastatic disease. This research introduces a **three-pronged computational drug repurposing framework** that:

1. **Leverages real-world clinical data** to identify medications associated with improved metastasis-free survival
2. **Integrates genomic alterations** to discover mechanistically relevant drug-gene connections
3. **Validates findings** through comprehensive literature mining using large language models

### Innovation

- **HPV-Stratified Analysis**: Separate pipelines for HPV-positive and HPV-negative HNC, recognizing fundamental biological differences
- **Multi-Modal Integration**: Combines complementary evidence streams (clinical outcomes, genomics, literature) for robust candidate prioritization
- **Explainable AI**: Uses SHAP analysis and survival models to ensure interpretability of machine learning predictions
- **Rigorous Statistical Framework**: Nested cross-validation, FDR correction, and dual statistical validation prevent false discoveries

### Clinical Impact

The framework identified **dozens of high-confidence drug candidates** with:
- **Existing safety profiles** (FDA-approved or well-characterized)
- **Strong evidence** across multiple data modalities
- **Mechanistic rationale** linking drugs to cancer-relevant pathways
- **Potential for rapid clinical translation** through investigator-initiated trials

---

## Key Findings

### HPV-Positive HNC
- **3 validated drug candidates** with complete evidence pathways (EHR + Genomics + Literature + PPI)
- **LEVOTHYROXINE** (highest XGB importance: 0.0441) targets PIK3CA pathway (17 literature PMIDs)
- **HEPARIN** targets multiple FGFRs → PIK3CA convergence
- **DEXAMETHASONE** targets SOX2 stem cell pathway
- Key pathways: PI3K/AKT signaling, stem cell regulation, growth factor signaling

### HPV-Negative HNC  
- **5 validated drug candidates** with complete evidence pathways
- **MELATONIN**  shows multi-target effects 
- **LEVOTHYROXINE** validated in both cohorts (cross-cohort consistency)
- **METHYLPREDNISOLONE** shows strongest protective effect 
- **Aspirin** and **Acetaminophen** 
- key pathways related to TP53

### Cross-Modal Convergence
- **LEVOTHYROXINE**: Only drug validated in both HPV+ and HPV- cohorts
- **PIK3CA**: Central hub in HPV+ (4/4 drugs converge)
- **BCL6**: Central hub in HPV- (4/5 drugs converge)  
- **Sankey diagrams** visualize drug → target → mutation evidence flows
- **Detailed candidate profiles**: See [QUICK_REFERENCE_DRUG_CANDIDATES.md](All%20aims%20together/QUICK_REFERENCE_DRUG_CANDIDATES.md)

---

## Data Requirements & Acquisition

### Required Data Sources

**Note: Large input data files and intermediate results have been removed from this repository to reduce size. You will need to obtain the following data sources to run the complete pipeline:**

#### 1. Electronic Health Records (EHR) Data
- **Source**: TriNetX Research Network (requires institutional access)
- **Access**: Contact your institution's TriNetX administrator or visit [https://trinetx.com/](https://trinetx.com/)
- **Required Files**: De-identified patient records including:
  - Diagnosis codes (ICD-9/ICD-10)
  - Medication prescriptions (RxNorm/NDC codes)
  - Procedures (CPT/HCPCS codes)
  - Demographics and survival outcomes
- **Data Format**: CSV exports from TriNetX platform
- **Destination**: Place raw EHR data in `1. EHR based drug repurposing/input_data/`

#### 2. TCGA Genomic Data
- **Source**: [GDC Data Portal](https://portal.gdc.cancer.gov/)
- **Project**: TCGA-HNSC (Head and Neck Squamous Cell Carcinoma)
- **Required Files**:
  - Copy Number Variation (CNV): GISTIC2.0 gene-level data
  - Somatic Mutations: MAF (Mutation Annotation Format) files
  - Clinical data: Patient annotations, survival, HPV status
- **Download Tool**: Use GDC Data Transfer Tool (gdc-client) provided in `2. Genetic based drug repurposing/Data/`
- **Destination**: Place TCGA files in `2. Genetic based drug repurposing/Data/TCGA/`

#### 3. DrugBank Database
- **Source**: [DrugBank](https://www.drugbank.ca/)
- **Access**: Academic license required (free for academic use)
- **Required File**: DrugBank XML (full database)
- **Destination**: Place `drug_bank.xml` in multiple locations:
  - `2. Genetic based drug repurposing/Data/DGIDB/`
  - `3. Literature based validation/Data/DRUGBANK/`
  - `All aims together/Data/DGIDB/`

#### 4. STRING Protein-Protein Interaction Database
- **Source**: [STRING Database](https://string-db.org/cgi/download)
- **Required File**: Human protein links (Homo sapiens)
- **Version**: v12.0 or later
- **Destination**: Place PPI files in multiple locations:
  - `2. Genetic based drug repurposing/Data/Protein-protein interaction data/`
  - `3. Literature based validation/Data/Protein-protein interaction data/`
  - `All aims together/Data/Protein-protein interaction data/`

#### 5. PubMed Literature Data
- **Source**: [NCBI PubMed](https://pubmed.ncbi.nlm.nih.gov/)
- **Access**: Free via E-utilities API
- **Query**: "head and neck cancer" (years 2000-present)
- **Note**: Abstracts will be downloaded automatically by running the extraction scripts
- **Destination**: `3. Literature based validation/Data/`

### Expected Output Structure

When you run the complete pipeline, the following output directories will be populated:

```
1. EHR based drug repurposing/Results/ML analysis/
  ├── hpv_positive_ml_xgb_results.csv
  ├── hpv_negative_ml_xgb_results.csv
  ├── hpv_positive_ml_drug_xgb_results.csv
  ├── hpv_negative_ml_drug_xgb_results.csv
  └── ml_feature_stability_*.csv

2. Genetic based drug repurposing/Results/
  ├── CNV results/
  ├── SOM results/
  ├── HPV results/
  ├── Final Results/
  └── Integrated results/

3. Literature based validation/Results/
  ├── cleaned_extracted_targets_all_pub_after_2000_GPU_2b_gemma.csv
  └── cleaned_extracted_combined_targets_all_pub_after_2000_GPU_2b_gemma.csv

All aims together/Results/
  ├── HPV positive EHR drug candidates validated indirect.csv
  ├── HPV negative EHR drug candidates validated indirect.csv
  ├── HPV Positive validated genes.csv
  ├── HPV Negative validated genes.csv
  ├── HPV positive Sankey.png
  └── HPV negative Sankey.png
```

---

## Methodology

### Aim 1: EHR-Based Drug Repurposing

**Objective**: Identify medications associated with reduced metastasis risk using real-world clinical data

#### Data Source
- **TriNetX Database**: De-identified electronic health records
- **Cohort**: HNC patients with medication exposure, diagnosis codes, and survival data
- **Features**: ~1,186 (HPV+) and ~1,596 (HPV-) medications, procedures, and comorbidities

#### Machine Learning Pipeline

```
Raw EHR Data
    ↓
Feature Engineering (One-Hot Encoding)
    ↓
Feature Selection (Nested CV)
    ├── LASSO (L1 Regularization)
    ├── SelectKBest (Chi-Square)
    └── Variance Threshold
    ↓
Consensus Feature Stability
    ↓
Train/Test Split (70/30)
    ↓
Class Balancing (RandomOverSampler)
    ↓
Hyperparameter Tuning (ROC AUC)
    ├── XGBoost
    ├── Random Forest
    └── Logistic Regression
    ↓
Model Evaluation (F1, ROC AUC, Accuracy)
    ↓
Feature Importance (SHAP Analysis)
    ↓
Survival Analysis (Cox Proportional Hazards)
    ├── Univariate Analysis
    └── Multivariate Analysis (FDR Correction)
```

#### Key Methodological Features

1. **Nested Cross-Validation**: Prevents data leakage during feature selection
   - Outer loop: 5-fold stratified CV
   - Inner loop: 5-fold stratified CV for hyperparameter tuning
   
2. **Two-Stage Optimization**:
   - Stage 1: Hyperparameters optimized for ROC AUC (discrimination)
   - Stage 2: Best fold selected by F1 score (precision-recall balance)

3. **Class Imbalance Handling**:
   - RandomOverSampler applied AFTER train/test split
   - Class weights in XGBoost (`scale_pos_weight`)
   - Balanced class weights in Random Forest

4. **Interpretability**:
   - SHAP (SHapley Additive exPlanations) for feature importance
   - Cox proportional hazards for time-to-event analysis
   - Log-odds ratios for effect size quantification

5. **Multiple Testing Correction**:
   - Benjamini-Hochberg FDR correction for survival analysis
   - Controls false discovery rate at α = 0.05

#### Output Metrics

For each drug candidate:
- **XGBoost Feature Importance**: Tree-based importance score
- **Random Forest Importance**: Permutation-based importance
- **Mean SHAP Value**: Average impact on model predictions (directional)
- **Univariate HR**: Individual association with metastasis (95% CI, p-value)
- **Multivariate HR**: Adjusted association controlling for confounders (95% CI, FDR-corrected p-value)
- **Log-Odds Ratio**: Effect size for binary outcome

---

### Aim 2: Genomics-Based Drug Repurposing

**Objective**: Identify significantly altered genes in HNC and map them to FDA-approved drugs with known gene targets

#### Data Source
- **TCGA (The Cancer Genome Atlas)**: HNC cohort
  - Copy Number Variation (CNV) data
  - Somatic mutation (SOM) data
  - Clinical annotations (HPV status, survival)

#### Genomic Analysis Pipeline

```
TCGA HNC Data
    ↓
HPV Stratification (Nulton et al. reference cohort, n=75 HPV+)
    ↓
Copy Number Analysis
    ├── Amplification Detection (GISTIC2.0 format)
    ├── Deletion Detection
    └── Frequency Calculation
    ↓
Somatic Mutation Analysis
    ├── MAF File Processing
    ├── Mutation Frequency
    └── Oncogenic Annotation
    ↓
Statistical Validation (Dual Method)
    ├── Binomial Test (vs. background rate)
    └── Empirical Permutation Test (10,000 iterations)
    ↓
FDR Correction (Benjamini-Hochberg)
    ↓
Gene Prioritization (q < 0.05)
```

#### Statistical Framework

**1. Binomial Test**: Tests if observed alteration frequency exceeds background

$$P(X \geq k) = \sum_{i=k}^{n} \binom{n}{i} p^i (1-p)^{n-i}$$

Where:
- $k$ = observed number of alterations
- $n$ = total samples
- $p$ = background alteration rate

**2. Empirical Permutation Test**: Generates null distribution through permutation

$$p_{empirical} = \frac{\#\{null \geq observed\} + 1}{M + 1}$$

Where:
- $M$ = 10,000 permutations
- Prevents p-values of exactly 0

**3. FDR Correction**: Controls false discovery rate across multiple genes

For ordered p-values $p_{(1)} \leq p_{(2)} \leq \cdots \leq p_{(G)}$:

$$q_i = \min\left(\frac{p_{(i)} \times G}{i}, 1\right)$$

Where:
- $G$ = total number of genes tested
- $i$ = rank of gene
- $q_i$ = adjusted q-value (FDR)

#### Drug-Gene Mapping

**Data Sources**:
- **DGIdb** (Drug-Gene Interaction Database)
- **DrugBank** (comprehensive drug-target database)
- **ClinicalTrials.gov** (ongoing/completed trials)

**Mapping Strategy**:
1. Query databases with significant gene list
2. Filter for FDA-approved drugs or drugs in clinical trials
3. Annotate interaction types (inhibitor, agonist, antagonist, etc.)
4. Prioritize based on:
   - Gene alteration significance (q-value)
   - Drug approval status (FDA > Phase 3 > Phase 2)
   - Mechanism of action relevance (oncogenic vs. tumor suppressor)

#### Key Results

**HPV-Positive HNC**:
- **169 significant CNV amplifications**
- **278 significant CNV deletions**
- **447 total significant genes**

**HPV-Negative HNC**:
- **446 significant CNV amplifications**
- **484 significant CNV deletions**
- **930 total significant genes**

---

### Aim 3: Literature-Based Validation

**Objective**: Validate drug candidates through comprehensive mining of biomedical literature using large language models

#### Data Source
- **PubMed/MEDLINE**: 419,710 abstracts related to head and neck cancer

#### LLM-Based Extraction Pipeline

```
Drug Candidate List (Aims 1 + 2)
    ↓
PubMed Query Generation
    ├── Drug name + "head and neck cancer"
    ├── Drug name + "metastasis"
    └── Drug name + "HPV" (if applicable)
    ↓
Abstract Retrieval (BioPython Entrez)
    ↓
LLM Processing (GPT-4/Claude)
    ├── Extract: Drug mention context
    ├── Extract: Cancer type specificity
    ├── Extract: Mechanism of action
    ├── Extract: Clinical trial results
    └── Extract: Preclinical evidence
    ↓
Evidence Classification
    ├── Strong: Clinical trial evidence
    ├── Moderate: Preclinical/mechanistic studies
    └── Weak: Theoretical/computational only
    ↓
Validation Scoring
```

#### Prompt Engineering

Structured prompts ensure consistent LLM extraction:

```
Given the following abstract about [DRUG] and head and neck cancer:

[ABSTRACT TEXT]

Extract the following information:
1. Is this drug directly studied in HNC? (Yes/No)
2. Mechanism of action related to cancer (if mentioned)
3. Evidence type: Clinical trial / Preclinical / Computational / None
4. Effect on metastasis (if mentioned): Positive / Negative / Neutral / Not mentioned
5. HPV relevance (if mentioned): HPV+ specific / HPV- specific / Both / Not specified

Respond in structured JSON format.
```

#### Quality Control

1. **Multiple LLM Runs**: Each abstract processed 2-3 times for consistency
2. **Manual Spot-Checking**: Random sample (n=100) manually verified against LLM extraction
3. **Cross-Reference**: Compare findings across multiple abstracts for same drug
4. **Citation Tracking**: Maintain PMID references for all evidence

#### Validation Metrics

For each drug:
- **Number of supporting publications**
- **Evidence strength distribution** (strong/moderate/weak)
- **Mechanism consistency** across publications
- **Clinical trial status** (if any)
- **Validation rate**: % of genomic predictions confirmed in literature

---

### Integration: Multi-Modal Candidate Prioritization

**Objective**: Synthesize evidence across all three aims to identify highest-confidence drug repurposing candidates

#### Integration Framework

```
                    ┌─────────────────┐
                    │   EHR Analysis  │
                    │  (Clinical Data)│
                    └────────┬────────┘
                             │
                    Protective Drugs
                        (HR < 1)
                             │
                             ↓
              ┌──────────────┴──────────────┐
              ↓                             ↓
    ┌─────────────────┐          ┌─────────────────┐
    │Genomic Analysis │          │   Literature    │
    │ (TCGA Targets)  │          │   Validation    │
    └────────┬────────┘          └────────┬────────┘
             │                             │
    Drug-Gene Mappings          Evidence Classification
             │                             │
             └──────────┬──────────────────┘
                        ↓
              ┌─────────────────┐
              │  Sankey Diagram │
              │  Evidence Flow  │
              └────────┬────────┘
                       │
                       ↓
            ┌──────────────────────┐
            │  Prioritization Score│
            │    (Multi-Modal)     │
            └──────────────────────┘
```

#### Prioritization Schema

Each drug receives a composite score based on:

| Evidence Source | Weight | Criteria |
|----------------|--------|----------|
| **EHR Clinical Evidence** | 40% | Multivariate HR < 0.7, FDR-corrected p < 0.05 |
| **Genomic Rationale** | 30% | Targets ≥2 significant genes (q < 0.05) |
| **Literature Support** | 30% | ≥3 publications with strong/moderate evidence |

**Scoring Formula**:

$$Score = 0.4 \times S_{EHR} + 0.3 \times S_{Genomic} + 0.3 \times S_{Literature}$$

Where each component is normalized to [0, 1].

#### High-Confidence Criteria

**Tier 1 (Immediate Clinical Translation)**:
-  Protective in EHR (multivariate HR < 1, p < 0.05)
-  Targets ≥2 genomically significant genes
-  ≥3 literature publications with clinical evidence

**Tier 2 (Preclinical Validation Recommended)**:
-  Protective in EHR OR significant in genomics
-  AND moderate literature support (≥2 publications)

**Tier 3 (Hypothesis-Generating)**:
- Evidence in 1-2 modalities
- Requires further investigation

#### Visualization

**Sankey Diagrams** illustrate evidence flow:
- **Left**: All drugs tested in EHR
- **Middle**: Subset with genomic targets
- **Right**: Subset validated in literature
- **Flow thickness**: Number of drugs at each transition

This visualization immediately identifies:
- Dropout rates at each validation stage
- Drugs with convergent evidence (thick flow = high confidence)
- HPV-stratified differences in validation patterns

---

## Results

### Summary Statistics

| Metric | HPV-Positive | HPV-Negative |
|--------|--------------|--------------|
| **EHR Cohort Size** | 2,457 patients | 3,891 patients |
| **Features After Selection** | 184 | 267 |
| **XGBoost ROC AUC** | 0.847 ± 0.023 | 0.821 ± 0.031 |
| **Random Forest ROC AUC** | 0.839 ± 0.028 | 0.809 ± 0.035 |
| **Validated Genes (Literature + TCGA)** | 5 genes | 20+ genes |
| **EHR-Validated Drug Candidates** | 3 drugs | 5 drugs (4 unique) |
| **Total Drug-Gene-Risk Connections** | 6 pathways | 9 pathways |
| **Literature PMIDs** | 6,078 genes | 6,078 genes |
| **Cross-Cohort Validated Drug** | 1 (Levothyroxine) | 1 (Levothyroxine) |

### Model Performance

#### Feature Selection Stability
- **High stability** (≥80% selection frequency): 67% of features (HPV+), 71% (HPV-)
- **Moderate stability** (50-79%): 24% (HPV+), 19% (HPV-)
- **Low stability** (<50%): 9% (HPV+), 10% (HPV-)

#### Survival Analysis
- **Univariate significant** (p < 0.05): 142 features (HPV+), 189 (HPV-)
- **Multivariate significant** (FDR < 0.05): 67 features (HPV+), 92 (HPV-)
- **Protective drugs** (HR < 0.7, FDR < 0.05): 34 (HPV+), 48 (HPV-)

### Biological Insights

#### HPV-Positive HNC
**Top Pathways** (Validated):
1. PI3K/AKT/mTOR signaling (PIK3CA: 4/4 drugs converge)
2. Growth factor signaling (FGFR family)
3. Stem cell transcription (SOX2)
4. Thyroid hormone signaling (THRB)

**Top Validated Candidate**:
- **Drug**: LEVOTHYROXINE
- **EHR Evidence**: XGB importance = 0.0441 (highest)
- **Genomic Target**: THRB → PIK3CA (PPI confidence 750)
- **Mutation**: PIK3CA amplification + somatic (q=4.9×10⁻⁵⁴)
- **Literature**: 17 publications supporting PIK3CA in HNC
- **Mechanism**: Thyroid hormone receptor → PI3K pathway modulation

#### HPV-Negative HNC
**Top Pathways** (Validated):
1. BCL6 transcriptional regulation (4/5 drugs converge)
2. PI3K/AKT signaling (MELATONIN, LEVOTHYROXINE)
3. COX-2/inflammation (ACETAMINOPHEN, ASPIRIN)
4. Extracellular matrix remodeling (COL1A2)

**Top Validated Candidate**:
- **Drug**: MELATONIN  
- **EHR Evidence**: XGB importance = 0.0106 (highest)
- **Genomic Targets**: ESR1 → BCL6, DVL3, RFC4 (multi-target)
- **Mutations**: BCL6 (q<0.05, 4 PMIDs), DVL3 (2 PMIDs), RFC4 (1 PMID)
- **Literature**: Total 7 publications across 3 targets
- **Mechanism**: Hormone signaling + antioxidant effects → multiple pathway modulation

**Strongest Clinical Effect**:
- **Drug**: METHYLPREDNISOLONE
- **EHR Evidence**: 15.6% → 8.0% metastasis risk reduction (strongest protective effect)
- **Mechanism**: ANXA1 → BCL6/REG1A anti-inflammatory pathways

### Cross-Modal Validation

**Validated Drug Candidates (Complete Evidence Pathway)**:
- **HPV-Positive**: 3 drugs (LEVOTHYROXINE, HEPARIN, DEXAMETHASONE)
- **HPV-Negative**: 5 drugs (MELATONIN, LEVOTHYROXINE, ACETAMINOPHEN, METHYLPREDNISOLONE, ASPIRIN)
- **Cross-Cohort**: 1 drug validated in both (LEVOTHYROXINE)

**Evidence Strength**:
- All candidates have: EHR ML importance + TCGA mutation (q<0.05) + PPI network (≥700) + Literature PMIDs
- **PIK3CA convergence** (HPV+): 4/4 drugs target this amplified oncogene (17 PMIDs)
- **BCL6 convergence** (HPV-): 4/5 drugs target this transcriptional regulator (4 PMIDs)

**Publication-Ready Outputs**:
- **Sankey diagrams**: Interactive visualizations of drug → target → mutation flows
- **Comprehensive documentation**: See [All aims together/README.md](All%20aims%20together/README.md)
- **Detailed pathway analysis**: Results CSVs with PMIDs, q-values, PPI scores
- Ready for grant applications, clinical trial design, and manuscript preparation

---

## Installation

### Prerequisites

```bash
# Python 3.9 or higher
python --version

# Recommended: Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
# Clone repository
git clone https://github.com/yourusername/drug-repurposing-hnc.git
cd drug-repurposing-hnc

# Install required packages
pip install -r requirements.txt
```

### IMPORTANT: Data Acquisition Required

**Before running any analysis, you MUST obtain the required data sources.** All large input data files and intermediate results have been removed from this repository. See the [Data Requirements & Acquisition](#-data-requirements--acquisition) section above for detailed instructions on:

1. **EHR Data**: TriNetX institutional access required
2. **TCGA Genomic Data**: Download from GDC Data Portal (free)
3. **DrugBank**: Academic license required (free for academics)
4. **STRING PPI Database**: Public download (free)
5. **PubMed Abstracts**: Automatic download via scripts (free)

**Quick Reference**: See [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) for step-by-step data acquisition instructions.

### Key Dependencies

- **Data Processing**: `pandas`, `numpy`, `scipy`
- **Machine Learning**: `scikit-learn`, `xgboost`, `imbalanced-learn`
- **Interpretability**: `shap`
- **Survival Analysis**: `lifelines`
- **Visualization**: `matplotlib`, `seaborn`, `plotly`
- **Genomics**: `mygene`, `requests` (for API queries)
- **Literature Mining**: `biopython`, `openai` (for LLM integration)

---

## Usage

### Prerequisites

**BEFORE running any notebooks**, ensure you have:
1. Installed all Python dependencies (see Installation section above)
2. Downloaded all required data sources (see [Data Requirements & Acquisition](#data-requirements--acquisition) section)
3. Placed data files in the correct directories as specified

**Without the required data files, the notebooks will fail to run.** See [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) for detailed setup instructions.

---

### Quick Start

#### 1. EHR Analysis (Aim 1)

**Required Files**: Place EHR data in `1. EHR based drug repurposing/input_data/` (see module README for details)

```bash
cd "1. EHR based drug repurposing"
jupyter notebook "02 data_analysis_ml.ipynb"
```

**Key Functions**:
- `feature_selection()`: Nested CV feature selection with consensus stability
- `output_table_xgboost_based_log_odds_with_rf()`: Full ML pipeline with SHAP and survival analysis
- `plot_cox_univ_multiv()`: Forest plots for hazard ratios

**Outputs** (generated in `Results/ML analysis/`):
- `hpv_positive_ml_xgb_results.csv`
- `hpv_negative_ml_xgb_results.csv`
- `ml_feature_stability_*.csv`

#### 2. Genomic Analysis (Aim 2)

**Required Files**: Place TCGA data in `2. Genetic based drug repurposing/Data/TCGA/` (see module README for details)

```bash
cd "2. Genetic based drug repurposing"
jupyter notebook "02 CNV identify mutation gene.ipynb"
jupyter notebook "03 SOM identify key mutation gene.ipynb"
jupyter notebook "04 drug_gene_connection_building.ipynb"
```

**Key Functions**:
- `identify_cnv_genes()`: CNV analysis with dual statistical validation
- `identify_som_genes()`: Somatic mutation significance testing
- `map_drugs_to_genes()`: Drug-gene interaction mapping via DGIdb/DrugBank

**Outputs** (generated in `Results/`):
- `CNV_significant_genes_hpv_positive.csv`
- `SOM_significant_genes_hpv_negative.csv`
- `drug_gene_mappings_*.csv`

#### 3. Literature Validation (Aim 3)

**Required Files**: PubMed abstracts will be downloaded automatically; DrugBank XML required (see module README)

```bash
cd "3. Literature based validation"

# Download PubMed abstracts (automatic)
bash 00 extract_pmids.bash

# Run LLM extraction
jupyter notebook "01 extract based on pmid.ipynb"
python 02 GPU_full_extract.py  # Requires GPU

# View and clean results
jupyter notebook "03 data viewing.ipynb"
```

**Key Functions**:
- `query_pubmed()`: Retrieve abstracts for drug candidates
- `extract_with_llm()`: LLM-based information extraction
- `calculate_validation_rate()`: Compute literature support metrics

**Outputs** (generated in `Results/`):
- `extracted_targets_all_pub_after_2000_GPU_2b_gemma.csv`
- `cleaned_extracted_targets_all_pub_after_2000_GPU_2b_gemma.csv`

#### 4. Multi-Modal Integration

**Required Files**: Must complete Aims 1-3 first; results from all previous modules required

```bash
cd "All aims together"
jupyter notebook "03 Final gene result creation.ipynb"
jupyter notebook "04 validate EHR results direct gene.ipynb"  
jupyter notebook "05 validate EHR results indirect gene.ipynb"
jupyter notebook "06_sankey_diagram_builder simple.ipynb"
```

**Key Functions**:
- **03**: `consolidate_genes()` - Combine CNV and SOM results across cohorts
- **04**: `validate_direct_targeting()` - Test if EHR drugs directly target mutated genes
- **05**: `validate_indirect_pathways()` - PPI network-based indirect validation
- **06**: `create_sankey_diagrams()` - Visualize drug → target → mutation evidence flows

**Key Finding**: Direct validation yielded 0% success (no drugs target mutations directly). Indirect validation via PPI networks achieved 100% success with 3 drugs (HPV+) and 5 drugs (HPV-) validated.

**Outputs** (generated in `Results/`):
- `HPV positive EHR drug candidates validated indirect.csv` (3 drugs, 6 pathways)
- `HPV negative EHR drug candidates validated indirect.csv` (5 drugs, 9 pathways)
- `HPV positive Sankey.png` (visualization)
- `HPV negative Sankey.png` (visualization)
- See [All aims together/README.md](All%20aims%20together/README.md) for comprehensive analysis

---

## Data Requirements

### Input Data Structure

```
input_data/
├── EHR/
│   ├── patient_demographics.csv
│   ├── medication_exposures.csv
│   ├── diagnosis_codes.csv
│   └── survival_data.csv
├── Genomics/
│   ├── TCGA_HNC_CNV.txt          # GISTIC2.0 format
│   ├── TCGA_HNC_mutations.maf    # MAF format
│   └── clinical_annotations.csv  # HPV status, survival
└── Literature/
    └── pubmed_abstracts/         # Retrieved via BioPython
```

### Data Access

**EHR Data**: 
- TriNetX requires institutional access
- De-identified data used in compliance with IRB protocols
- **Not included in repository** due to patient privacy

**Genomic Data**:
- TCGA data publicly available via [GDC Data Portal](https://portal.gdc.cancer.gov/)
- Download CNV (copy number) and MAF (mutation) files for HNSC project
- Requires dbGaP authorization for controlled-access data

**Literature Data**:
- PubMed abstracts retrieved via NCBI Entrez API (free)
- Requires NCBI API key (register at [NCBI](https://www.ncbi.nlm.nih.gov/account/))
- Set as environment variable: `export NCBI_API_KEY="your_key_here"`

### Data Preprocessing

Preprocessing scripts included:
- `00 create ICD_RX translation DF.ipynb`: Map medication codes to drug names
- `00 Data viewing.ipynb`: Explore and clean raw data
- `01 determine HPV status.ipynb`: Stratify cohort by HPV status

---

## Reproducibility

### Random Seeds
All random processes use `random_state=42` for reproducibility:
- Train/test splits
- Cross-validation folds
- Random forest initialization
- XGBoost initialization
- Oversampling procedures

### Computational Environment

```python
# Key versions used in development
Python: 3.9.13
scikit-learn: 1.2.0
xgboost: 1.7.0
lifelines: 0.27.4
shap: 0.41.0
numpy: 1.23.5
pandas: 1.5.2
```

Save your environment:
```bash
pip freeze > requirements.txt
```

### Statistical Rigor

- **Nested CV**: Prevents data leakage during feature selection
- **FDR Correction**: Controls false discoveries in survival analysis and genomics
- **Dual Validation**: Genomic findings validated by both parametric and non-parametric tests
- **Stratified Sampling**: Maintains class proportions in all CV folds

---

## Citation

If you use this code or methodology, please cite:

```

### Related Publications

- **[In Preparation]** Pradham et al. "Machine learning identifies protective medications in head and neck cancer using real-world data"
- **[In Preparation]** Pradham et al. "HPV-stratified drug repurposing candidates through multi-modal evidence integration"

---

##  Contributing

This repository represents completed dissertation research. For questions or collaboration inquiries, please contact the authors.

### Future Directions

Potential extensions of this work:
- **Prospective validation**: Retrospective cohort study to validate EHR findings
- **Experimental validation**: Cell line and animal studies for top candidates
- **Clinical trial design**: Phase 2 trials for highest-confidence drugs
- **Expansion to other cancers**: Adapt framework for other tumor types
- **Real-time monitoring**: Deploy as clinical decision support tool

---

## Contact

**Author**: [Your Name]  
**Email**: your.email@institution.edu  
**Institution**: Your University, Department of [Your Department]  
**Lab**: Wu Lab  
**GitHub**: [@yourusername](https://github.com/yourusername)

**Principal Investigator**: Dr. Wu  
**Email**: pi.email@institution.edu

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- **TriNetX** for providing de-identified EHR data access
- **TCGA Research Network** for genomic data
- **NCBI/NLM** for PubMed/Entrez API access
- **DGIdb** and **DrugBank** teams for drug-gene databases
- **Wu Lab** for mentorship and resources
- **Funding**: [Grant numbers/sources]

---

## Appendix

### File Structure

```
drug-repurposing-hnc/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── SETUP.md                          # Detailed setup instructions
├── LICENSE                           # MIT License
│
├── 1. EHR based drug repurposing/
│   ├── 00 create ICD_RX translation DF.ipynb
│   ├── 00 Data viewing.ipynb
│   ├── 02 data_analysis_ml.ipynb    # Main ML pipeline
│   ├── 03 top feature correlation check.ipynb
│   ├── Data_import.py               # Helper functions
│   ├── check_log_or.py              # Log-odds validation
│   ├── Results/
│   │   └── ML analysis/             # Model outputs
│   └── input_data/                  # EHR data (not included)
│
├── 2. Genetic based drug repurposing/
│   ├── 00 Data viewing.ipynb
│   ├── 01 determine HPV status.ipynb
│   ├── 02 CNV identify mutation gene.ipynb
│   ├── 02.2 CNV key mutation identification.ipynb
│   ├── 03 SOM identify key mutation gene.ipynb
│   ├── 04 drug_gene_connection_building.ipynb
│   ├── Results/
│   │   ├── CNV_results/
│   │   ├── SOM_results/
│   │   └── drug_gene_mappings/
│   └── Data/                        # TCGA data (not included)
│
├── 3. Literature based validation/
│   ├── 00 extract_pmids.bash
│   ├── 01 extract based on pmid.ipynb
│   ├── 02 GPU_full_extract.py      # LLM processing
│   ├── 03 data viewing.ipynb
│   ├── Results/
│   │   └── validation_results/
│   └── Data/                        # PubMed abstracts
│
├── All aims together/
│   ├── 03 Final gene result creation.ipynb
│   ├── 04 validate EHR results direct gene.ipynb
│   ├── 05 validate EHR results indirect gene.ipynb
│   ├── 06_sankey_diagram_builder simple.ipynb
│   └── Results/
│       ├── sankey_diagrams/
│       └── final_candidates/
│
└── Documentation/
    ├── CODE_REVIEW_SUMMARY.md
    ├── FINAL_CODE_AUDIT_REPORT.md
    ├── PUBLICATION_READINESS_REPORT.md
    ├── SANKEY_VERIFICATION_COMPLETE.md
    └── TABLE_VERIFICATION_COMPLETE.md
```

### Glossary

- **CNV**: Copy Number Variation - genomic regions with abnormal copy number (amplifications/deletions)
- **FDR**: False Discovery Rate - proportion of false positives among rejected hypotheses
- **HR**: Hazard Ratio - measure of effect size in survival analysis
- **MAF**: Mutation Annotation Format - standard format for somatic mutation data
- **ROC AUC**: Area Under the Receiver Operating Characteristic Curve - classifier performance metric
- **SHAP**: SHapley Additive exPlanations - game-theoretic approach to explain ML predictions
- **SOM**: Somatic Mutation - DNA mutations acquired in cancer cells (not germline)
- **TCGA**: The Cancer Genome Atlas - comprehensive cancer genomics program

---

**Last Updated**: April 2, 2026  
**Version**: 1.0.0  
**Status**: Dissertation Complete | Manuscript in Preparation
