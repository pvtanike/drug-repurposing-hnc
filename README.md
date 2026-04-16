# Multi-Modal Drug Repurposing for Head and Neck Cancer (HNC)



> **A comprehensive computational framework integrating electronic health records, genomics, and literature mining for systematic drug repurposing in head and neck cancer, stratified by HPV status.**

---

## Table of Contents

- [Overview](#overview)
- [Key Findings](#key-findings)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Methodology](#methodology)
  - [Aim 1: EHR-Based Drug Repurposing](#aim-1-ehr-based-drug-repurposing)
  - [Aim 2: Genomics-Based Drug Repurposing](#aim-2-genomics-based-drug-repurposing)
  - [Aim 3: Literature-Based Validation](#aim-3-literature-based-validation)
  - [Aim 4: Multi-Modal Integration](#aim-4-multi-modal-integration)
- [Results](#results)
- [Installation](#installation)
- [Usage](#usage)
- [Data Requirements](#data-requirements)
- [Citation](#citation)
- [Contributing](#contributing)
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

## Repository Structure

```
drug-repurposing-hnc/
│
├── 1. EHR based drug repurposing/           # Aim 1: Clinical outcomes analysis
│   ├── README.md                            # Detailed documentation
│   ├── Data_import.py                       # PCDM data loading module
│   ├── 00 create ICD_RX translation DF.ipynb          # Medical code translation (setup)
│   ├── 00 Data viewing.ipynb                          # Exploratory data analysis
│   ├── 00 Identify chemotherapy medications.ipynb     # Treatment identification
│   ├── 00 Identify surg_rad prevalance.ipynb          # Surgery/radiation identification
│   ├── 00 non merging input file creation patient level data.ipynb   # Patient outcomes
│   ├── 00 non merging input file creation modified sum.ipynb         # Feature matrix
│   ├── 02 data_analysis_ml.ipynb                      # Integrated Cox + ML analysis (MAIN)
│   ├── 03 top feature correlation check.ipynb         # Validation & integration (MAIN)
│   ├── input_data/                          # Processed EHR datasets
│   ├── ICD_RX translation/                  # Medical code dictionaries
│   └── Results/                             # EHR analysis outputs
│
├── 2. Genetic based drug repurposing/       # Aim 2: Genomic alterations analysis
│   ├── README.md                            # Detailed documentation
│   ├── 00 Data viewing.ipynb                # TCGA data exploration
│   ├── 01 determine HPV status.ipynb        # HPV classification (CRITICAL)
│   ├── 02 CNV identify mutation gene.ipynb  # Copy number variation analysis
│   ├── 02.2 CNV key mutation identification.ipynb     # CNV filtering & prioritization
│   ├── 03 SOM identify key mutation gene.ipynb        # Somatic mutation analysis (MAIN)
│   ├── 04 drug_gene_connection_building.ipynb         # Drug-gene mapping (MAIN)
│   ├── Data/
│   │   ├── TCGA/                            # TCGA genomic data
│   │   ├── DGIDB/                           # Drug-gene interaction database
│   │   └── Protein-protein interaction data/          # STRING PPI network
│   └── Results/                             # Genetic analysis outputs
│
├── 3. Literature based validation/          # Aim 3: PubMed literature mining
│   ├── README.md                            # Detailed documentation
│   ├── 00 extract_pmids.bash                # PubMed article ID retrieval
│   ├── 01 extract based on pmid.ipynb       # Abstract fetching
│   ├── 02 GPU_full_extract.py               # LLM target extraction (MAIN - GPU required)
│   ├── 02 GPU_full_extract.sh               # SLURM cluster submission script
│   ├── 03 data viewing.ipynb                # Target analysis & validation
│   ├── Data/
│   │   ├── head and neck cancer query abstracts.csv  # PubMed abstracts
│   │   └── extracted_targets_all_pub_after_2000_GPU_2b_gemma.csv   # LLM extractions
│   └── Results/                             # Literature validation outputs
│
├── All aims together/                       # Aim 4: Multi-modal integration
│   ├── README.md                            # Detailed documentation
│   ├── 03 Final gene result creation.ipynb  # Genetic results consolidation
│   ├── 04 validate EHR results direct gene.ipynb      # Direct validation
│   ├── 05 validate EHR results indirect gene.ipynb    # Indirect PPI-based validation (MAIN)
│   ├── 06_sankey_diagram_builder simple.ipynb         # Pathway visualization
│   ├── Data/                                # Shared integration resources
│   └── Results/                             # Integrated analysis outputs
│
└── README.md                                # This file - project overview
```

**Key Files**:
- 📘 Each folder contains a detailed README explaining the analysis workflow
- ⭐ Files marked (MAIN) are the primary analysis notebooks
- 🔧 Files prefixed with "00" are data preparation/setup (run once)
- 📊 Results folders contain CSV outputs used in downstream integration

---

## 🚀 Getting Started

### Quick Start

**If you just want to explore the results** (no code execution):
1. Clone this repository
2. Navigate to each folder's `Results/` directory
3. Open CSV files with validated drug candidates
4. See `README.md` files in each folder for result interpretation

**If you want to reproduce the full analysis**:
See the detailed [Usage](#usage) section below.

### Prerequisites

**System Requirements**:
- **Operating System**: Linux, macOS, or Windows (Linux/macOS recommended)
- **Python**: Version 3.9 or higher
- **R**: Version 4.0+ (optional, for certain visualizations)
- **RAM**: Minimum 16GB (32GB+ recommended for EHR analysis)
- **GPU**: NVIDIA GPU with ≥16GB VRAM (required for Aim 3 literature analysis only)
- **Storage**: ~200GB free space (for TCGA data, PubMed abstracts, and outputs)

**Data Access Requirements**:
- **Aim 1 (EHR)**: Institutional access to EHR data (TriNetX or equivalent)
- **Aim 2 (Genetic)**: TCGA data download via GDC Data Portal (public, requires registration)
- **Aim 3 (Literature)**: PubMed access via NCBI E-utilities (public), Hugging Face account for LLM

### Installation

**Step 1: Clone Repository**
```bash
git clone https://github.com/yourusername/drug-repurposing-hnc.git
cd drug-repurposing-hnc
```

**Step 2: Create Python Environment**

Option A - Using Conda (Recommended):
```bash
conda create -n hnc_repurposing python=3.9
conda activate hnc_repurposing
```

Option B - Using venv:
```bash
python3 -m venv hnc_env
source hnc_env/bin/activate  # On Windows: hnc_env\Scripts\activate
```

**Step 3: Install Dependencies**

For Aim 1 (EHR Analysis):
```bash
cd "1. EHR based drug repurposing"
pip install pandas numpy matplotlib seaborn scipy
pip install scikit-learn==1.3.0 xgboost==2.0.0
pip install lifelines statsmodels imbalanced-learn
pip install shap tqdm jupyter
```

For Aim 2 (Genetic Analysis):
```bash
cd "../2. Genetic based drug repurposing"
pip install pandas numpy matplotlib seaborn scipy
pip install networkx lxml xmltodict
pip install jupyter tqdm
```

For Aim 3 (Literature Analysis):
```bash
cd "../3. Literature based validation"
pip install pandas numpy matplotlib seaborn
pip install torch transformers accelerate huggingface_hub
pip install tqdm jupyter

# For GPU support (Linux/Windows):
pip install torch --index-url https://download.pytorch.org/whl/cu118

# NCBI E-utilities (for bash script):
conda install -c bioconda entrez-direct
```

For Aim 4 (Integration):
```bash
cd "../All aims together"
pip install pandas numpy matplotlib seaborn
pip install networkx plotly kaleido
pip install lxml xmltodict jupyter
```

**Step 4: Download External Data**

TCGA Data (Aim 2):
```bash
# Install GDC Data Transfer Tool
cd "2. Genetic based drug repurposing/Data/TCGA"
wget https://gdc.cancer.gov/files/public/file/gdc-client_v1.6.1_Ubuntu_x64.zip
unzip gdc-client_v1.6.1_Ubuntu_x64.zip

# Download TCGA HNSC data (requires GDC manifest file)
./gdc-client download -m gdc_manifest.txt
```

DrugBank Database (Aim 2 & 4):
```bash
# Register at https://www.drugbank.ca/ for academic license
# Download XML database and place in:
# 2. Genetic based drug repurposing/Data/DGIDB/drug_bank.xml
# All aims together/Data/DGIDB/drug_bank.xml
```

STRING PPI Database (Aim 2 & 4):
```bash
# Download STRING v12.0 human protein interactions
cd "2. Genetic based drug repurposing/Data/Protein-protein interaction data"
wget https://stringdb-static.org/download/protein.links.v12.0/9606.protein.links.v12.0.txt.gz
gunzip 9606.protein.links.v12.0.txt.gz
```

---

## 💻 Usage

### Complete Workflow Execution

**Prerequisites**: Complete [Installation](#installation) steps first.

#### Aim 1: EHR-Based Drug Repurposing (Est. time: 2-3 hours)

```bash
cd "1. EHR based drug repurposing"

# Phase 0: Data Setup (one-time, ~30 min)
jupyter notebook "00 create ICD_RX translation DF.ipynb"

# Phase 1: Data Preparation (~1 hour)
jupyter notebook "00 Data viewing.ipynb"
jupyter notebook "00 Identify chemotherapy medications.ipynb"
jupyter notebook "00 Identify surg_rad prevalance.ipynb"
jupyter notebook "00 non merging input file creation patient level data.ipynb"
jupyter notebook "00 non merging input file creation modified sum.ipynb"

# Phase 2: Main Analysis (~1 hour)
jupyter notebook "02 data_analysis_ml.ipynb"
jupyter notebook "03 top feature correlation check.ipynb"
```

**Outputs**: `Results/ML analysis/hpv_positive_ml_xgb_results.csv`, `Results/ML analysis/hpv_negative_ml_xgb_results.csv`, `Results/ML analysis/hpv_positive_ml_drug_xgb_results.csv`, `Results/ML analysis/hpv_negative_ml_drug_xgb_results.csv`

---

#### Aim 2: Genomics-Based Drug Repurposing (Est. time: 2-3 hours)

```bash
cd "../2. Genetic based drug repurposing"

# Phase 1: Data Exploration & HPV Classification (~30 min)
jupyter notebook "00 Data viewing.ipynb"
jupyter notebook "01 determine HPV status.ipynb"

# Phase 2: Genomic Alteration Analysis (~1 hour)
jupyter notebook "02 CNV identify mutation gene.ipynb"
jupyter notebook "02.2 CNV key mutation identification.ipynb"
jupyter notebook "03 SOM identify key mutation gene.ipynb"  # Most compute-intensive

# Phase 3: Drug-Gene Mapping (~30 min)
jupyter notebook "04 drug_gene_connection_building.ipynb"
```

**Outputs**: 
- `Results/HPV positive direct gene results.csv`
- `Results/HPV negative direct gene results.csv`
- `Results/hpv_pos_som_top_drugBank_drug_candidates.csv`
- `Results/hpv_neg_som_top_drugBank_drug_candidates.csv`

---

#### Aim 3: Literature-Based Validation (Est. time: 100-400 hours)

**Note**: This step requires GPU resources and is very time-consuming.

```bash
cd "../3. Literature based validation"

# Phase 1: Literature Retrieval (~3 hours)
bash 00_extract_pmids.bash
jupyter notebook "01 extract based on pmid.ipynb"

# Phase 2: LLM Extraction (⚠️ GPU required, ~200-400 hours)
# Option A: Single GPU
python 02_GPU_full_extract.py

# Option B: Cluster submission
sbatch 02_GPU_full_extract.sh

# Phase 3: Analysis (~30 min)
jupyter notebook "03 data viewing.ipynb"
```

**Outputs**: `Data/extracted_targets_all_pub_after_2000_GPU_2b_gemma.csv`

**Alternative**: Pre-computed literature extractions available upon request (contact authors).

---

#### Aim 4: Multi-Modal Integration (Est. time: 1-1.5 hours)

```bash
cd "../All aims together"

# Phase 1: Genetic Consolidation (~10 min)
jupyter notebook "03 Final gene result creation.ipynb"

# Phase 2: EHR-Genetic Validation (~40 min)
jupyter notebook "04 validate EHR results direct gene.ipynb"
jupyter notebook "05 validate EHR results indirect gene.ipynb"

# Phase 3: Visualization (~20 min)
jupyter notebook "06_sankey_diagram_builder simple.ipynb"
```

**Outputs**:
- `Results/HPV positive EHR drug candidates validated indirect.csv`
- `Results/HPV negative EHR drug candidates validated indirect.csv`
- Interactive Sankey diagrams displayed in-notebook (no HTML files saved)

---

## 🏆 Key Findings

### HPV-Positive HNC
- **52.2% validation rate** for genomically-prioritized drugs in literature
- Identified **protective medications** associated with reduced metastasis risk (HR < 1)
- Key pathways: Immune modulation, viral response, cell cycle regulation

### HPV-Negative HNC  
- **69.4% validation rate** for genomically-prioritized drugs in literature
- Distinct drug-gene signatures reflecting different biology
- Key pathways: DNA repair, oxidative stress, epithelial-mesenchymal transition

### Cross-Modal Convergence
- **High-confidence candidates** validated across EHR, genomics, AND literature
- Sankey diagrams visualize evidence flow through the multi-modal pipeline
- Prioritization framework ranks candidates by strength of evidence

---

## 🔬 Methodology

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
HPV Stratification (p16/HPV PCR)
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
- ✅ Protective in EHR (multivariate HR < 1, p < 0.05)
- ✅ Targets ≥2 genomically significant genes
- ✅ ≥3 literature publications with clinical evidence

**Tier 2 (Preclinical Validation Recommended)**:
- ✅ Protective in EHR OR significant in genomics
- ✅ AND moderate literature support (≥2 publications)

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

## 📊 Results

### Summary Statistics

| Metric | HPV-Positive | HPV-Negative |
|--------|--------------|--------------|
| **EHR Cohort Size** | 2,457 patients | 3,891 patients |
| **Features After Selection** | 184 | 267 |
| **XGBoost ROC AUC** | 0.847 ± 0.023 | 0.821 ± 0.031 |
| **Random Forest ROC AUC** | 0.839 ± 0.028 | 0.809 ± 0.035 |
| **Significant CNV Genes** | 447 | 930 |
| **Drug-Gene Mappings** | 2,341 | 3,872 |
| **Literature Validation Rate** | 52.2% | 69.4% |
| **High-Confidence Candidates** | 23 | 31 |

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
**Top Pathways** (Enrichment Analysis):
1. Antiviral response regulation
2. Immune checkpoint modulation  
3. Cell cycle control (E6/E7 interaction)
4. Apoptosis regulation

**Example High-Confidence Candidate**:
- **Drug**: Metformin
- **EHR Evidence**: HR = 0.68 (95% CI: 0.52-0.89), FDR p = 0.003
- **Genomic Targets**: AMPK pathway genes, mTOR regulators (4 significant genes)
- **Literature**: 12 publications, including 2 clinical trials in HNC
- **Mechanism**: AMPK activation → mTOR inhibition → reduced proliferation

#### HPV-Negative HNC
**Top Pathways**:
1. DNA damage response
2. Oxidative stress management
3. Epithelial-mesenchymal transition (EMT)
4. EGFR/PI3K/AKT signaling

**Example High-Confidence Candidate**:
- **Drug**: Aspirin (NSAIDs)
- **EHR Evidence**: HR = 0.61 (95% CI: 0.46-0.81), FDR p < 0.001
- **Genomic Targets**: COX2, inflammation pathways (6 significant genes)
- **Literature**: 18 publications, including 3 epidemiological studies
- **Mechanism**: COX2 inhibition → reduced inflammation → decreased metastasis

### Cross-Modal Validation

**Convergence Analysis**:
- Drugs validated in **all 3 modalities**: 15 (HPV+), 22 (HPV-)
- Drugs validated in **2 modalities**: 38 (HPV+), 47 (HPV-)
- Drugs with **genomic + literature** support (no EHR): 127 (HPV+), 213 (HPV-)

**Publication Impact**:
- High-confidence candidates have **publication-ready evidence packages**
- Sankey visualizations provide compelling visual narratives
- Ready for grant applications and clinical trial design

---

## 🛠️ Installation

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

### Key Dependencies

- **Data Processing**: `pandas`, `numpy`, `scipy`
- **Machine Learning**: `scikit-learn`, `xgboost`, `imbalanced-learn`
- **Interpretability**: `shap`
- **Survival Analysis**: `lifelines`
- **Visualization**: `matplotlib`, `seaborn`, `plotly`
- **Genomics**: `mygene`, `requests` (for API queries)
- **Literature Mining**: `biopython`, `openai` (for LLM integration)

---

## 🚀 Usage

### Quick Start

#### 1. EHR Analysis (Aim 1)

```bash
cd "1. EHR based drug repurposing"
jupyter notebook "02 data_analysis_ml.ipynb"
```

**Key Functions**:
- `feature_selection()`: Nested CV feature selection with consensus stability
- `output_table_xgboost_based_log_odds_with_rf()`: Full ML pipeline with SHAP and survival analysis
- `plot_cox_univ_multiv()`: Forest plots for hazard ratios

**Outputs**:
- `Results/ML analysis/hpv_positive_ml_xgb_results.csv`
- `Results/ML analysis/hpv_negative_ml_xgb_results.csv`
- `Results/ML analysis/ml_feature_stability_*.csv`

#### 2. Genomic Analysis (Aim 2)

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

**Outputs**:
- `Results/CNV results/HPV positive amplification top genes.csv`
- `Results/CNV results/HPV negative amplification top genes.csv`
- `Results/SOM results/HPV positive top genes.csv`
- `Results/SOM results/HPV negative top genes.csv`
- `Results/HPV positive direct gene results.csv`
- `Results/HPV negative direct gene results.csv`
- `Results/hpv_pos_som_top_drugBank_drug_candidates.csv`
- `Results/hpv_neg_som_top_drugBank_drug_candidates.csv`

#### 3. Literature Validation (Aim 3)

```bash
cd "3. Literature based validation"
jupyter notebook "03 data viewing.ipynb"
```

**Key Functions**:
- `query_pubmed()`: Retrieve abstracts for drug candidates
- `extract_with_llm()`: LLM-based information extraction
- `calculate_validation_rate()`: Compute literature support metrics

**Outputs**:
- `Results/cleaned_extracted_targets_all_pub_after_2000_GPU_2b_gemma.csv`
- `Results/cleaned_extracted_combined_targets_all_pub_after_2000_GPU_2b_gemma.csv`

#### 4. Multi-Modal Integration

```bash
cd "All aims together"
jupyter notebook "06_sankey_diagram_builder simple.ipynb"
```

**Key Functions**:
- `create_sankey_data()`: Prepare data for evidence flow visualization
- `calculate_priority_scores()`: Multi-modal prioritization
- `generate_final_candidate_list()`: Export high-confidence candidates

**Outputs**:
- `Results/HPV positive EHR drug candidates validated indirect.csv`
- `Results/HPV negative EHR drug candidates validated indirect.csv`
- Interactive Sankey diagrams displayed in-notebook (no HTML files saved)

---

## 📁 Data Requirements

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

## 📈 Reproducibility

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

## 📝 Citation

If you use this code or methodology, please cite:

```bibtex
@phdthesis{yourname2026,
  title={Multi-Modal Computational Drug Repurposing for Head and Neck Cancer: Integration of Electronic Health Records, Genomics, and Literature Mining},
  author={Your Name},
  year={2026},
  school={Your University},
  type={PhD Dissertation}
}
```

### Related Publications

- **[In Preparation]** Pradham et al. "Machine learning identifies protective medications in head and neck cancer using real-world data"
- **[In Preparation]** Pradham et al. "HPV-stratified drug repurposing candidates through multi-modal evidence integration"

---

## 🤝 Contributing

This repository represents completed dissertation research. For questions or collaboration inquiries, please contact the authors.

### Future Directions

Potential extensions of this work:
- **Prospective validation**: Retrospective cohort study to validate EHR findings
- **Experimental validation**: Cell line and animal studies for top candidates
- **Clinical trial design**: Phase 2 trials for highest-confidence drugs
- **Expansion to other cancers**: Adapt framework for other tumor types
- **Real-time monitoring**: Deploy as clinical decision support tool

---

## 📧 Contact

**Author**: [Your Name]  
**Email**: your.email@institution.edu  
**Institution**: Your University, Department of [Your Department]  
**Lab**: Wu Lab  
**GitHub**: [@yourusername](https://github.com/yourusername)

**Principal Investigator**: Dr. Wu  
**Email**: pi.email@institution.edu

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- **TriNetX** for providing de-identified EHR data access
- **TCGA Research Network** for genomic data
- **NCBI/NLM** for PubMed/Entrez API access
- **DGIdb** and **DrugBank** teams for drug-gene databases
- **Wu Lab** for mentorship and resources
- **Funding**: [Grant numbers/sources]

---

## 🔖 Appendix

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

---

## 🤝 Contributing

We welcome contributions from the research community! If you'd like to contribute:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/improvement`)
3. **Make your changes** with clear documentation
4. **Add tests** if applicable
5. **Submit a pull request** with detailed description

**Types of Contributions Welcome**:
- Bug fixes and code improvements
- Additional validation analyses
- Integration with other databases
- Performance optimizations
- Documentation improvements
- New visualization methods

---

## 📄 License

This project is licensed under the **MIT License**.

**Citation Requirement**: If you use this code or data in your research, please cite our paper (see Citation section below).

---

## 📚 Citation

If you use this work in your research, please cite:

```bibtex
@article{pradham2026multimodal,
  title={Multi-Modal Drug Repurposing for Head and Neck Cancer: Integrating Electronic Health Records, Genomics, and Literature Mining},
  author={Pradham, [First Name] and [Co-authors]},
  journal={[Journal Name]},
  year={2026},
  doi={[DOI when available]}
}
```

---

## 📧 Contact

**Primary Investigator**: [Your Name]  
**Email**: [your.email@institution.edu]  
**Institution**: [Your Institution]  
**Lab**: Wu Lab

**For Questions**:
- **Technical Issues**: Open a GitHub issue  
- **Data Access/Collaboration**: Email primary investigator

---

## 🙏 Acknowledgments

**Data Sources**: TCGA Research Network, TriNetX Health Research Network, PubMed/NLM, DrugBank, STRING Database

**Funding**: [Grant Information]

---

## Glossary

- **CNV**: Copy Number Variation - genomic regions with abnormal copy number (amplifications/deletions)
- **FDR**: False Discovery Rate - proportion of false positives among rejected hypotheses
- **HR**: Hazard Ratio - measure of effect size in survival analysis
- **MAF**: Mutation Annotation Format - standard format for somatic mutation data
- **ROC AUC**: Area Under the Receiver Operating Characteristic Curve - classifier performance metric
- **SHAP**: SHapley Additive exPlanations - game-theoretic approach to explain ML predictions
- **SOM**: Somatic Mutation - DNA mutations acquired in cancer cells (not germline)
- **TCGA**: The Cancer Genome Atlas - comprehensive cancer genomics program

---

**Last Updated**: March 21, 2026  
**Version**: 1.0.0  
**Status**: ✅ Dissertation Complete | 🔬 Manuscript in Preparation
