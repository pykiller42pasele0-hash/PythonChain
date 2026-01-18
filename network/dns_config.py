# network/dns_config.py
# Diese Datei simuliert deinen eigenen Domain-Eintrag im PythonChain-Netzwerk

DOMAIN_MAP = {
    "pykiller42.io": {
        "A": [
            "185.199.108.153",
            "185.199.109.153",
            "185.199.110.153",
            "185.199.111.153"
        ],
        "CNAME": "pykiller42pasele0-hash.github.io"
    }
}

def resolve_domain(domain):
    return DOMAIN_MAP.get(domain, "Domain nicht im PythonChain-Netz gefunden.")