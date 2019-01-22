<h1>Version history</h1>


<h2>Version 0.8</h2>
<b>NEW! version 0.8 is now available to run as a Docker image (elik1001/coreos-kubernetes-generator).</b>
<ul>
    <li>
        <b>NEW: </b>
        <br>The Kubernetes Ignition Generator is now available as a Docker image in the official Docker Hub.
        <br><i>Note: </i>Using a Docker image simplifies eliminate most requirements such as the need to install Python modules, etc...
        <br>To use the Docker image just pull the Image with <i>docker pull elik1001/coreos-kubernetes-generator</i>.
        <br>You can also run the Docker image directly which will pull / run the image.
    </li>
    <li>
        <b>Update: </b>
        <br>The script was enhanced to preserve user login / password for next use.
    </li>
</ul>

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
--rm -it kube-generate:0.8
</pre>

<h2>Version 0.7</h2>
<b>Version 0.7 works with kubernetes 1.13.1+</b>
<ul>
    <li>
        <b>NEW: </b>
        <br>Updated the script to work with kubernetes 1.13.1.
        <br><b>Note: </b>The current updated version will most likely not work with older kubernetes versions. i.e. pre 1.13.x versions.
    </li>
    <li>
        <b>Added: </b>
        <br>This version automatically configures role based access(RBAC).
    </li>
    <li>
        <b>Added: </b>
        <br>Automatic Node bootstrapping - includes auto SSL signing with tokens.
    </li>
    <li>
        <b>Update: </b>
        <br>Updated <b>Flannel</b> from verion <i>0.9.0</i> to version <i>0.10.0</i>.
    </li>
    <li>
        <b>Update: </b>
        <br>Updated <b>etcd</b> from version <i>3.2.17</i> to version <i>3.2.9</i>.
    </li>
    <li>
        <b>Tested: </b>
        <br>This version was tested with CoreOS stable version <i>1911.5.0</i> and Alpha version <i>1995.0.0</i>.
    </li>
</ul>

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
