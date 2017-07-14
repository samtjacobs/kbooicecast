import urllib
import subprocess
import xml.etree.ElementTree

LOCAL = "http://127.0.0.1"

def find_file(file_name):
    output = subprocess.Popen(['find', '/', '-name', file_name], stdout=subprocess.PIPE).communicate()[0]
    output = output.decode()
    return output.split('\n')

CONFIG_FILE = find_file("icecast.xml")[0]


def main():
    # Get authentication details from icecast config file
    config_xml = xml.etree.ElementTree.parse(CONFIG_FILE).getroot()
    usr = config_xml.find('authentication/admin-user')
    pw = config_xml.find('authentication/admin-password')


if __name__ == "__main__":
    main()