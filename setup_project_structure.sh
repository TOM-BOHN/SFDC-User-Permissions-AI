#!/bin/bash

# Create main directories
mkdir -p data/{raw,processed,output}
mkdir -p src/{scraping,processing,analysis,utils}
mkdir -p src/prompts/{templates,chains,system}
mkdir -p tests
mkdir -p docs/{api,guides}
mkdir -p config

# Create initial README files with descriptions
echo "# Raw Data
This directory contains the raw scraped data from Salesforce websites.
Do not modify files in this directory directly." > data/raw/README.md

echo "# Processed Data
This directory contains cleaned and processed datasets." > data/processed/README.md

echo "# Output Data
This directory contains final analysis results and outputs." > data/output/README.md

echo "# Source Code
This directory contains all the project's source code.

- scraping/: Web scraping scripts
- processing/: Data processing and transformation code
- analysis/: Analysis and AI/ML code
- utils/: Utility functions and helper modules
- prompts/: LLM prompt templates and chains
  - templates/: Reusable prompt templates
  - chains/: Multi-step prompt chains
  - system/: System-level prompts" > src/README.md

echo "# Prompts Directory
This directory contains all LLM-related prompts and chains.

## Structure:
- templates/: Individual, reusable prompt templates
- chains/: Multi-step prompt orchestration
- system/: System-level prompts and configurations

## Best Practices:
1. Keep prompts modular and reusable
2. Version control your prompts
3. Document expected inputs/outputs
4. Include examples where helpful" > src/prompts/README.md

echo "# Configuration
Store configuration files here. Do not include sensitive information directly in config files." > config/README.md

# Create initial requirements.txt if it doesn't exist
if [ ! -f requirements.txt ]; then
    echo "# Core dependencies
pandas
numpy
scikit-learn
jupyter
requests
beautifulsoup4
python-dotenv
langchain  # For LLM prompt chains
openai     # For OpenAI API integration" > requirements.txt
fi

# Update main README.md with project structure
cat << 'EOF' > README.md
# SFDC-User_Permissions-AI

This project analyzes Salesforce user permissions using AI/ML techniques.

## Project Structure

```
├── data/               # Data directory
│   ├── raw/           # Raw scraped data
│   ├── processed/     # Cleaned and processed datasets
│   └── output/        # Final analysis results
├── src/               # Source code
│   ├── scraping/     # Web scraping scripts
│   ├── processing/   # Data processing code
│   ├── analysis/     # Analysis and AI/ML code
│   ├── utils/        # Utility functions
│   └── prompts/      # LLM prompts and chains
│       ├── templates/  # Reusable prompt templates
│       ├── chains/    # Multi-step prompt chains
│       └── system/    # System-level prompts
├── notebooks/         # Jupyter notebooks
├── tests/            # Unit tests
├── docs/             # Documentation
├── config/           # Configuration files
└── requirements.txt  # Python dependencies
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

[Add usage instructions here]

## Contributing

[Add contribution guidelines here]

## License

[Add license information here]
EOF

echo "Project structure has been set up successfully!" 