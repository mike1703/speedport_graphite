def result2dict(raw):
    result = dict()
    for var in raw:
        result[var['varid']] = var['varvalue']

    return result

def flatten_dict(d):
    def expand(key, value):
        if isinstance(value, dict):
            return [ (key + '.' + k, v) for k, v in flatten_dict(value).items() ]
        else:
            return [ (key, value) ]

    items = [ item for k, v in d.items() for item in expand(k, v) ]

    return dict(items)

def arp_count(data):
    return len(data.get('arp'))

def get_dsl_download_bw(data):
    l = data.get('bonding_client').get('hybrid_show')
    for item in l:
        d = item.get('dsl_downloadbw')
        if d is not None:
            return d.split(' ')[0]
        else:
            continue
def get_dsl_upload_bw(data):
    l = data.get('bonding_client').get('hybrid_show')
    for item in l:
        d = item.get('dsl_downloadbw')
        if d is not None:
            return d.split(' ')[0]
        else:
            continue

def get_dsl_state(data):
    l = data.get('bonding_client').get('hybrid_show')
    for item in l:
        d = item.get('dsl_state')
        if d is not None:
            return d
        continue
def get_lte_state(data):
    l = data.get('bonding_client').get('hybrid_show')
    for item in l:
        d = item.get('lte_state')
        if d is not None:
            return d
        else:
            continue

def get_dhcp_v4_lease_count(data):
    return len(data.get('dhcp_server').get('ipv4'))

def get_dns_count(data):
    return len(data.get('dns').get('DCI'))

def get_dsl_line(data):
    line = data.get('dsl').get('Line')

    result = dict()
    # down_bins = line.get('dBIN').split('||')
    # result['down_bins'] = list()
    # for b in down_bins:
    #     result['down_bins'].extend(b.split('|')[1:])
    # up_bins = line.get('uBIN').split('||')
    # result['up_bins'] = list()
    # for b in up_bins:
    #     result['up_bins'].extend(b.split('|')[1:])
    result['actual_data_rate_up'] = line.get('uactual')
    result['actual_data_rate_down'] = line.get('dactual')
    result['attainable_data_rate_up'] = line.get('uattainable')
    result['attainable_data_rate_down'] = line.get('dattainable')
    result['snr_margin_up'] = line.get('uSNR')
    result['snr_margin_down'] = line.get('dSNR')
    result['signal_level_up'] = line.get('uSignal')
    result['signal_level_down'] = line.get('dSignal')
    result['line_attenuation_up'] = line.get('uLine')
    result['line_attenuation_down'] = line.get('dLine')
    result['codeword_up'] = line.get('uCodeword')
    result['codeword_down'] = line.get('dCodeword')
    result['interleave_delay_up'] = line.get('uInterleave')
    result['interleave_delay_down'] = line.get('dInterleave')
    result['crc_error_count_up'] = line.get('uCRC')
    result['crc_error_count_down'] = line.get('dCRC')
    result['header_error_correction_up'] = line.get('uHEC')
    result['header_error_correction_down'] = line.get('dHEC')
    result['forward_error_correction_up'] = line.get('uFEC')
    result['forward_error_correction_down'] = line.get('dFEC')
    return result

def get_cpu_load(data):
    return data.get('memory').get('cpu_load').rstrip('%')

def get_interfaces(data):
    interfaces = data.get('interfaces').get('line_status')

    result = dict()
    for interface in interfaces:
        # automatically converts WIFI_2.4 to WIFI_2-4
        result[interface.get('interface').replace(".","-")] = {
            'rx_errors':  interface.get('rx_errors'),
            'tx_errors':  interface.get('tx_errors'),
            'rx_packets': interface.get('rx_packets'),
            'tx_packets': interface.get('tx_packets')
        }

    return result

def get_lte_info(data):
    lte_info = data.get('lteinfo')
    return {'phycellid': lte_info.get('phycellid'),
            'rsrp': lte_info.get('rsrp'),
            'rsrq': lte_info.get('rsrq'),
            'tac': lte_info.get('tac')}

def get_wifi_clients(data):
    return len(data.get('wlan').get('WLAN_client5G'))

def get_wifi_24g_channel(data):
    return data.get('wlan').get('WLAN_information')[0].get('channel')

def get_wifi_5g_channel(data):
    return data.get('wlan').get('WLAN_information5G')[0].get('channel')

def get_wifi_24g_main_channel(data):
    return data.get('wlan').get('WLAN_information')[0].get('main_channel')

def get_wifi_5g_main_channel(data):
    return data.get('wlan').get('WLAN_information5G')[0].get('main_channel')

def get_wifi_5g_output_power(data):
    return data.get('wlan').get('WLAN_information5G')[0].get('output_power')

def get_wifi_24g_output_power(data):
    return data.get('wlan').get('WLAN_information')[0].get('output_power')

def get_wifi_5g_data_rate(data):
    return data.get('wlan').get('WLAN_information5G')[0].get('data_rate').split(' ')[0]

def get_wifi_24g_data_rate(data):
    return data.get('wlan').get('WLAN_information')[0].get('data_rate').split(' ')[0]


