__author__ = 'sabe6191'

# from locust import HttpLocust, TaskSet
#
# def login(l):
#     l.client.post("/login", {"username":"ellen_key", "password":"education"})
#
# def list(l):
#     l.client.get("/862456/deployments")
#
# def profile(l):
#     l.client.get("/profile")
#
# def deploy(l):
#     l.client.post("/862456/deployments", data={})
#
# class UserBehavior(TaskSet):
#     tasks = {list:1}
#     #tasks = {index:2, profile:1}
#
#     def on_start(self):
#         login(self)
#
# class HeatUser(HttpLocust):
#     task_set = UserBehavior
#     min_wait=5000
#     max_wait=9000


from locust import HttpLocust, TaskSet, task
import json
import pdb

json1 = """
{
    "stack_name": "Hello",
    "template_url": "https: //raw.githubusercontent.com/rackspace-orchestration-templates/wordpress-single/master/wordpress-single.yaml",
    "parameters": [
        {
            "flavor": "2GBPerformance"
        }
    ],
    "timeout_mins": 20
}
"""

json2 = """
{"stack_name": "qe_wordpress-singleORD-tempest-18416", "disable_rollback": true, "template": {"parameter_groups": [{"parameters": ["server_hostname", "image", "flavor"], "label": "Server Settings"}, {"parameters": ["domain", "username"], "label": "WordPress Settings"}, {"parameters": ["kitchen", "chef_version", "version", "prefix"], "label": "rax-dev-params"}], "heat_template_version": "2013-05-23", "description": "This is a Heat template to deploy a single Linux server running WordPress.\n", "parameters": {"server_hostname": {"default": "WordPress", "label": "Server Name", "type": "string", "description": "Hostname to use for the server that's built.", "constraints": [{"length": {"max": 64, "min": 1}}, {"allowed_pattern": "^[a-zA-Z][a-zA-Z0-9-]*$", "description": "Must begin with a letter and contain only alphanumeric characters.\n"}]}, "username": {"default": "wp_user", "label": "Username", "type": "string", "description": "Username for system, database, and WordPress logins.", "constraints": [{"allowed_pattern": "^[a-zA-Z0-9 _.@-]{1,16}$", "description": "Must be shorter than 16 characters and may only contain alphanumeric\ncharacters, ' ', '_', '.', '@', and/or '-'.\n"}]}, "domain": {"default": "example.com", "label": "Site Domain", "type": "string", "description": "Domain to be used with WordPress site", "constraints": [{"allowed_pattern": "^[a-zA-Z0-9.-]{1,255}.[a-zA-Z]{2,15}$", "description": "Must be a valid domain name"}]}, "image": {"default": "Ubuntu 12.04 LTS (Precise Pangolin)", "label": "Operating System", "type": "string", "description": "Required: Server image used for all servers that are created as a part of\nthis deployment.\n", "constraints": [{"description": "Must be a supported operating system.", "allowed_values": ["Ubuntu 12.04 LTS (Precise Pangolin)"]}]}, "prefix": {"default": "wp_", "label": "Database Prefix", "type": "string", "description": "Prefix to use for WordPress database tables", "constraints": [{"allowed_pattern": "^[0-9a-zA-Z$_]{0,10}$", "description": "Prefix must be shorter than 10 characters, and can only include\nletters, numbers, $, and/or underscores.\n"}]}, "version": {"default": "3.9.2", "label": "WordPress Version", "type": "string", "description": "Version of WordPress to install", "constraints": [{"allowed_values": ["3.9.2"]}]}, "database_name": {"default": "wordpress", "label": "Database Name", "type": "string", "description": "WordPress database name", "constraints": [{"allowed_pattern": "^[0-9a-zA-Z$_]{1,64}$", "description": "Maximum length of 64 characters, may only contain letters, numbers, and\nunderscores.\n"}]}, "flavor": {"default": "4 GB Performance", "label": "Server Size", "type": "string", "description": "Required: Rackspace Cloud Server flavor to use. The size is based on the\namount of RAM for the provisioned server.\n", "constraints": [{"description": "Must be a valid Rackspace Cloud Server flavor for the region you have\nselected to deploy into.\n", "allowed_values": ["1 GB Performance", "2 GB Performance", "4 GB Performance", "8 GB Performance", "15 GB Performance", "30 GB Performance", "1GB Standard Instance", "2GB Standard Instance", "4GB Standard Instance", "8GB Standard Instance", "15GB Standard Instance", "30GB Standard Instance"]}]}, "chef_version": {"default": "11.16.0", "type": "string", "description": "Version of chef client to use", "label": "Chef Version"}, "kitchen": {"default": "https://github.com/rackspace-orchestration-templates/wordpress-single.git", "type": "string", "description": "URL for a git repo containing required cookbooks", "label": "Kitchen URL"}}, "outputs": {"mysql_root_password": {"description": "MySQL Root Password", "value": {"get_attr": ["mysql_root_password", "value"]}}, "wordpress_password": {"description": "WordPress Password", "value": {"get_attr": ["database_password", "value"]}}, "private_key": {"description": "SSH Private Key", "value": {"get_attr": ["ssh_key", "private_key"]}}, "server_ip": {"description": "Server IP", "value": {"get_attr": ["wordpress_server", "accessIPv4"]}}, "wordpress_user": {"description": "WordPress User", "value": {"get_param": "username"}}}, "resources": {"sync_key": {"type": "OS::Nova::KeyPair", "properties": {"name": {"str_replace": {"params": {"%stack_id%": {"get_param": "OS::stack_id"}}, "template": "%stack_id%-sync"}}, "save_private_key": true}}, "wp_secure_auth": {"type": "OS::Heat::RandomString", "properties": {"length": 32, "sequence": "hexdigits"}}, "wordpress_server": {"type": "Rackspace::Cloud::Server", "properties": {"key_name": {"get_resource": "ssh_key"}, "flavor": {"get_param": "flavor"}, "name": {"get_param": "server_hostname"}, "image": {"get_param": "image"}, "metadata": {"rax-heat": {"get_param": "OS::stack_id"}}}}, "mysql_root_password": {"type": "OS::Heat::RandomString", "properties": {"length": 16, "sequence": "lettersdigits"}}, "mysql_debian_password": {"type": "OS::Heat::RandomString", "properties": {"length": 16, "sequence": "lettersdigits"}}, "wp_auth": {"type": "OS::Heat::RandomString", "properties": {"length": 32, "sequence": "hexdigits"}}, "wp_nonce": {"type": "OS::Heat::RandomString", "properties": {"length": 32, "sequence": "hexdigits"}}, "ssh_key": {"type": "OS::Nova::KeyPair", "properties": {"name": {"get_param": "OS::stack_id"}, "save_private_key": true}}, "wordpress_setup": {"depends_on": "wordpress_server", "type": "OS::Heat::ChefSolo", "properties": {"username": "root", "node": {"varnish": {"listen_port": "80"}, "sysctl": {"values": {"fs.inotify.max_user_watches": 1000000}}, "lsyncd": {"interval": 5}, "monit": {"mail_format": {"from": "monit@localhost"}, "notify_email": "root@localhost"}, "vsftpd": {"hide_ids": false, "chroot_local_user": false, "ssl_enable": true, "ssl_ciphers": "AES256-SHA", "write_enable": true, "ipaddress": "", "local_umask": "002"}, "wordpress": {"keys": {"logged_in": {"get_attr": ["wp_logged_in", "value"]}, "secure_auth_key": {"get_attr": ["wp_secure_auth", "value"]}, "nonce_key": {"get_attr": ["wp_nonce", "value"]}, "auth": {"get_attr": ["wp_auth", "value"]}}, "server_aliases": [{"get_param": "domain"}], "version": {"get_param": "version"}, "db": {"user": {"get_param": "username"}, "host": "127.0.0.1", "name": {"get_param": "database_name"}, "pass": {"get_attr": ["database_password", "value"]}}, "dir": {"str_replace": {"params": {"%domain%": {"get_param": "domain"}}, "template": "/var/www/vhosts/%domain%"}}}, "run_list": ["recipe[apt]", "recipe[build-essential]", "recipe[rax-wordpress::apache-prep]", "recipe[sysctl::attribute_driver]", "recipe[mysql::server]", "recipe[rax-wordpress::mysql]", "recipe[hollandbackup]", "recipe[hollandbackup::mysqldump]", "recipe[hollandbackup::main]", "recipe[hollandbackup::backupsets]", "recipe[hollandbackup::cron]", "recipe[rax-wordpress::x509]", "recipe[memcached]", "recipe[php]", "recipe[wordpress]", "recipe[rax-wordpress::wp-setup]", "recipe[rax-wordpress::user]", "recipe[rax-wordpress::memcache]", "recipe[lsyncd]", "recipe[vsftpd]", "recipe[rax-wordpress::vsftpd]", "recipe[varnish::apt_repo]", "recipe[varnish]", "recipe[rax-wordpress::apache]", "recipe[rax-wordpress::varnish]", "recipe[rax-wordpress::firewall]", "recipe[rax-wordpress::vsftpd-firewall]", "recipe[rax-wordpress::lsyncd]"], "mysql": {"bind_address": "127.0.0.1", "remove_test_database": true, "server_debian_password": {"get_attr": ["mysql_debian_password", "value"]}, "server_root_password": {"get_attr": ["mysql_root_password", "value"]}, "server_repl_password": {"get_attr": ["mysql_repl_password", "value"]}, "remove_anonymous_users": true}, "apache": {"listen_ports": [8080], "serversignature": "Off", "traceenable": "Off", "timeout": 30}, "memcached": {"listen": "127.0.0.1"}, "hollandbackup": {"main": {"mysqldump": {"host": "localhost", "password": {"get_attr": ["mysql_root_password", "value"]}, "user": "root"}, "backup_directory": "/var/lib/mysqlbackup"}}, "rax": {"apache": {"domain": {"get_param": "domain"}}, "varnish": {"master_backend": "localhost"}, "wordpress": {"admin_pass": {"get_attr": ["database_password", "value"]}, "admin_user": {"get_param": "username"}, "user": {"group": {"get_param": "username"}, "name": {"get_param": "username"}}}, "lsyncd": {"ssh": {"private_key": {"get_attr": ["sync_key", "private_key"]}}}}}, "private_key": {"get_attr": ["ssh_key", "private_key"]}, "kitchen": {"get_param": "kitchen"}, "host": {"get_attr": ["wordpress_server", "accessIPv4"]}, "chef_version": {"get_param": "chef_version"}}}, "database_password": {"type": "OS::Heat::RandomString", "properties": {"length": 16, "sequence": "lettersdigits"}}, "wp_logged_in": {"type": "OS::Heat::RandomString", "properties": {"length": 32, "sequence": "hexdigits"}}, "mysql_repl_password": {"type": "OS::Heat::RandomString", "properties": {"length": 16, "sequence": "lettersdigits"}}}}, "parameters": {"flavor": "2 GB Performance"}, "timeout_mins": 120}
"""

