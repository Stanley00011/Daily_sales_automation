import os

def get_data_path(filename="sales_master.csv"):
    """
    Returns the correct path depending on the environment:
    - Streamlit Cloud (reads from GitHub raw)
    - GitHub Actions (local repo during CI)
    - Local run (developer laptop / Codespace)
    """
    
    # 1. Streamlit Cloud: Accesses data via the web URL (most reliable)
    if os.environ.get("STREAMLIT_CLOUD") == "1":
        return (
            f"https://raw.githubusercontent.com/"
            f"Stanley00011/Daily_sales_automation/main/data/{filename}"
        )
    
    # 2. GitHub Actions: Accesses data locally within the CI environment
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return os.path.join("data", filename)

    # 3. Local Run (Fallback): This path is now relative to the repository root.
    #    This is the safest path, assuming the app is run from the root, 
    #    or if the deployed environment fails to set any environment variables.
    return os.path.join("data", filename)