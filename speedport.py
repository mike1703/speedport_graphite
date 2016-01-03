import requests
import hashlib
import simplejson
import re
import ConfigParser
import graphitesend
import lib

def get_challenge(hostname):
    data = {
        'csrf_token': 'nulltoken',
        'showpw': '0',
        'challengev': 'null'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    ret = requests.post("http://"+hostname+"/data/Login.json", headers=headers, data=data)
    result = lib.result2dict(ret.json())

    challengev = result.get('challengev')
    return challengev

def encrypt_password(password, challenge):
    return hashlib.sha256(challenge+':'+password).hexdigest()

def sanitize_json(json):
    # convert ' to "
    json = json.replace("\'", "\"")

    # sometimes there is a "}, ]" somewhere ... delete the comma
    json = re.sub("(}[^,]*,[^{\]]*\])", "}]", json)
    return json

def get_session(hostname, password):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'showpw': '0',
        'password': password,
        'csrf_token': 'nulltoken',
    }
    ret = requests.post("http://"+hostname+"/data/Login.json", headers=headers, data=data)
    # this json is defect... it has a <blafoo>},] at the end. delete this comma
    json = simplejson.loads(sanitize_json(ret.content))
    result = lib.result2dict(json)
    if result.get('login') == 'success':
        print 'login successful'
        return ret.cookies.get('SessionID_R3')
    else:
        return None

def get_data(hostname, module, session):
    cookies = {
        'SessionID_R3': session
    }
    ret = requests.get("http://"+hostname+"/data/"+module+".json",cookies=cookies)
    json = simplejson.loads(sanitize_json(ret.content))
    return json

def get_all_data(hostname, password, modules):

    challenge = get_challenge(hostname)
    password = encrypt_password(password, challenge)
    session = get_session(hostname, password)

    if session:
        data = dict()
        for module in modules:
            print "processing", module
            data[module] = get_data(hostname, module, session)
        return data
    return None

def process_data(inp):
    data = dict()

    data['arp'] = dict()
    data['arp']['count'] = lib.arp_count(inp)

    data['hybrid'] = dict()
    data['hybrid']['dsl_downloadbw'] = lib.get_dsl_download_bw(inp)
    data['hybrid']['dsl_uploadbw'] = lib.get_dsl_upload_bw(inp)
    data['hybrid']['dsl_state'] = lib.get_dsl_state(inp)
    data['hybrid']['lte_state'] = lib.get_lte_state(inp)

    data['dhcp_server'] = dict()
    data['dhcp_server']['lease_count'] = lib.get_dhcp_v4_lease_count(inp)

    data['dns'] = dict()
    data['dns']['count'] = lib.get_dns_count(inp)

    data['dsl'] = dict()
    data['dsl']['Line'] = lib.get_dsl_line(inp)

    data['interfaces'] = lib.get_interfaces(inp)

    data['hardware'] = dict()
    data['hardware']['cpu_load'] = lib.get_cpu_load(inp)

    data['wlan'] = dict()
    data['wlan']['clients'] = lib.get_wifi_clients(inp)
    data['wlan']['5g_channel'] = lib.get_wifi_5g_channel(inp)
    data['wlan']['24g_channel'] = lib.get_wifi_24g_channel(inp)
    data['wlan']['5g_main_channel'] = lib.get_wifi_5g_main_channel(inp)
    data['wlan']['2_4g_main_channel'] = lib.get_wifi_24g_main_channel(inp)
    data['wlan']['5g_data_rate'] = lib.get_wifi_5g_data_rate(inp)
    data['wlan']['2_4g_data_rate'] = lib.get_wifi_24g_data_rate(inp)

    return data

config = ConfigParser.RawConfigParser()
config.read('speedport.cfg')
modules = map(str.strip,config.get("Speedport", "modules").split(','))
password = config.get("Speedport", "password")
hostname = config.get("Speedport", "hostname")
graphite_server = config.get("Graphite", "server")
graphite_prefix = config.get("Graphite", "prefix")
graphite_hostname = config.get("Graphite", "hostname")

data = get_all_data(hostname, password, modules)
data = process_data(data)
data = lib.flatten_dict(data)

g = graphitesend.init(graphite_server=graphite_server, prefix=graphite_prefix, system_name=graphite_hostname)
g.send_dict(data)
