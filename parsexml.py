from bs4 import BeautifulSoup

with open("./AndroidManifest.xml") as f:
    dat = f.read()

soup = BeautifulSoup(dat, 'lxml')

package_name = soup.find_all("manifest")
print package_name[0].get("package")

permissons = soup.find_all("uses-permission")
for permisson in permissons:
    print permisson.get("android:name")

#exit()
print "\n\n"



activitys = soup.find_all("activity")
receivers = soup.find_all("receiver")
services = soup.find_all("service")
providers = soup.find_all("provider")

components = activitys + receivers + services + providers

for c in components:
    name = c.get("android:name")
    status = c.get("android:exported")
    if not status:
        status="false"
    if "xin" not in name:
        print name + " \t" + status



