import IP2Location
 
IP2LocObj = IP2Location.IP2Location()
IP2LocObj.open("data/IP-COUNTRY.BIN")
rec = IP2LocObj.get_all("19.5.10.1")
 
print(rec.country_short)
print(rec.country_long)