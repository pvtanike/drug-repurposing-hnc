
---
# Genetic-Based Drug Repurposing for Head and Neck Cancer

**Last Updated**: April 2, 2026

## Executive Summary

**Goal**: Identify significantly mutated genes in HNC and map them to druggable targets via protein-protein interaction networks.

**Key Results**:
- **HPV-Positive**: 5 literature-validated genes (PIK3CA, SOX2, CLDN1, RFC4, TLR7)
- **HPV-Negative**: 20+ literature-validated genes (TP53, PIK3CA, CDKN2A, BCL6, and others)
- **Statistical Validation**: Dual framework (binomial + empirical permutation, both q<0.05)
- **Drug-Gene Network**: DrugBank + STRING PPI (confidence ≥700) for indirect targeting

**Key Finding**: Direct drug-gene targeting failed (0% success) because most mutations are "undruggable". PPI network-based indirect targeting achieved 100% success.

**See Integration**: [All aims together/](../All%20aims%20together/) for validated drug candidates

---

## Overview

This module identifies drug repurposing candidates through comprehensive analysis of genomic alterations in head and neck squamous cell carcinoma (HNSC), using TCGA data to detect significantly mutated and copy number-altered genes, followed by literature validation, protein-protein interaction network expansion, and systematic drug-gene mapping using DrugBank. The analysis is stratified by HPV status to account for distinct tumor biology.

---

## Data Acquisition & Setup

**IMPORTANT: Genomic data files have been removed from this repository due to size and data sharing restrictions. You must obtain the following data:**

### Required Data Sources

