# coreos-kubernetes-generator
This document provides instructions on how to install and use the Python Kubernetes Generator Script. the script helps  automate a Kubernetes deployment on CoreOS. See the deployment notes for additional details.

This repository includes the Python Kubernetes Generator Script, as well as pre configured samples.
<ol>
	<li>The script helps automate a Kubernetes Multi-Master deployment on CoreOS.</li>
	<li>The script generates a CoreOS Ignition file that can be used, either as part of a 3 node Master cluster or just as a worker node.</li>
	<li>The generated Ignition file includes all required properties for, Etcd, Flannel(with CNI), Kubelet using (Rkt), etc.. all protocols are configured to use SSL.</li>
</ol>

The script uses a wizard-like approach with a minimum set of questions, just to be able to generate a configuration.

<h3>Getting Started</h3>

<h4>Installation</h4>
<h4>Dependencies / Prerequisites</h4>
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
subprocess,   
inquirer,
from contextlib import contextmanager
Crypto.PublicKey.RSA
</pre>
<i>Note: </i>You can manually install libraries by running <i>pip install [library]</i>

<h4>Usage examples</h4>
To use the application just run the <i>./generate_template.py</i>.

<b>Example</b>
You can leave most of the default values by just hitting enter - (Just replace the IP's, Hostnames if needed..).

<b>The default Hostname and IP Adress are below</b>
<table class="blueTable" style="width: 50%;" border="2">
<thead>
<tr>
<th style="text-align: center;" colspan="2">CoreOS Cluster IP Address</th>
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
<td>&nbsp;10.0.2.11/20</td>
</tr>
<tr>
<td>&nbsp;coreos2</td>
<td>&nbsp;10.0.2.12/20</td>
</tr>
<tr>
<td>&nbsp;coreos3</td>
<td>&nbsp;10.0.2.13/20</td>
</tr>
<tr>
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

Boot from a CoreOS ISO/CD/USB which already contains the <i>coreos-install</i> script or use any bootable CD, then download the CoreOS <i>coreos-install</i> script from <a href="https://raw.github.com/coreos/init/master/bin/coreos-install" rel="nofollow">here</a>.

Next, use the generated Ignition file, you can use the <i>IGN</i> file, or use the <i>ISO</i> which contains the <i>IGN</i> file, the process is the same (like the below).

Now, run the <i>coreos-install</i> with the below parameters.
<i>Note: </i>the <i>coreos-install</i> script comes pre-installed on CoreOS.
<pre>
coreos-install -d /dev/[sda] -C [stable|alpha] -i master1_template.ign
</pre>
Replace <i>sda</i> with your disk.
Use alpha or stable channel.

Once completed just reboot the server (or virtual) and you should be good to go.
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
