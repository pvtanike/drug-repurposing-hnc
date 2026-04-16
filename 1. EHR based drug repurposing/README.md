# EHR-Based Drug Repurposing for Head and Neck Cancer



---

## Data Availability Notice

**Input data files are NOT included in this repository** due to Protected Health Information (PHI) restrictions from the TriNetX database. To reproduce this analysis:

1. **Obtain IRB-approved access** to TriNetX PCDM (Patient-Centered Data Model) data
2. **Update data paths** in `Data_import.py`: Replace `IRB_ID` and `DATA_FOLDER` with your actual paths
3. **Run Phase 0 and Phase 1 notebooks** (see "Analysis Pipeline" below) to generate:
   - `input_data/` folder (feature matrices and patient outcomes)
   - `ICD_RX translation/` folder (medical code dictionaries)

Only after generating these files can you run the main analysis notebooks (Phase 2).

---

## Project Overview
This module identifies medication-metastasis associations in head and neck cancer (HNC) using electronic health records (EHR) from the TriNetX database. The analysis employs dual complementary approaches—**Cox Proportional Hazards survival analysis** and **Machine Learning classification**—both stratified by HPV status to account for distinct disease etiologies. Medications associated with reduced metastasis risk across both statistical frameworks represent high-confidence candidates for drug repurposing.

### Scientific Motivation
Head and neck cancers exhibit heterogeneous outcomes, with HPV-positive and HPV-negative tumors representing biologically distinct disease entities. Understanding medication-metastasis associations within these subgroups can:
- Identify potential drug repurposing opportunities
- Reveal inadvertent protective/harmful effects of common medications
- Guide personalized treatment strategies
- Elucidate biological mechanisms underlying metastatic progression

### Medication Feature Encoding Rationale
Medications are encoded as **cumulative prescription counts (sum per patient per row)** rather than binary indicators to capture treatment intensity and longitudinal exposure patterns. Each patient's row contains the total sum of all their prescriptions for each medication. This approach preserves clinically meaningful variation in medication utilization that may reflect underlying disease severity, comorbidity burden, and sustained pharmacologic exposure relevant to metastasis risk. Prescription frequency serves as a proxy for both treatment intensity and duration, which are critical pharmacoepidemiologic parameters in cancer outcomes research. Count-based encoding provides several advantages: (1) captures dose-response relationships where higher medication exposure may have greater biological effects, (2) distinguishes patients with single prescriptions from those with sustained chronic use, (3) provides more statistical power for gradient-based machine learning algorithms to learn non-linear relationships, and (4) mirrors mutation count analysis in genomics where quantitative measures provide greater biological interpretability than binary indicators.

### Key Research Questions
1. Which medications are independently associated with metastasis risk after controlling for treatment confounders?
2. Do medication-metastasis associations differ between HPV+ and HPV- patients?
3. Which features demonstrate robust prognostic value across multiple statistical methods and validation strategies?
4. How do findings from time-to-event (Cox) and binary prediction (ML) frameworks complement each other?

### Analysis Framework
- **Integrated Cox Proportional Hazards & Machine Learning Analysis**: Combined survival modeling and classification in a unified pipeline
  - **Cox Analysis**: Time-to-metastasis survival modeling with both univariate (individual feature effects) and multivariate (adjusted effects) analyses, Benjamini-Hochberg FDR-corrected p-values
  - **Machine Learning Classification**: XGBoost, Random Forest, and Logistic Regression with nested cross-validation and hyperparameter tuning
  - **SHAP Analysis**: Explainable AI for directional feature importance (protective vs. harmful effects)
- **HPV Stratification**: Separate models for HPV+ and HPV- subgroups recognizing distinct tumor biology
- **Robust Feature Selection**: Multi-method approach (Chi-square, Lasso, Variance Threshold, tree-based importance) with stability assessment
- **Correlation Analysis**: Identification of features without strong treatment confounder correlations (r < 0.5)

---

## Statistical Rigor & Publication Standards

### Multiple Testing Correction
- **Univariate Cox analyses**: Benjamini-Hochberg FDR correction applied (conservative approach for discovery)
- **Multivariate Cox analyses**: No correction (single joint model, not independent tests)
- **Interpretation**: Features reported as significant at both uncorrected p<0.05 and FDR<0.05

### Feature Selection Robustness
- **Nested cross-validation**: Feature selection performed within each CV fold to prevent data leakage
- **Multi-method intersection**: Features selected by ALL 3 methods (Lasso, Chi-square, Variance Threshold) to ensure robust selection
- **Stability metrics**: Selection frequency tracked across CV folds (≥80% threshold)
- **Independent validation**: Train/test split (70/30) with stratification by outcome

### Model Validation
- **Cox models** (integrated in ML pipeline):
  - **Univariate Cox**: Each feature tested individually with FDR correction (Benjamini-Hochberg)
  - **Multivariate Cox**: Joint model adjusting for all features simultaneously
  - Concordance index (C-index) for predictive accuracy assessment
  - Hazard ratios with 95% confidence intervals
  - Forest plots for visualization of effect sizes
  - Significant features reported at both p<0.05 (uncorrected) and FDR<0.05 (corrected)

- **ML models** (integrated with Cox):
  - 5-fold stratified cross-validation with RandomizedSearchCV
  - Multiple algorithms with hyperparameter tuning:
    - XGBoost (primary model with class balancing)
    - Random Forest (ensemble validation)
    - Logistic Regression (interpretable linear model)
  - SHAP values for directional feature importance (protective vs. harmful)
  - Mean absolute SHAP values for feature ranking
  - Log-odds ratios for interpretable effect sizes
  - Comprehensive metrics: ROC-AUC, accuracy, precision, recall, F1-score

### Confounding Control
- **Treatment confounders**: Surgery, Radiation, Chemotherapy, Immunotherapy
- **Correlation filtering**: Features with |r| > 0.5 to treatment flagged
- **Multivariate adjustment**: All models include confounders as covariates
- **Subgroup analysis**: HPV stratification controls for major disease heterogeneity

---

## Repository Structure

```
1. EHR based drug repurposing/
├── README.md                                # ← START HERE: Project overview and execution guide
├── Data_import.py                           # ← Data loading module (fully documented)
│
├── input_data/                              # NOT INCLUDED - Contains PHI (Protected Health Information)
│   │                                        # MUST BE GENERATED by running Phase 0 & Phase 1 notebooks
│   ├── one_hot_encoded_sum_per_pat.csv     # Feature matrix: 1 row per patient, SUM of medications/procedures
│   │                                        # Created by: "00 non merging input file creation modified sum.ipynb"
│   ├── patient level data.csv              # Patient outcomes: 1 row per patient with demographics & survival
│   │                                        # Created by: "00 non merging input file creation patient level data.ipynb"
│   ├── raw_input_data.csv                  # Intermediate file created during feature engineering
│   └── ICD_RX translation/                 # Medical code dictionaries (generated by Phase 0)
│       ├── HNC Diagnosis ICD Translation DF.csv    # ICD diagnosis codes → readable names
│       ├── HNC procedure ICD translation DF.csv    # ICD procedure codes → readable names
│       ├── ndcCodeTranslationDF_HNC.csv            # NDC drug codes → generic names
│       └── rxCodeTranslationDF_HNC.csv             # RxNorm codes → generic names
│
├── ICD_RX translation/                      # NOT INCLUDED - Medical code dictionaries (may contain PHI)
│   │                                        # MUST BE GENERATED by running: "00 create ICD_RX translation DF.ipynb"
│   ├── HNC Diagnosis ICD Translation DF.csv    # ICD diagnosis codes → readable names
│   ├── HNC procedure ICD translation DF.csv    # ICD procedure codes → readable names
│   ├── ndcCodeTranslationDF_HNC.csv            # NDC drug codes → generic names
│   └── rxCodeTranslationDF_HNC.csv             # RxNorm codes → generic names
│
├── Results/                                 # Analysis outputs (CSV files)
│   └── ML analysis/
│       ├── hpv_positive_ml_xgb_results.csv         # PRIMARY: Comprehensive HPV+ results (Cox + ML + SHAP)
│       ├── hpv_negative_ml_xgb_results.csv         # PRIMARY: Comprehensive HPV- results (Cox + ML + SHAP)
│       ├── hpv_positive_ml_drug_xgb_results.csv    # HPV+ drug candidates filtered from full results
│       ├── hpv_negative_ml_drug_xgb_results.csv    # HPV- drug candidates filtered from full results
│       ├── ml_feature_stability_hpv_positive.csv   # Feature stability across CV folds (HPV+)
│       └── ml_feature_stability_hpv_negative.csv   # Feature stability across CV folds (HPV-)
│
├── 00 create ICD_RX translation DF.ipynb   # Medical code translation (setup)
├── 00 Data viewing.ipynb                   # Exploratory data analysis
├── 00 Identify chemotherapy medications.ipynb  # Identify chemotherapy drugs
├── 00 Identify surg_rad prevalance.ipynb   # Identify surgery/radiation prevalence
├── 00 non merging input file creation modified sum.ipynb   # Feature engineering (sum aggregation)
├── 00 non merging input file creation patient level data.ipynb  # Patient-level data preparation
├── 02 data_analysis_ml.ipynb              # Integrated Cox + ML analysis (MAIN)
└── 03 top feature correlation check.ipynb # Validation & correlation analysis (MAIN)
```