json3 = """{"stack_name": "sabeen-php-app-12", "disable_rollback": true, "template": {"outputs": {"public_ip": {"description": "The public ip address of the server", "value": {"get_attr": ["php_app", "PublicIp"]}}, "private_ip": {"description": "The private ip address of the server", "value": {"get_attr": ["php_app", "PrivateIp"]}}, "website_url": {"description": "URL for PHP app", "value": {"str_replace": {"params": {"%ip%": {"get_attr": ["php_app", "PublicIp"]}}, "template": "http://%ip%/"}}}}, "heat_template_version": "2013-05-23", "description": "A template implementation of a resource that provides a PHP application server\n", "parameters": {"key_name": {"required": true, "type": "String", "description": "Nova keypair name for ssh access to the server"}, "flavor": {"default": "1GB Standard Instance", "type": "String", "description": "Rackspace Cloud Server flavor", "constraints": [{"description": "must be a valid Rackspace Cloud Server flavor.", "allowed_values": ["512MB Standard Instance", "1GB Standard Instance", "2GB Standard Instance", "4GB Standard Instance", "8GB Standard Instance", "15GB Standard Instance", "30GB Standard Instance"]}]}, "git_url": {"required": true, "type": "String", "description": "URL of a Git repository containing the PHP code."}, "server_name": {"default": "PHP application", "type": "String", "description": "the instance name"}}, "resources": {"php_app": {"type": "Rackspace::Cloud::Server", "properties": {"key_name": {"get_param": "key_name"}, "flavor": {"get_param": "flavor"}, "user_data": {"str_replace": {"params": {"%git_url%": {"get_param": "git_url"}}, "template": "#!/bin/bash -v\nyum -y install httpd git php\n/etc/init.d/httpd start\nchkconfig httpd on\niptables -I INPUT -p tcp --dport 80 -j ACCEPT\niptables-save > /etc/sysconfig/iptables\ngit clone %git_url% /var/www/html/\n"}}, "image": "CentOS 6.4", "name": {"get_param": "server_name"}}}}}, "parameters": {"key_name": "sabeen", "git_url": "https://github.com/timductive/phphelloworld"}, "timeout_mins": 60}"""

