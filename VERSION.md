<h1>Version history</h1>
<h2>Version 0.5</h2>
<b>Update/Fix: Python 3.x compatibility</b>
<ul>
    <li>
        <b>update: </b>
        <br>Updated the script to work with Python 3.x.
        <br><b>Note: </b>The old script is still available and was renamed to <i>generate_template-python_2_only.py</i>.
    </li>
</ul>

<h2>Version 0.2</h2>
<ul>
    <li>
        <b>add: </b>
        <br>Add Virtualbox example documentation.
    </li>
    <li>
        <b>add: </b>
        <br>Add DNS pod sample files.
    </li>
    <li>
        <b>update: </b>
        <br>Updated IP schema due to issues with Host to Pod overlapping.
    </li>
    <li>
        <b>bug: </b><a href="https://github.com/elik1001/coreos-kubernetes-generator/issues/3">resulting ignition file contains references to a http_proxy server that doesn't exist</a>
        <br> Set default to no <i>http_proxy</i>, provide option to set an <i>http_proxy</i>.
    </li>
    <li>
        <b>bug: </b> <a href="https://github.com/elik1001/coreos-kubernetes-generator/issues/1">generate_template.py can't determine what version of Crypto.PublicKey.RSA to install</a>
        <br> Verify / install <i>pycrypto</i> module.
    </li>
    <li>
        <b>bug: </b> <a href="https://github.com/elik1001/coreos-kubernetes-generator/issues/2">generate_template.py doesn't create iso file </a>
        <br> Verify if <i>mkisofs</i> is installed, try to install if not, notify user of issue.
    </li>
    <li>
        <b>bug: </b>
        <br>Function overwrites wrong dictionary data (line 618 mod_global_set).
    </li>
    <li>
        <b>enhancement: </b><a href="https://github.com/elik1001/coreos-kubernetes-generator/issues/4">resulting ignition file doesn't install kubectl  </a>
        <br> Download kubectl, provide instructions how to use (manuell copy after install is still required till matchbox integration).
    </li>
    <li>
        <b>enhancement: </b>
        <br>Various minor changes to enhance security and usability issues.
    </li>
</ul>

<h2>Version 0.1</h2>
<b>Initial(beta) release</b>
<ul>
    <li>
        The script helps automate a Kubernetes Multi-Master deployment on CoreOS.
    </li>
    <li>
        The script generates a CoreOS Ignition file that can be used, either as part of a 3 node Master cluster or just as a worker node.
    </li>
    <li>
        The generated Ignition file includes all required properties for, Etcd, Flannel(with CNI), Kubelet using (Rkt), etc.. all protocols are configured to use SSL.
    </li>
</ul>
