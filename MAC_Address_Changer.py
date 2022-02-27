#!/usr/bin/env python3

# subprocess is a module. it has its own functions that can be used with subprocess.xxx
# allows creation of new processes using functions such as those found in the OS
# here ifconfig is a linux bash command
# re is regex, see pythex.org
import subprocess
import optparse
import re

parser = optparse.OptionParser()
parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address of")
parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
parser.parse_args()
(options, arguments) = parser.parse_args()
interface = options.interface
new_mac = options.new_mac


# Create an error message if interface and mac options are not given
if not options.interface:
    parser.error(" - Please specify an interface, use --help for more info.")
elif not options.new_mac:
    parser.error(" - Please specify a new mac address, use --help for more info")

# subprocess.run waits until command is completed before moving to next line
# run function has 2 arguments: command to execute and setting shell variable to true to run linux commands
# in python 2 this was subprocess.call
# brackets indicate that first argument is a command and others are options/arguments
subprocess.run(["ifconfig", interface, "down"])
subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
subprocess.run(["ifconfig", interface, "up"])

print("Changing MAC address to " + new_mac)

# check ifconfig output to see if program worked
# subprocess.check_output to run a command and use the output, ie save to variable
# re.search is regex search for given parameter
# .group(0) to specify first found item in search. search output contains lots of info otherwise
ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
# print(options.new_mac)
# print(search_result.group(0))
if search_result.group(0) == options.new_mac:
    print("MAC address changed successfully to " + str(search_result.group(0)))
else:
    print("MAC address was not changed")

# these would work but are not secure, as user could enter a bash command as input
# subprocess.run("ifconfig " + interface + " down", shell=True)
# subprocess.run("ifconfig " + interface + " hw ether" + new_mac, shell=True)
# subprocess.run("ifconfig " + interface + " up", shell=True)

