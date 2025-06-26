import nmap

scanner = nmap.PortScanner()
scanner.scan("192.168.0.0/24", "80,443")

for host in scanner.all_hosts():
    for proto in scanner[host].all_protocols():
        ports = scanner[host][proto].keys()
        if ports:
            print(f"{host} hat Port {', '.join(str(p) for p in ports)} offen")
