#!/bin/env python
import socket
import random
import urllib.request
import json

class Servers:
    """
    Class to handle the servers of the radiobrowser api
    """

    def __init__(self):
        pass

    def get_radiobrowser_base_urls(self):
        """
        Get all base urls of all currently available radiobrowser servers

        Returns: 
        list: a list of strings
        """
        hosts = []
        # get all hosts from DNS
        ips = socket.getaddrinfo('all.api.radio-browser.info',
                                80, 0, 0, socket.IPPROTO_TCP)
        for ip_tupple in ips:
            ip = ip_tupple[4][0]
            # do a reverse lookup on every one of the ips to have a nice name for it
            host_addr = socket.gethostbyaddr(ip)
            # add the name to a list if not already in there
            if host_addr[0] not in hosts:
                hosts.append(host_addr[0])
        # sort list of names
    
        hosts.sort()
        # add "https://" in front to make it an url
        return hosts
        # return list(map(lambda x: "https://" + x, hosts))

    def downloadUri(self, uri, param):
        """
        Download file with the correct headers set

        Returns: 
        a string result
        """
        paramEncoded = None
        if param is not None:
            paramEncoded = json.dumps(param).encode('utf-8')
            print('Request to ' + uri + ' Params: ' + str(param))
        else:
            print('Request to ' + uri)

        req = urllib.request.Request(uri, data=paramEncoded)
        req.add_header('User-Agent', 'MyApp/0.0.1')
        req.add_header('Content-Type', 'application/json')
        response = urllib.request.urlopen(req)
        data = response.read()
        response.close()
        return data

    def downloadRadiobrowser(self, path, param):
        """
        Download file with relative url from a random api server.
        Retry with other api servers if failed.

        Returns: 
        a string result
        """
        servers = self.get_radiobrowser_base_urls()
        random.shuffle(servers)
        for i, server_base in enumerate(servers):
            print('Random server: ' + server_base + ' Try: ' + str(i))
            uri = server_base + path
            try:
                data = self.downloadUri(uri, param)
                return data
            except Exception as e:
                print("Unable to download from api url: " + uri, e)
                continue
        return {}

    def downloadRadiobrowserStats(self):
        stats = self.downloadRadiobrowser("/json/stats", None)
        return json.loads(stats)

    def downloadRadiobrowserStationsByCountry(self, countrycode):
        stations = self.downloadRadiobrowser("/json/stations/bycountrycodeexact/" + countrycode, None)
        return json.loads(stations)

    def downloadRadiobrowserStationsByName(self, name):
        stations = self.downloadRadiobrowser("/json/stations/search", {"name": name})
        return json.loads(stations)
    
    def getCountries(self):
        countries = self.downloadRadiobrowser("/json/countries", None)
        return json.loads(countries)
# if __name__ == "__main__":
#     server = Servers()

#     print("All available urls")
#     print("------------------")
#     for host in server.get_radiobrowser_base_urls():
#         print(host)
#     print("")

#     print("Stats")
#     print("------------")
#     print(json.dumps(server.downloadRadiobrowserStats(), indent=4))
# http://de2.api.radio-browser.info/json/stations
