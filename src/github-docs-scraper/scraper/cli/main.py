import os
import requests
import zipfile
import io
from dotenv import load_dotenv
from pathlib import Path
import tempfile
import json

__top_level_module__ = Path(__file__).resolve().parent.parent.name

def get_latest_commit_sha(repo_owner: str, repo_name: str, token: str | None = None) -> str:
    """
    Retrieves the latest commit SHA from the 'main' branch using the GitHub API.
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/main"
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Failed to retrieve latest commit SHA. Status {response.status_code}: {response.text}"
        )
    data = response.json()
    return data["sha"]

def download_github_repo(repo_owner, repo_name, output_dir, token=None):
    """
    Checks the latest commit SHA from GitHub. If that specific ZIP file does not exist
    in the temp directory, downloads and extracts the repo ZIP. Otherwise, skip re-downloading.
    """
    # 1. Get the latest commit
    latest_sha = get_latest_commit_sha(repo_owner, repo_name, token)

    # 2. Name the zip file with the commit SHA in a temp directory
    zip_file = Path(output_dir) / f"{repo_name}_{latest_sha}.zip"
    if zip_file.exists():
        print(f"Detected existing ZIP for commit {latest_sha}. Skipping download.")
        # Depending on your needs, you can re-extract or skip entirely.
        return zip_file

    # Convert GitHub repo URL to the ZIP download URL
    repo_url = f"https://github.com/{repo_owner}/{repo_name}/"
    zip_url = repo_url + "archive/refs/heads/main.zip"  # main branch; change if needed

    print(f"Downloading repository from {zip_url}")

    # Set up headers for authentication if a token is provided
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"

    # Send a GET request to download the ZIP file
    response = requests.get(zip_url, headers=headers)
    if response.status_code == 404:
        raise Exception(f"You have no access to the repository {repo_owner}/{repo_name}. Check your token or repository visibility.")
    if response.status_code != 200:
        raise Exception(f"Failed to download repository. Status code: {response.status_code}")

    # Save the ZIP file with the commit SHA in its name
    with open(zip_file, "wb") as f:
        f.write(response.content)

    # Extract the ZIP file
    with zipfile.ZipFile(zip_file) as z:
        z.extractall(zip_file.parent)

    print(f"Repository extracted to: {zip_file.parent}")
    return zip_file

def find_markdown_files(directory):
    """
    Recursively finds all Markdown (.md or .mdx) files in the given directory.
    """
    markdown_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md") or file.endswith(".mdx"):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def combine_markdown_files(markdown_files, output_file, base_directory=None):
    """
    Combines the content of all Markdown files into a single file, stripping out
    any local tmp_dir path so that the header references only the repo directory structure.
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for md_file in markdown_files:
            # Skip if it's CHANGELOG.md
            base_name = os.path.basename(md_file)
            if base_name == "CHANGELOG.md":
                continue

            # Compute a relative path, stripping out the tmp_dir prefix
            if base_directory is not None:
                file_in_repo = os.path.relpath(md_file, base_directory)
            else:
                file_in_repo = md_file

            outfile.write("\n\n---\n\n")  # Separator between files
            outfile.write(f"# File: {file_in_repo}\n\n")  # Name as a header
            with open(md_file, 'r', encoding='utf-8', errors='ignore') as infile:
                outfile.write(infile.read())

    print(f"Combined Markdown content written to: {output_file}")

def main():
    print(f"{__top_level_module__}:")
    # Load environment variables from .env.local
    load_dotenv(".env.local", override=True, verbose=True)

    # GitHub repository details
    repo_owner = os.getenv("REPO_OWNER")
    if repo_owner is None:
        raise ValueError("REPO_OWNER is not set in .env.local")
    repo_name = os.getenv("REPO_NAME")
    if repo_name is None:
        raise ValueError("REPO_NAME is not set in .env.local")

    # Create a temp directory for storing the fetched ZIP
    tmp_dir = tempfile.mkdtemp()
    output_combined_md = "./combined_markdown.md"

    # GitHub personal access token (optional)
    token = os.getenv("GITHUB_TOKEN")
    if token is None:
        print("No GITHUB_TOKEN found. Please set it in .env.local if you want to download private repositories.")

    # Download and extract the GitHub repository (if not already downloaded)
    try:
        downloaded_zip = download_github_repo(repo_owner, repo_name, tmp_dir, token=token)
        if downloaded_zip is None:
            # Means the ZIP already existed; we can keep going
            downloaded_zip = next(Path(tmp_dir).glob("*.zip"), None)
            # If needed, you could re-extract from that existing ZIP or skip
    except Exception as e:
        print(f"Error downloading repository: {e}")
        return

    # Step 2: Find all Markdown files
    markdown_files = find_markdown_files(tmp_dir)
    print(f"Found {len(markdown_files)} Markdown files.")

    # Step 3: Combine all Markdown files into one, stripping the tmp_dir part from the headers
    if markdown_files:
        combine_markdown_files(markdown_files, output_combined_md, base_directory=tmp_dir)
    else:
        print("No Markdown files found.")


if __name__ == "__main__":
    main()