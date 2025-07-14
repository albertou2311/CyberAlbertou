import argparse
import modules.chain_attack as chain_attack

def main():
    parser = argparse.ArgumentParser(description="CyberAlbertoU saldırı zinciri aracı")
    parser.add_argument("-t", "--target", required=True, help="Hedef IP veya URL")
    parser.add_argument("-a", "--ssh", action='store_true', help="SSH saldırısını aktif et")
    parser.add_argument("-b", "--ftp", action='store_true', help="FTP saldırısını aktif et")
    parser.add_argument("-c", "--bruteforce", action='store_true', help="Bruteforce saldırısını aktif et")
    parser.add_argument("-f", "--full", action='store_true', help="Tüm saldırıları çalıştır")

    args = parser.parse_args()
    options = {
        'ssh': args.ssh or args.full,
        'ftp': args.ftp or args.full,
        'bruteforce': args.bruteforce or args.full,
    }

    chain_attack.chain_attack(args.target, options)

if __name__ == "__main__":
    main()
