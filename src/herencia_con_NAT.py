import stun

STUN_SERVERS = (
    'stun.ekiga.net',
    'stun.ideasip.com',
    'stun.voiparound.com',
    'stun.voipbuster.com',
    'stun.voipstunt.com',
    'stun.voxgratia.org'
)

def check_my_nat():
    reference_ip, reference_port = None, None  # Para almacenar la IP y el puerto de referencia
    successful_responses = 0  # Contador de respuestas exitosas de los servidores STUN

    for server in STUN_SERVERS:
        #print(f"Comprobando con el servidor STUN: {server}")
        try:
            # Intentamos obtener la IP pública y el puerto desde el servidor STUN
            nat_type, external_ip, external_port = stun.get_ip_info(stun_host=server)
            print(f"Servidor STUN: {server} -> IP: {external_ip}, Puerto: {external_port}")

            # Ignoramos respuestas con IP o puerto 'None'
            if external_ip is None or external_port is None:
                #print(f"El servidor STUN {server} no devolvió una IP o puerto válidos.\n")
                continue

            if reference_ip is None and reference_port is None:
                # Si es la primera vez que obtenemos una respuesta válida, guardamos los valores
                reference_ip, reference_port = external_ip, external_port
                print(f"IP y puerto de referencia: IP={reference_ip}, Puerto={reference_port}")
            else:
                # Comprobamos si la IP y el puerto coinciden con los anteriores
                if external_ip != reference_ip or external_port != reference_port:
                    print(f"IP/puerto no coinciden con los anteriores (IP: {external_ip}, Puerto: {external_port})")
                    return False  # Si no coinciden, devolvemos False
            
            successful_responses += 1  # Contamos esta respuesta como exitosa

        except Exception as e:
            # Ignoramos los errores si el servidor STUN no responde
            print(f"Error al conectar con el servidor STUN {server}: {e}")
            continue

    # Si sólo un servidor respondió
    if successful_responses == 1:
        return "Solo un STUN respondió"

    # Si todos los servidores que respondieron devuelven la misma IP y puerto
    if successful_responses > 1:
         return f"La NAT es Full Cone. Tu IP externa es {external_ip} con el puerto {external_port}"  # Todas las IPs y puertos coinciden
    
    return "La NAT NO es Full Cone "  # No se recibió respuesta de ningún servidor STUN



if __name__ == "__main__":
    print(check_my_nat())
