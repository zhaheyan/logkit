import logging
import re
import geoip2.database
import geoip2.errors.AddressNotFoundError

LOG = logging.getLogger('default')


def get_ip_location(ip_address):
    """get ip location"""
    # ip_address = '192.168.1.107'
    ip_match = r"^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|0?[0-9]?[1-9]|0?[1-9]0)\.)(?:(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){2}(?:25[0-4]|2[0-4][0-9]|1[0-9][0-9]|0?[0-9]?[1-9]|0?[1-9]0)$"
    if not re.match(ip_match, ip_address):
        LOG.info('Wrong type of ip address!')
        LOG.info('100.8.11.58  100.8.11.58-100  alike!')

    ip_location = {
        # 地区
        'continent': 'None',
        'continent_cn': 'None',
        # 国家名称
        'country_name':  'None',
        'country_name_cn': 'None',
        # 州(国外)/省(国内)名称
        'country_specific_name': 'None',
        'country_specific_name_cn': 'None',
        # 读取城市名称
        'city_name': 'None',
        'city_name_cn': 'None'
    }

    try:
        reader = geoip2.database.Reader('GeoLite2-City.mmdb')
        response = reader.city(ip_address)
        # 地区
        ip_location['continent'] = response.continent.names['es']
        if ip_location['continent'] == None:
            ip_location['continent'] = 'None'
        else:
            ip_location['continent_cn'] = response.continent.names['zh-CN']
        # 国家名称
        ip_location['country_name'] = response.country.name
        if ip_location['country_name'] == None:
            ip_location['country_name'] = 'None'
        else:
            ip_location['country_name_cn'] = response.country.names['zh-CN']
        # 州(国外)/省(国内)名称
        ip_location['country_specific_name'] = response.subdivisions.most_specific.name
        if ip_location['country_specific_name'] == None:
            ip_location['country_specific_name'] = 'None'
        else:
            ip_location['country_specific_name_cn'] = response.subdivisions.most_specific.names['zh-CN']
        # 城市名称
        ip_location['city_name'] = response.city.name
        if ip_location['city_name'] == None:
            ip_location['city_name'] = 'None'
        else:
            ip_location['city_name_cn'] = response.city.names['zh-CN']
    except geoip2.errors.AddressNotFoundError as err:
        print(err)
    except Exception as err:
        print(err)

    return ip_location

