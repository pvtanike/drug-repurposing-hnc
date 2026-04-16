
---
# Literature-Based Validation for Drug Repurposing in Head and Neck Cancer

**Last Updated**: April 2, 2026

## Executive Summary

**Goal**: Use LLM-based NLP to extract gene-disease associations from 419,710 PubMed abstracts to validate drug repurposing candidates.

**Key Results**:
- **Abstracts Processed**: 419,710 publications (2000-2025)
- **Genes Extracted**: 6,078 unique genes with HNC associations
- **Model**: Google Gemma-2B-IT for scalable extraction
- **Validation Success**: 100% of TCGA-identified genes have literature support

**Key Finding**: All mutated genes from genomic analysis (Aim 2) and drugs from EHR analysis (Aim 1) have literature validation, providing robust multi-modal evidence for repurposing candidates.

**See Integration**: [All aims together/](../All%20aims%20together/) for validated pathways

---

## Overview

## Overview

This module employs large language model (LLM)-based natural language processing to systematically extract disease targets from head and neck cancer literature, validating drug repurposing candidates identified through EHR and genetic analyses. Using Google Gemma-2B-IT to process ~420,000 PubMed abstracts published from 2000 onwards, we extracted 6,078 unique gene targets mentioned in HNC research, providing comprehensive literature support for genomic alterations and drug-gene-pathway connections.

---

## Data Acquisition & Setup

**IMPORTANT: Literature data and resulting files have been removed from this repository. Follow these steps to regenerate the data:**

### Automatic Data Acquisition (Recommended)

The literature abstracts will be automatically downloaded when you run the extraction pipeline:

1. **PubMed Abstracts** (automatic download via scripts):
   - **Source**: NCBI PubMed E-utilities API
   - **Query**: "head and neck cancer"
   - **Years**: 2000-present
   - **Format**: CSV with PMID, Title, Year, Abstract
   - **No manual download needed** - Run `00 extract_pmids.bash` to fetch automatically

### Required External Data Sources

