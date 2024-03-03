import machine
import network
from micropython_wol import wol

# Verander de volgende variabelen naar jouw netwerkinstellingen en het MAC-adres van je pc
SSID = 'jouw_wifi_naam'
PASSWORD = 'jouw_wifi_wachtwoord'
PC_MAC_ADDRESS = b'00:11:22:33:44:55'

# Maak een WLAN-interface en verbind met het netwerk
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Wacht tot de WLAN-verbinding tot stand is gebracht
while not wlan.isconnected():
    pass

# Functie om het WOL-pakket te verzenden
def send_wol_packet():
    wol.send_magic_packet(PC_MAC_ADDRESS)

# Maak een HTTP-server en definieer de handler voor de root-URL
import usocket as socket

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        request = conn.recv(1024)
        conn.sendall('HTTP/1.1 200 OK\nContent-Type: text/html\n\n')
        conn.sendall('''<!DOCTYPE html>
<html>
<head><title>Wake On LAN</title></head>
<body>
<h1>Wake On LAN</h1>
<form method="POST" action="/">
    <button type="submit" name="submit">Wake up</button>
</form>
</body>
</html>''')
        conn.close()

        # Als het verzoek een POST-verzoek is, stuur dan het WOL-pakket
        if b'POST / HTTP/1.1' in request and b'Wake up' in request:
            send_wol_packet()

if __name__ == "__main__":
    main()
