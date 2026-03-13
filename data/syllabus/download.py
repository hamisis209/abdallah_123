import os, urllib.request
files = {
    'physics_o.pdf': 'https://www.tie.go.tz/uploads/documents/sw-1727257838-PHYSICS%20FOR%20ORDINARY%20SECONDARY%20EDUCATION%20FINAL.pdf',
    'chemistry_o.pdf': 'https://www.tie.go.tz/uploads/documents/sw-1727192894-CHEMISTRY%20O%27LEVEL%20EDUCATION%20FINAL.pdf',
    'physics_a.pdf': 'https://www.tie.go.tz/uploads/documents/sw-1727271434-Physics%20Syllabus%20for%20Advanced%20final.pdf',
    'chemistry_a.pdf': 'https://www.tie.go.tz/uploads/documents/sw-1727269817-CHEMISTRY%20SYLLABUS%20FINAL.pdf',
}
os.makedirs('data/syllabus', exist_ok=True)
for name, url in files.items():
    path = os.path.join('data', 'syllabus', name)
    urllib.request.urlretrieve(url, path)
