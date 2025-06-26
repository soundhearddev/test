import requests
import ssl
import socket
import dns.resolver
import whois
from urllib.parse import urlparse

def get_http_headers(url):
    try:
        r = requests.get(url, timeout=5)
        return r.headers
    except Exception as e:
        return f"HTTP Fehler: {e}"

def get_ssl_info(hostname):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.settimeout(5)
            s.connect((hostname, 443))
            cert = s.getpeercert()
        return cert
    except Exception as e:
        return f"SSL Fehler: {e}"

def get_dns_records(domain):
    records = {}
    try:
        records['A'] = [str(ip) for ip in dns.resolver.resolve(domain, 'A')]
    except:
        records['A'] = []
    try:
        records['MX'] = [str(mx.exchange) for mx in dns.resolver.resolve(domain, 'MX')]
    except:
        records['MX'] = []
    try:
        records['NS'] = [str(ns) for ns in dns.resolver.resolve(domain, 'NS')]
    except:
        records['NS'] = []
    return records

def get_whois(domain):
    try:
        w = whois.whois(domain)
        return w
    except Exception as e:
        return f"Whois Fehler: {e}"

def main(url):
    parsed = urlparse(url)
    hostname = parsed.hostname or url

    print(f"--- Technische Infos für {hostname} ---\n")

    print("1. HTTP Header:")
    headers = get_http_headers(url)
    if isinstance(headers, dict):
        for k, v in headers.items():
            print(f"{k}: {v}")
    else:
        print(headers)
    print("\n2. SSL Zertifikat:")
    ssl_info = get_ssl_info(hostname)
    if isinstance(ssl_info, dict):
        subject = ssl_info.get('subject', [])
        issuer = ssl_info.get('issuer', [])
        print("Subject:", subject)
        print("Issuer:", issuer)
        print("Gültig von:", ssl_info.get('notBefore'))
        print("Gültig bis:", ssl_info.get('notAfter'))
    else:
        print(ssl_info)

    print("\n3. DNS Records:")
    dns_records = get_dns_records(hostname)
    for typ, wert in dns_records.items():
        print(f"{typ}: {wert}")

    print("\n4. Whois:")
    whois_info = get_whois(hostname)
    if isinstance(whois_info, dict) or hasattr(whois_info, 'domain_name'):
        print(f"Domain Name: {whois_info.get('domain_name')}")
        print(f"Registrar: {whois_info.get('registrar')}")
        print(f"Creation Date: {whois_info.get('creation_date')}")
        print(f"Expiration Date: {whois_info.get('expiration_date')}")
        print(f"Name Servers: {whois_info.get('name_servers')}")
    else:
        print(whois_info)

if __name__ == "__main__":
    url = input("Gib die URL ein (z.B. https://example.com): ").strip()
    if not url.startswith("http"):
        url = "http://" + url
    main(url)
