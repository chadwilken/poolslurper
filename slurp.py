import os
import csv
import time
from datetime import datetime
import json
import requests


# quick app to grab mining pool data for several pools and save in csv files
# process:
#   1) record "now"
#   2) poll pool api data (in threads?)
#   3) organize data for new row of csv file
#   4) write csv file
class Pool(object):
    def __init__(self,
                    name=None,
                    apiurl=None,
                    apiparams=dict(),
                    csvfile=None,
                    csvactual=None,
                ):
        self.name = name
        self.apiurl = apiurl
        self.apiparams = apiparams
        self.csvfile = csvfile
        self.csvactual = csvactual
        self.response = ""
        self.algorithms = {}
        self.timeouts = 0
        self.failures = 0

    def __repr__(self):
        return "Pool(" + \
                "\'name\'=\'{}\', ".format(self.name) + \
                "\'apiurl\'=\'{}\', ".format(self.apiurl) + \
                "\'apiparams\'=\'{}\', ".format(self.apiparams) + \
                "\'algorithms\'=\'{}\', ".format(self.algorithms) + \
                "\'timeouts\'=\'{}\', ".format(self.timeouts) + \
                "\'failures\'=\'{}\'".format(self.failures) + \
                ")"

    def __str__(self):
        return self.__dict__

    def poll_api(self):
        sleeptime=5
        self.timeouts = 0
        r = None
        while self.timeouts < 3:
            try:
                if self.apiparams:
                    r = requests.get(url=self.apiurl, params=self.apiparams)
                else:
                    r = requests.get(url=self.apiurl)
                r.raise_for_status()
            except requests.exceptions.Timeout:
                self.timeouts += 1
                time.sleep(sleeptime)
                sleeptime += 3
                continue
            except requests.exceptions.HTTPError as err:
                self.timeouts = 404
            except requests.exceptions.RequestException as e:
                self.timeouts = 666
            break
        if self.timeouts >= 3 or r is None or r.text is None or "{" not in r.text:
            self.failures += 1
            print("Failure of some kind updating API data for {}".format(self.name))
            return False
        data = json.loads(r.text)
        if data is None or data is False:
            self.failures += 1
            print("Failure of some kind updating API data for {}".format(self.name))
            return False
        self.response = data
            print("Successfully grabbed API data for {}".format(self.name))
        return True

    def update_algorithms(self, valid_algos):
        self.algorithms = {}
        if not self.poll_api():
            return
        else:
            for key in self.response:
                if key in valid_algos:
                    self.algorithms[valid_algos[key]]=dict(
                            estimate=self.response[key]['estimate_current'],
                            actual24h=self.response[key]['actual_last24h']
                        )
            print("Processed algorithm data for {}".format(self.name))

    def get_algorithms(self):
        return self.algorithms

    def get_name(self):
        return self.name

    def get_csv_string(self, new_timestamp, algo_map):
        new_row = [new_timestamp]
        for i in range(len(algo_map)):
            if algo_map[i] in self.algorithms:
                new_row.append(str(self.algorithms[algo_map[i]]['estimate']))
            else:
                new_row.append('')
        return new_row

    def get_csv_string_actual(self, new_timestamp, algo_map):
        new_row = [new_timestamp]
        for i in range(len(algo_map)):
            if algo_map[i] in self.algorithms:
                new_row.append(str(self.algorithms[algo_map[i]]['actual24h']))
            else:
                new_row.append('')
        return new_row

    def append_row_to_csv(self, new_row):
        with open(self.csvfile, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(new_row)
        print("Appended estimate data for {p} to {f}".format(p=self.name, f=self.csvfile))

    def append_row_to_csv_actual(self, new_row):
        with open(self.csvactual, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(new_row)
        print("Appended actual data for {p} to {f}".format(p=self.name, f=self.csvactual))




class MiningPoolHub(Pool):
    def __init__(self,
                    name=None,
                    apiurl=None,
                    apiparams=None,
                    csvfile=None
                ):
        Pool.__init__(self, name, apiurl, apiparams, csvfile, divisors)

    def update_algorithms(self, valid_algos):
        self.algorithms = {}
        poll_result = self.poll_api()
        if not poll_result or not self.response['success']:
            return
        else:
            for obj in self.response['return']:
                obj['algo'] = obj['algo'].lower()
                if obj['algo'] in valid_algos:
#                    self.algorithms[valid_algos[obj['algo']]] = obj['profit']
                    self.algorithms[valid_algos[obj['algo']]]=dict(
                            estimate=obj['profit']
                        )
            print("Processed algorithm data for {}".format(self.name))




class Nicehash(Pool):
    def __init__(self,
                    name=None,
                    apiurl=None,
                    apiparams=None,
                    csvfile=None
                ):
        Pool.__init__(self, name, apiurl, apiparams, csvfile)

    def update_algorithms(self, valid_algos):
        self.algorithms = {}
        poll_result = self.poll_api()
        if poll_result is False or \
				'simplemultialgo' not in str(self.response) or \
				self.response['result'] is False or \
				self.response['result']['simplemultialgo'] is False:
            return
        else:
            for obj in self.response['result']['simplemultialgo']:
                if obj['name'] in valid_algos:
                    self.algorithms[valid_algos[obj['name']]]=dict(
                            estimate=obj['paying']
                        )
            print("Processed algorithm data for {}".format(self.name))





def main():
    script_home = os.path.split(os.path.abspath(__file__))[0]

    valid_algos = {
        "bitcore": "bitcore",
        "blake": "blakecoin",
        "blake2s": "blake2s",
        "blakecoin": "blakecoin",
        "blakevanilla": "blakevanilla",
        "c11": "c11",
        "cryptonight": "cryptonight",
        "daggerhashimoto": "ethash",
        "darkcoinmod": "x11",
        "decred": "decred",
        "equihash": "equihash",
        "eth": "ethash",
        "ethash": "ethash",
        "groestl": "groestl",
        "groestlcoin": "groestl",
        "hmq1725": "hmq1725",
        "hsr": "hsr",
        "jha": "jha",
        "keccak": "keccak",
        "lbry": "lbry",
        "lyra2re2": "lyra2v2",
        "lyra2rev2": "lyra2v2",
        "lyra2v2": "lyra2v2",
        "lyra2z": "lyra2z",
        "maxcoin": "keccak",
        "myrgr": "myriadgroestl",
        "myr-gr": "myriadgroestl",
        "myriadcoingroestl": "myriadgroestl",
        "myriadgroestl": "myriadgroestl",
        "neoscrypt": "neoscrypt",
        "nist5": "nist5",
        "pascal": "pascal",
        "phi": "phi",
        "poly": "polytimos",
        "polytimos": "polytimos",
        "quark": "quark",
        "quarkcoin": "quark",
        "qubit": "qubit",
        "qubitcoin": "qubit",
        "scrypt": "scrypt",
        "sha256": "sha256",
        "sib": "sib",
        "sibcoinmod": "sib",
        "sigt": "skunk",
        "skein": "skein",
        "skeincoin": "skein",
        "skunk": "skunk",
        "timetravel": "timetravel",
        "tribus": "tribus",
        "vanilla": "blakevanilla",
        "whirlpoolx": "whirlpoolx",
        "veltor": "veltor",
        "x11": "x11",
        "x11gost": "sib",
        "x11evo": "x11evo",
        "x17": "x17",
        "xevan": "xevan",
        "xmr": "cryptonight",
        "yescrypt": "yescrypt",
        "zec": "equihash",
        "zuikkis": "scrypt"
    }


    algo_map = ["bitcore", "blake2s", "blakecoin", "c11", "cryptonight", \
                "decred", "equihash", "ethash", "groestl", "hmq1725", \
                "hsr", "keccak", "lbry", "lyra2v2", "lyra2z", "m7m", \
                "myr-gr", "neoscrypt", "nist5", "pascal", "phi", \
                "polytimos", "quark", "qubit", "scrypt", "sha256", \
                "sia", "sib", "skein", "skunk", "timetravel", "tribus", \
                "whirlpoolx", "x11", "x11evo", "x11gost", "x13", "x14", \
                "x15", "x17", "xevan", "yescrypt", "yescryptR16"]


    pools = []

    # ahashpool
    pools.append(Pool(
            name='ahashpool',
            apiurl='https://www.ahashpool.com/api/status/',
            csvfile=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'ahashpool.csv'),
            csvactual=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'ahashpool_actual.csv')
        )
    )

    # blazepool
    pools.append(Pool(
            name='blazepool',
            apiurl='http://api.blazepool.com/status',
            csvfile=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'blazepool.csv'),
            csvactual=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'blazepool_actual.csv')
        )
    )

    # zergpool
    pools.append(Pool(
            name='zergpool',
            apiurl='http://api.zergpool.com/api/status',
            csvfile=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'zergpool.csv'),
            csvactual=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'zergpool_actual.csv')
        )
    )

    # zpool
    pools.append(Pool(
            name='zpool',
            apiurl='http://www.zpool.ca/api/status/',
            csvfile=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'zpool.csv'),
            csvactual=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'zpool_actual.csv')
        )
    )

    # miningpoolhub
    pools.append(MiningPoolHub(
            name='miningpoolhub',
            apiurl='https://miningpoolhub.com/index.php',
            apiparams=dict(
                page='api',
                action='getautoswitchingandprofitsstatistics'
            ),
            csvfile=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'miningpoolhub.csv')
        )
    )

    # nicehash
    pools.append(Nicehash(
            name='nicehash',
            apiurl='https://api.nicehash.com/api',
            apiparams=dict(
                method='simplemultialgo.info'
            ),
            csvfile=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'nicehash.csv')
        )
    )


    # so that should give us a list of the pools as class objects
    while (1):
        new_datetime = datetime.now()
        new_timestamp = new_datetime.strftime('%x %X')
        for pool in pools:
            pool.update_algorithms(valid_algos)
            pool.append_row_to_csv(pool.get_csv_string(new_timestamp, algo_map))
            if pool.csvactual is not None:
                pool.append_row_to_csv_actual(pool.get_csv_string_actual(new_timestamp, algo_map))
        time.sleep(60)



if __name__ == '__main__':
    main()