---

## Analysis Pipeline


### Complete Execution Order

**PREREQUISITE**: Before running any notebooks, you must have IRB-approved access to TriNetX data and update the file paths in `Data_import.py` (replace `IRB_ID` and `DATA_FOLDER` placeholders).

Run notebooks sequentially to reproduce the full analysis from raw EHR data:

```bash
# PHASE 0: Data Setup & Translation (REQUIRED - creates translation dictionaries)
# Output: ICD_RX translation/ folder
jupyter notebook "00 create ICD_RX translation DF.ipynb"       # Medical code translations

# PHASE 1: Data Exploration & Feature Engineering (REQUIRED - creates input data files)
# Output: input_data/ folder
jupyter notebook "00 Data viewing.ipynb"                       # Exploratory data analysis
jupyter notebook "00 Identify chemotherapy medications.ipynb"  # Identify chemotherapy drugs
jupyter notebook "00 Identify surg_rad prevalance.ipynb"       # Identify surgery/radiation prevalence
jupyter notebook "00 non merging input file creation patient level data.ipynb"  # Patient outcomes
jupyter notebook "00 non merging input file creation modified sum.ipynb"        # Feature matrix

# PHASE 2: Statistical Analysis (main analysis - requires Phase 0 & 1 outputs)
jupyter notebook "02 data_analysis_ml.ipynb"               # Integrated Cox + ML analysis
jupyter notebook "03 top feature correlation check.ipynb"  # Validation & integration
```

**IMPORTANT**: Phase 0 and Phase 1 are **NOT optional** - they generate the required input files that are excluded from the repository due to PHI.

### Notebook Descriptions

---

### PHASE 0: Data Setup (One-Time Execution)

#### `00 create ICD_RX translation DF.ipynb` - Medical Code Translation
**Purpose**: Creates human-readable translation dictionaries for medical codes using UMLS and RxNorm APIs

**Key Functions**:
- `query_UMLS(query, codingSystem)` - Translates ICD codes via UMLS API
- `translateICD(query)` - Tries multiple coding systems (CPT, HCPCS, ICD9CM, ICD10CM)
- `extractIngredientFromRxNorm(query)` - Gets medication active ingredients from RxNorm
- `NDCtoRXNorm(query)` - Converts NDC codes to RxNorm CUI codes
- `queryNDC(query)` - Queries NDC codes via RxNorm API

**Requirements**:
- UMLS API key (set as environment variable)
- Internet connection for API calls

**Outputs** (saved to `ICD_RX translation/`):
- `HNC Diagnosis ICD Translation DF.csv` - ICD diagnosis code translations
- `HNC procedure ICD translation DF.csv` - Procedure code translations  
- `rxCodeTranslationDF_HNC.csv` - RxNorm CUI → medication names
- `ndcCodeTranslationDF_HNC.csv` - NDC → medication names

**Runtime**: ~20-30 minutes (API-dependent)  
**When to Run**: Initial setup only; update if new codes appear

---

###  PHASE 1: Data Exploration & Feature Engineering

#### `00 Data viewing.ipynb` - Exploratory Data Analysis
**Purpose**: Initial exploration of raw PCDM (Patient-Centered Data Model) data

**Key Analyses**:
- Table shape and column descriptions
- Patient demographics distribution
- Medication code frequencies
- Diagnosis prevalence in HNC cohort
- Temporal patterns (encounter dates, treatment dates)
- Missing data assessment
- Death proportion calculations

**Inputs**: Raw PCDM tables from `Data_import.py`  
**Outputs**: Statistical summaries and visualizations  
**Runtime**: ~5-10 minutes

---

#### `00 Identify chemotherapy medications.ipynb` - Chemotherapy Identification
**Purpose**: Identifies and labels chemotherapy medications for confounding adjustment

**Key Methods**:
- Regex pattern matching on medication names
- Cross-referencing with FDA-approved chemotherapy databases
- Manual curation of HNC-specific chemotherapy agents
- Extraction from medication administration and prescription tables

**Key Outputs**:
- Binary chemotherapy classification (integrated into feature matrix)
- Chemotherapy prevalence statistics
- Co-prescription patterns

**Inputs**: PCDM_PRESCRIBING, PCDM_MED_ADMIN + translation dictionaries  
**Runtime**: ~10-15 minutes  
**When to Run**: Before feature engineering (necessary for treatment confounding control)

---

#### `00 Identify surg_rad prevalance.ipynb` - Surgery/Radiation Identification
**Purpose**: Identifies surgical and radiation treatment exposure for confounding adjustment

**Key Analyses**:
- ICD procedure codes for surgeries (CPT codes)
- Radiation therapy identification (procedure codes, clinical observations, diagnosis codes)
- Treatment type prevalence rates by HPV status
- Co-occurrence patterns (surgery + radiation combinations)
- Temporal distribution of treatments relative to diagnosis

**Key Outputs**:
- Binary surgery indicator (SURGERY column)
- Binary radiation indicator (RADIATION column)
- Treatment prevalence tables
- Visualization of treatment patterns

**Statistical Methods**: Frequency analysis, cross-tabulation  
**Inputs**: PCDM_PROCEDURES, PCDM_DIAGNOSIS, PCDM_OBS_CLIN  
**Runtime**: ~15-20 minutes  
**When to Run**: Before feature engineering (for confounding variables)

---

#### `00 non merging input file creation patient level data.ipynb` - Patient Outcomes
**Purpose**: Creates patient-level demographic and survival outcome data

**Key Features Created**:
- Patient ID (anonymized)
- Age at diagnosis
- Sex, race, ethnicity
- HPV status
- HNC diagnosis date (index date)
- Metastasis event indicator (binary: 1 = metastasis, 0 = censored)
- Survival time (days from diagnosis to metastasis or censoring)
- Death dates and censoring information

**Process**:
1. Loads PCDM demographic and diagnosis tables
2. Identifies HNC diagnosis as index date
3. Searches for metastasis diagnosis codes (C77.x, C78.x, C79.x)
4. Calculates survival time (diagnosis → outcome)
5. Determines censoring (patients without metastasis)
6. Integrates death records

**Output**: `input_data/patient level data.csv`  
**Data Format**: One row per patient with demographic and outcome columns  
**Runtime**: ~10-15 minutes

---

#### `00 non merging input file creation modified sum.ipynb` - Feature Matrix Engineering
**Purpose**: Creates the primary feature matrix with 1 row per patient, where each row aggregates the SUM of all medication prescriptions, procedures, and diagnoses for that patient

**Key Features Engineered**:
- **Medications**: Count-based medication exposure (sum of ALL prescriptions/administrations per patient)
  - Format: `_medication_name` (leading underscore)
  - Example: `_atorvastatin`, `_metformin`, `_levothyroxine`
- **Procedures**: Binary indicators for specific procedures
  - Format: ICD procedure codes (e.g., `CPT_99213`)
- **Diagnoses**: Binary indicators for comorbidities
  - Format: ICD diagnosis codes (e.g., `I10`, `E11.9`)
- **Treatment Confounders**: Binary indicators
  - `SURGERY` - Any surgical procedure
  - `RADIATION` - Radiation therapy
  - `CHEMOTHERAPY` - Chemotherapy administration
  - `IMMUNOTHERAPY` - Immunotherapy treatment

**Aggregation Strategy**:
- **Medications**: Sum of prescription/administration counts (captures cumulative exposure)
- **Procedures/Diagnoses**: Binary presence/absence

**Data Processing Details**:
- Temporal filtering: Only exposures BEFORE metastasis/censoring date included
- Duplicate handling: Similar medications merged (e.g., `_thiamine` and `_thiamine hcl`)
- Code translation: Medical codes converted to readable names using translation dictionaries
- One-hot encoding: Features converted to binary/count columns

**Output**: `input_data/one_hot_encoded_sum_per_pat.csv`  
**Data Format**: **1 row per patient** × 1000-2000 feature columns
- Each column = sum/count of a specific medication, procedure, or diagnosis for that patient
- Medications: Cumulative prescription counts (e.g., 5 prescriptions of atorvastatin = value of 5)
- Procedures/Diagnoses: Binary presence (0 or 1)
**Runtime**: ~15-25 minutes

**Rationale for Count-Based Encoding**:
Medications are encoded as cumulative prescription counts rather than binary indicators to:
1. Capture dose-response relationships (higher exposure → greater biological effect)
2. Distinguish single prescriptions from sustained chronic use
3. Provide more statistical power for machine learning algorithms
4. Mirror quantitative approaches in genomics (mutation counts)
5. Reflect clinically meaningful vaIntegrated Cox Proportional Hazards & Machine Learning Analysis MAIN
**Purpose**: Comprehensive survival analysis and binary classification combining Cox Proportional Hazards models with ensemble machine learning methods

