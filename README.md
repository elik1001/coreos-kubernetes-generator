# coreos-kubernetes-generator
This document provides instructions on how to install and use the Python Kubernetes Generator Script. the script helps  automate a Kubernetes deployment on CoreOS. See the deployment notes for additional details.

This repository includes the Python Kubernetes Generator Script, as well as pre configured samples.
<ol>
	<li>The script helps automate a Kubernetes Multi-Master deployment on CoreOS.</li>
	<li>The script generates a CoreOS Ignition file that can be used, either as part of a 3 node Master cluster or just as a worker node.</li>
	<li>The generated Ignition file includes all required properties for, Etcd, Flannel(with CNI), Kubelet using (Rkt), etc.. all protocols are configured to use SSL.</li>
</ol>

<b>NEW! version 0.8 is now available to run as a Docker image (elik1001/coreos-kubernetes-generator)</b>
<br>To use the Docker image just run the below.
<br><i>Note: </i>Output for use will be saved in the configs directory. all settings selected doing run time, will be stored in a list of directory's like ssl, ssh keys, etc...
<pre>
docker run \
-e PYTHONUNBUFFERED=0 \
--env HTTP_PROXY=$http_proxy --env HTTPS_PROXY=$http_proxy --env NO_PROXY=$no_proxy \
--env http_proxy=$http_proxy --env https_proxy=$http_proxy --env no_proxy=$no_proxy \
-v $(pwd)/configs:/kub-generator/configs:rw,shared \
-v $(pwd)/keys:/kub-generator/keys:rw,shared \
-v $(pwd)/bin:/kub-generator/bin:rw,shared \
-v $(pwd)/ssl:/kub-generator/ssl:rw,shared \
-v $(pwd)/work:/kub-generator/work:rw,shared \
-v $(pwd)/tmp:/kub-generator/tmp:rw,shared \
--rm -it elik1001/coreos-kubernetes-generator:0.8.3
</pre>

<br>The script uses a wizard-like approach with a minimum set of questions. 
<br>The script then generates a workable CoreOS configuration file(s) in 3 formats.
<ol>
<li><b>YAML</b> The script uses the yaml file to generate the ignition file (.ign).</li>
<li><b>IGN</b> The ignition file is used by the CoreOS live CD to create / install the OS with all required configurations.</li>
<li><b>ISO</b> The script then creates / generates an ISO containing the ignition file, so you can just mount the ISO in the CoreOS live CD to install.</li>
</ol>
<br>

<i>Note: </i> Version (0.7+) will only work with Kubernetes version 1.13.x+

<br>You run the script for each Node Master or Worker.
<br>The first time you run the script it generates the SSH keys, SSL CA and SSL keys, you select / modify the options like dns, domain, proxy, etc..
<br>You re-run the script for each master or worker node, it will remember/keep all your previous settings.
<br>For each run/Node it will generated an output ignition configuration file in 3 formats (YAML, IGN, ISO) for you to use.

With this configuration you can hopefully run / configure a new Kubernetes in a matter of minutes.

<h3>Getting Started</h3>

<b>Please read the <a href="VERSION.md">change log</a> before you begin.</b>

<h4>Installation</h4>

<h5>Docker Image Usage</h5>
<br>To use the Docker image just run the below.
<br><i>Note: </i>Output for use will be saved in the configs directory. all settings selected doing run time, will be stored in a list of directory's like ssl, ssh keys, etc...
<pre>
docker run \
-e PYTHONUNBUFFERED=0 \
--env HTTP_PROXY=$http_proxy --env HTTPS_PROXY=$http_proxy --env NO_PROXY=$no_proxy \
--env http_proxy=$http_proxy --env https_proxy=$http_proxy --env no_proxy=$no_proxy \
-v $(pwd)/configs:/kub-generator/configs:rw,shared \
-v $(pwd)/keys:/kub-generator/keys:rw,shared \
-v $(pwd)/bin:/kub-generator/bin:rw,shared \
-v $(pwd)/ssl:/kub-generator/ssl:rw,shared \
-v $(pwd)/work:/kub-generator/work:rw,shared \
-v $(pwd)/tmp:/kub-generator/tmp:rw,shared \
--rm -it elik1001/coreos-kubernetes-generator:0.8.3
</pre>

<br>You can also build / create your own Docker image, by running the below.
<pre>
# Build image
docker build --no-cache \
-t coreos-kubernetes-generator:0.8.3 app

