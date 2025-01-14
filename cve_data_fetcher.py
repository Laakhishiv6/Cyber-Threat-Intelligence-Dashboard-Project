import requests


def get_cve_data():

    url = "https://services.nvd.nist.gov/rest/json/cves/1.0"

    response = requests.get(url)
   
    if response.status_code == 200:
        data = response.json()  # Convert response to JSON
  
        cve_list = []
        for item in data.get("result", {}).get("CVE_Items", []):
            cve_id = item["cve"]["CVE_data_meta"]["ID"]
            description = item["cve"]["description"]["description_data"][0]["value"]
            cve_list.append({"id": cve_id, "description": description})
        return cve_list
    else:
        return [{"id": "N/A", "description": "Failed to fetch CVE data"}]
