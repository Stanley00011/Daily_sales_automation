import os

def get_data_path(filename="sales_master.csv"):
    """
    Returns the correct path depending on the environment:
    - Streamlit Cloud (reads from GitHub raw)
    - GitHub Actions (local repo during CI)
    - Local run (developer laptop)
    """
    
    # Streamlit Cloud
    if os.environ.get("STREAMLIT_CLOUD") == "1":
        return (
            f"https://raw.githubusercontent.com/"
            f"Stanley00011/Daily_sales_automation/main/data/{filename}"
        )
    
    # GitHub Actions
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return os.path.join("data", filename)

    # Local run
    return os.path.join("../data", filename)
