# scraper

Simple CLI tool to scrape a GitHub repository (optionally a private one) and combine all the Markdown files it finds into a single file.
This file can then be easily uploaded to ChatGPT, Deepseek, Qwen, etc.

## Usage

Create a `.env.local` file with the following variables:

- `REPO_OWNER`: The owner of the GitHub repository.
- `REPO_NAME`: The name of the GitHub repository.
- `GITHUB_TOKEN`: The GitHub personal access token.

For instance:

```
REPO_OWNER=your_org_name
REPO_NAME=your_repo_name
GITHUB_TOKEN=your_github_token
```

## Installation

```bash
uv run scraper
```
