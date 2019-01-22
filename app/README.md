<h3>Supported tags and respective Dockerfile links</h3>
<ul>
    <li>0.8.2</li>   
<ul>

<h4>Reference<h4>
Documentation and usage references are available <a href="https://www.devtech101.com/>on my blog</a>, Or in a my <a href="https://github.com/elik1001/coreos-kubernetes-generator">GitHub Repository</a>.

Full source code is also available in my <a href="https://github.com/elik1001/coreos-kubernetes-generator">GitHub Repository</a>.

<h4>What is CoreOS Kubernetes Generator?<h4>

This repository/image includes a Python Kubernetes Generator Ignition Script.

The script helps  automate a Kubernetes deployment on CoreOS. See the deployment notes for additional details.
<ol>
        <li>The script helps automate a Kubernetes Multi-Master deployment on CoreOS.</li>
        <li>The script generates a CoreOS Ignition file that can be used, either as part of a 3 node Master cluster or just as a worker
node.</li>
        <li>The generated Ignition file includes all required properties for, Etcd, Flannel(with CNI), Kubelet using (Rkt), etc.. all pr
otocols are configured to use SSL.</li>
</ol>

<h4>How to use this image<h4>

To just use/run the image, run something like the below.
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
--rm -it coreos-kubernetes-generator:0.8.2
</pre>

<b>Notes: </b>
The <i>configs</i> will store the generated ignition, iso and yaml files.
The <i>ssl</i> will store your root and kubernetes certificates for future runs.
The <i>keys</i> will store your ssh keys for future runs.
The <i>bin</i> will store the ct and kubectl utilities.
The <i>work</i> will store all your selections doing first run for future runs.

<h4>Building your own image</h4>
Just clone the <a href="https://github.com/elik1001/coreos-kubernetes-generator">GitHub Repository</a>.
<pre>
git clone https://github.com/elik1001/coreos-kubernetes-generator
</pre>
Then to build the image, just run the below.
<pre>
# Build image
docker build --no-cache \
-t coreos-kubernetes-generator:0.8.2 app

# If behind a proxy
docker build --no-cache --build-arg HTTP_PROXY=$http_proxy \
--build-arg HTTPS_PROXY=$http_proxy --build-arg NO_PROXY=$no_proxy \
--build-arg http_proxy=$http_proxy --build-arg https_proxy=$http_proxy \
--build-arg no_proxy=$no_proxy -t coreos-kubernetes-generator:0.8.2 app
</pre>

<h4>License<h4>
<a href="https://github.com/elik1001/coreos-kubernetes-generator/blob/master/LICENSE">MIT License - Full License Details is available here</a>.
