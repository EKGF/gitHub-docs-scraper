# github-docs-scraper

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

## Development Setup

1. Clone the repository:

   If you don't have the repo yet, you can clone it first:

   ```bash
   git clone https://github.com/EKGF/github-docs-scraper.git
   cd github-docs-scraper
   ```

2. Open the project in your editor:

   - For Visual Studio Code:
     ```bash
     code .
     ```
   - For Cursor:
     ```bash
     cursor .
     ```

3. Install dependencies using uv:

   Rather than using the usual `pip install -r requirements.txt`, we use `uv` to install the dependencies. For more information on uv, see the [uv docs](https://docs.astral.sh/uv/getting-started/installation/).

   ```bash
   uv sync
   ```

4. Run the scraper:

   ```bash
   uv run github-docs-scraper
   ```


