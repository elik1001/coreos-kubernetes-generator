<h1>Virtualbox Kubernetes Master / Worker Nodes Configuration</h1>

<p>To use Virtualbox for testing a Kubernetes Master / Worker Node setup, you must configure a network switch first.</p>

<p>Download a CoreOS ISO, install the OS with coreos-install using the generated ignition script.
<br>Once installation is completed, before you reboot, follow the instructions below to configure the network.</p>

<p>To create a new network switch, from the main Virtualbox GUI screen.
<br>Click on File > Preferences >  Network.
<br>Click on the right button <i>Add  new NAT network</i>
<br>Something like the screen shut below.</p>

<p>Then name the switch, in this case I used <i>CoreOS-SW1</i>, this name will be used latter on each VM.
<br>Set the network CIDR, in this case I used <i>172.20.0.0/20</i>.</p>

<p><b>Something like the screen shut below, Set Network Name and Network Range.</b>
<br><img src="vbox-setup1.png" alt="VBox Part1" align="middle" height="50%"></p>

<p>Next, click on <i>Port Forwarding</i>, then click on the green + <i>Add new port forwarding rule</i>.
<br>Create 6 rules, for each master / worker node.</p>
<p><b>Something like the screen shut below, Set port forwarding rules.</b> 
<br><img src="vbox-setup2.png" alt="VBox Part2" align="middle" height="50%"></p> 

<p>Now you <i>NAT Network</i> is all set.</p>

<b>Note: </b>When setting up a new VM, make sure to set 1500/Mb+ Memory(the default is only 1024/Mb), to prevent the Boot stuck at "Starting Switch Root".
<br>
<p>Next lets move to the VM configuration.
<br>Click on your VM > Settings > Network.
<br>Under <i>Attach to:</i> Select <i>NAT Network</i>
<br>Under <i>Name:</i> Select <i>CoreOS-SW1</i> (or the name used for your switch).</p>
<p><b>Something like the screen shut below, Set VM Vm Switch.</b> 
<br><img src="vbox-setup3.png" alt="VBox Part3" align="middle" height="50%"></p>
<p>Click ok to save changes.
<br>Next, Reboot the node.
<p>To connect to a master / worker, the below should work.
<br>For example: Master1 if configured port forward was configured to port 2011.
<br>ssh -p 2011 your_user@localhost</p>
