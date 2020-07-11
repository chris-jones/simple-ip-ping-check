# simple-ip-ping-check
A simple IP checker that takes in a list of IP addresses, pings them, and displays them, sorted by latency.


Simple IP list Ping Check
=======================

A simple script that takes in a file containing IP addresses, pings them a set number of times, and returns the results sorted by average latency.

Built so I could test unpublished SurfShark VPN server lists, so that I could find the lowest latency servers with the lowest ping failure rates from my location.

Also good if you've got a list of game servers, and you want to test the latency between yourself and them.

The structure of the input file is very flexible. It will find the first IP address per line, and use that as the target for testing. A sample file is included.

Pandas is used to sort the gathered data and display them appropriately.


Instructions:
-------------

Clone this repo:

    git clone git@github.com:chris-jones/simple-ip-ping-check.git

Install the requirements:

    pip install -r requirements.txt

Run:

    python ip-check.py --file=sample-ips.txt

