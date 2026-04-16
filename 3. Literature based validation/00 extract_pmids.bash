#!/bin/bash
# Define the query
QUERY="head and neck cancer"

#Set api key
export NCBI_API_KEY=${NCBI_API_KEY:-"your-key-here"}

# Define the output file
OUTPUT_FILE="pmids.txt"

# Perform the search and extract PMIDs
esearch -db pubmed -query "head and neck cancer" | efetch -format uid > "$OUTPUT_FILE"

# Output the results
echo "PMIDs have been saved to $OUTPUT_FILE"