#!/usr/bin/env python
#title           :generate_template.py
#description     :CoreOS Kubernetes Ignition generator
#author          :Eli Kleinman
#date            :20190208
#version         :0.8.5
#usage           :python generate_template.py
#notes           :Now available as a Docker image (image uses python version 3.6.x)  
#python_version  :Tested with 2.7.14 or 3.6.3
#==============================================================================
from __future__ import print_function   # fix print code to work in python 2 and 3!
real_raw_input = vars(__builtins__).get('raw_input',input)  # fix raw_input code to work in python 2 and 3!
import sys
import os
import pip
from contextlib import contextmanager

os.environ['PATH'] += os.pathsep + '.'
replace_template = 'tmp/modifylist.txt'
ct_url = 'https://github.com/coreos/container-linux-config-transpiler/releases/download/v0.9.0/ct-v0.9.0-x86_64-unknown-linux-gnu'
kubectl_url = 'https://storage.googleapis.com/kubernetes-release/release/v1.13.1/bin/linux/amd64/kubectl'
cert_config = 'cert.conf'
msg_list = 'src/msg_list'
no_mkisofs = 'y'
required_pkgs = {
    're': ['re'],
    'ast': ['ast'],
    'pwd': ['pwd'],
    'uuid': ['uuid'],
    'crypt': ['crypt'],
    'shutil': ['shutil'],
    'pprint': ['pprint'],
    'getpass': ['getpass'],
    'requests': ['requests'],
    'platform': ['platform'],
    'subprocess': ['subprocess'],
    'inquirer': ['inquirer'],
    'pycryptodome': ['Crypto.PublicKey.RSA']
}
files_to_prep = [
    'modifylist.txt', 
    'master_templ.txt', 
    'worker_templ.txt',
]
manifests_files = [
    'kube-apiserver.yaml', 
    'kube-controller-manager.yaml',
    'kube-proxy-master.yaml',
    'kube-proxy-work.yaml',
    'kube-scheduler.yaml',
]
dir_list = [
    'tmp',
    'ssl', 
    'keys', 
    'configs', 
    'manifests', 
]
dict_list = {
    'master_nodes': ['master_list.txt'],
    'worker_nodes': ['worker_list.txt'],
    'global_settings': ['global_settings.txt'],
    'ca_ssl_list': ['ca_ssl_list.txt'],
    'ssl_list': ['ssl_list.txt'],
    'srv_cert_list': ['srv_cert_list.txt'],
    'ip_cert_list': ['ip_cert_list.txt'],
}
masters = 1

#=======================================
# Verifying required python modules
@contextmanager
def suppress_stdout():
    with open(os.devnull, 'w') as devnull:
      old_stdout = sys.stdout
      sys.stdout = devnull
      try:
          yield
      finally:
          sys.stdout = old_stdout

#=======================================
# Select Node type - Master or worker node

def server_type():
    questions = [
      inquirer.List('master_worker',
                    message = 'What kubernetes system type are you building ?',
                    choices = ['Master', 'Worker']
      ),
    ]
    answers = inquirer.prompt(questions)

    if answers['master_worker'] == 'Master':
      print_msg(['1'])
      return 'tmp/master_templ.txt', "Master"
    else:
      print_msg(['2'])
      return 'tmp/worker_templ.txt', "Worker"

#=====================================
# Preparing template files

def prep_template(src, dst, prp_tp):
    if prp_tp == 'cp':
      shutil.copyfile(src, dst)
    else:
      shutil.move(src, dst)

#=====================================
# Preparing directorys
def prep_dir(prep_dir):
    if not os.path.exists(prep_dir):
      os.makedirs(prep_dir)

#=====================================
# loading data dictionarie files.

def load_lists(dict_file, dict_var):
    print_msg(['84']), print_msg(dict_var), print_msg('\n')
    with open(dict_file,'r') as dict_list:
      return ast.literal_eval(dict_list.read())

#=====================================
# Downloading the CT Utility

def download_app(url, file_name):

    with open(file_name, 'wb') as file:
      response = requests.get(url)
      file.write(response.content)
      os.chmod(file_name, 0o755)

def app_exists(app):
    return any(
      os.path.exists(os.path.join(path, app))
      for path in os.environ['PATH'].split(os.pathsep)
    )

#=======================================
# Generating password

