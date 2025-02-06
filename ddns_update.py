#!/usr/bin/env python3
import requests
import json
import os

# Import configuration values from config.py
import config

NPM_API_URL = config.NPM_API_URL
NPM_API_USER = config.NPM_API_USER
NPM_API_PASS = config.NPM_API_PASS
CLOUDFLARE_API_TOKEN = config.CLOUDFLARE_API_TOKEN
CLOUDFLARE_ZONE_ID = config.CLOUDFLARE_ZONE_ID
SERVER_IP_OR_HOSTNAME = config.SERVER_IP_OR_HOSTNAME

def get_npm_token():
    """Gets an API token from NPM."""
    url = f"{NPM_API_URL}/tokens"
    data = {"identity": NPM_API_USER, "secret": NPM_API_PASS}
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()['token']

def get_proxy_hosts(token):
    """Gets the list of proxy hosts from NPM."""
    url = f"{NPM_API_URL}/nginx/proxy-hosts"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def update_host_file(current_hosts, filename):
    """Writes the current hosts into the file."""
    with open(filename, "w") as f:
        for host in current_hosts:
            f.write(host + "\n")

def check_cloudflare_record_exists(domain):
    """Checks if a CNAME record already exists for the given domain in Cloudflare."""
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"
    params = {"type": "CNAME", "name": domain}
    headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    results = response.json().get('result', [])
    return len(results) > 0

def create_cloudflare_cname(domain):
    """Creates a CNAME record in Cloudflare if one does not already exist."""
    if check_cloudflare_record_exists(domain):
        print(f"CNAME record already exists for {domain}, skipping creation.")
        return

    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "CNAME",
        "name": domain,
        "content": SERVER_IP_OR_HOSTNAME,
        "ttl": 3600,
        "proxied": True  # Set to False if you do not want proxying
    }
    response = requests.post(url, headers=headers, json=data)
    try:
        response.raise_for_status()
        print(f"CNAME record created for {domain}")
    except requests.exceptions.HTTPError:
        error_detail = response.json()
        print(f"Error creating Cloudflare CNAME for {domain}: {response.status_code} {response.reason}")
        print("Details:", error_detail)

def delete_cloudflare_cname(domain):
    """Deletes a CNAME record in Cloudflare."""
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"
    params = {"type": "CNAME", "name": domain}
    headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    results = response.json().get('result', [])
    if not results:
        print(f"No CNAME record found for {domain}")
        return
    for record in results:
        record_id = record.get('id')
        del_url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records/{record_id}"
        del_response = requests.delete(del_url, headers=headers)
        try:
            del_response.raise_for_status()
            print(f"CNAME record deleted for {domain}")
        except requests.exceptions.HTTPError:
            error_detail = del_response.json()
            print(f"Error deleting Cloudflare CNAME for {domain}: {del_response.status_code} {del_response.reason}")
            print("Details:", error_detail)

if __name__ == "__main__":
    token = get_npm_token()
    proxy_hosts = get_proxy_hosts(token)
    current_domains = {domain for host in proxy_hosts for domain in host['domain_names']}

    filename = "proxy_hosts.txt"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            previous_domains = {line.strip() for line in f if line.strip()}
    else:
        previous_domains = set()

    created_domains = current_domains - previous_domains
    deleted_domains = previous_domains - current_domains

    if created_domains:
        print("Created proxy hosts:")
        for domain in created_domains:
            print(f"  - {domain}")
    if deleted_domains:
        print("Deleted proxy hosts:")
        for domain in deleted_domains:
            print(f"  - {domain}")
    if not created_domains and not deleted_domains:
        print("No changes in proxy hosts.")

    for domain in created_domains:
        try:
            create_cloudflare_cname(domain)
        except Exception as e:
            print(f"Error processing Cloudflare creation for {domain}: {e}")

    for domain in deleted_domains:
        try:
            delete_cloudflare_cname(domain)
        except Exception as e:
            print(f"Error processing Cloudflare deletion for {domain}: {e}")

    update_host_file(current_domains, filename)