**Core Analysis Pipeline** (`output_table_xgboost_based_log_odds_with_rf` function):

**1. Machine Learning Classification**
- **XGBoost**: Gradient boosting with extensive hyperparameter tuning
  - RandomizedSearchCV with 5-fold cross-validation
  - Parameters tuned: n_estimators, learning_rate, max_depth, min_child_weight, gamma, subsample, colsample_bytree, regularization (L1/L2)
  - Class balancing via scale_pos_weight and RandomOverSampler
- **Random Forest**: Ensemble validation
  - Hyperparameter tuning: n_estimators, max_depth, min_samples_split/leaf, max_features, bootstrap
  - Balanced class weights
- **Logistic Regression**: Interpretable linear baseline
  - L1 and L2 regularization with liblinear solver
  - Log-odds ratios for effect size interpretation

**2. SHAP (SHapley Additive exPlanations) Analysis**
- TreeExplainer for XGBoost model interpretation
- Mean absolute SHAP values for feature importance ranking
- SHAP summary plots for:
  - All features (top 50 displayed)
  - Drug features only (excluding treatment confounders)
- Directional importance: positive SHAP = increased metastasis risk, negative SHAP = protective

**3. Cox Proportional Hazards Survival Analysis**

**STEP 1: Univariate Cox Analysis**
- Each feature tested individually for survival association
- Generates hazard ratios (HR) with 95% confidence intervals
- **FDR correction** (Benjamini-Hochberg) for multiple testing
- Outputs both uncorrected and FDR-corrected p-values
- Reports:
  - Top 10 protective features (HR < 1)
  - Top 10 risk features (HR > 1)
  - Concordance index per feature

**STEP 2: Multivariate Cox Analysis**
- Joint model with all top features (selected by XGBoost importance)
- **All drug features automatically included** regardless of XGBoost ranking
- Adjusted hazard ratios controlling for confounding
- Model concordance index (C-index) for overall predictive performance
- Forest plots for visualization

**4. Log-Odds Ratio Calculation**
- 2×2 contingency tables for each feature vs. metastasis outcome
- Calculates odds ratios and log-transforms
- Separate visualization for drug features

**Key Outputs**:
- **Feature importance tables** combining:
  - XGBoost importance (signed)
  - Random Forest importance
  - Logistic Regression coefficients
  - Mean SHAP values (true and absolute)
  - Log-odds ratios
  - Univariate Cox: HR, CI, p-value, FDR-corrected p-value
  - Multivariate Cox: adjusted HR, CI, p-value, FDR-corrected p-value
- **Visualizations**:
  - SHAP summary plots (all features and drug-specific)
  - Forest plots (multivariate Cox HRs)
  - Top 50 protective features from Cox (custom forest plot)
  - Log-odds ratio bar plots (all features and drugs)
  - Feature importance bar plots

**Saved Outputs**:
- `Results/ML analysis/hpv_positive_ml_xgb_results.csv` - Comprehensive HPV+ results
- `Results/ML analysis/hpv_negative_ml_xgb_results.csv` - Comprehensive HPV- results
- `Results/ML analysis/hpv_positive_ml_drug_xgb_results.csv` - HPV+ drug-only filtered results
- `Results/ML analysis/hpv_negative_ml_drug_xgb_results.csv` - HPV- drug-only filtered results
- `Results/ML analysis/ml_feature_stability_hpv_positive.csv` - HPV+ feature selection stability
- `Results/ML analysis/ml_feature_stability_hpv_negative.csv` - HPV- feature selection stability
- Contains all metrics from ML, SHAP, Cox (univariate & multivariate), and log-odds analyses

**Statistical Rigor**:
- **Multiple testing correction**: Benjamini-Hochberg FDR for univariate Cox
- **Dual statistical frameworks**: Time-to-event (Cox) + binary classification (ML)
- **Feature stability**: Consistent selection across CV folds
- **Confounding control**: Surgery, radiation, chemotherapy, immunotherapy included
- **Interpretability**: SHAP + Cox HR + log-odds for triangulated understanding

**Runtime**: ~45-60 minutes per subgroup (HPV+ and HPV-)alidation with class balancing (RandomOverSampler)
- SHAP values for directional feature importance (protective vs. harmful)
- Log-odds ratios from Logistic Regression (interpretable coefficients)
- Comprehensive metrics: AUC, accuracy, precision, recall, F1
- Feature stability assessment across folds

**Runtime**: ~20-30 minutes

---

#### `03 top feature correlation check.ipynb` - Validation & Correlation Analysis MAIN
**Purpose**: Load ML/Cox results from `02 data_analysis_ml.ipynb`, perform confounder correlation analysis, and generate visualizations for top drug candidates

**Key Steps**:
1. Loads `input_data/one_hot_encoded_sum_per_pat.csv` and `input_data/patient level data.csv`
2. Loads HPV status from external IRB data volume
3. Loads ML results from `Results/ML analysis/hpv_*_ml_xgb_results.csv`
4. Runs Cox analysis on top ML-selected features
5. Performs confounder correlation analysis: flags features with |r| > 0.5 to SURGERY/RADIATION/CHEMOTHERAPY/IMMUNOTHERAPY
6. Generates summary tables and visualizations (displayed in notebook; no CSV output files)

**Key Features**:
- Confounder filtering: reports features strongly correlated with treatment confounders
- Kaplan-Meier plots for top validated drug candidates
- Forest plots for hazard ratio visualization
- HPV subgroup comparison: shared vs. unique features
- Summary statistics of drug candidates with confounder annotations

**Runtime**: ~15-20 minutes

**Critical Validation Checks**:
1. ✓ Univariate Cox significant (FDR < 0.05)
2. ✓ Multivariate Cox significant (p < 0.05)
3. ✓ High ML feature importance (top quartile)
4. ✓ No strong treatment confounder correlation (|r| < 0.5)
5. ✓ Consistent direction across methods

---

## Key Output Files

### For Primary Results

| File | Content | Use Case |
|------|---------|----------|
| `Results/ML analysis/hpv_positive_ml_xgb_results.csv` | **Comprehensive integrated results (HPV+)**: ML (XGBoost, RF, LR) + SHAP + Cox (univariate & multivariate) + log-odds | **PRIMARY results file - all methods combined** |
| `Results/ML analysis/hpv_negative_ml_xgb_results.csv` | **Comprehensive integrated results (HPV-)**: ML (XGBoost, RF, LR) + SHAP + Cox (univariate & multivariate) + log-odds | **PRIMARY results file - all methods combined** |
| `Results/ML analysis/hpv_positive_ml_drug_xgb_results.csv` | Drug-only subset of HPV+ results | **Drug candidates for downstream integration** |
| `Results/ML analysis/hpv_negative_ml_drug_xgb_results.csv` | Drug-only subset of HPV- results | **Drug candidates for downstream integration** |

**Note**: The `hpv_*_ml_xgb_results.csv` files from `02 data_analysis_ml.ipynb` contain the most comprehensive feature profiles, combining all statistical methods in a single integrated analysis.

### Columns in Comprehensive Results (`hpv_*_ml_xgb_results.csv`)

These files contain the complete integrated analysis from `output_table_xgboost_based_log_odds_with_rf()`:

**Machine Learning Features**:
```
xgb_importance                    - XGBoost feature importance (signed)
xgb_absolute_Importance          - XGBoost importance (unsigned, for ranking)
rf_importance                    - Random Forest importance
rf_absolute_Importance           - Random Forest importance (unsigned)
log_reg_coef                     - Logistic Regression coefficient
```

**SHAP (Explainable AI) Features**:
```
XGB Mean SHAP Value (True)       - Directional SHAP (negative = protective, positive = risk)
XGB Mean Absolute SHAP Value     - SHAP magnitude for ranking
XGB Mean Absolute SHAP           - Alternative SHAP metric
```

**Cox Proportional Hazards Features**:
```
univariate_coef                  - Cox coefficient (log hazard ratio) - individual feature effect
univariate_hr                    - Hazard ratio (exp(coef)) - interpretable effect size
univariate_se                    - Standard error of coefficient
univariate_p                     - P-value (uncorrected)
univariate_p_fdr                 - FDR-corrected p-value (Benjamini-Hochberg) USE THIS
univariate_ci_lower              - 95% CI lower bound for HR
univariate_ci_upper              - 95% CI upper bound for HR
univariate_c_index               - Concordance index (predictive accuracy)
univariate_significant           - Boolean: p < 0.05 (uncorrected)
univariate_significant_fdr       - Boolean: FDR < 0.05 (corrected) RECOMMENDED

multivariate_coef                - Adjusted Cox coefficient - effect after controlling for other features
multivariate_hr                  - Adjusted hazard ratio
multivariate_se                  - Standard error of adjusted coefficient
multivariate_p                   - P-value in multivariate model
multivariate_p_fdr               - FDR-corrected p-value (multivariate) USE THIS
multivariate_ci_lower            - 95% CI lower bound for adjusted HR
multivariate_ci_upper            - 95% CI upper bound for adjusted HR
multivariate_significant         - Boolean: p < 0.05
multivariate_significant_fdr     - Boolean: FDR < 0.05
```