#### 1. TCGA-HNSC Genomic Data
- **Source**: GDC Data Portal
- **Website**: [https://portal.gdc.cancer.gov/](https://portal.gdc.cancer.gov/)
- **Project**: TCGA-HNSC (Head and Neck Squamous Cell Carcinoma)

**Required Files:**
- **Copy Number Variation (CNV)**:
  - File type: GISTIC2.0 gene-level copy number data
  - Format: TSV with genes × samples
  - Location in portal: CNV → Gene Level → GISTIC2
  
- **Somatic Mutations**:
  - File type: Masked Somatic Mutation (MAF format)
  - Format: MAF (Mutation Annotation Format)
  - Location in portal: Simple Nucleotide Variation → Masked Somatic Mutation
  
- **Clinical Data**:
  - File type: Clinical Supplement
  - Required fields: Patient ID, HPV status, survival data

**Download Instructions:**
```bash
cd "2. Genetic based drug repurposing/Data"

# Use the provided gdc-client tool
./gdc-client download -m <manifest_file.txt>

# Alternative: Download via GDC Portal web interface
# 1. Go to https://portal.gdc.cancer.gov/
# 2. Select Projects → TCGA-HNSC
# 3. Download CNV (GISTIC2), MAF files, and clinical data
# 4. Place files in Data/TCGA/ directory
```

**Where to place files**: `2. Genetic based drug repurposing/Data/TCGA/`

#### 2. DrugBank Database
- **Source**: DrugBank
- **Website**: [https://www.drugbank.ca/](https://www.drugbank.ca/)
- **Access**: Free academic license (registration required)
- **Required File**: Full DrugBank XML database
- **Download**: 
  1. Register for academic account
  2. Navigate to Downloads → Full Database
  3. Download XML format
- **Where to place**: `2. Genetic based drug repurposing/Data/DGIDB/drug_bank.xml`

#### 3. STRING Protein-Protein Interaction Database
- **Source**: STRING Database
- **Website**: [https://string-db.org/cgi/download](https://string-db.org/cgi/download)
- **Species**: Homo sapiens (taxonomy ID: 9606)
- **Required File**: Protein links (physical and functional interactions)
- **File name**: `9606.protein.links.v12.0.txt.gz`
- **Where to place**: `2. Genetic based drug repurposing/Data/Protein-protein interaction data/`

#### 4. Supplementary Data (Nulton et al.)
- **Source**: Nulton TJ et al. publication supplementary materials
- **Purpose**: HPV status validation and reference mutation data
- **Where to place**: `2. Genetic based drug repurposing/Data/Supplementary data Nulton/`
- **Note**: Available from original publication or contact authors

### Expected Output Structure

When you run the analysis notebooks in order, the following results will be generated:

```
Results/
├── HPV results/
│   ├── HPV_positive_samples.csv              # List of HPV+ patient IDs
│   └── HPV_negative_samples.csv              # List of HPV- patient IDs
│
├── CNV results/
│   ├── hpv_positive_cnv_amplifications.csv   # Significant amplifications
│   ├── hpv_positive_cnv_deletions.csv        # Significant deletions
│   ├── hpv_negative_cnv_amplifications.csv
│   └── hpv_negative_cnv_deletions.csv
│
├── SOM results/
│   ├── hpv_positive_somatic_mutations.csv    # Significantly mutated genes
│   └── hpv_negative_somatic_mutations.csv
│
├── Final Results/
│   ├── HPV_positive_literature_validated_genes.csv
│   └── HPV_negative_literature_validated_genes.csv
│
└── Integrated results/
    ├── hpv_positive_drug_gene_connections.csv     # Drug-target mappings
    ├── hpv_negative_drug_gene_connections.csv
    ├── hpv_positive_ppi_expanded_network.csv      # PPI network results
    └── hpv_negative_ppi_expanded_network.csv
```

---

## Scientific Rationale

Head and neck cancers exhibit profound genomic heterogeneity with distinct mutation profiles between HPV-positive and HPV-negative tumors. By identifying genes with recurrent genomic alterations (amplifications, deletions, somatic mutations) significantly exceeding random expectation, we can pinpoint dysregulated pathways that represent druggable targets. Integration with literature-validated protein-protein interaction networks enables expansion beyond directly mutated genes to functionally connected pathways, dramatically increasing the therapeutic target space. Systematic mapping to DrugBank identifies FDA-approved and investigational agents targeting these networks, providing a rational basis for drug repurposing.

---

## Methods

### 1. Data Sources

**TCGA Genomic Data (HNSC Cohort):**
- **Copy Number Variation (CNV):** Gene-level copy number values (gistic2 data)
  - Thresholds: High-level amplification (CN > 4), High-level deletion (CN < 1)
  - CNV values capped at 7 to prevent outlier effects
- **Somatic Mutations:** MAF format mutation calls from Nulton et al. supplementary data
  - Filtered to non-synonymous mutations (frame shifts, indels, missense, nonsense, splice site)
  - Gene length normalization using GENCODE v48 CDS annotations

**HPV Status Determination:**
- Based on literature-curated HPV+ case IDs from Nulton et al.
- HPV-positive: 75 patients identified from paper as highly validated HPV+ cases
- HPV-negative: remaining TCGA HNSC patients not in the HPV+ reference set
- Final cohorts: HPV-positive (n=75), HPV-negative (remaining patients)

**Literature Validation:**
- PubMed literature mining for gene-disease associations
- PMIDs extracted for each candidate gene
- Only literature-supported genes retained for downstream analysis

**Protein-Protein Interaction (PPI) Network:**
- **Database:** STRING v12.0 (human protein interactions, 11.8M interactions)
- **Confidence Threshold:** Combined score ≥ 700 (high confidence)
- **Purpose:** Expand from directly altered genes to functionally connected pathway components

**Drug-Gene Interaction Database:**
- **DrugBank XML:** 9,368 unique drugs, 4,187 target genes, 23,136 drug-gene interactions
- **Drug Types:** FDA-approved, investigational, experimental, nutraceuticals
- **Target Information:** Enzyme, carrier, transporter, and target gene relationships

---

### 2. Copy Number Variation (CNV) Analysis

**Statistical Framework - Dual Validation:**

**A. Binomial Test:**
Tests whether CNV events in a gene exceed random expectation based on genome-wide CNV instability.

- **Null Hypothesis:** CNV events are randomly distributed proportional to background CNV rate
- **Background Rate Calculation:** 
  ```
  p_null = (total high-level CNV events genome-wide) / (total genes × patients)
  ```
- **Test Statistic:** 
  ```
  P(X ≥ x) = Σ(k=x to n) [C(n,k) × p_null^k × (1-p_null)^(n-k)]
  ```
  where x = observed CNV events in gene, n = number of patients

**B. Empirical/Permutation Test:**
Data-driven validation through simulation.

- **Procedure:** 1,000 permutations sampling CNV values with replacement
- **Null Distribution:** Generated by randomly permuting patient-level CNV assignments
- **P-value:** Proportion of permutations with CNV frequency ≥ observed

**C. Multiple Testing Correction:**
- Benjamini-Hochberg False Discovery Rate (FDR) correction
- **Threshold:** q-value < 0.05 for both binomial and empirical tests

**D. Gene Prioritization Score:**
GISTIC-like composite scoring:
```
CNV_Score = Frequency_Percentage × Normalized_Intensity
```
- **Frequency:** Percentage of patients with high-level CNV
- **Intensity:** Average copy number among affected patients

---

### 3. Somatic Mutation (SOM) Analysis

**Mutation Filtering:**
- **Included:** Frame shift insertions/deletions, in-frame indels, missense, nonsense, nonstop, splice site, translation start site mutations
- **Excluded:** Synonymous mutations (for test set), intronic variants
- **Total mutations analyzed:** All mutations including synonymous used for background rate calculation

**Gene Length Normalization:**
Critical for accounting for mutational target size bias.

- **Gene Lengths:** Coding sequence (CDS) lengths from GENCODE v48 GTF annotation
- **Probability Adjustment:** 
  ```
  P(mutation in gene_i) = L_i / Σ(all L)
  ```
  where L_i = coding sequence length of gene i

**Statistical Framework - Dual Validation:**

**A. Binomial Test (Length-Adjusted):**
Tests whether non-synonymous mutations in a gene exceed random expectation based on gene length and genome-wide mutation rate.

- **Null Hypothesis:** Mutations distributed proportional to gene length
- **Probability Calculation:**
  ```
  p_i = CDS_length_i / total_CDS_length
  ```
- **Test:** Binomial test of observed non-synonymous mutations vs. expected under null
- **Background Denominator:** Total mutations (synonymous + non-synonymous) to accurately capture genome-wide mutation rate. This provides stable background estimation and tests whether non-synonymous mutations deviate from overall mutational processes.
- **Rationale:** Using all mutations in the denominator establishes the true genome-wide mutational load, while testing non-synonymous mutations specifically targets functionally relevant alterations. This approach accounts for regional mutation rate variation and mutational processes affecting both synonymous and non-synonymous sites.

**B. Multinomial/Monte Carlo Test:**
Empirical validation using data-driven simulation with focus on functional mutation landscape.

- **Procedure:** 10,000 Monte Carlo simulations
- **Distribution:** Multinomial with probabilities proportional to gene lengths
- **Total Mutations Simulated:** Match observed non-synonymous mutation burden only
- **Null Distribution:** Generated from the empirical distribution of non-synonymous mutations, as these represent the functionally relevant mutational landscape
- **P-value:** Proportion of simulations with mutation count ≥ observed
- **Rationale:** This empirical test validates against the observed non-synonymous mutation distribution, providing complementary evidence that gene-specific enrichment persists even when accounting for the functional mutation landscape.

**Dual-Validation Framework Rationale:**
The intentional use of different denominators (all mutations for binomial, non-synonymous only for multinomial) provides **complementary validation** with distinct null hypotheses. The binomial test assesses deviation from genome-wide mutation patterns considering all mutational processes, while the empirical test validates enrichment against the functional mutation landscape. Both tests use gene length normalization, but different denominators enable: (1) binomial test captures whether a gene shows excess functional mutations relative to its overall mutational exposure, and (2) empirical test confirms enrichment persists when compared specifically against other genes' functional mutation patterns. Genes passing both statistical frameworks (q<0.05 for both tests) demonstrate robust evidence of positive selection and biological significance, substantially reducing false positive discoveries that might arise from single-method approaches.

**C. Composite Mutation Score:**
Integrates mutation frequency and significance:
```
Mutation_Score = (Observed_Count / Expected_Count) × Frequency_Percentage
```

**D. Filtering Criteria (HPV-Stratified):**

**HPV-Positive:**
- Frequency ≥ 5% of patients
- Mutation score ≥ 0.002
- Both q-values (binomial and empirical) < 0.05

**HPV-Negative:**
- Frequency ≥ 0.01% of patients (more permissive due to larger cohort)
- Both q-values < 0.05
- No minimum mutation score threshold

---

### 4. Literature Validation

**PubMed Literature Mining:**
- **Query Strategy:** Gene symbol + "head and neck cancer"
- **Extraction:** PMIDs for publications mentioning each candidate gene
- **Documentation:** PMID count and specific article IDs stored
- **Validation Threshold:** At least 1 literature mention required for gene retention

**Purpose:**
- Ensures genes have documented relevance to head and neck cancer biology
- Filters out passenger mutations with no known disease association
- Provides mechanistic support for gene-cancer relationships

---

### 5. Protein-Protein Interaction (PPI) Network Expansion

**Rationale:**
Directly mutated genes represent the tip of dysregulated pathways. Expanding to PPI network neighbors identifies additional therapeutic targets within the same biological modules.

**Network Construction:**
- **Database:** STRING v12.0
- **Edge Filtering:** Combined confidence score ≥ 700 (high confidence interactions)
- **Confidence Score Components:**
  - Text mining evidence
  - Experimental evidence
  - Database knowledge
  - Co-expression correlation
  - Neighborhood evidence (genomic context)
  - Gene fusion evidence
  - Co-occurrence across species

**Expansion Algorithm:**
1. **Seed Genes:** Literature-validated genes with significant CNV or somatic mutations
2. **Network Query:** For each seed gene, retrieve all PPI partners with STRING score ≥ 700
3. **Secondary Validation:** Filter PPI partners to those also found in HNC literature
4. **Network Pruning:** Retain only literature-validated connections to ensure biological relevance

**Network Statistics:**
- **HPV-Negative:** 21 seed genes → expanded networks (varies by gene)
  - Example: TP53 network → 64 connected genes
  - Example: PIK3CA network → 66 connected genes
- **HPV-Positive:** 5 seed genes → expanded networks
  - Example: SOX2 network → 40 connected genes
  - Example: PIK3CA network → 66 connected genes

---

### 6. Drug-Gene Connection Building

**DrugBank Mapping:**

**Direct Pathway:**
- Drugs directly targeting seed genes (CNV/mutation-altered genes)
- Relationship types: Target, enzyme, carrier, transporter

**Indirect Pathway:**
- Drugs targeting PPI network neighbors
- Multi-step pathway: Drug → Gene_Target → PPI → Seed_Gene
- All intermediate genes must be literature-validated

**Drug-Gene Connection Methodology:**

**A. Direct DrugBank Mapping:**
For each statistically significant gene (passing both binomial and empirical tests with FDR q<0.05):
- Query DrugBank database for drugs targeting the gene
- Extract drug name, target gene, action mechanism, and functional annotations
- No enrichment testing - direct one-to-one mapping

**B. PPI Network Expansion:**
- Expand significant genes through STRING database PPI network
- Filter PPI interactions to combined_score ≥ 700 (high confidence)
- Identify drugs targeting PPI neighbor genes (indirect connections)
- Pathway structure: Drug → PPI_Neighbor_Gene → Risk_Gene

**C. Literature Validation (Aim 3 Integration):**
- All pathway components (target genes and risk genes) must have literature support
- Literature validation uses LLM-extracted genes from 419,710 PubMed abstracts
- Filter: NUMBER_OF_ARTICLES > 0 for both target and root genes
- Ensures biological plausibility beyond computational prediction

**Drug Candidate Prioritization:**
Drugs ranked by:
1. Number of pathway connections to mutation networks
2. XGBoost feature importance from EHR analysis (Aim 1 integration)
3. Number of distinct risk genes connected
4. Pathway length (direct > 1-hop indirect)

---

### 7. Integration with EHR Data

**Cross-Validation Approach:**
Drugs identified through genetic analysis are cross-referenced with EHR-derived protective medications.

**Integration Algorithm:**
1. **EHR Drug Import:** Machine learning-derived drug importance scores from Aim 1
2. **DrugBank Mapping:** Map EHR drugs to DrugBank target genes
3. **Network Tracing:** Trace paths from drug targets → PPI network (STRING ≥700) → mutation genes
4. **Literature Validation:** Verify all pathway components (target and root genes) have literature support (NUMBER_OF_ARTICLES > 0)
5. **Connection Documentation:** Preserve complete pathway with PMIDs for both levels

**Drug Validation Criteria:**
For a drug to be considered fully validated, it must satisfy:
- Identified in EHR analysis with positive XGBoost feature importance (protective association)
- Target gene connected via high-confidence PPI (STRING combined_score ≥700) to risk gene
- Both target gene AND risk gene have literature support (at least 1 PMID each)
- Risk gene passes dual statistical validation (binomial FDR q<0.05 AND empirical FDR q<0.05)
```

**Validation Criteria:**
- Complete literature-validated pathway from drug → target → PPI → mutation gene
- Statistical significance for genetic alteration (q < 0.05)
- XGBoost feature importance > 0.005 (or top features for HPV+)
- Literature support (PMIDs) for all pathway components

---

## Key Results

### HPV-Negative Head and Neck Cancer

**Genomic Landscape:**
- **21 Significantly Altered Genes** (dual statistical validation)
- **Mutation Types:** 9 somatic, 8 amplifications, 1 amplification+somatic, 1 deletion+somatic, 1 deletion

**Top Altered Genes (with literature support):**
1. **TP53** (29 PMIDs) - Somatic mutations - Tumor suppressor
   - Network: 64 connected genes including EGFR, EZH2, TOP1, PTEN
2. **PIK3CA** (17 PMIDs) - Amplification + Somatic - PI3K catalytic subunit
   - Network: 66 connected genes
   - Central node in oncogenic signaling
3. **CDKN2A** (16 PMIDs) - Deletion + Somatic - Cell cycle regulator
   - Loss of p16INK4a tumor suppressor
4. **EPHA2** (5 PMIDs) - Somatic - Receptor tyrosine kinase
5. **BCL6** (4 PMIDs) - Amplification - Transcriptional repressor

**Other Key Genes:**
- **Oncogenes:** EGFR, CCND1, MYC (amplifications)
- **Tumor Suppressors:** PTEN, RB1, CDKN2B, NOTCH1
- **Cell Signaling:** HRAS, NFE2L2, FAT1, CASP8, EP300

**DrugBank Drug Candidates:**
- **Total:** 666 drug-gene-target combinations
- **Unique Drugs:** ~200+ candidates

**Top Drug Classes:**
1. **Tyrosine Kinase Inhibitors:**
   - **Fostamatinib** (SYK inhibitor) - Dominant candidate with 47+ pathway connections
   - Regorafenib, Sorafenib, Ponatinib, Lenvatinib
   - Targets: EGFR, IGF1R, ROS1, AXL pathways

2. **FGFR Inhibitors:**
   - Erdafitinib, Pemigatinib, Infigratinib, Nintedanib
   - Targets: FGFR1/2/3 pathways

3. **Multi-Kinase Inhibitors:**
   - Targeting PIK3CA network, cell cycle checkpoints

**EHR-Validated Drug Candidates (11 validated pathways, 5 unique drugs):**

1. **MELATONIN** (XGBoost importance: 0.0106)
   - Target: ESR1 (estrogen receptor alpha)
   - Pathway: ESR1 → BCL6, DVL3, RFC4 (all amplified)
   - Cox HR: 0.950 (5.0% risk reduction, p=0.001)
   - Mechanism: Hormone receptor modulation, antioxidant effects

2. **LEVOTHYROXINE** (XGBoost importance: 0.0050)
   - Targets: ITGAV, ITGB3, THRB
   - Pathway: THRB → COL1A2 (somatic), BCL6, RFC4 (amplifications)
   - Cox HR: 0.931 (6.9% risk reduction, p<0.001)
   - **Only drug validated in BOTH HPV cohorts**

3. **METHYLPREDNISOLONE** (XGBoost importance: 0.0043)
   - Target: ANXA1 (Annexin A1)
   - Pathway: ANXA1 → REG1A (somatic), BCL6 (amplification)
   - Cox HR: 0.844 → 0.920 (15.6% → 8.0% risk reduction after adjustment)
   - **Strongest protective association in entire study**

4. **ACETAMINOPHEN** (XGBoost importance: 0.0045)
   - Target: PTGS2 (COX-2)
   - Pathway: PTGS2 → BCL6 (amplification)
   - Cox HR: 0.979 (2.1% risk reduction, p<0.001)

5. **ASPIRIN** (XGBoost importance: 0.0033)
   - Target: PTGS2 (COX-2)
   - Pathway: PTGS2 → BCL6 (amplification)
   - Cox HR: 0.969 (3.1% risk reduction, p=0.194)
   - Mechanism: COX-2 inhibition, anti-inflammatory

**Additional Validated Candidates:**
- **Folic Acid:** TYMS → RAC1, BCL6
- **Heparin:** Multiple FGFR connections

---

### HPV-Positive Head and Neck Cancer

**Genomic Landscape:**
- **5 Significantly Altered Genes** (dual statistical validation)
- **Mutation Types:** 3 amplifications, 1 amplification+somatic, 1 deletion
- Smaller mutation signature reflects HPV-driven oncogenic mechanisms

**Significantly Altered Genes (with literature support):**
1. **PIK3CA** (17 PMIDs) - Amplification + Somatic
   - Network: 66 connected genes
   - **Most significant:** q = 4.9×10⁻⁵⁴ (binomial test)
2. **SOX2** (1 PMID) - Amplification
   - Stem cell transcription factor
   - Network: 40 connected genes
   - q = 1.3×10⁻⁵⁵
3. **CLDN1** (2 PMIDs) - Amplification
   - Tight junction protein
4. **RFC4** (1 PMID) - Amplification
   - DNA replication factor C subunit 4
5. **TLR7** (1 PMID) - Deletion
   - Toll-like receptor 7 (innate immunity)

**DrugBank Drug Candidates:**
- **Total:** 518 drug-gene-target combinations
- **Unique Drugs:** ~150+ candidates
- Similar kinase inhibitor profile to HPV-negative but fewer total candidates

**Top Drug Classes:**
1. **Tyrosine Kinase Inhibitors:**
   - Fostamatinib (dominant candidate)
   - JAK Inhibitors: Ruxolitinib, Tofacitinib, Baricitinib
   
2. **FGFR Inhibitors:**
   - Erdafitinib, Pemigatinib, Infigratinib

3. **PI3K/AKT/mTOR Pathway Inhibitors:**
   - Targeting PIK3CA network

**EHR-Validated Drug Candidates (8 validated pathways, 4 unique drugs):**

1. **LEVOTHYROXINE** (XGBoost importance: 0.0441)
   - Target: THRB (thyroid hormone receptor beta)
   - Pathway: THRB → PIK3CA (amplification+somatic)
   - Cox HR: 0.931 (6.9% risk reduction, p<0.001)
   - **Highest ML importance in HPV-positive cohort**
   - **Validated in both HPV+ and HPV- cohorts**

2. **HEPARIN** (XGBoost importance: 0.0096)
   - Targets: FGFR1, FGFR2, FGFR4, FGF4
   - Pathways: 
     - FGFR1/2/4 → PIK3CA (amplification+somatic)
     - FGF4 → SOX2 (amplification)
   - Cox HR: Not available (underpowered in HPV+ cohort)
   - Mechanism: FGF signaling modulation

3. **DEXAMETHASONE** (XGBoost importance: 0.0081)
   - Target: ANXA1 (Annexin A1)
   - Pathway: ANXA1 → SOX2 (amplification, q=1.3×10⁻⁵⁵)
   - Mechanism: Anti-inflammatory, immune modulation

4. **FOLIC ACID** (XGBoost importance: 0.0)
   - Target: TYMS (thymidylate synthase)
   - Pathway: TYMS → RFC4 (amplification)
   - Mechanism: DNA synthesis pathway modulation

---

## Biological Pathways Implicated

### 1. **PI3K/AKT/mTOR Signaling** (Both HPV Groups)
- **Central Node:** PIK3CA (amplification + somatic mutations)
- **Drugs:** Levothyroxine (via THRB), Heparin (via FGFRs)
- **Function:** Cell growth, proliferation, survival, metabolism
- **Dysregulation:** Oncogenic activation in both HPV+ and HPV- HNC

### 2. **Cell Cycle Regulation** (Primarily HPV-Negative)
- **Genes:** CDKN2A, CDKN2B (deletions), TP53 (mutations)
- **Function:** G1/S checkpoint control, p53-mediated apoptosis
- **Dysregulation:** Loss of tumor suppressors enabling uncontrolled proliferation

### 3. **Inflammation and Immune Response**
- **Drugs:** Methylprednisolone, Dexamethasone → ANXA1
- **Pathways:** REG1A, BCL6, SOX2 (HPV-specific)
- **Function:** Inflammatory signaling, immune cell recruitment
- **Clinical Relevance:** Anti-inflammatory effects may reduce tumor-promoting inflammation

### 4. **DNA Replication and Repair**
- **Gene:** RFC4 (amplification in both cohorts)
- **Drug:** Folic Acid → TYMS → RFC4
- **Function:** DNA replication factor complex, cell division
- **Dysregulation:** Amplification suggests replication stress

### 5. **Stem Cell and Developmental Pathways**
- **HPV-Positive:** SOX2 amplification (pluripotency transcription factor)
- **HPV-Negative:** DVL3 amplification (WNT/β-catenin signaling)
- **Clinical Relevance:** Stem cell markers associated with tumor initiation and therapy resistance

### 6. **Growth Factor Signaling**
- **Pathway:** Heparin → FGFRs → PIK3CA/SOX2
- **Function:** FGF-mediated angiogenesis, proliferation
- **Dysregulation:** Amplification of FGF receptors and downstream targets

### 7. **Transcriptional Regulation**
- **Genes:** BCL6 (transcriptional repressor), TP53 (transcription factor)
- **Drugs:** Multiple drugs converge on BCL6 (acetaminophen, aspirin, melatonin)
- **Function:** Gene expression control, apoptosis regulation

---

## Discussion

### Integration of Genetic and Clinical Evidence

This analysis successfully integrated three independent data streams to identify high-confidence drug repurposing candidates:

1. **TCGA Genomic Data:** Identified genes with statistically significant genomic alterations
2. **DrugBank:** Mapped FDA-approved/investigational drugs to genetic targets
3. **EHR Clinical Outcomes:** Validated drugs associated with improved survival in real-world patients
4. **Literature Mining:** Ensured all pathway components documented in HNC research

The convergence of genetic mechanisms with clinical outcomes provides the strongest evidence for drug repurposing, as it demonstrates both:
- **Biological plausibility:** Drugs target pathways disrupted by genomic alterations
- **Clinical efficacy:** Drugs associated with improved outcomes in patient populations

### Priority Drug Candidates

**Tier 1 - Highest Confidence (Validated Across Multiple Modalities):**

1. **LEVOTHYROXINE**
   - **Evidence:** Only drug validated in BOTH HPV+ and HPV- cohorts
   - **Mechanism:** THRB → PIK3CA (HPV+), THRB → COL1A2/BCL6/RFC4 (HPV-)
   - **Clinical:** Significant protection in both cohorts (HR=0.931, p<0.001)
   - **Safety:** FDA-approved, well-tolerated, inexpensive
   - **Pathway:** Thyroid hormone signaling → PI3K/AKT pathway modulation
   - **Rationale:** Thyroid hormone receptors modulate metabolism and cell proliferation; disruption of THRB signaling may alter PI3K pathway activation

2. **METHYLPREDNISOLONE** (HPV-Negative)
   - **Evidence:** Strongest protective association in entire study
   - **Mechanism:** ANXA1 → REG1A (somatic), BCL6 (amplification)
   - **Clinical:** 15.6% univariate risk reduction, maintains 8.0% after adjustment
   - **Safety:** FDA-approved corticosteroid, established safety profile
   - **Pathway:** Anti-inflammatory via annexin A1
   - **Rationale:** Chronic inflammation promotes tumor progression; anti-inflammatory effects may reduce tumor-promoting cytokine signaling

**Tier 2 - Strong Evidence (Genetic + Clinical Validation):**

3. **MELATONIN** (HPV-Negative)
   - **Mechanism:** ESR1 → BCL6, DVL3, RFC4
   - **Clinical:** 5.0% risk reduction (p=0.001)
   - **Safety:** OTC supplement, excellent safety profile
   - **Pathway:** Hormone receptor modulation, antioxidant effects
   - **Rationale:** Antioxidant properties reduce oxidative DNA damage; circadian rhythm regulation affects cell cycle

4. **HEPARIN** (HPV-Positive)
   - **Mechanism:** FGFR1/2/4, FGF4 → PIK3CA, SOX2
   - **Clinical:** XGBoost importance 0.0096
   - **Safety:** FDA-approved anticoagulant
   - **Pathway:** FGF signaling modulation
   - **Rationale:** FGFs promote angiogenesis and proliferation; heparin may block FGF-receptor interactions

**Tier 3 - Supporting Evidence:**

5. **ACETAMINOPHEN** (Both cohorts)
   - Validated in both HPV groups through PTGS2 → BCL6
   - Modest but consistent protective associations
   - Widespread use, excellent safety profile

6. **ASPIRIN** (HPV-Negative)
   - COX-2 inhibition pathway
   - Established chemoprevention literature
   - Anti-inflammatory mechanisms

7. **FOLIC ACID** (Both cohorts)
   - DNA synthesis pathway
   - Nutritional support during cancer treatment
   - Validated connections to RFC4

### HPV-Specific Therapeutic Strategies

**HPV-Negative:**
- **Broader mutation landscape** (21 genes) suggests more therapeutic targets
- **TP53-centric pathways:** Loss of p53 tumor suppressor function is central
- **Immune/inflammatory modulation:** Methylprednisolone shows strongest effects
- **Multiple pathway convergence:** Several drugs converge on BCL6 amplification

**HPV-Positive:**
- **Focused mutation profile** (5 genes) centered on PIK3CA and SOX2
- **PI3K pathway dominance:** PIK3CA amplification+somatic is primary target
- **Stem cell pathways:** SOX2 amplification suggests targeting stemness
- **Levothyroxine shows highest importance:** THRB → PIK3CA pathway

### Biological Mechanisms

**PI3K/AKT/mTOR Axis (Central to Both HPV Groups):**
- PIK3CA alterations activate downstream AKT/mTOR signaling
- Promotes cell growth, survival, proliferation, and metabolism
- Levothyroxine may modulate this pathway via thyroid hormone receptor crosstalk
- Heparin may affect upstream FGF receptor activation

**Inflammation and Tumor Microenvironment:**
- Chronic inflammation promotes tumor progression via cytokines, growth factors
- ANXA1 (annexin A1) is anti-inflammatory mediator
- Methylprednisolone/dexamethasone enhance ANXA1 activity
- May reduce tumor-promoting inflammatory signaling

**Cell Cycle Dysregulation:**
- Loss of CDKN2A/CDKN2B removes G1/S checkpoint control
- TP53 mutations eliminate p53-mediated cell cycle arrest and apoptosis
- Targeting downstream pathways (BCL6, RFC4) may compensate for lost checkpoints

**DNA Replication Stress:**
- RFC4 amplification suggests increased replication machinery demand
- Folic acid → TYMS pathway supports DNA synthesis
- May reflect dependency on nucleotide biosynthesis pathways

### Comparison with Prior Literature

**Levothyroxine and Thyroid Hormones:**
- Previous studies show thyroid hormone signaling affects cell proliferation and metabolism
- Hypothyroidism associated with altered cancer risk in some studies
- Our findings suggest thyroid hormone pathway modulation may affect HNC progression via PI3K signaling

**Corticosteroids in Cancer:**
- Historically used for symptom management (nausea, edema)
- Emerging evidence for direct anti-tumor effects via immune modulation
- Our analysis provides genomic-level mechanistic support (ANXA1 pathway)

**Melatonin as Anti-Cancer Agent:**
- Extensive literature on antioxidant and circadian rhythm effects
- Some clinical trials in various cancers show benefit
- Our genetic validation (ESR1 → BCL6/DVL3/RFC4) provides novel mechanistic insights

**FGFR Inhibitors and Heparin:**
- FGFR amplifications documented in subset of HNCs
- Clinical trials of FGFR inhibitors ongoing
- Heparin's anti-FGF activity provides mechanistic rationale for repurposing

### Study Strengths

1. **Multi-Modal Validation:**
   - Genomic alterations (TCGA)
   - Clinical outcomes (EHR)
   - Literature validation (PubMed)
   - Biological pathways (STRING PPI)
   - Drug-gene connections (DrugBank)

2. **Dual Statistical Testing:**
   - Both parametric (binomial) and non-parametric (empirical permutation) tests
   - FDR correction throughout for multiple testing
   - Robust to statistical assumptions

3. **HPV Stratification:**
   - Recognizes fundamental biological differences between HPV+ and HPV- HNC
   - Enables precision medicine approach
   - Identifies shared (levothyroxine) and specific (methylprednisolone, heparin) targets

4. **Literature Grounding:**
   - All genes and pathway components supported by published literature
   - PMIDs documented for verification
   - Reduces false positives from spurious statistical associations

5. **Clinical Actionability:**
   - Focus on FDA-approved or well-characterized drugs
   - Prioritizes drugs with established safety profiles
   - Immediate translational potential

### Limitations and Future Directions

**Limitations:**

1. **Sample Size Constraints:**
   - HPV-positive cohort smaller → fewer validated candidates
   - Some promising drugs (metformin, losartan) excluded due to data sparsity
   - Limited statistical power for rare mutations

2. **Observational Nature:**
   - EHR data is retrospective and observational
   - Cannot establish causality definitively
   - Confounding by indication possible despite adjustment

3. **Pathway Complexity:**
   - PPI networks may include indirect or context-dependent interactions
   - STRING confidence scores are estimates, not absolute measures
   - Tissue-specific pathway activity not captured

4. **Mutation Heterogeneity:**
   - Tumor heterogeneity not fully captured in bulk TCGA data
   - Subclonal mutations may be missed
   - Temporal evolution of mutations not tracked

**Future Directions:**

1. **Prospective Clinical Validation:**
   - Phase II clinical trials for top candidates (levothyroxine, methylprednisolone)
   - Randomized controlled trials to establish causality
   - Biomarker-stratified trials (HPV status, mutation profiles)

2. **Mechanistic Studies:**
   - Cell line experiments with levothyroxine in PIK3CA-mutant HNC cells
   - Animal models to validate protective effects
   - Molecular pathway profiling (phospho-proteomics) to confirm mechanism

3. **Expanded Genomic Analysis:**
   - Single-cell sequencing to capture heterogeneity
   - Whole-genome sequencing for non-coding alterations
   - Mutational signature analysis (APOBEC, smoking, HPV)

4. **Combination Therapy Studies:**
   - Synergy testing between repurposed drugs
   - Combination with standard chemotherapy/radiation
   - Personalized regimens based on mutation profiles

5. **Pharmacokinetic Optimization:**
   - Dose-finding studies for repurposed indications
   - Tissue distribution and tumor penetration studies
   - Formulation optimization for cancer treatment

6. **Biomarker Development:**
   - Mutation-based patient selection criteria
   - Predictive biomarkers for drug response
   - Resistance mechanism identification

---

## Conclusions

This comprehensive genetic analysis identified **levothyroxine** and **methylprednisolone** as the highest-priority drug repurposing candidates for head and neck cancer, with validation across genomic alterations, clinical outcomes, and biological pathway networks.

**Key Findings:**

1. **HPV-Negative HNC:** 930 significantly altered genes (23 literature-validated) converging on TP53, PIK3CA, and CDKN2A pathways; methylprednisolone shows strongest protective association (15.6% risk reduction)

2. **HPV-Positive HNC:** 447 significantly altered genes (8 literature-validated) dominated by PIK3CA and SOX2; levothyroxine shows highest machine learning importance (0.0441)

3. **Cross-HPV Candidate:** Levothyroxine is the only drug validated in both cohorts, targeting the PI3K pathway via thyroid hormone receptor signaling

4. **Mechanistic Validation:** All drug candidates have complete literature-validated pathways from drug targets → PPI networks → genomically altered genes

5. **Clinical Actionability:** All priority candidates are FDA-approved with established safety profiles, enabling rapid clinical translation

**Clinical Implications:**

The convergence of genetic evidence (TCGA), clinical outcomes (EHR), and biological pathways (PPI networks) provides strong rationale for prospective clinical trials of levothyroxine and methylprednisolone as adjuvant therapies in head and neck cancer, stratified by HPV status and mutation profiles.

**Next Steps:**

Initiation of phase II clinical trials to validate protective effects and elucidate mechanisms of action, with particular focus on levothyroxine in HPV-positive patients with PIK3CA alterations and methylprednisolone in HPV-negative patients with inflammatory pathway dysregulation.

---

## File Structure

```
2. Genetic based drug repurposing/
├── 00 Data viewing.ipynb                     # Initial data exploration
├── 01 determine HPV status.ipynb             # HPV classification from Nulton et al. reference cohort
├── 02 CNV identify mutation gene.ipynb       # Copy number variation analysis
├── 02.2 CNV key mutation identification.ipynb # CNV statistical validation
├── 03 SOM identify key mutation gene.ipynb   # Somatic mutation analysis
├── 04 drug_gene_connection_building.ipynb    # DrugBank mapping and validation
│
├── Results/
│   ├── HPV negative direct gene results.csv   # HPV- genes
│   ├── HPV positive direct gene results.csv   # HPV+ genes
│   ├── HPV negative indirect gene results.csv # HPV- PPI expansion
│   ├── HPV positive indirect gene results.csv # HPV+ PPI expansion
│   ├── hpv_neg_som_top_drugBank_drug_candidates.csv # DrugBank candidates (HPV-)
│   ├── hpv_pos_som_top_drugBank_drug_candidates.csv # DrugBank candidates (HPV+)
│   ├── Final Results/                          # hpv_positive_ehr_genetic_overlap_grouped.csv, etc.
│   ├── Integrated results/                     # hpv_positive_indirect_ehr_overlap.csv, etc.
│   ├── CNV results/  # Copy number variation statistical outputs
│   ├── SOM results/  # Somatic mutation statistical outputs
│   └── HPV results/  # HPV positive/negative patient lists
│
├── Data/
│   ├── TCGA/                    # TCGA genomic data (CNV, mutations)
│   ├── DGIDB/                   # Drug Gene Interaction Database
│   ├── Protein-protein interaction data/  # STRING database
│   └── Supplementary data Nulton/         # Mutation annotation files
│
└── Validation pipeline/         # Literature validation scripts
    ├── 00 extract_pmids.bash    # PubMed PMID extraction
    └── 02 GPU_full_extract.py   # LLM-based target extraction
```

---

## Data Availability

**TCGA Data:**
- Publicly available at [GDC Data Portal](https://portal.gdc.cancer.gov/)
   - access using gdc client and available manifests
- Project: TCGA-HNSC (Head and Neck Squamous Cell Carcinoma)
- Data types: Gene-level copy number (gistic2), somatic mutations (MAF)

**DrugBank:**
- Academic license required from [DrugBank](https://www.drugbank.ca/)
- XML download contains drug-target relationships

**STRING Database:**
- Freely available at [STRING](https://string-db.org/)
- Human protein-protein interactions, version 12.0

**Literature Data:**
- PubMed abstracts retrieved via NCBI E-utilities
- PMIDs documented in results files for verification

---

## Citation

If using this analysis or methodology, please cite:
- TCGA Research Network
- DrugBank (Wishart DS, et al.)
- STRING database (Szklarczyk D, et al.)
- This repository and associated publications

---

## Contact

For questions about methods, results, or data access, please contact [Institution/PI information].
