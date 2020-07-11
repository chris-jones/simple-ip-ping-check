from colorama import Fore, Back, Style
import click
import numpy as np
import pandas as pd
import pexpect
import re
import sys



class Ping(object):

    def __init__(self, ip, interval=0.5, timeout=1200):

        object.__init__(self)

        self.ip = ip
        self.interval = interval
        self.latency = []
        self.timeout = 0
        ping_command = 'ping -i ' + str(self.interval) + ' ' + self.ip
        self.ping = pexpect.spawn(ping_command)
        self.ping.timeout = timeout
        self.ping.readline()  # init
        
    def run(self, n_test):
        for n in range(n_test):
            p = self.ping.readline()

            try:
                ping_time = float(p[p.find(b'time=') + 5:p.find(b' ms')])
                self.latency.append(ping_time)

            except:
                self.timeout = self.timeout + 1

        self.timeout = self.timeout / float(n_test)
        self.latency = np.array(self.latency)

    def get_mean_latency(self):
        if self.latency.size > 0:
            return np.mean(self.latency)
        else:
            return None

    def get_std_latency(self):
        if self.latency.size > 0:
            return np.std(self.latency)
        else:
            return None

    def get_timeout(self):
        return self.timeout * 100



@click.command()
@click.option(
    '--file',
    type=click.File('r'),
    required=True,
    help='File containing list of IP addresses to check.'
)
@click.option(
    '--count',
    show_default=True,
    default=15,
    type=int,
    required=False,
    help='Number of pings to send to each IP address.'
)
def parse_and_ping_ip_list(file, count):
    try:
        targets = []
        records = []
        progress = 0

        for line in file.readlines():
            line = line.rstrip()
            ip_address = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', line)[0]

            if ip_address:
                label = line.replace(ip_address,'').strip()
                targets.append([ip_address, label])


        click.echo(click.style(f'Pinging {len(targets)} IP addresses:', fg='green'))


        with click.progressbar(length=len(targets)) as bar:

            for target in targets:

                ip = target[0]
                label = target[1]

                check = Ping(ip)
                check.run(count)
                
                records.append({
                                'Server': label, 
                                'IP': ip, 
                                'Mean latency': check.get_mean_latency(), 
                                'Std latency': check.get_std_latency(), 
                                'Timeouts': check.get_timeout()
                                })
                progress=+1
                bar.update(progress)

            bar.finish()

        dataset = pd.DataFrame(records)
        dataset = dataset.sort_values(
                                    by='Mean latency', 
                                    ascending=True
                                    )


        def highlight_timeouts(val):
            if val < 30:
                color = Fore.CYAN
            elif val < 50:
                color = Fore.GREEN
            elif val < 75:
                color = Fore.YELLOW
            else:
                color = Fore.RED
            return color + str(f'{round(val, 2)}') + Style.RESET_ALL

        dataset["Timeouts"] = dataset["Timeouts"].apply(highlight_timeouts)

        click.echo(dataset)


    except IOError as e:
        print("I/O Error: {e}")


if __name__ == '__main__':
    parse_and_ping_ip_list()


