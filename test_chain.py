# test_chain.py
from modules.chain_attack import chain_attack

target = "scanme.nmap.org"  # test için güvenli hedef
options = {
    "whois": True,
    "subdomains": False,
    "web": True,
    "ssh": False,
    "ftp": False,
    "ai": True
}

chain_attack(target, options)