def gen_pass_hash(user_account, password, default=None):

    if default:
        print_msg(['37']), print_msg(user_account), print_msg(['38']), print_msg(password), print_msg(['39']),
        user_passwd = getpass.getpass(print_msg(['return1', '40'])) or password
        salt = '$6$' + (uuid.uuid4().hex) + '$'
        return (crypt.crypt(user_passwd, salt))
    else:
        print_msg(['37']), print_msg(user_account), print_msg('.\n')
        user_passwd = getpass.getpass(print_msg(['return2', 'Or hit enter to keep existing encrypted password', ': '])) or password
        salt = '$6$' + (uuid.uuid4().hex) + '$'
        if user_passwd == password:
            return password
        else:
            return (crypt.crypt(user_passwd, salt))


#=====================================
# Generating ssh keys - needs pycrypto

def create_ssh_key():

    if os.path.exists('keys/id_rsa'):
      global_mod_yn = mod_set_yn(print_msg(['return1', '41']), False)
      if global_mod_yn:
        private_key, public_key = gen_ssh_key()
        return (private_key, public_key)
      else:
        print_msg(['3'])
        f = open('keys/id_rsa.pub','r')
        public_key = f.read()
        f.close()
        return ('private_key', public_key)
    else:
      private_key, public_key = gen_ssh_key()
      return (private_key, public_key)

# ------------------------------------------
def gen_ssh_key():

    print_msg(['4']), print_msg(['10'])
    import Crypto.PublicKey.RSA
    # Create private key
    key = Crypto.PublicKey.RSA.generate(2048)
    private_key = key.exportKey('PEM')
    f = open('keys/id_rsa','wb')
    f.write(private_key)
    f.close()

    # Create public key
    pubkey = key.publickey()
    public_key = pubkey.exportKey('OpenSSH')
    f = open('keys/id_rsa.pub','wb')
    f.write(public_key)
    f.close()
    return (private_key, public_key.decode("utf-8"))

#=====================================
# Generate Kubernetes SSL certificates
def create_certs(ssl, msg, sslpem):
    if os.path.exists(sslpem):
      global_mod_yn = mod_set_yn(' overwrite the' + msg + 'keys ? (existing keys were found in the ssl directory)', False)
      if global_mod_yn:
        for s in ssl:
          ext_cmd(s)
        print_msg(['5']), print_msg(msg), print_msg(['6'])
        if msg == ' master/worker ':
          print_msg(['10']), print_msg(['11']), print_msg(['12']), 
          print_msg(['8']), print_msg(['13']), print_msg(['10'])
      else:
        print_msg(['10']), print_msg(['13']), print_msg(['10'])
        print_msg(['14']), print_msg('\n'), print_msg(['10']),
    else:
      for s in ssl:
        ext_cmd(s)
      print_msg(['5']), print_msg(msg), print_msg(['6']), print_msg('\n')
      if msg == ' master/worker ':
        print_msg(['10']), print_msg(['11']), print_msg(['12']),
        print_msg(['8']), print_msg(['13']), print_msg(['10'])

