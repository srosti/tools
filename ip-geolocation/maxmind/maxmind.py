import geoip2.database

# This creates a Reader object. You should use the same object
# across multiple requests as creation of it is expensive.
reader = geoip2.database.Reader('GeoLite2-Country.mmdb')

# Replace "city" with the method corresponding to the database
# that you are using, e.g., "country".
#response = reader.country('128.101.101.101')
#response = reader.country('172.19.10.99')
response = reader.country('216.64.128.45')
import pdb; pdb.set_trace()

print(response.country.iso_code)
print(response.country.name)
print(response.country.names['zh-CN'])
reader.close()
