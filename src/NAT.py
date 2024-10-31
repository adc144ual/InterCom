import stun

STUN_SERVERS = (
    'stun.ekiga.net',
    'stun.ideasip.com',
    'stun.voiparound.com',
    'stun.voipbuster.com',
    'stun.voipstunt.com',
    'stun.voxgratia.org'
)

def get_public_ip_and_port(stun_server):
    try:
        nat_type, external_ip, external_port = stun.get_ip_info(stun_host=stun_server)
        return nat_type, external_ip, external_port
    except Exception as e:
        return None, None, None

if __name__ == "__main__":
    for server in STUN_SERVERS:
        print(f"Comprobando con el servidor STUN: {server}")
        nat, ip, port = get_public_ip_and_port(server)
        
        if ip and port:
            print(f"Servidor STUN: {server}")
            print(f"Tipo de NAT: {nat}")
            print(f"IP pública: {ip}")
            print(f"Puerto público: {port}\n")
        else:
            print(f"No se pudo obtener información del servidor STUN: {server}\n")
