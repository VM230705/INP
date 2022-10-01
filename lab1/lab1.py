import dpkt
import socket
import sys
import base64


def parsepcap(pcap):
    with open(pcap, 'rb') as pcap_in:
        # ts->timestamp
        for ts, buf in dpkt.pcap.Reader(pcap_in):
            # 獲取乙太網部分資料
            eth = dpkt.ethernet.Ethernet(buf)
            # check is ARP or IPV4
            if eth.type == 2048:
                ip = eth.data
                tcp = ip.data
                ttl, tos = ip.ttl, ip.tos
                payload = tcp.data
                # 把儲存在inet_ntoa中的IP地址轉換成一個字串
                dst_ip = socket.inet_ntoa(ip.dst)
                src_ip = socket.inet_ntoa(ip.src)
            else:
                dst_ip, src_ip, payload, ttl, tos = 0, 0, 0, 0, 0
            yield dst_ip, src_ip, payload, ttl, tos


def main(pcap_path):
    try:
        print(f'{pcap_path}')
        max_ttl = 0
        max_payload = ""
        for (dst_ip, src_ip, payload, ttl, tos) in parsepcap(pcap_path):
            if (src_ip == '140.113.213.213') and ttl > max_ttl:
                max_ttl = ttl
                max_payload = payload
        string = base64.b64decode(max_payload).decode('UTF-8')
        print(f'payload: {string}')
    except FileNotFoundError:
        print(f' File "{pcap_path}" does not exist.')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('input file name')
        sys.exit(1)
    main(sys.argv[1])