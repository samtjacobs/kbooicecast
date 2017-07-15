import urllib.request
import subprocess
from xml.etree import ElementTree

LOCAL = "http://127.0.0.1"
PORT = "8000"
def find_file(file_name):
    output = subprocess.Popen(['find', '/', '-name', file_name], stdout=subprocess.PIPE).communicate()[0]
    output = output.decode()
    return output.split('\n')

CONFIG_FILE = find_file("icecast.xml")[0]

def authenticated_req(url, usr, pw):
    # create a password manager
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

    # Add the username and password.
    # If we knew the realm, we could use it instead of None.
    password_mgr.add_password(None, url, usr, pw)

    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

    # create "opener" (OpenerDirector instance)
    return urllib.request.build_opener(handler)

    # use the opener to fetch a URL
    #opener.open(a_url)

    # Install the opener.
    # Now all calls to urllib.request.urlopen use our opener.
    #urllib.request.install_opener(opener)


def main():
    # Get authentication details from icecast config file
    config_xml = ElementTree.parse(CONFIG_FILE).getroot()
    usr = config_xml.find('authentication/admin-user').text
    pw = config_xml.find('authentication/admin-password').text
    top_level = LOCAL + ":" + PORT + "/admin"
    opener = authenticated_req(top_level, usr, pw)
    # get list of mounts
    mount_pg = opener.open(top_level + '/listmounts')
    mount_html = mount_pg.read().decode('utf-8')
    xml = ElementTree.ElementTree(mount_html)
    mounts = xml.getroot().find('icestats')
    print(mounts)
    # Request stats



if __name__ == "__main__":
    main()