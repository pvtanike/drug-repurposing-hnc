"""
Data Import Module for Head and Neck Cancer Analysis

Purpose:
--------
This module loads all raw Patient-Centered Data Model (PCDM) tables from the external drive.
These tables contain comprehensive electronic health record data for head and neck cancer patients.

Requirements:
-------------
- External drive must be mounted at: /path/to/IRB_DATA_DRIVE/
  (Replace IRB_ID with your actual IRB approval number)
- PCDM data snapshot from: 2023-03-09

Tables Loaded:
--------------
1. Clarity_ID: Patient identifier mapping with fixed MRNs
2. PCDM_CONDITION: Patient conditions and comorbidities
3. PCDM_DEATH_CAUSE: Cause of death information
4. PCDM_DEATH: Death records
5. PCDM_DEMOGRAPHIC: Patient demographics (age, sex, race, ethnicity)
6. PCDM_DIAGNOSIS: Diagnosis records with ICD codes
7. PCDM_ENCOUNTER: Patient encounters and visits
8. PCDM_IMMUNIZATION: Vaccination records
9. PCDM_LAB_RESULT_CM: Laboratory test results
10. PCDM_LDS_ADDRESS_HISTORY: Address history for patients
11. PCDM_MED_ADMIN: Medication administration records
12. PCDM_OBS_CLIN: Clinical observations
13. PCDM_OBS_GEN: General observations
14. PCDM_PRESCRIBING: Prescription records (RxNorm CUI and NDC codes)
15. PCDM_PROCEDURES: Procedure records with ICD procedure codes
16. PCDM_PROVIDER: Healthcare provider information
17. PCDM_VITAL: Vital signs (BP, HR, temp, etc.)

Usage:
------
Import this module in notebooks to access all PCDM tables:
    from Data_import import *
"""

### Import required libraries
import pandas as pd

### Load Patient Identifier Mapping
# Contains mapping between different patient identifier systems with corrected MRN values
Clarity_ID = pd.read_csv('/path/to/IRB_DATA_DRIVE/DATA_FOLDER/IRB_CLARITY_ID_fixed_MRNs.csv')
print("1/17 Read in Clarity_ID")

### Clinical Notes (Currently Commented Out)
# Note: Clinical notes split across 8 files - not currently used in analysis
# Uncomment if needed for NLP or text mining analysis
# Clarity_Notes_0 = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_CLARITY_NOTES_0.psv')
# Clarity_Notes_1 = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_CLARITY_NOTES_1.psv')
# Clarity_Notes_2 = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_CLARITY_NOTES_2.psv')
# Clarity_Notes_3 = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_CLARITY_NOTES_3.psv')
# Clarity_Notes_4 = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_CLARITY_NOTES_4.psv')
# Clarity_Notes_5 = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_CLARITY_NOTES_5.psv')
# Clarity_Notes_6 = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_CLARITY_NOTES_6.psv')
# Clarity_Notes_7 = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_CLARITY_NOTES_7.psv')

### Load PCDM Condition Table
# Contains patient conditions, comorbidities, and disease states
PCDM_CONDITION = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_PCDM_CONDITION.csv')
print("2/17 Read in Condition")

### Load Death-Related Tables
# PCDM_DEATH_CAUSE: Primary and contributing causes of death
PCDM_DEATH_CAUSE = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_PCDM_DEATH_CAUSE.csv')
print("3/17 Read in PCDM_DEATH_CAUSE")

# PCDM_DEATH: Death dates and related information for survival analysis
PCDM_DEATH = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_PCDM_DEATH.csv')
print("4/17 Read in PCDM_DEATH")

### Load Patient Demographics
# Contains age, sex, race, ethnicity - used for confounding adjustment
PCDM_DEMOGRAPHIC = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_PCDM_DEMOGRAPHIC.csv')
print("5/17 Read in PCDM_DEMOGRAPHIC")

### Load Diagnosis Table
# Contains ICD-10 diagnosis codes and dates
# Note: Uses latin-1 encoding and skips bad lines due to data quality issues
PCDM_DIAGNOSIS = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_PCDM_DIAGNOSIS.csv',
                             on_bad_lines='skip', encoding='latin-1', engine='python')
print("6/17 Read in PCDM_DIAGNOSIS")

### Load Encounter Table
# Contains patient visit dates and encounter types (inpatient, outpatient, etc.)
PCDM_ENCOUNTER = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_PCDM_ENCOUNTER.csv',
                             on_bad_lines='skip', encoding='latin-1', engine='python')
print("7/17 Read in PCDM_ENCOUNTER")

### Load Immunization Records
# Contains vaccination records - not primary focus of current analysis
PCDM_IMMUNIZATION = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_PCDM_IMMUNIZATION.csv')
print("8/17 Read in PCDM_IMMUNIZATION")

### Load Laboratory Results
# Contains lab test results (values, dates, test codes)
PCDM_LAB_RESULT_CM = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_PCDM_LAB_RESULT_CM.csv',
                                 on_bad_lines='skip', encoding='latin-1', engine='python')
print("9/17 Read in PCDM_LAB_RESULT_CM")

### Load Address History
# Contains patient address history for geographic analysis
PCDM_LDS_ADDRESS_HISTORY = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_PCDM_LDS_ADDRESS_HISTORY.csv')
print("10/17 Read in PCDM_LDS_ADDRESS_HISTORY")

### Load Medication Administration Records
# Contains records of medications administered in clinical settings
PCDM_MED_ADMIN = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_PCDM_MED_ADMIN.csv',
                             on_bad_lines='skip', encoding='latin-1', engine='python')
print("11/17 Read in PCDM_MED_ADMIN")

### Load Clinical Observations
# Contains clinical measurements and observations from patient visits
PCDM_OBS_CLIN = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_PCDM_OBS_CLIN.csv',
                            on_bad_lines='skip', encoding='latin-1', engine='python')
print("12/17 Read in PCDM_OBS_CLIN")

### Load General Observations
# Contains general patient observations and assessments
PCDM_OBS_GEN = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_PCDM_OBS_GEN.csv',
                           on_bad_lines='skip', encoding='latin-1', engine='python')
print("13/17 Read in PCDM_OBS_GEN")

### Load Prescribing Records
# Contains prescription orders with RxNorm CUI and NDC codes
# Primary source for medication features in the analysis
PCDM_PRESCRIBING = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_PCDM_PRESCRIBING.csv',
                               on_bad_lines='skip', encoding='latin-1', engine='python')
print("14/17 Read in PCDM_PRESCRIBING")

### Load Procedures Table
# Contains ICD procedure codes for surgeries, treatments, and other procedures
PCDM_PROCEDURES = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_PCDM_PROCEDURES.csv',
                              on_bad_lines='skip', encoding='latin-1', engine='python')
print("15/17 Read in PCDM_PROCEDURES")

### Load Provider Information
# Contains healthcare provider details
PCDM_PROVIDER = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_PCDM_PROVIDER.csv')
print("16/17 Read in PCDM_PROVIDER")

### Load Vital Signs
# Contains vital sign measurements (BP, heart rate, temperature, weight, etc.)
PCDM_VITAL = pd.read_csv('/path/to/IRB_DATA_DRIVE/PCDM_2023_03_09/IRB_PCDM_VITAL.csv',
                         on_bad_lines='skip', encoding='latin-1', engine='python')
print("17/17 Read in PCDM_VITAL")

print("\n" + "="*80)
print("All PCDM tables successfully loaded!")
print("="*80)

print("finished")