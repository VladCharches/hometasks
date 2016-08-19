import re
from collections import Counter

f = open('/usr/local/apache2/logs/access_log')
data = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', f.read())
f.close()
for ip in Counter(data).most_common(10):
    print (ip[0])
