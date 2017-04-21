#!/usr/bin/env python

import paramiko

def main():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect("test.sirena-travel.ru", 22, "apushkin", "zxcmnb86$")
    stdin, stdout, stderr = client.exec_command('ls -l')
    print(stdout.read().decode())

if __name__ == "__main__":
    main()