# If behind a proxy
docker build --no-cache --build-arg HTTP_PROXY=$http_proxy \
--build-arg HTTPS_PROXY=$http_proxy --build-arg NO_PROXY=$no_proxy \
--build-arg http_proxy=$http_proxy --build-arg https_proxy=$http_proxy \
--build-arg no_proxy=$no_proxy -t coreos-kubernetes-generator:0.8.3 app
</pre>

<h5>Standalone Github Application</h5>
<h5>Dependencies / Prerequisites</h5>
<b>The following libraries are required:</b>
<i>Note: </i>The script will (try to) download and install the required libraries (if needed).
<pre>
sys,
os,
pip,
re,   
ast,   
pwd,   
uuid,   
crypt,   
shutil,   
pprint,
getpass,   
requests,   
pycryptodome,
platform,
subprocess,   
inquirer,
from contextlib import contextmanager
Crypto.PublicKey.RSA
</pre>
<i>Note: </i>You can manually install libraries by running <i>pip install [library]</i>
<br>At the current time, <i>openssl</i> is required, as its used as part of the certificate creation.
<br>(this requirement will be removed once certificate creation is fully done in Python).


<h4>Usage examples</h4>
To use the application just run the <i>./generate_template.py</i>.

<b>Example</b>
You can leave most of the default values by just hitting enter - (Just replace the IP's, Hostnames if needed..).

<b>The default network settings are below</b>
<table class="blueTable" style="width: 50%;" border="2">
<thead>
<tr>
<th style="text-align: center;" colspan="2">Default cluster IP Address (everything can be overwritten/updated if liked)</th>
</tr>
</thead>
<tbody>
<tr>
<tr>
<td><b>&nbsp;Name</b></td>
<td><b>&nbsp;IP Addrss</b></td>
</tr>
<tr>
<td>&nbsp;coreos1</td>
<td>&nbsp;172.20.0.11/20</td>
</tr>
<tr>
<td>&nbsp;coreos2</td>
<td>&nbsp;172.20.0.12/20</td>
</tr>
<tr>
<td>&nbsp;coreos3</td>
<td>&nbsp;172.20.0.13/20</td>
</tr>
<tr>
<td>&nbsp;worker1</td>
<td>&nbsp;172.20.0.51/20</td>
</tr>
<tr>
<td>&nbsp;worker2</td>
<td>&nbsp;172.20.0.52/20</td>
</tr>
<tr>
<td>&nbsp;worker3</td>
<td>&nbsp;172.20.0.53/20</td>
</tr>
<tr>
<td>&nbsp;Default Gateway</td>
<td>&nbsp;172.20.0.1</td>
</tr>
</tbody>
<thead>
<tr>
<th style="text-align: center;" colspan="2">Cluster Network Ranges</th>
</tr>
</thead>
<tbody>
<tr>
<td><b>&nbsp;Name</b></td>
<td><b>&nbsp;Range</b></td>
</tr>
<tr>
<td>&nbsp;Pod CIDR</td>
<td>&nbsp;172.20.0.0/20</td>
</tr>
<tr>
<td>&nbsp;Cluster CIDR</td>
<td>&nbsp;10.20.0.0/21</td>
</tr>
</tbody>
<thead>
<tr>
<th style="text-align: center;" colspan="2">DNS Configuration</th>
</tr>
</thead>
<tbody>
<tr>
<td><b>&nbsp;Name</b></td>
<td><b>&nbsp;IP Address</b></td>
</tr>
<tr>
<td>&nbsp;Google DNS1</td>
<td>&nbsp;8.8.8.8</td>
</tr>
<tr>
<td>&nbsp;Google DNS2</td>
<td>&nbsp;8.8.4.4</td>
</tr>
<tr>
<td>&nbsp;Cluster DNS <br>(requires kube-dns)</td>
<td>&nbsp;10.3.0.10</td>
</tr>
<tr>
<td>&nbsp;Default Domain Name</td>
<td>&nbsp;example.com</td>
</tr>
</tbody>
</table>

<i>Tip: </i>Re-run the script for every Master, worker, etc.. each run will generate a new configuration file that you can use.
<pre>
./generate_template.py
[..] snip
[?] What kubernetes system type are you building ?: Master
 > Master
   Worker

[..] snip
Ignition Template created successfully.
-----------------------------------------------------------
  SSH private key is             : keys/id_rsa
  SSH public key is              : keys/id_rsa.pub
  SSL certificates are in        : ./ssl/
  Build Template file is         : configs/coreos1_template.yaml 
  Ignition Template file is      : configs/coreos1_template.ign 
  Ignition Template ISO file is  : configs/coreos1_template.iso
</pre>
<h4>Details</h4>
The script generates the below list of files and Directories.
<ol>
	<li><b>ssl: </b>Contains all SSL certificates used in the configuration including the CA certificate</li>
	<li><b>manifests: </b>Contains all the manifests used to generate the Ignition</li>
	<li><b>keys: </b>Contains the SSH Private and Public keys in the configuration</li>
	<li><b>configs: </b>Contains the final configuration files, like. Ignition (mastr[n].ign), ISO with Ignition data on it(master[n].iso) and the YAML config(master[n].yaml).</li>
	<li><b>tmp: </b>Contains all temporary configuration files.</li>
	<li><b>src: </b>Contains the default Kubernetes properties, these files get updated at run time, based on your selections set as the default properties(for the next run).</li>
	<li><b>template: </b>Contains all templates or ready sample templates used in the configuration.</li>
</ol>

<h4>Additional Details</h4>
You can use the ign (or ISO with ign file) in a verity of ways.
If you are using bear-metal or virtual box, an example is explained below.

First, configure VirtualBox Networking. for more details you can follow this <a href="docs/VirtualBox/README.md">document</a>.

Boot from a CoreOS ISO/CD/USB which already contains the <i>coreos-install</i> script or use any bootable CD, then download the CoreOS <i>coreos-install</i> script from <a href="https://raw.github.com/coreos/init/master/bin/coreos-install" rel="nofollow">here</a>.

Next, use the generated Ignition file, you can use the <i>IGN</i> file, or use the <i>ISO</i> which contains the <i>IGN</i> file, the process is the same (like the below).

Now, run the <i>coreos-install</i> with the below parameters.
<i>Note: </i>the <i>coreos-install</i> script comes pre-installed on CoreOS.
<pre>
mount /dev/[sr0] /media
coreos-install -d /dev/[sda] -C [stable|alpha] -i /media/master1_template.ign
</pre>
Replace <i>sr0</i> with your cdrom.
Replace <i>sda</i> with your disk.
Use alpha or stable channel.

Once completed just reboot the server (or virtual) and just login with the user/password you selected.
<i>Note: </i>If using VirtualBox you login by doing ssh user@localhost -p 2011

<br>For <i>RBAC</i> to work properly you will need to run the below one of the Master(s) once Kubernetes is fully up, you can verify with <i>kubectl get all --all-namepsaces -o wide</i>.

<br>Add/create the below role binding (this will address admin access errors)
<pre>
kubectl create clusterrolebinding cluster-admin-binding \
--clusterrole=cluster-admin \
--namespace=kube-system \
--user=admin
</pre>

<br> For the ERROR below, just run the below rolebinding.
<pre>
# ERROR
W1221 15:36:11.451721       1 authentication.go:262] Unable to get configmap/extension-apiserver-authentication in kube-system.  Usually fixed by 'kubectl create rolebinding -n kube-system ROLE_NAME --role=extension-apiserver-authentication-reader --serviceaccount=YOUR_NS:YOUR_SA'
configmaps "extension-apiserver-authentication" is forbidden: User "admin" cannot get resource "configmaps" in API group "" in the namespace "kube-system"