#### 1. DrugBank Database
- **Source**: [https://www.drugbank.ca/](https://www.drugbank.ca/)
- **Access**: Free academic license (registration required)
- **Required File**: Full DrugBank XML
- **Where to place**: `3. Literature based validation/Data/DRUGBANK/drug_bank.xml`

#### 2. STRING Protein-Protein Interaction Database
- **Source**: [https://string-db.org/cgi/download](https://string-db.org/cgi/download)
- **Required File**: Human protein links (9606.protein.links.v12.0.txt.gz)
- **Where to place**: `3. Literature based validation/Data/Protein-protein interaction data/`

### Hardware Requirements for LLM Extraction

- **GPU**: CUDA-compatible GPU with ≥16GB VRAM (recommended: NVIDIA A100, RTX 3090, or better)
- **RAM**: ≥32GB system RAM
- **Storage**: ≥50GB free space for abstracts and results
- **Processing Time**: ~200-500 hours on single GPU for full dataset

**Note**: If GPU is unavailable, you can:
1. Use Google Colab (free with limitations)
2. Request GPU time from your institution's computing cluster
3. Use the validation pipeline results (provided in published data)

### Expected Output Structure

When you run the complete pipeline, outputs will be generated in `Results/`:

```
Results/
├── extracted_targets_all_pub_after_2000_GPU_2b_gemma.csv
│   # Raw LLM extraction: gene targets from each abstract
│   # Columns: PMID, extracted_targets, abstract_snippet
│
├── cleaned_extracted_targets_all_pub_after_2000_GPU_2b_gemma.csv
│   # Cleaned gene list with validation
│   # Columns: gene_symbol, pmid_count, pmids, literature_evidence
│
└── cleaned_extracted_combined_targets_all_pub_after_2000_GPU_2b_gemma.csv
    # Aggregated results: unique genes with literature counts
    # Columns: gene_symbol, total_pmids, pmid_list
```

### Step-by-Step Data Generation

```bash
# Step 1: Extract PMIDs from PubMed (automatic download)
bash 00 extract_pmids.bash
# Output: Data/head and neck cancer query abstracts.csv

# Step 2: Process abstracts with LLM extraction
# Open and run: 01 extract based on pmid.ipynb
# Output: Prepared data for GPU extraction

# Step 3: Run LLM extraction on GPU
python 02 GPU_full_extract.py
# OR submit as batch job: sbatch 02 GPU_full_extract.sh
# Output: Results/extracted_targets_all_pub_after_2000_GPU_2b_gemma.csv

# Step 4: Clean and validate extracted genes
# Open and run: 03 data viewing.ipynb
# Output: Results/cleaned_extracted_targets*.csv
```

---

## Scientific Rationale

The exponential growth of biomedical literature makes manual curation of gene-disease associations impractical, with over 400,000 publications discussing head and neck cancer. Large language models enable scalable extraction of disease targets from unstructured text, providing literature validation for:

1. **Genes identified from TCGA genomic analysis** - confirming their documented relevance to HNC biology
2. **Protein-protein interaction network components** - validating pathway connections
3. **Drug target mechanisms** - supporting biological plausibility of repurposing candidates

By cross-referencing LLM-extracted targets with our genetic and clinical findings, we ensure that repurposing candidates have:
- **Genomic evidence** (TCGA alterations)
- **Clinical evidence** (EHR survival associations)
- **Literature consensus** (multiple publications documenting gene-disease relationships)

This triangulation approach dramatically increases confidence in identified candidates compared to single-modality analyses.

---

## Methods

### 1. Literature Retrieval

**PubMed Query:**
- **Search Term:** "head and neck cancer"
- **API:** NCBI E-utilities (esearch + efetch)
- **Fields Retrieved:** PMID, Title, Year, Abstract
- **Total Results:** 419,710 publications

**Temporal Filtering:**
- **Inclusion:** Publications from year 2000 onwards
- **Rationale:** Focus on modern drug repurposing targets and mechanisms
- **Final Dataset:** ~419,710 abstracts spanning 25 years (2000-2025)

**Implementation:**
```bash
# Bash script: 00 extract_pmids.bash
esearch -db pubmed -query "head and neck cancer" | \
  efetch -format xml | \
  xtract -pattern PubmedArticle -element MedlineCitation/PMID \
    ArticleTitle PubDate/Year AbstractText
```

**Data Structure:**
```csv
PMID,TITLE,YEAR,ABSTRACT
12345678,"Title of paper",2020,"Abstract text discussing EGFR..."
```

---

### 2. LLM-Based Target Extraction

**Model Selection:**
- **Model:** Google Gemma-2B-IT (instruction-tuned variant)
- **Size:** 2 billion parameters (optimized for GPU memory efficiency)
- **Alternative:** Gemma-7B-IT available for increased accuracy (requires more GPU RAM)
- **Source:** HuggingFace Transformers library

**Hardware Requirements:**
- **GPU:** CUDA-compatible with ≥16GB VRAM (tested on NVIDIA A100)
- **Batch Processing:** Sequential processing of abstracts (no batching due to variable length)
- **Processing Time:** ~419,710 abstracts × 2-5 seconds each ≈ 200-500 hours on single GPU

**Prompt Engineering:**

**Task Description:**
```
You are required to read the given abstract and determine any key disease 
targets for the cancer mentioned. Responding with the disease target, if 
there are multiple separate by comma. Explain your answer with the sentence 
where the information is found. If there is no information related to the 
disease target, respond with "No information available". Always place answer 
of disease targets after "Key disease targets:" and sentence where information 
is found after "Sentence where information is found:".

You should either respond:
- Key disease targets: [targets], and the sentence where information is found
  Sentence where information is found: [sentence]
- "No information available": The abstract did not contain information related 
  to the disease target
```

**User Prompt Template:**
```
Analyze the following abstract to determine key disease targets for the 
cancer type mentioned. If there are multiple targets separate by comma. 
Provide sentence where the information is found for explanation:

{abstract}
```

**Response Format:**
```
Key disease targets: EGFR, PIK3CA, TP53
Sentence where information is found: "Mutations in EGFR, PIK3CA, and TP53 
were associated with poor prognosis in head and neck cancer patients."
```

---

### 3. Post-Processing and Validation

**Text Cleaning:**
- Convert all gene names to uppercase for consistency
- Remove markdown formatting (**, ##, etc.)
- Extract targets using regex patterns:
  ```python
  pattern = r'key disease targets:\s*(.+?)\s*\n?sentence'
  ```
- Clean "No information available" responses

**Gene Symbol Validation:**
- **Cross-reference with DrugBank** (4,187 gene symbols)
- **Cross-reference with STRING database** (human proteome)
- **Filter invalid symbols** (non-gene terms, general phrases)
- **Standardize synonyms** (e.g., "p53" → "TP53", "BCL-6" → "BCL6")

**Literature Count Assignment:**
- **Count PMIDs** for each gene across all abstracts
- **Range:** 1-206 publications per gene
- **Top genes:** TP53 (29), PIK3CA (17), CDKN2A (16), EGFR (multiple)

**Quality Control:**
- Manual review of top 100 extracted genes
- Validation against known HNC oncogenes and tumor suppressors
- False positive filtering (remove generic terms like "cancer", "metastasis")

---

### 4. Integration with Genomic and Clinical Data

**Validation Pipeline:**

**Step 1: Genetic Validation**
- Genes identified from TCGA (CNV/somatic mutations) cross-referenced with literature
- **Criterion:** Gene must have ≥1 PMID in literature extraction
- **Result:** All 21 HPV-negative and 5 HPV-positive genes literature-validated

**Step 2: PPI Network Validation**
- STRING database neighbors cross-referenced with literature
- **Criterion:** PPI partners must be literature-validated to be retained
- **Effect:** Reduces spurious network connections, ensures biological relevance

**Step 3: Drug-Gene Pathway Validation**
- EHR-derived drugs mapped to DrugBank targets
- Targets connected to PPI network → mutation genes
- **Criterion:** All pathway components must be literature-validated
- **Result:** Complete evidence chain: Drug → Target (lit) → PPI (lit) → Mutation gene (lit)

**Statistical Integration:**
```
Evidence_Score = (Literature_Count × Genetic_Q-value × EHR_Importance) / Pathway_Length
```

Where:
- Literature_Count = Number of PMIDs supporting gene-HNC association
- Genetic_Q-value = Significance of genomic alteration (inverse, so lower is better)
- EHR_Importance = XGBoost feature importance from clinical analysis
- Pathway_Length = Number of steps from drug to mutation gene (penalizes indirect pathways)

---

## Key Results

### Literature Extraction Summary

**Extraction Scale:**
- **Input:** 419,710 PubMed abstracts (2000-2025)
- **Raw Extraction:** ~6,078 unique genes/targets identified
- **After Validation:** Filtered to genes in DrugBank or STRING database
- **Literature Depth:** 1-206 PMIDs per gene (median varies by gene importance)

**Top Validated Genes (Literature Support):**

| Gene | PMIDs | Function | Found in TCGA |
|------|-------|----------|---------------|
| **TP53** | 29 | Tumor suppressor (p53 pathway) | Yes (HPV-) |
| **PIK3CA** | 17 | PI3K catalytic subunit | Yes (Both HPV+/-) |
| **CDKN2A** | 16 | Cell cycle (p16INK4a) | Yes (HPV-) |
| **EGFR** | Multiple | Receptor tyrosine kinase | Yes (HPV-) |
| **CCND1** | Multiple | Cell cycle (Cyclin D1) | Yes (HPV-) |
| **MYC** | Multiple | Oncogenic transcription factor | Yes (HPV-) |
| **BCL2** | Multiple | Anti-apoptotic protein | Network |
| **NOTCH1** | Multiple | Developmental signaling | Yes (HPV-) |
| **BRCA1/2** | Multiple | DNA repair | Network |

**Coverage Statistics:**
- **21 HPV-negative TCGA genes:** 100% have literature support (range: 1-29 PMIDs)
- **5 HPV-positive TCGA genes:** 100% have literature support (range: 1-17 PMIDs)
- **PPI network genes:** 85-90% have literature support (others filtered out)

---

### Validation of EHR Drug Candidates

#### HPV-Negative Head and Neck Cancer

**Validated Drugs (11 pathways, 5 unique drugs):**

| Drug | XGB Score | Target | Literature Path | Root Gene | PMIDs |
|------|-----------|--------|-----------------|-----------|-------|
| **Melatonin** | 0.0106 | ESR1 | ESR1 → BCL6 | BCL6 (Amp) | 4 |
| | | ESR1 | ESR1 → DVL3 | DVL3 (Amp) | - |
| | | ESR1 | ESR1 → RFC4 | RFC4 (Amp) | 1 |
| **Levothyroxine** | 0.0050 | ITGAV | ITGAV → COL1A2 | COL1A2 (Som) | - |
| | | ITGB3 | ITGB3 → BCL6 | BCL6 (Amp) | 4 |
| | | THRB | THRB → RFC4 | RFC4 (Amp) | 1 |
| **Acetaminophen** | 0.0045 | PTGS2 | PTGS2 → BCL6 | BCL6 (Amp) | 4 |
| **Methylprednisolone** | 0.0043 | ANXA1 | ANXA1 → REG1A | REG1A (Som) | - |
| | | ANXA1 | ANXA1 → BCL6 | BCL6 (Amp) | 4 |
| **Aspirin** | 0.0033 | PTGS2 | PTGS2 → BCL6 | BCL6 (Amp) | 4 |

**Key Literature-Validated Pathways:**

1. **PTGS2 (COX-2) → BCL6 Pathway**
   - Targeted by: Acetaminophen, Aspirin
   - Literature: 4 PMIDs supporting BCL6 in HNC
   - Mechanism: COX-2 inhibition reduces inflammation → affects BCL6 transcriptional repression

2. **ESR1 (Estrogen Receptor) → Multiple Amplifications**
   - Targeted by: Melatonin
   - Connects to: BCL6 (4 PMIDs), DVL3, RFC4 (1 PMID)
   - Mechanism: Hormone receptor modulation affects cell proliferation pathways

3. **ANXA1 (Annexin A1) → Immune/Inflammatory Pathway**
   - Targeted by: Methylprednisolone
   - Connects to: REG1A (somatic mutation), BCL6 (amplification)
   - Mechanism: Anti-inflammatory signaling reduces tumor-promoting inflammation

#### HPV-Positive Head and Neck Cancer

**Validated Drugs (8 pathways, 4 unique drugs):**

| Drug | XGB Score | Target | Literature Path | Root Gene | PMIDs | Q-value |
|------|-----------|--------|-----------------|-----------|-------|---------|
| **Levothyroxine** | 0.0441 | THRB | THRB → PIK3CA | PIK3CA (Amp+Som) | 17 | 4.9×10⁻⁵⁴ |
| **Heparin** | 0.0096 | FGFR1 | FGFR1 → PIK3CA | PIK3CA (Amp+Som) | 17 | 4.9×10⁻⁵⁴ |
| | | FGFR2 | FGFR2 → PIK3CA | PIK3CA (Amp+Som) | 17 | 4.9×10⁻⁵⁴ |
| | | FGFR4 | FGFR4 → PIK3CA | PIK3CA (Amp+Som) | 17 | 4.9×10⁻⁵⁴ |
| | | FGF4 | FGF4 → SOX2 | SOX2 (Amp) | 1 | 1.3×10⁻⁵⁵ |
| **Dexamethasone** | 0.0081 | ANXA1 | ANXA1 → SOX2 | SOX2 (Amp) | 1 | 1.3×10⁻⁵⁵ |
| **Folic Acid** | 0.0 | TYMS | TYMS → RFC4 | RFC4 (Amp) | 1 | - |

**Key Literature-Validated Pathways:**

1. **THRB → PIK3CA Pathway (Levothyroxine)**
   - **Highest XGBoost importance** (0.0441) in HPV+ cohort
   - PIK3CA: 17 PMIDs, q=4.9×10⁻⁵⁴ (most significant genetic alteration)
   - Mechanism: Thyroid hormone receptor crosstalk with PI3K/AKT signaling

2. **FGFRs → PIK3CA/SOX2 Pathways (Heparin)**
   - Multiple FGFR targets (FGFR1/2/4) all connect to PIK3CA (17 PMIDs)
   - FGF4 connects to SOX2 (1 PMID, q=1.3×10⁻⁵⁵)
   - Mechanism: FGF signaling modulation affects stem cell and proliferation pathways

3. **ANXA1 → SOX2 Pathway (Dexamethasone)**
   - SOX2: 1 PMID, q=1.3×10⁻⁵⁵ (highly significant amplification)
   - Mechanism: Anti-inflammatory effects on stem cell transcription factor

---

### Cross-Cohort Validation

**LEVOTHYROXINE - Only Drug Validated in BOTH HPV Groups:**

**HPV-Negative:**
- XGBoost: 0.0050
- Cox HR: 0.931 (6.9% risk reduction, p<0.001)
- Pathway: THRB → COL1A2 (somatic), BCL6 (4 PMIDs), RFC4 (1 PMID)

**HPV-Positive:**
- XGBoost: 0.0441 (highest importance)
- Cox HR: Not available (underpowered)
- Pathway: THRB → PIK3CA (17 PMIDs, q=4.9×10⁻⁵⁴)

**Literature Support:**
- **PIK3CA:** 17 PMIDs documenting role in HNC pathogenesis
- **BCL6:** 4 PMIDs supporting involvement in HNC
- **THRB:** Thyroid hormone receptor signaling documented in cancer biology

**Cross-Validation Strength:**
The convergence of clinical evidence (EHR survival benefit), genetic evidence (TCGA alterations), and literature consensus (17+ PMIDs for PIK3CA) provides exceptionally strong multi-modal support for levothyroxine repurposing.

---

## Discussion

### Literature Validation Confirms Genomic-Clinical Convergence

The LLM-based literature extraction successfully validated 100% of genes identified through TCGA genomic analysis, confirming that statistically significant genomic alterations correspond to genes with documented roles in HNC biology. This cross-validation dramatically reduces the likelihood that identified genes represent statistical artifacts or passenger mutations without biological relevance.

**Key Validation Findings:**

1. **High-Confidence Genes Have Extensive Literature:**
   - TP53: 29 PMIDs (most studied HNC gene)
   - PIK3CA: 17 PMIDs (validates its centrality to both HPV+ and HPV- pathogenesis)
   - CDKN2A: 16 PMIDs (confirms p16 pathway importance)

2. **Pathway Components Are Literature-Supported:**
   - All PPI network neighbors retained for drug validation have literature support
   - Ensures drug-target-mutation pathways represent established biology, not speculative connections

3. **Drug Mechanisms Have Literature Precedent:**
   - PTGS2 (COX-2) → BCL6: Inflammation-cancer axis documented
   - THRB → PIK3CA: Thyroid hormone-PI3K crosstalk established
   - FGFRs → PIK3CA: FGF signaling in HNC extensively studied

### Comparison with Manual Curation

**LLM Advantages:**
- **Scale:** Processed 419,710 abstracts vs. ~100 manually feasible
- **Speed:** ~200-500 hours GPU time vs. months of manual curation
- **Consistency:** Standardized extraction criteria vs. variable human interpretation
- **Coverage:** Identified 6,078 genes vs. ~50-100 typically curated

**Limitations:**
- **False Positives:** LLM may extract genes mentioned but not causally implicated
- **Context Loss:** May miss nuanced relationships (e.g., "gene X does NOT cause Y")
- **Synonym Issues:** Requires post-processing to standardize gene names

**Validation Against Gold Standard:**
- All known HNC oncogenes/tumor suppressors correctly identified (TP53, PIK3CA, EGFR, CDKN2A, NOTCH1, etc.)
- Literature counts correlate with known gene importance (TP53 highest)
- Cross-database validation (DrugBank, STRING) filters noise

### Integration Strengthens Repurposing Evidence

The triangulation of EHR clinical evidence, TCGA genomic evidence, and literature consensus provides the strongest possible support for drug repurposing candidates:

**Evidence Hierarchy:**

**Tier 1 (Highest Confidence):**
- Drug shows clinical benefit in EHR (Cox HR, XGBoost importance)
- Drug targets genes with genomic alterations (TCGA q-value < 0.05)
- All pathway components have literature support (PMIDs documented)
- Example: **Levothyroxine** (validated in both HPV cohorts, 17 PMIDs for PIK3CA)

**Tier 2 (Strong Evidence):**
- Drug shows clinical benefit in EHR
- Drug targets pathways connected to genomic alterations (via PPI)
- Pathway has literature support
- Example: **Methylprednisolone** (15.6% risk reduction, ANXA1→BCL6 pathway, 4 PMIDs)

**Tier 3 (Moderate Evidence):**
- Drug shows clinical association in EHR
- Pathway to genomic alterations exists but indirect
- Some literature support
- Example: Additional medications with protective trends

### Mechanistic Insights from Literature

**1. PI3K/AKT Pathway (PIK3CA - 17 PMIDs):**
- Most extensively documented pathway in HNC literature
- Central to cell growth, metabolism, survival
- Levothyroxine modulation via THRB provides novel therapeutic angle
- Heparin modulation via FGFRs represents alternative entry point

**2. Inflammation-Cancer Axis (PTGS2, ANXA1):**
- Chronic inflammation promotes tumor progression (well-documented)
- COX-2 inhibition (acetaminophen, aspirin) reduces inflammatory signaling
- Corticosteroid anti-inflammatory effects (methylprednisolone, dexamethasone) via ANXA1
- Literature supports inflammation reduction as cancer prevention/treatment strategy

**3. Stem Cell Pathways (SOX2 - 1 PMID but q=1.3×10⁻⁵⁵):**
- SOX2 amplification highly significant in HPV+ tumors
- Stem cell markers associated with tumor initiation, therapy resistance
- Less extensively studied in HNC specifically (only 1 PMID) but well-established in cancer stem cell biology generally
- Dexamethasone → ANXA1 → SOX2 pathway provides novel targeting approach

**4. Cell Cycle Dysregulation (CDKN2A - 16 PMIDs):**
- p16INK4a pathway extensively studied as HPV classifier
- Loss of G1/S checkpoint control central to HNC pathogenesis
- Downstream pathway targeting (BCL6, etc.) may compensate for lost checkpoint

### Limitations of Literature Validation

**1. Publication Bias:**
- Well-studied genes (TP53, PIK3CA) accumulate more publications
- Novel or understudied genes may have fewer PMIDs despite biological importance
- Example: SOX2 only 1 PMID in HNC literature, but extremely significant genetically (q=1.3×10⁻⁵⁵)

**2. Temporal Coverage:**
- Filtered to 2000+ for modern relevance
- May miss historical foundational studies (pre-2000)
- Most relevant for drug repurposing (modern pharmacology)

**3. LLM Extraction Accuracy:**
- ~85-90% accuracy based on manual validation
- False positives (genes mentioned but not causally related)
- False negatives (genes discussed but not extracted)
- Mitigated by cross-database validation (DrugBank, STRING)

**4. Literature Depth vs. Genetic Significance:**
- No perfect correlation between PMID count and biological importance
- Emerging targets (SOX2 in HPV+) may be highly significant but understudied
- Literature count used as supporting evidence, not sole criterion

---

## Conclusions

### Key Findings

1. **100% of TCGA-identified genes validated in literature** (21 HPV-negative, 5 HPV-positive), confirming genomic alterations correspond to documented HNC biology

2. **Levothyroxine has strongest multi-modal validation:**
   - Clinical: XGBoost 0.0050-0.0441, Cox HR 0.931 (p<0.001)
   - Genetic: PIK3CA q=4.9×10⁻⁵⁴
   - Literature: 17 PMIDs supporting PIK3CA in HNC
   - Only drug validated across both HPV cohorts

3. **PIK3CA emerges as central therapeutic target:**
   - 17 PMIDs (2nd most studied gene after TP53)
   - Altered in both HPV+ and HPV-
   - Targeted by multiple drugs (levothyroxine, heparin)
   - Highly significant genetic alteration (q=4.9×10⁻⁵⁴)

4. **LLM-based extraction enables comprehensive validation:**
   - Processed 419,710 abstracts (infeasible manually)
   - Extracted 6,078 genes (vastly exceeds manual curation)
   - Provides literature support for all pathway components

### Clinical Translation

The convergence of literature, genomic, and clinical evidence provides exceptionally strong rationale for:

1. **Immediate Clinical Trials:**
   - **Levothyroxine:** Phase II trial in HNC patients stratified by HPV status and PIK3CA alteration
   - **Methylprednisolone:** Phase II trial in HPV-negative HNC focusing on patients with inflammatory markers

2. **Biomarker-Guided Therapy:**
   - PIK3CA status (amplification/mutation) as predictive biomarker for levothyroxine response
   - HPV status as stratification variable
   - TP53/CDKN2A status for patient selection

3. **Mechanistic Studies:**
   - THRB-PIK3CA crosstalk mechanisms
   - ANXA1 anti-inflammatory effects in tumor microenvironment
   - FGFR-PI3K pathway modulation by heparin

### Future Directions

1. **Expand Temporal Coverage:** Include pre-2000 foundational studies
2. **Multi-Language Processing:** Extend to non-English literature
3. **Fine-Tune LLM:** Train domain-specific model on HNC literature for improved extraction
4. **Real-Time Updates:** Continuous literature monitoring for emerging targets
5. **Pathway Enrichment:** Use literature co-mention networks to identify additional pathway connections

---

## File Structure

```
3. Literature based validation/
├── 00 extract_pmids.bash                # PubMed literature retrieval
├── 01 extract based on pmid.ipynb       # PMID processing
├── 02 GPU_full_extract.py               # LLM-based target extraction
├── 02 GPU_full_extract.sh               # GPU job submission script
├── 03 data viewing.ipynb                # Results exploration
│
├── Data/
│   └── head and neck cancer query abstracts.csv  # PubMed abstracts
│
└── Results/
    ├── cleaned_extracted_targets_all_pub_after_2000_GPU_2b_gemma.csv      # Cleaned LLM extraction results
    └── cleaned_extracted_combined_targets_all_pub_after_2000_GPU_2b_gemma.csv  # Combined/deduplicated targets
```

---

## Data Availability

**PubMed Abstracts:**
- Freely available via NCBI E-utilities API
- Query: "head and neck cancer"
- Total: 419,710 abstracts (2000-2025)

**Google Gemma Model:**
- Available via HuggingFace: `google/gemma-2b-it`
- Requires HuggingFace account and API token
- Academic use permitted

**Extracted Targets:**
- Results files included in repository
- Cross-referenced with DrugBank and STRING databases

---

## Citation

If using this literature validation approach or results, please cite:
- PubMed/NCBI for literature database
- Google for Gemma LLM model
- HuggingFace for model hosting
- This repository and associated publications

---

## Contact

For questions about LLM extraction methods, results interpretation, or data access, please contact [Institution/PI information].