def ext_cmd(cmd):
    if cmd != 'no_mkisofs':
      proces = subprocess.Popen(cmd, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

      for line in proces.stderr:
        logger(line)
        logger(cmd)
        errcode = proces.returncode
        if errcode:
          logger(errcode)
          logger(cmd)
      print_msg(['94'])

#=====================================
# SSL and CT log output
def logger(log):
    f = open('tmp/output.log', 'a+')
    f.write(str(log) + '\n')
    sys.stdout.flush()
    f.close()

#=================================
# Modifying / adding certificates
def do_modifications(replacelist, server_template):

    with open(replacelist,'r') as inf:
      list = ast.literal_eval(inf.read())

    for xkey in list:
      for xval in list[xkey]:
        for ykey in xval:
          for yval in xval[ykey]:
            for zval in yval:
              # Fields: Type, Dst_Key_Name, Src_Key/File_Name, Dst_File/Data_path, Template_File
              # Uncomment for debug
              #print (xkey, ykey, zval, yval[zval], server_template)
              inplace_change(xkey, ykey, zval, yval[zval], server_template)

def inplace_change(repl_type, repl_keyname, sfilepath, filecount, filetomodify):

    if repl_type == 'file':
      f = open(sfilepath,'r')
      fromdata = f.read()
      f.close()

      x = ""
      for line in fromdata.splitlines():
        x += re.sub('^', '          ', line) + '\n'

    if repl_type == 'entry':
      x = filecount

    f = open(filetomodify, 'r')
    todata = f.read()
    f.close()

    if 'PROXY1@' in filecount or 'PROXY2@' in filecount:
      newdata = todata.replace(repl_keyname, "#" + sfilepath + "=")
    else:
      newdata = todata.replace(repl_keyname, x)
    f = open(filetomodify, 'w')
    f.write(newdata)
    f.close()

#=======================================
# Modify Host / IP Address

def modify_source(update_source, x, y):
    if y is not None:
      update_source = update_source.replace(x, y)
      return update_source

def prepare_source(update_source, i, host_name, ip_addr, masters):

    new_host_name = real_raw_input('Please provide "Master' \
                        + str(masters) \
                        + '" hostname (default: ' + host_name + ')?: ') or host_name
    new_ip_addr = real_raw_input('Please provide master' \
                      + str(masters) \
                      + '(' + new_host_name + ') \"ip address\" (default: ' + ip_addr + ') ?: ') or ip_addr
    node = re.findall(r'\d+', host_name)

    update_source = modify_source(update_source, '#NODE' \
                        + (str(masters)[0]) + '@', new_host_name)
    master_nodes[i][0] = new_host_name

    update_source = modify_source(update_source, '#NODE' \
                        + (str(masters)[0]) + '_IP@', new_ip_addr)
    master_nodes[i][1] = new_ip_addr
    masters += 1

    return masters, update_source

#=======================================
# Modify Global properties

def mod_set_yn(msg, default):
    questions = [
      inquirer.Confirm('continue',
                       message='Would you like to' + msg, default=default)
    ]
    answers = inquirer.prompt(questions)
    return answers['continue']

#=====================================
# Update Certificate alt names
def mod_global_set(global_settings, i, x):

    new_prop = real_raw_input('Please enter the new value for ' + \
                         global_settings[i][0] + '(default: ' + x + '): ') or x
    global_settings[i][1] = new_prop
    return global_settings

def mod_prop_list(gs, update):
    if update == 'n':
      for i in sorted(gs, key=lambda s: s.lower()):
        if gs[i][1] is not None:
          print_msg(gs[i][0]), print_msg(':'), print_msg(gs[i][1]), print_msg('\n')
    else:
      alt_name = ""
      if update == 'DNS':
        if overwrite_cert_file(cert_config):
          for i in sorted(gs, key=lambda s: s.lower()):
            alt_name += 'DNS.' + gs[i][0] + '              = ' + gs[i][1]+'\n'
          update_cert_file('ssl/' + cert_config, '#DNS#', alt_name)
        else:
          pass
      if update == 'IP':
        for i in sorted(gs, key=lambda s: s.lower()):
          alt_name += 'IP.' + gs[i][0] + '              = ' + gs[i][1]+'\n'
        update_cert_file('ssl/' + cert_config, '#IP#', alt_name)

def overwrite_cert_file(srcfile):

    if os.path.exists(srcfile):
      global_mod_yn = mod_set_yn(print_msg(['return1', '79']), False)
      if global_mod_yn:
        prep_template('template/' + srcfile, 'ssl/' + srcfile, 'cp')
        return True
      else:
        return False
    else:
      prep_template('template/' + srcfile, 'ssl/' + srcfile, 'cp')
      return True

def update_cert_file(srcfile, x, y):
    f = open(srcfile, 'r')
    update_source = f.read()
    f.close()
    cert_alt_list = modify_source(update_source, x, y)

    f = open(srcfile, 'w')
    f.write(cert_alt_list)
    f.close()

#=======================================
# Create ignition file
def ignition_platform():
    questions = [
      inquirer.List('ign_platform',
                    message='What cloud provider are you building for (use vagrant-virtualbox for bare metal) ? available options are.',
                    choices=['azure', 'cloudstack-configdrive', 'cloudstack-metadata', 'digitalocean', 'ec2', \
                             'gce', 'openstack-metadata', 'oracle-oci', 'packet', 'vagrant-virtualbox'
                    ],
                    default='vagrant-virtualbox',
      ),
    ]
    answers = inquirer.prompt(questions)
    return answers['ign_platform']

def create_ignition(server_template, ign_template):
    ign_cmd = 'bin/ct -in-file ' + server_template + ' -platform ' \
              + ignition_platform() + ' -out-file ' + ign_template

    ign_output = subprocess.Popen(ign_cmd, shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

    for line in ign_output.stderr:
      logger(line)
      errcode = ign_output.returncode
      if errcode:
        logger(errcode)
    return ign_template

#=======================================
# Update certificate CN/name/ip list
def update_alt_crt(alt_cert, x, y):
    update_alt_crt = update_source.replace(x, y)
    return update_alt_crt

def mod_global_set(alt_cert, i, x):

    new_prop = real_raw_input('Please enter the new value for ' + alt_cert[i][0] + ': (default: ' + x + '): ') or x
    alt_cert[i][1] = new_prop
    return alt_cert

def add_cert_val(val_list, name, rec, n_rec):
    add_value = '-'
    add_value = real_raw_input('Please Enter additional ' + name + ' , one per line. (leave empty when done): ') or add_value

    if not add_value == '-':
      val_list.update({str(rec): [n_rec, add_value]})
      return ('true', val_list)
    else:
      return ('false', val_list)

#=======================================
# Continue updating system properties
def update_dict_src(dict_update, file_dst):

    with open(file_dst, 'wt') as out:
      pprint.pprint(dict_update, stream=out)

#=======================================
# Check for mkisofs utility
def install_platform_pkg():
    if 'Ubuntu' in platform.dist()[0]:
       print_msg(['96'])
       return 'apt-get -y install genisoimage'
    elif 'redhat' in platform.dist()[0]:
       print_msg(['97'])
       return 'yum -y install mkisofs'
    elif '' in platform.dist()[0]:
       print_msg(['108']), print_msg(['10'])
       print ('mkisofs -l -r -o configs/' + this_host_name + '_template.iso configs/' + this_host_name + '_template.ign')
       print_msg(['10'])
       no_mkisofs = 'y'
       return 'no_mkisofs'

# ===========================================================
#    ******************** Main *************************
# ===========================================================

# Verifying required openssl
if not app_exists('openssl'):
   print ('Missing required dependency (openssl), please install openssl, then re-run. \nExiting.')
   sys.exit(0)

# Verifying required python modules
#-------------------------------------
print ('Verifying required python modules \
\n-----------------------------------------------------------')
for pkg in required_pkgs:
  try:
    globals()[required_pkgs[pkg][0]] = __import__(required_pkgs[pkg][0])
    print ('Skipping module: ' + pkg + ', already installed')
  except ImportError as e:
    print ('\n-----------------------------------------------------------')
    answr_yn = real_raw_input('You are missing a required Python module: ' + pkg + \
    '\nShould we try to install the \"' + pkg + '\" module ?[n] ')
    if answr_yn == 'y':
      print ('Installing missing module: ' + pkg)
      with suppress_stdout():
        pip.main(['install', pkg])
        globals()[required_pkgs[pkg][0]] = __import__(required_pkgs[pkg][0])
    else:
      print ('\n----------------------------------------------------------- \
      \nMissing required module(s), exiting safely')
      exit(1)
print ('-----------------------------------------------------------\n')

#--------------------------------------------
# ----- Pre-load the print message list -----
with open(msg_list,'r') as msg_data:
  print_list = ast.literal_eval(msg_data.read())

def print_msg(msg):
    if 'return1' in msg[0]:
      return print_list[msg[1]][0]
    elif 'return2' in msg[0]:
      return msg[1] + msg[2]
    elif isinstance(msg, list):
      print (print_list[msg[0]][0], end='')
    elif msg == '\n':
      print ('\n', end='')
    else:
      print (msg, end='')

#-------------------------------------
# Load data from dictionarie files.
for val in dict_list:
    for item in dict_list[val]:
        if not app_exists('work/' + item):
            print ("Copying files for the first run", item)
            prep_template('src/' + item, 'work/' + item, 'cp')
            dict_list[val] = ['work/' + item]
        else:
            print (item, "exists")
            dict_list[val] = ['work/' + item]

print_msg(['83']), print_msg(['10']),
master_nodes = load_lists(dict_list['master_nodes'][0], 'master_nodes')
worker_nodes = load_lists(dict_list['worker_nodes'][0], 'worker_nodes')
global_settings = load_lists(dict_list['global_settings'][0], 'global_settings')
ca_ssl_list = load_lists(dict_list['ca_ssl_list'][0], 'ca_ssl_list')
ssl_list = load_lists(dict_list['ssl_list'][0], 'ssl_list')
srv_cert_list = load_lists(dict_list['srv_cert_list'][0], 'srv_cert_list')
ip_cert_list = load_lists(dict_list['ip_cert_list'][0], 'ip_cert_list')
if global_settings['#TOKEN@'][1] is None:
    token = uuid.uuid4().hex[0:32]
else:
    token = global_settings['#TOKEN@'][1]

#-------------------------------------
# Preparing directorys and template files
print_msg(['26']), print_msg(['10'])
for i in dir_list:
  print_msg(['27']), print_msg(i), print_msg('\n')
  prep_dir(i)

print_msg('\n'), print_msg(['24']), print_msg(['10'])
for i in files_to_prep:
  print_msg(['25']), print_msg(i), print_msg('\n')
  prep_template('template/' + i, 'tmp/' + i, 'cp')

print_msg('\n'), print_msg(['80']), print_msg(['10'])
for i in manifests_files:
  print_msg(['81']), print_msg(i), print_msg('\n')
  prep_template('template/' + i, 'manifests/' + i, 'cp')

print ('-----------------------------------------------------------\n')
f = open(replace_template, 'r')
update_source = f.read()
f.close()

# Select a Server type
#-------------------------------------
server_template, server_type_selected = server_type()
print_msg(['10'])

# Download CT if not available
#-------------------------------------
print_msg(['28'])

if not app_exists('bin/ct'):
  print_msg(['29'])
  download_app(ct_url, 'bin/ct')
  print_msg(['30'])
else:
  print_msg(['31'])
print_msg(['10'])

# Set User login / Password
#-------------------------------------
print_msg(['32']), print_msg(['33']), print_msg(['10']), print_msg(['34'])
if global_settings['#USER@'][1] == 'user_account':
    user_account = real_raw_input(print_msg(['return2', global_settings['#USER@'][1], '): '])) or 'usera'
else:
    user_account = real_raw_input(print_msg(['return2', global_settings['#USER@'][1], ': '])) or global_settings['#USER@'][1]

if global_settings['#PASSWD@'][1] == 'Admin_Password':
    pass_hash = gen_pass_hash(user_account, 'Admin_Password', 'y')
else:
    pass_hash = gen_pass_hash(user_account, global_settings['#PASSWD@'][1])

# Setup http_proxy
#-------------------------------------
print_msg(['8'])
print_msg(['98']), print_msg(['99']), print_msg(['100']), print_msg(['101'])
print_msg(['8'])
global_mod_yn = mod_set_yn(print_msg(['return1', '102']), False)
print_msg(['10'])
if global_mod_yn:
  if global_settings['#HTTP_PROXY2@'][1]:
    proxy_addr = re.split(':|@|/', global_settings['#HTTP_PROXY2@'][1])[-2]
    proxy_port =  re.split(':|@|/', global_settings['#HTTP_PROXY2@'][1])[-1]
  proxy_addr = real_raw_input(print_msg(['return1', '103'])) or proxy_addr
  proxy_port = real_raw_input(print_msg(['return1', '104'])) or proxy_port
  print_msg(['105'])
  proxy_account = real_raw_input(print_msg(['return1', '106']))
  if proxy_account:
    user_passwd = getpass.getpass(print_msg(['return1', '107']))
    global_settings['#HTTP_PROXY2@'][1] = "HTTP_PROXY=http://"+proxy_account+":"+user_passwd+"@"+proxy_addr+":"+proxy_port
    global_settings['#HTTPS_PROXY2@'][1] = "HTTPS_PROXY=http://"+proxy_account+":"+user_passwd+"@"+proxy_addr+":"+proxy_port
    print_msg(['10'])
  else:
    global_settings['#HTTP_PROXY2@'][1] = "HTTP_PROXY=http://"+proxy_addr+":"+proxy_port
    global_settings['#HTTPS_PROXY2@'][1] = "HTTPS_PROXY=http://"+proxy_addr+":"+proxy_port
    print_msg(['10'])

# Generating ssh keys - needs pycrypto
#-------------------------------------
priv_key, pub_key = create_ssh_key()
print_msg(['36'])

# Set Properties like user/passwd, ip/host in template files
#-------------------------------------
print_msg(['42'])
if server_type_selected == "Master":
    this_host_name = real_raw_input(print_msg(['return2', master_nodes['node1'][0], '): '])) \
                           or master_nodes['node1'][0]
else:
    this_host_name = real_raw_input(print_msg(['return2', worker_nodes['worke1'][0], '): '])) \
                           or worker_nodes['worke1'][0]

print_msg(['44']), print_msg(this_host_name), print_msg(['45'])
if server_type_selected == "Master":
    this_ip_addr = real_raw_input(print_msg(['return2', master_nodes['node1'][1], '): '])) \
                         or master_nodes['node1'][1]
else:
    this_ip_addr = real_raw_input(print_msg(['return2', worker_nodes['worke1'][1], '): '])) \
                         or worker_nodes['worke1'][1]

#-------------------------------------
# Update system properties
update_source = modify_source(update_source, '#THIS_NODE@', this_host_name)
update_source = modify_source(update_source, '#THIS_NODE_IP@', this_ip_addr)
update_source = modify_source(update_source, '#USER@', user_account)
update_source = modify_source(update_source, '#PASSWD@', pass_hash)
update_source = modify_source(update_source, '#SSH_KEY@', pub_key)
update_source = modify_source(update_source, '#TOKEN@', token)

global_settings['#THIS_NODE@'][1] = this_host_name
global_settings['#THIS_NODE_IP@'][1] = this_ip_addr
global_settings['#USER@'][1] = user_account
global_settings['#PASSWD@'][1] = pass_hash
global_settings['#SSH_KEY@'][1] = pub_key
global_settings['#TOKEN@'][1] = token

print_msg(['46']), print_msg(['47']), print_msg(['10'])
for i in sorted(master_nodes):
  masters, update_source = prepare_source(update_source, i, master_nodes[i][0], master_nodes[i][1], masters)
update_dict_src(master_nodes, dict_list['master_nodes'][0])

print_msg(['10']), print_msg(['48']), print_msg(['10'])
mod_prop_list(global_settings, 'n')

print_msg(['10'])
global_mod_yn = mod_set_yn(print_msg(['return1', '49']), False)
if global_mod_yn:
  print_msg(['50']), print_msg(['51']), print_msg(['52']), print_msg(['10'])
  for i in sorted(global_settings, key=lambda s: s.lower()):
    if global_settings[i][1] is not None:
      global_settings = mod_global_set(global_settings, i, global_settings[i][1])

  print_msg(['10'])
  print_msg(['53']), print_msg(['10'])
  mod_prop_list(global_settings, 'n')

else:
  pass

print_msg(['10']), print_msg(['57']), print_msg(['10'])
for i in sorted(global_settings, key=lambda s: s.lower()):
  if global_settings[i][1]:
    update_source = modify_source(update_source, i, global_settings[i][1])
update_dict_src(global_settings, dict_list['global_settings'][0])

# Write all changes to template file
f = open(replace_template,'w')
f.write(update_source)
f.close()

# Update SSL certificate names in cert.conf
#-------------------------------------
print_msg(['54']), print_msg(['10'])
mod_prop_list(srv_cert_list, 'n')
print_msg(['10'])
global_mod_yn = mod_set_yn(print_msg(['return1', '49']), False)

if global_mod_yn:
  print_msg(['50']), print_msg(['51']), print_msg(['10'])
  for i in sorted(srv_cert_list, key=lambda s: s.lower()):
    srv_cert_list = mod_global_set(srv_cert_list, i, srv_cert_list[i][1])

print_msg(['10'])
global_mod_yn = mod_set_yn(print_msg(['return1', '55']), False)
if global_mod_yn:
  done_add = 'true'
  while done_add == 'true':
    if (int(srv_cert_list.keys()[-1])+1) < 10:
      rec = '0' + str(int(srv_cert_list.keys()[-1])+1)
      n_rec = str(int(srv_cert_list.keys()[-1])+1)
      done_add, srv_cert_list = add_cert_val(srv_cert_list, 'Host Name', rec, n_rec)
    else:
      rec = str(int(len(srv_cert_list.keys()))+1)
      n_rec = str(int(len(srv_cert_list.keys()))+1)
      done_add, srv_cert_list = add_cert_val(srv_cert_list, 'Host Names', rec, n_rec)

print_msg(['10']), print_msg(['56']), print_msg(['10'])
mod_prop_list(srv_cert_list, 'n')

print_msg(['8'])
mod_prop_list(srv_cert_list, 'DNS')

print_msg(['10']), print_msg(['58']), print_msg(['10'])
mod_prop_list(ip_cert_list, 'n')
print_msg(['10'])
global_mod_yn = mod_set_yn(print_msg(['return1', '49']), False)
if global_mod_yn:
   print_msg(['50']), print_msg(['51']), print_msg(['10'])
   for i in sorted(ip_cert_list, key=lambda s: s.lower()):
     ip_cert_list = mod_global_set(ip_cert_list, i, ip_cert_list[i][1])

update_dict_src(srv_cert_list, dict_list['srv_cert_list'][0])

print_msg(['10'])
global_mod_yn = mod_set_yn(print_msg(['return1', '59']), False)
if global_mod_yn:
  done_add = 'true'
  while done_add == 'true':
    if (int(ip_cert_list.keys()[-1])+1) < 10:
      rec = '0' + str(int(ip_cert_list.keys()[-1])+1)
      n_rec = str(int(ip_cert_list.keys()[-1])+1)
      done_add, ip_cert_list = add_cert_val(ip_cert_list, 'IP Address', rec, n_rec)
    else:
      rec = str(int(len(ip_cert_list.keys()))+1)
      n_rec = str(int(len(ip_cert_list.keys()))+1)
      done_add, ip_cert_list = add_cert_val(ip_cert_list, 'IP Address', rec, n_rec)

print_msg(['10']), print_msg(['56']), print_msg(['10'])
mod_prop_list(ip_cert_list, 'n')

print_msg(['8'])
mod_prop_list(ip_cert_list, 'IP')
update_dict_src(ip_cert_list, dict_list['ip_cert_list'][0])

# Generating Kubernetes SSL certificates
#-------------------------------------
create_certs(ca_ssl_list, ' CA ', 'ssl/ca.pem')
print_msg(['60']), print_msg(['10'])
create_certs(ssl_list, ' master/worker ', 'ssl/etcd-node.pem')

#-------------------------------------
# Modifying manifest files
print_msg(['82']), print_msg(['10'])
for i in sorted(manifests_files, key=lambda s: s.lower()):
  do_modifications(replace_template, 'manifests/' + i)

#-------------------------------------
# Adding modifications SSL certificates to template file
print_msg(['61']), print_msg('\n')
do_modifications(replace_template, server_template)

print_msg(['62']), print_msg(['10'])

print_msg(['65']), print_msg(['10'])
ign_template = create_ignition(server_template, 'configs/' + this_host_name + '_template.ign')
print_msg(['10']), print_msg(['76']), print_msg(['10'])

print_msg(['72']), 
print_msg(['73']), print_msg('configs/' + server_template), print_msg(['74']),
print_msg(this_host_name), sys.stdout.write(''), print_msg(['75'])
prep_template(server_template, 'configs/' + this_host_name + '_template.yaml', 'mv')

print_msg(['10']), print_msg(['76']), print_msg(['10'])

# Install mkisofs if not available
#-------------------------------------
print_msg(['92'])
if not app_exists('mkisofs'):
  print_msg(['93'])
  ext_cmd(install_platform_pkg())
else:
  no_mkisofs = 'n'
  print_msg(['95'])

if no_mkisofs == 'n':
  print_msg(['77']), print_msg(['10'])
  ext_cmd('mkisofs -l -r -o configs/' + this_host_name + '_template.iso configs/' + this_host_name + '_template.ign')

# Download Kubectl if not available
#-------------------------------------
print_msg(['85'])

if not app_exists('bin/kubectl'):
  print_msg(['86'])
  download_app(kubectl_url, 'bin/kubectl')
  print_msg(['87'])
else:
  print_msg(['88'])
print_msg(['10'])
print_msg(['89']), print_msg(['90'])
print_msg(['10'])
print_msg(['91'])
print_msg(['10'])

#-------------------------------------
# Print summary information
print_msg(['66']), print_msg(['10'])
print_msg(['67']), 
print_msg(['68']), 
print_msg(['69']),
print_msg(['70']), print_msg('configs/' + this_host_name), sys.stdout.write(''), print_msg('_template.yaml'),
print_msg(['71']), print_msg(ign_template), print_msg('\n'),
print_msg(['78']), print_msg('configs/' + this_host_name), sys.stdout.write(''), print_msg('_template.iso'), print_msg('\n')