json4 = """
{"stack_name": "qe_wordpress-singleORD-tempest-16230", "disable_rollback": true, "template": {"parameter_groups": [{"parameters": ["server_hostname", "image", "flavor"], "label": "Server Settings"}, {"parameters": ["domain", "username"], "label": "WordPress Settings"}, {"parameters": ["kitchen", "chef_version", "version", "prefix"], "label": "rax-dev-params"}], "heat_template_version": "2013-05-23", "description": "This is a Heat template to deploy a single Linux server running WordPress.\n", "parameters": {"server_hostname": {"default": "WordPress", "label": "Server Name", "type": "string", "description": "Hostname to use for the server that's built.", "constraints": [{"length": {"max": 64, "min": 1}}, {"allowed_pattern": "^[a-zA-Z][a-zA-Z0-9-]*$", "description": "Must begin with a letter and contain only alphanumeric characters.\n"}]}, "username": {"default": "wp_user", "label": "Username", "type": "string", "description": "Username for system, database, and WordPress logins.", "constraints": [{"allowed_pattern": "^[a-zA-Z0-9 _.@-]{1,16}$", "description": "Must be shorter than 16 characters and may only contain alphanumeric\ncharacters, ' ', '_', '.', '@', and/or '-'.\n"}]}, "domain": {"default": "example.com", "label": "Site Domain", "type": "string", "description": "Domain to be used with WordPress site", "constraints": [{"allowed_pattern": "^[a-zA-Z0-9.-]{1,255}.[a-zA-Z]{2,15}$", "description": "Must be a valid domain name"}]}, "image": {"default": "Ubuntu 12.04 LTS (Precise Pangolin)", "label": "Operating System", "type": "string", "description": "Required: Server image used for all servers that are created as a part of\nthis deployment.\n", "constraints": [{"description": "Must be a supported operating system.", "allowed_values": ["Ubuntu 12.04 LTS (Precise Pangolin)"]}]}, "prefix": {"default": "wp_", "label": "Database Prefix", "type": "string", "description": "Prefix to use for WordPress database tables", "constraints": [{"allowed_pattern": "^[0-9a-zA-Z$_]{0,10}$", "description": "Prefix must be shorter than 10 characters, and can only include\nletters, numbers, $, and/or underscores.\n"}]}, "version": {"default": "3.9.2", "label": "WordPress Version", "type": "string", "description": "Version of WordPress to install", "constraints": [{"allowed_values": ["3.9.2"]}]}, "database_name": {"default": "wordpress", "label": "Database Name", "type": "string", "description": "WordPress database name", "constraints": [{"allowed_pattern": "^[0-9a-zA-Z$_]{1,64}$", "description": "Maximum length of 64 characters, may only contain letters, numbers, and\nunderscores.\n"}]}, "flavor": {"default": "4 GB Performance", "label": "Server Size", "type": "string", "description": "Required: Rackspace Cloud Server flavor to use. The size is based on the\namount of RAM for the provisioned server.\n", "constraints": [{"description": "Must be a valid Rackspace Cloud Server flavor for the region you have\nselected to deploy into.\n", "allowed_values": ["1 GB Performance", "2 GB Performance", "4 GB Performance", "8 GB Performance", "15 GB Performance", "30 GB Performance", "1GB Standard Instance", "2GB Standard Instance", "4GB Standard Instance", "8GB Standard Instance", "15GB Standard Instance", "30GB Standard Instance"]}]}, "chef_version": {"default": "11.16.0", "type": "string", "description": "Version of chef client to use", "label": "Chef Version"}, "kitchen": {"default": "https://github.com/rackspace-orchestration-templates/wordpress-single.git", "type": "string", "description": "URL for a git repo containing required cookbooks", "label": "Kitchen URL"}}, "outputs": {"mysql_root_password": {"description": "MySQL Root Password", "value": {"get_attr": ["mysql_root_password", "value"]}}, "wordpress_password": {"description": "WordPress Password", "value": {"get_attr": ["database_password", "value"]}}, "private_key": {"description": "SSH Private Key", "value": {"get_attr": ["ssh_key", "private_key"]}}, "server_ip": {"description": "Server IP", "value": {"get_attr": ["wordpress_server", "accessIPv4"]}}, "wordpress_user": {"description": "WordPress User", "value": {"get_param": "username"}}}, "resources": {"sync_key": {"type": "OS::Nova::KeyPair", "properties": {"name": {"str_replace": {"params": {"%stack_id%": {"get_param": "OS::stack_id"}}, "template": "%stack_id%-sync"}}, "save_private_key": true}}, "wp_secure_auth": {"type": "OS::Heat::RandomString", "properties": {"length": 32, "sequence": "hexdigits"}}, "wordpress_server": {"type": "Rackspace::Cloud::Server", "properties": {"key_name": {"get_resource": "ssh_key"}, "flavor": {"get_param": "flavor"}, "name": {"get_param": "server_hostname"}, "image": {"get_param": "image"}, "metadata": {"rax-heat": {"get_param": "OS::stack_id"}}}}, "mysql_root_password": {"type": "OS::Heat::RandomString", "properties": {"length": 16, "sequence": "lettersdigits"}}, "mysql_debian_password": {"type": "OS::Heat::RandomString", "properties": {"length": 16, "sequence": "lettersdigits"}}, "wp_auth": {"type": "OS::Heat::RandomString", "properties": {"length": 32, "sequence": "hexdigits"}}, "wp_nonce": {"type": "OS::Heat::RandomString", "properties": {"length": 32, "sequence": "hexdigits"}}, "ssh_key": {"type": "OS::Nova::KeyPair", "properties": {"name": {"get_param": "OS::stack_id"}, "save_private_key": true}}, "wordpress_setup": {"depends_on": "wordpress_server", "type": "OS::Heat::ChefSolo", "properties": {"username": "root", "node": {"varnish": {"listen_port": "80"}, "sysctl": {"values": {"fs.inotify.max_user_watches": 1000000}}, "lsyncd": {"interval": 5}, "monit": {"mail_format": {"from": "monit@localhost"}, "notify_email": "root@localhost"}, "vsftpd": {"hide_ids": false, "chroot_local_user": false, "ssl_enable": true, "ssl_ciphers": "AES256-SHA", "write_enable": true, "ipaddress": "", "local_umask": "002"}, "wordpress": {"keys": {"logged_in": {"get_attr": ["wp_logged_in", "value"]}, "secure_auth_key": {"get_attr": ["wp_secure_auth", "value"]}, "nonce_key": {"get_attr": ["wp_nonce", "value"]}, "auth": {"get_attr": ["wp_auth", "value"]}}, "server_aliases": [{"get_param": "domain"}], "version": {"get_param": "version"}, "db": {"user": {"get_param": "username"}, "host": "127.0.0.1", "name": {"get_param": "database_name"}, "pass": {"get_attr": ["database_password", "value"]}}, "dir": {"str_replace": {"params": {"%domain%": {"get_param": "domain"}}, "template": "/var/www/vhosts/%domain%"}}}, "run_list": ["recipe[apt]", "recipe[build-essential]", "recipe[rax-wordpress::apache-prep]", "recipe[sysctl::attribute_driver]", "recipe[mysql::server]", "recipe[rax-wordpress::mysql]", "recipe[hollandbackup]", "recipe[hollandbackup::mysqldump]", "recipe[hollandbackup::main]", "recipe[hollandbackup::backupsets]", "recipe[hollandbackup::cron]", "recipe[rax-wordpress::x509]", "recipe[memcached]", "recipe[php]", "recipe[wordpress]", "recipe[rax-wordpress::wp-setup]", "recipe[rax-wordpress::user]", "recipe[rax-wordpress::memcache]", "recipe[lsyncd]", "recipe[vsftpd]", "recipe[rax-wordpress::vsftpd]", "recipe[varnish::apt_repo]", "recipe[varnish]", "recipe[rax-wordpress::apache]", "recipe[rax-wordpress::varnish]", "recipe[rax-wordpress::firewall]", "recipe[rax-wordpress::vsftpd-firewall]", "recipe[rax-wordpress::lsyncd]"], "mysql": {"bind_address": "127.0.0.1", "remove_test_database": true, "server_debian_password": {"get_attr": ["mysql_debian_password", "value"]}, "server_root_password": {"get_attr": ["mysql_root_password", "value"]}, "server_repl_password": {"get_attr": ["mysql_repl_password", "value"]}, "remove_anonymous_users": true}, "apache": {"listen_ports": [8080], "serversignature": "Off", "traceenable": "Off", "timeout": 30}, "memcached": {"listen": "127.0.0.1"}, "hollandbackup": {"main": {"mysqldump": {"host": "localhost", "password": {"get_attr": ["mysql_root_password", "value"]}, "user": "root"}, "backup_directory": "/var/lib/mysqlbackup"}}, "rax": {"apache": {"domain": {"get_param": "domain"}}, "varnish": {"master_backend": "localhost"}, "wordpress": {"admin_pass": {"get_attr": ["database_password", "value"]}, "admin_user": {"get_param": "username"}, "user": {"group": {"get_param": "username"}, "name": {"get_param": "username"}}}, "lsyncd": {"ssh": {"private_key": {"get_attr": ["sync_key", "private_key"]}}}}}, "private_key": {"get_attr": ["ssh_key", "private_key"]}, "kitchen": {"get_param": "kitchen"}, "host": {"get_attr": ["wordpress_server", "accessIPv4"]}, "chef_version": {"get_param": "chef_version"}}}, "database_password": {"type": "OS::Heat::RandomString", "properties": {"length": 16, "sequence": "lettersdigits"}}, "wp_logged_in": {"type": "OS::Heat::RandomString", "properties": {"length": 32, "sequence": "hexdigits"}}, "mysql_repl_password": {"type": "OS::Heat::RandomString", "properties": {"length": 16, "sequence": "lettersdigits"}}}}, "parameters": {"flavor": "2 GB Performance"}, "timeout_mins": 120}
"""

heat_headers = """
{"Content-Type": "application/json", "X-Auth-User": "heatqe2", "Accept": "application/json", "X-Auth-Token":"2995601778914fc69c429e1dcaf5654e"}
"""

class MyTaskSet(TaskSet):

    @task
    def get(self):
        response = self.client.get("/stacks", headers={"Content-Type": "application/json", "X-Auth-User": "heatqe2", "Accept": "application/json", "X-Auth-Token":"2995601778914fc69c429e1dcaf5654e"})
        print "Response for get is:", response.status_code
        print "Response content is:", response.content

class MyLocust(HttpLocust):
    task_set = MyTaskSet
    min_wait = 5000
    max_wait = 15000