**Log-Odds Features**:
```
log_odds_ratio                   - Log-odds from 2×2 contingency table
```

### Interpretation Guide for Integrated Results

**Effect Direction**:
- **Cox HR > 1** OR **Positive SHAP**: Increased metastasis risk (harmful)
- **Cox HR < 1** OR **Negative SHAP**: Decreased metastasis risk (protective)
- **Consistent direction across Cox, SHAP, and log-odds**: Strong evidence

**Effect Magnitude**:
- **Hazard Ratio Interpretation**:
  - HR = 1.5: 50% increased risk per unit increase
  - HR = 0.7: 30% decreased risk per unit increase
  - HR = 2.0: 100% increased risk (doubles risk)
  - HR = 0.5: 50% decreased risk (halves risk)
- **SHAP Values**: Larger |SHAP| = stronger predictive importance
- **Feature Importance**: Higher rank = more critical for model decisions

**Statistical Significance**:
- **FDR < 0.05** (univariate_significant_fdr): Gold standard after multiple testing correction
- **p < 0.05** (multivariate_significant): Significant after adjusting for other features
- **Both univariate and multivariate significant**: Strong independent effect

**Model Performance**:
- **C-index**: 0.5 = random guess, 0.7 = good discrimination, 0.8 = excellent, 0.9+ = outstanding
- **XGBoost ROC-AUC**: Similar interpretation to C-index

**Prioritization Strategy** (recommended):
1. Features with **univariate_significant_fdr = True** (FDR < 0.05)
2. Features with **multivariate_significant = True** (p < 0.05)
3. High ML importance (top quartile in xgb_absolute_Importance)
4. Consistent direction across Cox HR and SHAP
5. No strong treatment confounder correlation (check in notebook 03)

---

## Reproducibility Checklist

### Environment Setup
```bash
# Required Python packages
pip install pandas numpy matplotlib seaborn
pip install scikit-learn xgboost imbalanced-learn
pip install lifelines statsmodels
pip install shap tqdm

# Alternative: conda
conda create -n hnc_analysis python=3.9
conda activate hnc_analysis
conda install pandas numpy matplotlib seaborn scikit-learn
conda install -c conda-forge xgboost imbalanced-learn lifelines statsmodels shap
```

### Data Requirements

**IMPORTANT**: Input data files and translation dictionaries are **NOT included** in this repository due to Protected Health Information (PHI) restrictions.

**You MUST generate these files first** by running Phase 0 and Phase 1 notebooks:

#### Required Files (Generated by You):
1. **`input_data/one_hot_encoded_sum_per_pat.csv`** - Main feature matrix
   - **Created by**: `00 non merging input file creation modified sum.ipynb`
   - **Format**: 1 row per patient, each column = SUM of specific medication/procedure counts
   - **Contains**: Cumulative medication prescription counts + binary procedure/diagnosis indicators
   - Example: If patient had 3 prescriptions of levothyroxine, column `_levothyroxine` = 3

2. **`input_data/patient level data.csv`** - Patient outcomes
   - **Created by**: `00 non merging input file creation patient level data.ipynb`
   - **Format**: 1 row per patient with demographic and survival data
   - **Contains**: Demographics, survival time, metastasis status, HPV status

3. **`ICD_RX translation/*.csv`** - Medical code dictionaries
   - **Created by**: `00 create ICD_RX translation DF.ipynb`
   - Required for: Translating medical codes to human-readable drug/diagnosis names

**To generate these files**: See "Analysis Pipeline" section below and run notebooks in Phase 0 → Phase 1 order.

### Expected Runtime
- Full pipeline: ~1.5-2 hours (on standard laptop)
- Cox notebook: ~35 minutes (most compute-intensive)
- ML notebook: ~25 minutes
- Correlation notebook: ~18 minutes

---

## Troubleshooting

### Common Issues

**Issue**: `FileNotFoundError: [Errno 2] No such file or directory: 'input_data/...'` or `ICD_RX translation/...`
- **Cause**: Required input files are not included in the repository (PHI restrictions)
- **Fix**: You MUST generate these files by running Phase 0 and Phase 1 notebooks first
- **Steps**:
  1. Update paths in `Data_import.py` (replace `IRB_ID` and `DATA_FOLDER`)
  2. Run `00 create ICD_RX translation DF.ipynb` to create translation dictionaries
  3. Run Phase 1 notebooks to create `input_data/` files
  4. Only then run Phase 2 analysis notebooks
- **See**: "Data Availability Notice" at top of README for full details

**Issue**: `AttributeError: 'RandomOverSampler' object has no attribute '_check_n_features'`
- **Cause**: Scikit-learn/imbalanced-learn version mismatch
- **Fix**: `conda update scikit-learn imbalanced-learn` OR use the compatibility patch in ML notebook imports cell

**Issue**: Cox model convergence warnings
- **Solution**: Penalization (λ=0.01) is applied automatically; warnings can be ignored if model converges
- **Check**: Verify `multivariate_coef` column has values (not NaN)

**Issue**: Memory errors during feature selection
- **Solution**: Reduce number of CV folds or features
- **Edit**: Change `cv=StratifiedKFold(n_splits=5)` to `n_splits=3`

**Issue**: Missing output files
- **Check**: Ensure `Results/` directory exists
- **Fix**: `mkdir -p Results` before running notebooks

**Issue**: Jupyter kernel crashes during XGBoost
- **Solution**: Reduce `n_estimators` or `max_depth` in XGBoost parameters
- **Alternative**: Run with more memory or on cluster

---

## Documentation Guide

This project has comprehensive documentation across multiple files:

### 1. **README.md** (This File)
**Purpose**: Workflow overview and execution instructions

**Read this for**:
- Understanding the overall analysis pipeline
- Learning what each notebook does
- Execution order and dependencies
- Input/output file descriptions
- Troubleshooting common issues
- Quick reference for results interpretation

**Best for**: Users who want to run the analysis or understand the workflow

---

### 2. **CODE_COMMENTS_GUIDE.md** 
**Purpose**: In-depth code explanations and statistical methodology

**Read this for**:
- Detailed function explanations with examples
- Understanding WHY code is written a certain way
- Statistical concepts (nested CV, feature stability, etc.)
- Line-by-line code walkthroughs
- Methodology decisions and justifications
- Common questions answered

**Best for**: Developers, researchers, or anyone wanting deep understanding of the code

**Key sections**:
- Data preparation processes (how features are created)
- Feature selection methodology (multi-method nested CV explained)
- Cox analysis (survival modeling details)
- ML analysis (XGBoost, Random Forest, Logistic Regression)
- Common functions (pull_drugs, age_group, etc.)
- Statistical concepts (class imbalance, feature stability)

---

---

### 3. **Data_import.py**
**Purpose**: Load all PCDM tables from external drive

**Contains**: Connection strings and data loading functions for OMOP CDM tables (used for data preparation notebooks 00*)

---

## Publication-Ready Results

### For Methods Section
Extract from **"Statistical Rigor & Publication Standards"** section above:
- Cox regression with penalization (λ=0.01)
- Benjamini-Hochberg FDR correction for univariate analyses  
- Nested 5-fold cross-validation for feature selection
- Multi-method consensus (≥3 of 5 methods: Chi-square, Lasso, Variance, XGBoost, Random Forest)
- Train/test validation (80/20 stratified split)
- C-index for Cox discrimination, ROC-AUC for ML
- SHAP values for directional feature importance

### For Results Tables

**Table 1: Top Protective Factors (HPV+)**
- Sort by: `univariate_hr` ascending (HR < 1) 
- Filter: `univariate_significant_fdr == True`
- Columns: feature, univariate_hr, 95% CI, FDR p-value, multivariate_hr, ML importance

**Table 2: Top Risk Factors (HPV+)**  
- Sort by: `univariate_hr` descending (HR > 1)
- Filter: `univariate_significant_fdr == True`
- Columns: Same as Table 1

**Table S1: Complete Results**
- Use: `cox_comprehensive_all_patients.csv` (all features)

### For Figures

**Figure 1: Forest Plot of Top Features**
- Generated automatically in notebook 03
- Shows HRs with 95% CIs, sorted by magnitude
- Includes both HPV+ and HPV- side-by-side

**Figure 2: Kaplan-Meier Curves**  
- Generated for top 5-10 features in notebooks 02 and 03
- Shows survival probability by feature exposure (high vs. low)
- Log-rank test p-values displayed

**Figure 3: Feature Importance Comparison**
- Cox HR (x-axis) vs. ML Importance (y-axis)
- Points colored by significance status
- Identify concordant features (both methods agree)

### Recommended Reporting

For each validated feature, report:
1. **Univariate Cox**: HR (95% CI), FDR-corrected p-value, C-index
2. **Multivariate Cox**: Adjusted HR (95% CI), p-value
3. **ML Evidence**: XGBoost importance, mean |SHAP|, direction
4. **Validation**: Train vs test C-index, cross-validation stability
5. **Clinical Context**: Drug class, mechanism, existing literature

