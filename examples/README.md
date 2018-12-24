<h1>Example Files</h1>

<p>The pre-generated sample files in this directory are ready to be used in a 3 master / 3 worker node configuration.</p>
<p><b>User: </b> usera</p>.
<p><b>User: </b> Admin_Password</p>.
<b>The Hostname / IP scheme are below</b>.
<table class="blueTable" style="width: 50%;" border="2">
<thead>
<tr>
<th style="text-align: center;" colspan="2">Cluster IP Address</th>
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
