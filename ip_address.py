import requests


def get_address_by_ip(ip: str):
    """

    :param ip:
    :return:
    """
    address = ''
    ignore_ips = ['127.0.0.1', 'localhost', '192.168', '0.0.0.0']
    if ip in ignore_ips:
        address = "本地"
    else:
        url = 'http://ip.taobao.com/service/getIpInfo.php?ip={}&accessKey=alibaba-inc'.format(ip)
        data = requests.get(url).json()
        if data['code'] == 0:
            address = data['data']['country'] + data['data']['area'] + data['data']['region'] + \
                      data['data']['city']
    return address

# 在Django中从request中提取访问IP
# from django.core.validators import validate_ipv46_address
# def get_request_ip(request):
#     headers = (
#         'HTTP_CLIENT_IP', 'HTTP_X_FORWARDED_FOR', 'HTTP_X_FORWARDED',
#         'HTTP_X_CLUSTERED_CLIENT_IP', 'HTTP_FORWARDED_FOR', 'HTTP_FORWARDED',
#         'REMOTE_ADDR'
#     )
#     for header in headers:
#         if request.META.get(header, None):
#             ip = request.META[header].split(',')[0]
#             try:
#                 validate_ipv46_address(ip)
#                 return ip
#             except ValidationError:
#                 pass
