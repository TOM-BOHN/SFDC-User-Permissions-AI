# SFDC-User_Permissions-AI

This project analyzes Salesforce user permissions using AI/ML techniques.

## Project Structure

```
├── data/                  # Data directory
│   ├── raw/              # Raw scraped data from Salesforce
│   ├── processed/        # Cleaned and processed datasets
│   └── output/           # Final analysis results
├── src/                  # Source code
│   ├── scraping/        # Web scraping scripts
│   ├── processing/      # Data processing code
│   ├── analysis/        # Analysis and AI/ML code
│   ├── utils/          # Utility functions
│   └── prompts/        # LLM prompts and chains
│       ├── templates/  # Reusable prompt templates
│       ├── chains/    # Multi-step prompt chains
│       └── system/    # System-level prompts
├── notebooks/           # Jupyter notebooks
├── tests/              # Unit tests
├── docs/               # Documentation
│   ├── api/           # API documentation
│   └── guides/        # User guides and tutorials
├── config/             # Configuration files
└── requirements.txt    # Python dependencies
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

3. Environment Configuration:
   - Copy `.env.example` to `.env`
   - Add your API keys and configurations to `.env`
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

## Data Organization

- `data/raw/`: Store raw scraped data from Salesforce
  - `private/`: For sensitive data (automatically gitignored)
- `data/processed/`: Store cleaned and transformed datasets
- `data/output/`: Store analysis results and outputs

## LLM Components

The project uses LLM (Large Language Models) for analysis, with components organized as follows:

- `src/prompts/templates/`: Individual prompt templates

### LLM Best Practices

1. Keep sensitive information in `.env`
2. Store prompt templates separately from logic
3. Version control your prompts
4. Use the cache directories for optimization

## Development Guidelines

1. Follow the project structure for new code
2. Add tests for new functionality
3. Document changes in appropriate docs
4. Use debug directories for temporary outputs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

[Add license information here]
