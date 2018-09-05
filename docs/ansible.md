# Automation with Ansible

## What's Ansible

## Hello word: install and deploy a webserver with Ansible

### Playbooks

- install the apache2 packages on localhost

``` yaml
---
- hosts: localhost
  connection: local
  tasks:
  - name: Apache | Make sure the Apache packages are installed
    apt: name=apache2 update_cache=yes
    when: ansible_os_family == "Debian"

  - name: Apache | Make sure the Apache packages are installed
    yum: name=httpd
    when: ansible_os_family == "RedHat"
```

- start services after configuration customization

``` yaml
---
- hosts: localhost
  connection: local
  tasks:
  - name: Configure apache 1/2
    get_url:
      force: true
      url: https://raw.githubusercontent.com/DODAS-TS/SOSC-2018/master/templates/hands-on-1/apache-config/port.conf
      dest: /etc/apache2/ports.conf
  
  - name: Configure apache 2/2
    get_url:
      force: true
      url: https://raw.githubusercontent.com/DODAS-TS/SOSC-2018/master/templates/hands-on-1/apache-config/000-default.conf
      dest: /etc/apache2/sites-enabled/000-default.conf

  - name: Start Apache service
    service: name=apache2 state=restarted
    when: ansible_os_family == "Debian"

  - name: Start Apache service
    service: name=httpd state=restarted
    when: ansible_os_family == "RedHat"
```

### Run the playbooks

- install the apache2 packages on localhost

``` bash
ansible-playbook templates/hands-on-1/ansible-role-install.yml
```

- start services after configuration customization

``` bash
ansible-playbook templates/hands-on-1/ansible-role-apache.yaml
```

- the apache default webpage should now being served at `localhost:4880`