**Example**:
> "Drug X showed protective association with metastasis in HPV+ patients (univariate HR=0.65, 95% CI: 0.52-0.81, FDR p=0.003). This association remained significant after adjusting for age, sex, and treatments (multivariate HR=0.71, 95% CI: 0.56-0.90, p=0.012). Machine learning models concordantly identified Drug X as highly important (XGBoost importance=0.082, SHAP=-0.15, indicating protective effect). The model achieved C-index=0.72 (95% CI: 0.68-0.76) in independent test data."

---

## Citation & Acknowledgments

### Software Dependencies
- **Python 3.9+**: Core analysis environment
- **pandas/numpy**: Data manipulation and numerical computing
- **scikit-learn**: Machine learning and preprocessing
- **lifelines**: Cox survival analysis (Davidson-Pilon, 2019)
- **XGBoost**: Gradient boosting (Chen & Guestrin, 2016)
- **statsmodels**: Statistical tests and FDR correction
- **SHAP**: Interpretable ML (Lundberg & Lee, 2017)

### Key References
1. Davidson-Pilon, C. (2019). lifelines: survival analysis in Python. *Journal of Open Source Software*, 4(40), 1317.
2. Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *KDD*, 785-794.
3. Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. *NeurIPS*, 30.
4. Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate. *Journal of the Royal Statistical Society: Series B*, 57(1), 289-300.

### Dataset
OMOP Common Data Model (CDM) v5.3 - Electronic Health Records from [Institution Name]

---

## Contact & Support

For questions about:
- **Analysis methodology**: See CODE_COMMENTS_GUIDE.md
- **Execution errors**: See Troubleshooting section above
- **Results interpretation**: See Key Output Files section
- **Code modifications**: Contact [Maintainer]

**Validation Status**: All notebooks executable, all tests passing (last verified: [Date])

**License**: [Specify license - e.g., MIT, Apache 2.0, or Proprietary]

---

*This analysis pipeline is publication-ready with comprehensive statistical rigor, validation, and documentation. All results are reproducible using the provided notebooks and input data.*

**Read this for**:
- Understanding data sources
- Table-by-table purpose descriptions
- Why specific encoding is used
- Module docstring with full table list

**Best for**: Understanding raw data structure

---

### 4. **VERIFICATION_SUMMARY.md**
**Purpose**: Verification report from testing all notebooks

**Read this for**:
- Confirmation that all notebooks are properly structured
- Known dependencies (external drive, HPV data)
- Verification of bug fixes
- Status of each notebook

**Best for**: Confirming analysis is ready to run

---

### How to Use This Documentation

**If you want to**:

- **Run the analysis** → Read [README.md](README.md) sections: "Execution Order", "Expected Outputs", "Troubleshooting"

- **Understand a specific function** → Search [CODE_COMMENTS_GUIDE.md](CODE_COMMENTS_GUIDE.md) for the function name

- **Learn about feature selection** → [CODE_COMMENTS_GUIDE.md](CODE_COMMENTS_GUIDE.md) → "Feature Selection Function (Cox)" section

- **Interpret results** → [README.md](README.md) → "Results Interpretation Guide" section

- **Debug an error** → [README.md](README.md) → "Common Issues and Troubleshooting" section

- **Understand why we use both Cox and ML** → [CODE_COMMENTS_GUIDE.md](CODE_COMMENTS_GUIDE.md) → "02 ML Analysis" → "Why Machine Learning?" section

- **Learn what pull_drugs() does** → [CODE_COMMENTS_GUIDE.md](CODE_COMMENTS_GUIDE.md) → "Drug Filtering: pull_drugs()" section

---

## Workflow Pipeline

### Phase 0: Data Preparation (00 notebooks)

#### **00 Data viewing.ipynb**
- **Purpose**: Initial exploration of raw PCDM (Patient-Centered Data Model) data
- **Process**:
  - Imports raw data from `Data_import.py`
  - Examines data structure, patient counts, and death records
  - Validates data quality and completeness

#### **00 non merging input file creation patient level data.ipynb**
- **Purpose**: Creates patient-level demographic and outcome data
- **Process**:
  1. Loads PCDM tables from `Data_import.py`
  2. Loads ICD/RX code translation dictionaries
  3. Extracts patient demographics (age, sex, race, ethnicity)
  4. Defines metastasis outcome from diagnosis codes
  5. Calculates survival time (diagnosis date → outcome date)
  6. Creates binary event indicator (metastasis = 1, censored = 0)
  7. **Output**: `./input_data/patient level data.csv`

#### **00 non merging input file creation modified sum.ipynb**
- **Purpose**: Feature engineering for medications, procedures, and diagnoses
- **Process**:
  1. Loads PCDM medication, procedure, and diagnosis tables
  2. Translates medical codes to readable drug/procedure names using translation dictionaries
  3. Aggregates medication exposures per patient:
     - Counts occurrences of each medication before metastasis/censoring
     - One-hot encodes categorical features
     - Sum aggregation strategy (total exposure count per feature)
  4. Handles thiamine duplicate by merging `_thiamine` and `_thiamine hcl`
  5. Adds treatment confounders: SURGERY, RADIATION, CHEMOTHERAPY, IMMUNOTHERAPY
  6. **Output**: `./input_data/one_hot_encoded_sum_per_pat.csv`

**Key Data Processing Decisions**:
- Sum aggregation chosen over binary (any exposure) to capture cumulative medication effects
- Medications coded with leading underscore (e.g., `_atorvastatin`)
- ICD diagnosis/procedure codes kept as-is (e.g., `Z85.3`, `J96.01`)
- Survival time calculated in days from HNC diagnosis to outcome/censoring

---

### Phase 1: Feature Selection

Both Cox and ML analyses use **multi-method feature selection** to identify robust predictive features:

#### **Feature Selection Methods**

**Cox Analysis** (`02_data_analysis_cox.ipynb`):
1. **LASSO Cox Regression**: L1 regularization with cross-validated penalty selection
2. **Univariate Cox Selection**: Individual univariate C-index evaluation
3. **Variance Thresholding**: Removes low-variance features

**ML Analysis** (`02 data_analysis_ml.ipynb`):
1. **LASSO Logistic Regression**: L1 regularized feature selection
2. **Chi-squared Test**: Statistical association with outcome
3. **Variance Thresholding**: Removes features with <80% stability
4. **XGBoost Feature Importance**: Gradient boosting-based importance
5. **Random Forest Feature Importance**: Tree-based importance

#### **Feature Stability Framework**

Both analyses use **nested cross-validation** to ensure robust feature selection:

```
Outer Loop (5-fold stratified CV):
  ├─ Split data → Training (80%) + Test (20%)
  └─ For each training fold:
       Inner Loop (Feature Selection):
         ├─ Run all selection methods
         ├─ Record which features are selected
         └─ Track selection frequency across folds
```

**Feature Stability Metrics**:
- **Selection Frequency**: Proportion of CV folds selecting each feature
- **Highly Stable Features**: Selected in ≥80% of folds
- **Output**: `./Results/ML analysis/ml_feature_stability_hpv_positive.csv` and `./Results/ML analysis/ml_feature_stability_hpv_negative.csv`

**Why Stability Matters**:
- Features selected consistently across folds are more likely to generalize
- Reduces overfitting from random data splits
- Provides confidence metric for each feature

---

### Phase 2: Cox Survival Analysis

#### **02_data_analysis_cox.ipynb**

**Purpose**: Time-to-metastasis survival analysis using Cox Proportional Hazards models

**Key Steps**:

1. **Data Loading and Preprocessing**
   - Merges `one_hot_encoded_sum_per_pat.csv` with `patient level data.csv`
   - Merges thiamine duplicate columns
   - Creates age groups
   - Filters patients with `Survival_Time > 2` days
   - Adds HPV status from external dataset
   - Splits into HPV+ and HPV- subgroups

2. **Feature Selection per Subgroup** (see Phase 1)
   - Run separately for: All patients, HPV+, HPV-
   - Outputs feature stability DataFrames
   - Identifies features to drop (`drop_var_cox_hpv_pos`, `drop_var_cox_hpv_neg`)

3. **Final Cox Model Fitting** (HPV+ and HPV-)
   ```python
   # Uses features NOT in drop_var_cox (features that passed selection)
   selected_features = [col for col in x.columns 
                        if col not in drop_var_cox_hpv_pos 
                        or col in confounders]
   
   # Fit Cox model
   cph = CoxPHFitter()
   cph.fit(train_df, duration_col='Survival_Time', 
           event_col='event', show_progress=False)
   ```

4. **Extract Cox Coefficients**
   - **coef**: Log hazard ratio (β coefficient)
   - **exp(coef)**: Hazard ratio (HR)
     - HR > 1: Increased metastasis risk
     - HR < 1: Decreased metastasis risk
   - **p**: Statistical significance
   - **abs_coef**: Absolute coefficient magnitude (for ranking)

5. **Drug-Specific Analysis**
   - Extract top 100 features by `abs_coef`
   - Filter for drug features using `pull_drugs()` function:
     - Excludes ICD codes (features with digit as 2nd character)
     - Keeps only medication features
   - Create visualizations showing Cox coefficients for top 20 drugs
   - Color coding: Red = protective (HR<1), Blue = risk factor (HR>1)

