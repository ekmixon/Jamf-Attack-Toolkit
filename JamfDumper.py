import xmltodict
import requests
import os
import xml.dom.minidom

from base64 import b64encode
from getpass import getpass

url = input("[?] JSS URL (https://blah.jamfcloud.com): ")
username = input("[?] JSS Username: ")
password = getpass("[?] JSS Password: ")
auth_string = f"{username}:{password}"

auth = f'Basic {b64encode(auth_string.encode("utf-8")).decode("utf-8")}'

api_url = f"{url}/JSSResource"

try:
    os.mkdir(url)
except:
    pass

#################################################################################################################################################
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#################################################################################################################################################

def dump(friendly_name, name, item_list, item):
    print("\n")
    print("#"*(len(friendly_name) + 4))
    print(f"# {friendly_name} #")
    print("#"*(len(friendly_name) + 4))
    print("\n")

    try:
        os.mkdir(f"{url}/{friendly_name}")
    except:
        pass

    r = requests.get(f"{api_url}/{name}", headers={ "Authorization": auth })

    if r.status_code != 200:
        print(r)
        print(r.text)
        raise Exception("An error occured. Request didn't return a 200")

    # Iterate and Print
    for item in xmltodict.parse(r.text)[item_list][item]:
        if os.path.exists(f"{url}/{friendly_name}/{item['id']}"):
            print(f"{item['id']} already exists... skipping.")
            continue

        print(f"{item['id']} - {item['name']}")

        r = requests.get(
            api_url + f"/{name}/id/{item['id']}",
            headers={"Authorization": auth},
        )


        if r.status_code != 200:
            print(r)
            print(r.text)
            raise Exception("An error occured. Request didn't return a 200")

        dom = xml.dom.minidom.parseString(r.text)
        pretty_xml = dom.toprettyxml()

        with open(f"{url}/{friendly_name}/{item['id']}", "w") as f:
            f.write(pretty_xml)


#################################################################################################################################################
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#################################################################################################################################################

if __name__ == '__main__':
    dump("Policies", "policies", "policies", "policy")
    dump("XAs", "computerextensionattributes", "computer_extension_attributes", "computer_extension_attribute")
    dump("Scripts", "scripts", "scripts", "script")
