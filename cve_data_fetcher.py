import requests

# Function to fetch CVE data (live)
def get_cve_data():
    # API URL for CVE data from NVD (National Vulnerability Database)
    url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
    
    # Sending the request to the NVD API to get CVE data
    response = requests.get(url)
    
    # If the request was successful, extract and return the data
    if response.status_code == 200:
        data = response.json()  # Convert response to JSON
        # Return a simplified list of CVE IDs and descriptions
        cve_list = []
        for item in data.get("result", {}).get("CVE_Items", []):
            cve_id = item["cve"]["CVE_data_meta"]["ID"]
            description = item["cve"]["description"]["description_data"][0]["value"]
            cve_list.append({"id": cve_id, "description": description})
        return cve_list
    else:
        return [{"id": "N/A", "description": "Failed to fetch CVE data"}]
