# Automation of SROS Backup

There are two ways to get running configs for host(s):

1. Use a python file
2. Use an ansible playbook

A cron job can be added later to run at certain times.

> Note  

* Take note of RSA fingerprints  
* Modify ssh config to support the legacy equipment with old ciphers etc.  

    ```SSH Config
    Host SR*  
        Ciphers aes256-cbc  
        HostKeyAlgorithms ssh-dss  
        KexAlgorithms diffie-hellman-group1-sha1  
        User admin
    ```

## Using a Python script

* Use netmiko
* Send command to device(s):  
    `admin display-config`
* Store output to a file  

See [main.py](./python_script/main.py)

## Using Ansible

* Add hosts fqdn to /etc/hosts if you don't have a dns server (optional)  
* Set up git and upload ssh keys to git server.  
* Create inventory file with necessary parameters.  
* Create group_vars folder and yaml files with necessary parameters(optional). Had to add the below options to my nokia group yaml file on ubuntu server 18.04:  
`ansible_python_interpreter: /usr/bin/python3`  
`ansible_network_os: nokia.sros.classic`  
* Tasks ([Playbook](./playbooks/backup_sros_v2.yaml)):
    1. Use `community.network.sros_command` collection plugin
    2. Send command to device(s):  
    `admin display-config`  
    3. Store output to a variable  
    4. Save output to file  
    5. Run git commands  