# Create rolebinding
kubectl create rolebinding -n kube-system extension-api-server-role --role=extension-apiserver-authentication-reader --serviceaccount=kube-system:admin
</pre>

Add the below to the <i>template/master_templ.txt</i> to automaticly download and create the kubectl file.
<pre>
    - path: /opt/bin/kubectl
      filesystem: root
      mode: 511 # 0555
      contents:
        remote:
          url: http://storage.googleapis.com/kubernetes-release/release/v1.13.1/bin/linux/amd64/kubectl
          verification:
            hash:
              function: sha512
              sum: d991aa36f239b4c5262077b9fa2eeb1c4931c01c5223748ed5167838b9886b8d53cfff36ebe1344db5e7c1962af90faa0902d9b0a73174c3defa1029b6a04841
</pre>
<i>Note: </i> If you are behind a proxy the above code might/will not work, so copy the kubectl to /opt/bin manually.

<h4>To Do's</h4>
<ol>
	<li>Complete Documentation</li>
	<li>Code Optimization</li>
	<li>Convert SSL subprocess to pure Python code.</li>
	<li>Convert configuration files (in src directory) to a DB layer.</li>
	<li>Add include matchbox, PXE, DHCP, as an option for full automation.</li>
	<li>Add a Web-UI interface to manipulate properties.</li>
</ol>
<h4>Known Issues/Troubleshooting</h4>

<h4>License</h4>
This project is licensed under the MIT License - see the LICENSE file for details
