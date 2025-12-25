import urllib.request
r = urllib.request.urlopen('http://localhost:5000/kategori')
content = r.read().decode('utf-8')
print('Status:', r.status)
print('Has Kategori Makanan:', 'Kategori Makanan' in content)
print('Has bounce:', 'data-aos="bounce"' in content)