6. **Results Export**
   - `hpv_positive_cox_coef_results.csv`: All HPV+ Cox coefficients
   - `hpv_negative_cox_coef_results.csv`: All HPV- Cox coefficients
   - `hpv_positive_cox_coef_drug_results.csv`: Drug-only results (HPV+)
   - `hpv_negative_cox_coef_drug_results.csv`: Drug-only results (HPV-)
   - `hpv_drug_comparison_cox_coef.csv`: Cross-subgroup drug comparison

**Key Cox Metrics**:
- **C-index** (Concordance Index): Model discrimination (0.5 = random, 1.0 = perfect)
- **Hazard Ratio Interpretation**:
  - HR = 1.5: 50% increased risk
  - HR = 0.7: 30% decreased risk
  - HR = 2.0: 100% increased risk (doubles risk)

**Confounders Always Retained**: SURGERY, RADIATION, CHEMOTHERAPY, IMMUNOTHERAPY

---

### Phase 3: Machine Learning Classification

#### **02 data_analysis_ml.ipynb**

**Purpose**: Binary classification of metastasis occurrence using ensemble ML methods

**Key Steps**:

1. **Data Loading** (identical to Cox analysis)
   - Merges feature matrix with patient data
   - Splits by HPV status
   - Target variable: `METASTASIS` (binary: 0/1)

2. **Feature Selection per Subgroup**
   - Multi-method selection (LASSO, Chi-squared, Variance, XGBoost, Random Forest)
   - Nested CV for feature stability
   - Outputs: `ml_feature_stability_hpv_positive.csv`, `ml_feature_stability_hpv_negative.csv`

3. **Model Training with Hyperparameter Tuning**
   
   For each subgroup (All, HPV+, HPV-), train 3 models:
   
   **A. XGBoost Classifier**
   ```python
   # Hyperparameters tuned via RandomizedSearchCV:
   - n_estimators: 50-600 (number of trees)
   - learning_rate: 0.01-0.3 (step size)
   - max_depth: 3-11 (tree depth)
   - min_child_weight: 1-11 (regularization)
   - gamma: 0-0.5 (split threshold)
   - subsample: 0.6-0.9 (data sampling)
   - colsample_bytree: 0.6-0.9 (feature sampling)
   - reg_alpha/lambda: L1/L2 regularization
   - scale_pos_weight: Class imbalance handling
   ```
   
   **B. Random Forest Classifier**
   ```python
   - n_estimators: 50-500 (number of trees)
   - max_depth: 10-100 or None
   - min_samples_split: 2, 5, 10
   - min_samples_leaf: 1, 2, 4
   - max_features: sqrt, log2, None
   - class_weight: None or 'balanced'
   ```
   
   **C. Logistic Regression**
   ```python
   - C: 10^-4 to 10^4 (regularization strength)
   - penalty: L1, L2
   - solver: liblinear
   - class_weight: None or 'balanced'
   ```

4. **Class Imbalance Handling**
   - **RandomOverSampler**: Duplicate minority class samples
   - Applied to training data only (not test data)
   - Prevents test set leakage

5. **Cross-Validation and Model Selection**
   - 5-fold stratified CV
   - Metrics: Accuracy, ROC-AUC, F1-score
   - Best model selected by F1-score (balances precision/recall)
   - ROC curves plotted for each fold + mean ROC

6. **Feature Importance Extraction**
   
   **XGBoost Importance**:
   - **xgb_importance**: Raw feature weight from gradient boosting
   - **xgb_absolute_Importance**: Absolute value (for ranking)
   - **XGB Mean SHAP Value**: SHAP (SHapley Additive exPlanations) values
     - Explains contribution to prediction
     - Model-agnostic interpretability
   
   **Random Forest Importance**:
   - Based on Gini impurity reduction
   
   **Logistic Regression Coefficients**:
   - Linear model weights (log-odds)

7. **Cox Model Integration** (Bonus)
   - Fits Cox model on top 15 XGBoost features
   - Provides hazard ratios for ML-selected features
   - Bridges classification and survival analysis

8. **Log-Odds Ratio Calculation**
   ```python
   # For each feature, calculate odds ratio from 2x2 contingency table:
   n11 = patients with feature AND no metastasis
   n10 = patients with feature AND metastasis
   n01 = patients without feature AND no metastasis
   n00 = patients without feature AND metastasis
   
   odds_ratio = (n11 * n00) / (n10 * n01)
   log_odds_ratio = log(odds_ratio)
   ```

