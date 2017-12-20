from flux_led import BulbScanner, WifiLedBulb


def scan_bulb():
    scanner = BulbScanner()
    scanner.scan()

    print scanner.found_bulbs

    ipaddr = scanner.found_bulbs[0]['ipaddr']
    return ipaddr

def switch_on(ipaddress):
    flux_bulb = WifiLedBulb(ipaddr=ipaddress)
    flux_bulb.turnOn()

def switch_off(ipaddress):
    flux_bulb = WifiLedBulb(ipaddr=ipaddress)
    flux_bulb.turnOff()



# if __name__ == '__main__':
#     ipaddr = scan_bulb()
#     switch_on(ipaddr)
#     switch_off(ipaddr)