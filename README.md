# Automation of SROS Backup

There are two ways to get running configs for host(s):

1. Use a python file
2. Use an ansible playbook

A cron job can be added later to run at certain times.

> Note  

* Take note of RSA fingerprints  
* Modify ssh config to support the legacy equipment with old ciphers etc. This happened to me in my lab with old sros images:  

    ```SSH Config
    Host <hostname>  
        Ciphers aes256-cbc  
        HostKeyAlgorithms ssh-dss  
        KexAlgorithms diffie-hellman-group1-sha1  
        User <username>
    ```

## Using a Python script

* Use netmiko
* Send command to device(s):  
    `admin display-config`
* Store output to a file  

See [main.py](./python_script/main.py)

## Using Ansible

Ansible version at time of writing is 2.9.19

My Directory structure:

```text
.
├── inventory
│   ├── group_vars
│   │   └── Nokia.yaml
│   └── hosts
├── playbooks
    ├── backup_w_cn_module.yaml
    ├── backup_w_cn_sros_config.yaml
    └── backup_w_ns_module.yaml
```

* Set up git and upload ssh keys to git server.
* Set up repo and sync with backup folder
* (Optional) Add hosts fqdn to /etc/hosts if you don't have a dns server. Makes it easier to read the hosts files.  
* On ubuntu server 18.04 since default python is python 2.7, you might have to add this to your host group yaml or in the playbook:  
`ansible_python_interpreter: /usr/bin/python3`  

### Option 1: Using community.network module sros_command (v2.1.0)

[More Info](https://docs.ansible.com/ansible/latest/collections/community/network/sros_command_module.html)

* Install module `ansible-galaxy collection install community.network`

* Create inventory file with necessary parameters.

* Create group_vars folder and yaml files with necessary parameters(optional). You can add this to your nokia group yaml file or as a variable in the playbook:  
`ansible_network_os: sros`  

* **Tasks** ([Playbook](./playbooks/backup_w_cn_module.yaml)):
    1. Use `community.network.sros_command` collection plugin
    2. Send command to device(s):  
    `admin display-config`  
    3. Store output to a variable  
    4. Save output to file  
    5. Run git commands  

The disadvantage of this module is that it just copies the output of the `admin display-config` command which has the timestamp the file was generated. Hence anytime the playbook is run the time is different and so you don't really get to benefit from Ansible's idempotency.  
Also Git will always register that line as a change.

### Option 2: Using nokia.sros (v1.6.0)

[More Info](https://galaxy.ansible.com/nokia/sros)

* Install module `ansible-galaxy collection install nokia.sros`

* Create inventory file with necessary parameters.

* Create group_vars folder and yaml files with necessary parameters(optional). HYou can add this to your nokia group yaml file or as a variable in the playbook:  
`ansible_network_os: nokia.sros.classic`  

* **Tasks** ([Playbook](./playbooks/backup_w_ns_module.yaml)):
    1. Use `nokia.sros` collection
    2. Use `cli_config` plugin
    3. Use the `backup: yes` and under that use `backup options` with the dir_path and filename options. You can leave the filename and the module will create the file with the hostname and timestamp.
    4. Save output to file  
    5. Run git commands  

The advantage of this module is that it saves the configs without the top heading with the SROS version and the timestamp. So you get to benefit from Ansible's idempotency.  
Disadvantage is that you will have to depend on Git and the file properties to know when the file was generated.

### Option 3 Using community.network module sros_config (v2.1.0)

[More Info](https://docs.ansible.com/ansible/latest/collections/community/network/sros_config_module.html)

This has a similar setup like Option 1 but uses a backup module simliar to the nokia.sros module. Also the output is similar to the first option. Check out the playbook:  
[Playbook](./playbooks/backup_w_ns_module.yaml)

The disadvantage of this module is that it just copies the output of the `admin display-config` command which has the timestamp the file was generated. Hence anytime the playbook is run the time is different and so you don't really get to benefit from Ansible's idempotency.  
Also Git will always register that line as a change.

> Note: Remember to run the playbook with the -i <inventory_filepath> flag when your inventory isn't in the default location.

## Cron Job

Set up cron job to automatically run the playbook at specific times. This cronjob will run at 1am daily:  
`0 1 * * * /usr/bin/ansible-playbook /home/ubuntu/config_backup/playbooks/config_backup.yml`

## References

<https://docs.ansible.com/ansible/latest/collections/community/network/sros_command_module.html>  
<https://github.com/nokia/ansible-networking-collections/tree/master/sros>  
<https://packetswitch.co.uk/ncm-ansible-git/>  
<https://www.rogerperkin.co.uk/network-automation/ansible/ansible-tutorial-network-engineers/>  