9. **Drug-Specific Analysis**
   - Load feature importance CSV: `{file_name}_hpv_positive_working_data_feature_importances.csv`
   - Extract top 100 features by `xgb_absolute_Importance`
   - Filter for drugs using `pull_drugs()` function
   - Visualize top 20 drugs with XGBoost importance bar charts
   - Color: HPV+ = Blue (#2E86AB), HPV- = Purple (#A23B72)

10. **Results Export**
    - `hpv_positive_ml_xgb_results.csv`: All HPV+ ML features
    - `hpv_negative_ml_xgb_results.csv`: All HPV- ML features
    - `hpv_positive_ml_xgb_drug_results.csv`: Drug features only (HPV+)
    - `hpv_negative_ml_xgb_drug_results.csv`: Drug features only (HPV-)
    - `hpv_drug_comparison_ml_xgb.csv`: Cross-subgroup drug comparison
    - K-fold CV results for each model type

**Key ML Metrics**:
- **ROC-AUC**: Area under receiver operating characteristic curve (0.5-1.0)
- **F1-Score**: Harmonic mean of precision and recall
- **Accuracy**: Overall correct predictions
- **C-index**: Concordance for Cox model component (survival analysis)

**Note**: This section describes the legacy ML-only analysis workflow. The current integrated approach in `output_table_xgboost_based_log_odds_with_rf()` function combines all these steps with Cox analysis in a unified pipeline.

---

### Phase 2: Validation and Integration

#### **03 top feature correlation check.ipynb**

**Purpose**: Validate integrated results from `02 data_analysis_ml.ipynb`, assess confounding, and perform correlation analysis

**Key Steps**:

1. **Load Integrated Results from 02 data_analysis_ml.ipynb**
   ```python
   # Load comprehensive feature importance files (Cox + ML combined)
   results_hpv_pos = pd.read_csv('./Results/ML analysis/hpv_positive_ml_xgb_results.csv')
   results_hpv_neg = pd.read_csv('./Results/ML analysis/hpv_negative_ml_xgb_results.csv')
   ```
   
   These files already contain:
   - Machine Learning metrics (XGBoost, Random Forest, Logistic Regression)
   - SHAP values for interpretation
   - Cox Proportional Hazards results (univariate & multivariate)
   - Log-odds ratios

2. **Combined Results Analysis**
   
   The integrated results already contain:
   - **From ML**: `xgb_importance`, `xgb_absolute_Importance`, `XGB Mean Absolute SHAP Value`, `rf_importance`, `log_reg_coef`, `log_odds_ratio`
   - **From Cox**: 
     - Univariate: `univariate_coef`, `univariate_hr`, `univariate_p`, `univariate_p_fdr`, `univariate_ci_lower`, `univariate_ci_upper`, `univariate_c_index`, `univariate_significant`, `univariate_significant_fdr`
     - Multivariate: `multivariate_coef`, `multivariate_hr`, `multivariate_p`, `multivariate_p_fdr`, `multivariate_ci_lower`, `multivariate_ci_upper`, `multivariate_significant`, `multivariate_significant_fdr`

3. **Feature Prioritization**
   - Identifies features significant in **both** Cox (FDR<0.05) and ML (high SHAP/importance)
   - Creates combined importance scores
   - Quantifies agreement between survival and classification approaches
   - Focus on features with consistent direction (protective vs. harmful) across methods

4. **Visualization: Cox vs ML Scatter Plot**
   ```python
   def plot_cox_vs_ml_importance(combined_df, title, top_n=20):
       # Scatter plot: x = abs_coef, y = xgb_absolute_Importance
       # Color: Cox p-value (green = significant, red = not significant)
       # Labels: Top 10 features annotated
   ```
   - Helps identify features strong in both analyses (top-right quadrant)
   - Color-coded by statistical significance

5. **Correlation Analysis Function**
   ```python
   def calculation_confounding_effect(data, variable):
       # Calculates Pearson correlation between variable and all others
       # Identifies potential confounding variables
       # Visualizes top 20 correlations with bar chart
   ```
   
   **Correlation Strength Interpretation**:
   - 0.00 - 0.10: Negligible
   - 0.10 - 0.30: Weak
   - 0.30 - 0.50: Moderate
   - 0.50 - 0.70: Strong
   - 0.70 - 0.90: Very Strong
   - 0.90 - 1.00: Nearly Perfect

6. **Kaplan-Meier Plots by Drug Exposure**
   ```python
   def km_plot_by_group(data, med):
       # Plots survival curves: med=0 vs med≠0
       # Performs log-rank test for significance
       # Annotates p-value on plot
   ```
   - Visual assessment of drug impact on survival
   - Statistical test for differences between exposure groups

7. **Forest Plot for Hazard Ratios**
   ```python
   def forest_plot(data, variables):
       # Fits Cox model on selected variables
       # Plots hazard ratios with confidence intervals
       # Visual comparison of drug effects
   ```

8. **Top Drug Lists** (Manually Defined)
   ```python
   # HPV+ top drugs
   top_hpv_pos_meds = ['_atorvastatin', '_thiamine', '_melatonin', 
                       '_levothyroxine', '_heparin']
   
   # HPV- top drugs
   top_hpv_neg_meds = ['_valacyclovir', '_melatonin', '_levothyroxine', 
                       '_atorvastatin', '_thiamine', '_lidocaine']
   ```

9. **Comprehensive Analysis Loop**
   ```python
   for med in top_hpv_pos_meds:
       # 1. Correlation analysis (confounding assessment)
       calculation_confounding_effect(hpv_positive_working_data, med)
       
       # 2. Kaplan-Meier survival curves
       km_plot_by_group(hpv_positive_working_data, med)
   
   # 3. Forest plot for all top drugs together
   forest_plot(hpv_positive_working_data, top_hpv_pos_meds)
   ```

10. **Results Export**
    - `combined_cox_ml_hpv_positive.csv`: Merged Cox + ML results (HPV+)
    - `combined_cox_ml_hpv_negative.csv`: Merged Cox + ML results (HPV-)

**Analysis Goals**:
- **Confounding Assessment**: Check if drug effects are confounded by age, other medications, or treatments
- **Survival Validation**: Verify ML predictions align with actual survival differences
- **Consistency Check**: Ensure Cox and ML methods identify similar important features

---

## Key Functions and Utilities

### Data Processing Functions

```python
def age_group(age):
    """
    Bins age into 8 categorical groups for analysis.
    
    Returns:
    --------
    1: 10-20 years
    2: 21-30 years
    3: 31-40 years
    4: 41-50 years
    5: 51-60 years
    6: 61-70 years
    7: 71-80 years
    8: 80+ years
    
    Purpose: Captures non-linear age effects on metastasis risk
    """
    Parameters:
    -----------
    feature_list : list
        List of feature names to filter
    has_underscore : bool, default=True
        Whether features start with underscore
    
    Logic:
    ------
    Medical codes are prefixed with underscore: _atorvastatin, _Z85.3, _J96.01
    
    Decision Rule:
    - Examine 2nd character (position 1 after '_'):
        - If DIGIT → ICD code (diagnosis/procedure) → EXCLUDE
        - If LETTER → Medication name → INCLUDE
    
    Examples:
    ---------
    KEEP (medications):
    - '_atorvastatin' → 'a' is letter → drug
    - '_thiamine' → 't' is letter → drug
    - '_levothyroxine' → 'l' is letter → drug
    
    EXCLUDE (non-medications):
    - '_Z85.3' → 'Z' followed by '8' (digit) → ICD diagnosis code
    - '_J96.01' → 'J' followed by '9' (digit) → ICD procedure code
    - 'SURGERY' → Treatment variable, not medication
    
    Returns:
    --------
    top_drugs : list
        Filtered list containing only medication features
    
    Note: This function is critical for drug-specific analysis to separate
          medication effects from diagnosis/procedure codes
    Returns:
    --------
    x : pandas.DataFrame
        Feature matrix (all columns after first 5: medications, procedures, diagnoses)
    y : pandas.Series
        Binary metastasis outcome (0 = no metastasis, 1 = metastasis)
    """
    
def load_cox_data(data):
    """
    Loads features, survival time, and event indicator for Cox regression.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Working dataset with survival data
    
    Returns:
    --------
    x : pandas.DataFrame
        Feature matrix (fillna(0) and convert to int)
    survival_time : pandas.Series
        Time in days from HNC diagnosis to outcome/censoring
    event : pandas.Series
        Event indicator (1 = metastasis occurred, 0 = censored)
    
    Note: Columns 0-6 contain patient IDs and outcome data, features start at column 7
    """
```

### Drug Filtering Function

```python
def pull_drugs(feature_list, has_underscore=True):
    """
    Filters feature list to extract only medication features.
    
    Logic:
    - Features with underscore start at position 1
    - If 2nd character (after '_') is a digit → ICD/procedure code → exclude
    - If 2nd character is a letter → medication → include
    
    Examples:
    - '_atorvastatin' → KEEP (drug)
    - '_thiamine' → KEEP (drug)
    - '_Z85.3' → EXCLUDE (ICD diagnosis code)
    - '_J96.01' → EXCLUDE (ICD procedure code)
    """
```

### Feature Selection Function (Cox)

```python
def cox_feature_selection(data, fast_mode=True):
    """
    Multi-method Cox feature selection with nested cross-validation.
    
    Purpose:
    --------
    Identifies robust features for Cox modeling by selecting features that:
    1. Have non-zero LASSO coefficients
    2. Show strong univariate association with survival
    3. Have sufficient variance across patients
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Working dataset with survival data
    fast_mode : bool, default=True
        If True, uses 3 CV folds; if False, uses 5 folds
    
    Methods Applied:
    ----------------
    1. **LASSO Cox Regression**:
       - L1 regularization penalizes less important features
       - Automatically performs feature selection by shrinking coefficients to zero
       - Cross-validated alpha parameter selection
       - Features with non-zero coefficients are selected
    
    2. **Univariate Cox Selection**:
       - Fits individual Cox model for each feature
       - Calculates C-index (concordance) for each feature
       - Selects features above median C-index
       - Identifies features with independent survival association
    
    3. **Variance Threshold**:
       - Removes features with low variance (< threshold)
       - Eliminates features that are constant or near-constant
       - Reduces overfitting from uninformative features
    
    Cross-Validation Strategy:
    --------------------------
    Uses Stratified K-Fold CV (preserves outcome ratio in each fold):
    
    Outer Loop (K=3 or 5 folds):
      For each fold:
        1. Split data into train (80%) and test (20%)
        2. Apply all 3 feature selection methods to training data
        3. Record which features are selected
        4. Track selection frequency across folds
    
    Feature Stability:
    ------------------
    - Features selected in ≥80% of folds are "highly stable"
    - Stability indicates feature is robust across different data splits
    - More stable features are more likely to generalize to new data
    
    Confounders:
    ------------
    Always retained regardless of selection results:
    - SURGERY (surgical intervention)
    - RADIATION (radiation therapy)
    - CHEMOTHERAPY (chemotherapy treatment)
    - IMMUNOTHERAPY (immunotherapy treatment)
    
    These are clinically important and must be adjusted for.
    
    Returns:
    --------
    drop_var : list
        Features to EXCLUDE from final model (low stability)
    feature_stability : pandas.DataFrame
        Columns:
        - feature: Feature name
        - lasso_freq: Selection frequency by LASSO (0.0-1.0)
        - univariate_freq: Selection frequency by univariate Cox (0.0-1.0)
        - variance_freq: Selection frequency by variance threshold (0.0-1.0)
        - mean_freq: Average frequency across all methods
        - highly_stable: Boolean, True if mean_freq ≥ 0.8
    
    Usage Example:
    --------------
    # Run feature selection for HPV+ patients
    drop_var_hpv_pos, stability_hpv_pos = cox_feature_selection(
        hpv_positive_data, 
        fast_mode=True
    )
    
    # Use selected features (NOT in drop_var) for final model
    selected_features = [f for f in all_features 
                         if f not in drop_var_hpv_pos 
                         or f in confounders]
    """
```

### Model Training Function (ML)

```python
def output_table_xgboost_based_log_odds_with_rf(data, file_name):
    """
    Comprehensive ML pipeline:
    1. Train XGBoost, Random Forest, Logistic Regression
    2. Hyperparameter tuning via RandomizedSearchCV
    3. 5-fold stratified CV with RandomOverSampler
    4. Extract feature importances from all models
    5. Calculate SHAP values for XGBoost
    6. Fit Cox model on top 15 features
    7. Calculate log-odds ratios
    8. Export feature importance table
    
    Returns: DataFrame with all feature metrics
    """
```

### Visualization Functions

```python
def plot_cox_vs_ml_importance(combined_df, title, top_n=20):
    """Scatter plot comparing Cox coefficients vs XGBoost importance"""

def calculation_confounding_effect(data, variable):
    """Pearson correlation analysis with visualization"""

def km_plot_by_group(data, med):
    """Kaplan-Meier survival curves with log-rank test"""

def forest_plot(data, variables):
    """Cox hazard ratio forest plot"""
```

---

## Results Interpretation Guide

### Cox Coefficients

**Hazard Ratio (HR) = exp(coef)**

| Hazard Ratio | Interpretation | Example |
|--------------|----------------|---------|
| HR = 1.0 | No effect | Neutral |
| HR = 1.5 | 50% increased risk | Risk factor |
| HR = 2.0 | 100% increased risk (doubles) | Strong risk factor |
| HR = 0.7 | 30% decreased risk | Protective |
| HR = 0.5 | 50% decreased risk | Strong protective |

**P-value**: Statistical significance (typically p < 0.05)

### XGBoost Importance

- **Higher values = more important for prediction**
- Relative scale (compare within same analysis)
- Based on how often feature is used for splitting and gain improvement

### SHAP Values

- **Mean Absolute SHAP**: Average contribution to prediction across all samples
- Positive SHAP: Pushes prediction toward metastasis
- Negative SHAP: Pushes prediction away from metastasis
- More interpretable than raw feature importance

### Log-Odds Ratio

- **Positive**: Feature associated with lower metastasis risk
- **Negative**: Feature associated with higher metastasis risk
- Magnitude indicates strength of association

---

## Expected Outputs

### From Integrated Analysis (`02 data_analysis_ml.ipynb`) PRIMARY OUTPUTS

**The main comprehensive results files:**

1. **Feature Importance Tables** (Cox + ML + SHAP combined)
   - `Results/ML analysis/hpv_positive_ml_xgb_results.csv` **PRIMARY HPV+ RESULTS**
   - `Results/ML analysis/hpv_negative_ml_xgb_results.csv` **PRIMARY HPV- RESULTS**
   - `Results/ML analysis/hpv_positive_ml_drug_xgb_results.csv` - Drug-only HPV+ results
   - `Results/ML analysis/hpv_negative_ml_drug_xgb_results.csv` - Drug-only HPV- results
   - `Results/ML analysis/ml_feature_stability_hpv_positive.csv` - Feature stability (HPV+)
   - `Results/ML analysis/ml_feature_stability_hpv_negative.csv` - Feature stability (HPV-)
   
   These files contain ALL metrics for each feature:
   - XGBoost, Random Forest, Logistic Regression importances
   - SHAP values (directional and absolute)
   - Univariate Cox: HR, p-value, FDR-corrected p-value, CI, C-index
   - Multivariate Cox: adjusted HR, p-value, FDR-corrected p-value, CI
   - Log-odds ratios

2. **Visualizations Generated**
   - SHAP summary plots (all features, top 50)
   - SHAP summary plots (drug features only)
   - Mean absolute SHAP bar plots for drugs
   - XGBoost/Random Forest feature importance plots
   - Multivariate Cox forest plots
   - Top 50 protective features forest plot (custom)
   - Log-odds ratio bar plots (all features and drugs separately)
   - ROC curves with cross-validation metrics
   - Classification reports and confusion matrices

3. **Model Performance Metrics**
   - Printed to console: accuracy, ROC-AUC, precision, recall, F1-score
   - Cox C-index (multivariate model)
   - Cross-validation fold results

### From Validation Analysis (`03 top feature correlation check.ipynb`)

1. **Outputs**
   - No CSV files are saved — all results are displayed as in-notebook visualizations

2. **Visualizations**
   - Correlation bar charts (top features per drug category)
   - Kaplan-Meier survival curves (per drug)
   - Forest plots (hazard ratios for top drugs)

---

## Critical Parameters and Settings

### Feature Selection Thresholds

- **Feature Stability**: ≥80% selection frequency across CV folds
- **Variance Threshold**: Features with variance > threshold retained
- **LASSO Penalty**: Cross-validated via grid search (10^-3 to 10^1)

### Cross-Validation

- **Folds**: 5 (stratified by outcome)
- **Stratification**: Ensures balanced outcome distribution in each fold
- **Random State**: 42 (for reproducibility)

### Class Imbalance

- **Method**: RandomOverSampler (duplicate minority class)
- **Applied**: Training data only
- **Alternative**: Class weights in model hyperparameters

### Hyperparameter Search

- **Method**: RandomizedSearchCV
- **Iterations**: 50 (per parameter grid)
- **Scoring**: ROC-AUC (primary), Accuracy (secondary)
- **CV**: 5-fold inner CV within each outer fold

### Confounders

**Always Retained** (never dropped regardless of selection results):
- `SURGERY`
- `RADIATION`
- `CHEMOTHERAPY`
- `IMMUNOTHERAPY`

### Data Filtering

- **Survival Time**: Patients with `Survival_Time > 2` days
- **HPV Status**: External dataset used for stratification

---

## Reproducibility Notes

### Random Seeds

- `random_state=42` used throughout for:
  - Train-test splits
  - Cross-validation folds
  - Model training
  - Hyperparameter search

### Data Versions

- **Input Data Date**: 03/05/25 (March 5, 2025)
- **PCDM Data**: 2023-03-09 snapshot
- **HPV Data**: From `/Volumes/Tanikella_Pradham_IRB_ID/yixiang/HPV/` (Update IRB_ID with your actual IRB approval number)

### Dependencies

```python
# Core
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Survival Analysis
from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.statistics import logrank_test

# Machine Learning
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

# Imbalance Handling
from imblearn.over_sampling import RandomOverSampler, SMOTE

# Interpretability
import shap

# Other
from tqdm import tqdm
import scipy.stats as stats
```

---

## Common Issues and Troubleshooting

### 1. Missing Results Files

**Problem**: `FileNotFoundError` when loading results in notebook 03

**Solution**: 
- Run notebooks 02 (Cox and ML) completely first
- Ensure `./Results/` directory exists
- Check file names match exactly (case-sensitive)

### 2. Empty Feature Lists

**Problem**: No drugs found in top features

**Solution**:
- Check `pull_drugs()` function is correctly filtering
- Verify feature names have leading underscore
- Increase top N threshold (e.g., top 200 instead of 100)

### 3. Cox Model Convergence Issues

**Problem**: `ConvergenceWarning` from CoxPHFitter

**Solution**:
- Check for highly correlated features (multicollinearity)
- Reduce feature set size
- Increase iteration limit
- Check for constant features (zero variance)

### 4. Class Imbalance Warnings

**Problem**: Severe class imbalance (e.g., 90:10 ratio)

**Solution**:
- Use `scale_pos_weight` in XGBoost
- Apply SMOTE or RandomOverSampler
- Use `class_weight='balanced'` in models
- Consider collecting more positive cases

### 5. Long Runtime

**Problem**: Analysis takes hours to complete

**Solution**:
- Use `fast_mode=True` in feature selection functions
- Reduce number of CV folds (e.g., 3 instead of 5)
- Reduce hyperparameter grid size
- Use fewer RandomizedSearchCV iterations (e.g., 20 instead of 50)

---

## Execution Order

**Must run in this order**:

1. **00 notebooks** (any order within this phase)
   - Data viewing (optional)
   - Patient level data creation
   - Feature engineering

2. **02 data_analysis_ml.ipynb** (Integrated Cox + ML analysis) MAIN
   - Generates comprehensive feature importance results combining Cox Proportional Hazards and Machine Learning
   - Includes univariate/multivariate Cox analysis with FDR correction
   - Includes XGBoost, Random Forest, Logistic Regression with SHAP
   - Takes ~45-60 minutes per HPV subgroup
   - Exports `Results/ML analysis/hpv_positive_ml_xgb_results.csv` and `hpv_negative_ml_xgb_results.csv`
   - Also exports `hpv_positive_ml_drug_xgb_results.csv`, `hpv_negative_ml_drug_xgb_results.csv`
   - Also exports `ml_feature_stability_hpv_positive.csv` and `ml_feature_stability_hpv_negative.csv`

3. **03 top feature correlation check.ipynb** (Validation and confounding assessment)
   - Requires output from step 2
   - Validates results and assesses confounding
   - Generates visualizations in-notebook (no CSV file output)
   - Results displayed as tables and plots within the notebook

**Note**: Steps 2 and 3 must run sequentially (step 3 depends on step 2's outputs).

---

## Citation and Contact

**Project**: Head and Neck Cancer Metastasis Prediction
**Institution**: Wu Lab
**Last Updated**: January 2026

For questions or issues, please contact the project maintainers.

---

## Appendix: File Naming Conventions

### Feature Files

Format: `{method}_{subgroup}_feature_importances.csv`

Examples:
- `sum_per_pat_feature_selection_chisqr_lasso_var_xgboost_rf_hpv_positive_working_data_feature_importances.csv`

Components:
- **sum_per_pat**: Aggregation method
- **feature_selection**: Processing step
- **chisqr_lasso_var_xgboost_rf**: Selection methods used
- **hpv_positive_working_data**: Subgroup
- **feature_importances**: File type

### K-Fold Results

Format: `{method}_{subgroup}_{model}_kfold_results.csv`

Examples:
- `sum_per_pat_feature_selection_chisqr_lasso_var_xgboost_rf_hpv_positive_working_data_XGBClassifier_kfold_results.csv`

Models: `XGBClassifier`, `RandomForestClassifier`, `LogisticRegression`

### Drug Analysis Results

Format: `hpv_{subgroup}_{analysis}_{method}_results.csv`

Examples:
- `hpv_positive_ml_xgb_results.csv`
- `hpv_negative_cox_coef_results.csv`
- `hpv_drug_comparison_ml_xgb.csv`

---

## Version History

- **v1.0** (January 2026): Initial comprehensive README
  - Documented complete workflow from data prep to final analysis
  - Added explicit execution order and dependencies
  - Included troubleshooting section
