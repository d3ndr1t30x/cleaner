import re
from urllib.parse import urlparse
import textwrap

def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain

def filter_urls(input_file, output_file, unwanted_domains):
    # Read URLs from the input file
    with open(input_file, 'r') as file:
        urls = file.readlines()

    # Filter out unwanted URLs
    filtered_urls = [url.strip() for url in urls if all(unwanted not in url for unwanted in unwanted_domains)]

    # Extract domain names
    domains = [extract_domain(url) for url in filtered_urls]

    # Remove duplicates
    unique_domains = list(set(domains))

    # Write the unique, valid domains to the output file
    with open(output_file, 'w') as file:
        for domain in unique_domains:
            file.write(domain + '\n')

def prompt_for_unwanted_domains(unique_domains):
    unwanted_domains = []
    while True:
        unwanted_domain = input("Enter a domain to remove (or press Enter to finish): ").strip()
        if unwanted_domain:
            if unwanted_domain in unique_domains:
                unwanted_domains.append(unwanted_domain)
            else:
                print(f"Domain '{unwanted_domain}' not found in the list of extracted domains.")
        else:
            break
    return unwanted_domains

def extract_domains_from_urls(urls):
    domains = [extract_domain(url.strip()) for url in urls]
    unique_domains = list(set(domains))
    return unique_domains

def display_domains_in_columns(domains, columns=3):
    max_len = max(len(domain) for domain in domains) + 2
    domain_lines = textwrap.wrap('  '.join(domains), width=columns * max_len)
    for line in domain_lines:
        print(line)

if __name__ == "__main__":
    # User specifies the input file and output file
    input_file = input("Enter the input file path: ").strip()
    output_file = input("Enter the output file path: ").strip()

    # Read URLs from the input file
    with open(input_file, 'r') as file:
        urls = file.readlines()

    # Extract unique domains from URLs
    unique_domains = extract_domains_from_urls(urls)

    # Show extracted domains to the user in columns
    print("Extracted domains:")
    display_domains_in_columns(unique_domains)

    # Prompt user to remove unwanted domains
    print("\nSpecify unwanted domains to remove.")
    unwanted_domains = prompt_for_unwanted_domains(unique_domains)

    if unwanted_domains:
        print("\nUnwanted domains:")
        for domain in unwanted_domains:
            print(f" - {domain}")

    confirmation = input("\nDo you want to proceed with removing these domains? (yes/no): ").strip().lower()
    if confirmation == 'yes':
        filter_urls(input_file, output_file, unwanted_domains)
        print(f"Filtered URLs have been saved to {output_file}")
    else:
        print("Operation cancelled.")
