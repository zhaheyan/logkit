import logging
import os
import re
import geoip2.database
import geoip2.errors

LOG = logging.getLogger('default')


def get_ip_location(ip_address):
    """get ip location"""
    ip_match = r"^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|0?[0-9]?[1-9]|0?[1-9]0)\.)(?:(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){2}(?:25[0-4]|2[0-4][0-9]|1[0-9][0-9]|0?[0-9]?[1-9]|0?[1-9]0)$"
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
    if not re.match(ip_match, ip_address):
        LOG.info('Wrong type of ip address!')
        LOG.info('192.168.1.107  192.168.1.107-100  alike!')
        return ip_location

    try:
        fileish = os.path.dirname(__file__) + '/GeoLite2-City.mmdb'
        reader = geoip2.database.Reader(fileish)
        response = reader.city(ip_address)
        # 地区
        ip_location['continent'] = response.continent.names['es']
        if ip_location['continent'] == None:
            ip_location['continent'] = 'None'
        else:
            if 'zh-CN' in response.continent.names:
                ip_location['continent_cn'] = response.continent.names['zh-CN']
            else:
                ip_location['continent_cn'] = ip_location['continent']
        # 国家名称
        ip_location['country_name'] = response.country.name
        if ip_location['country_name'] == None:
            ip_location['country_name'] = 'None'
        else:
            if 'zh-CN' in response.country.names:
                ip_location['country_name_cn'] = response.country.names['zh-CN']
            else:
                ip_location['country_name_cn'] = ip_location['country_name']
        # 州(国外)/省(国内)名称
        ip_location['country_specific_name'] = response.subdivisions.most_specific.name
        if ip_location['country_specific_name'] == None:
            ip_location['country_specific_name'] = 'None'
        else:
            if 'zh-CN' in response.subdivisions.most_specific.names:
                ip_location['country_specific_name_cn'] = response.subdivisions.most_specific.names['zh-CN']
            else:
                ip_location['country_specific_name_cn'] = ip_location['country_specific_name']
        # 城市名称
        ip_location['city_name'] = response.city.name
        if ip_location['city_name'] == None:
            ip_location['city_name'] = 'None'
        else:
            if 'zh-CN' in response.city.names:
                ip_location['city_name_cn'] = response.city.names['zh-CN']
            else:
                ip_location['city_name_cn'] = ip_location['city_name']
    except geoip2.errors.AddressNotFoundError as err:
        LOG.error('geoip2.errors.AddressNotFoundError: %s', err)
    except Exception as err:
        LOG.error('Exception: %s', err)

    return ip_location

