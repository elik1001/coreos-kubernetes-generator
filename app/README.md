### Supported tags and respective Dockerfile links

*   latest
*   0.8.1
*   0.8.2

#### Reference

Documentation and usage references are available in my [GitHub Repository](https://github.com/elik1001/coreos-kubernetes-generator), Or in [my blog](https://www.devtech101.com). 

Full source code is also available in my [GitHub Repository](https://github.com/elik1001/coreos-kubernetes-generator).

#### What is CoreOS Kubernetes Generator?

This repository/image includes a Python Kubernetes Generator Ignition Script.

The script helps automate a Kubernetes deployment on CoreOS. See the deployment notes for additional details.

1.  The script helps automate a Kubernetes Multi-Master deployment on CoreOS.
2.  The script generates a CoreOS Ignition file that can be used, either as part of a 3 node Master cluster or just as a worker node.
3.  The generated Ignition file includes all required properties for, Etcd, Flannel(with CNI), Kubelet using (Rkt), etc.. all pr otocols are configured to use SSL.

#### How to use this image

To just use/run the image, run something like the below.

docker run 
-e PYTHONUNBUFFERED=0
-v $(pwd)/configs:/kub-generator/configs:rw,shared
-v $(pwd)/keys:/kub-generator/keys:rw,shared
-v $(pwd)/bin:/kub-generator/bin:rw,shared
-v $(pwd)/ssl:/kub-generator/ssl:rw,shared
-v $(pwd)/work:/kub-generator/work:rw,shared
-v $(pwd)/tmp:/kub-generator/tmp:rw,shared
--rm -it elik1001/coreos-kubernetes-generator:0.8.2

**Behind a proxy, use the below.**

docker run
-e PYTHONUNBUFFERED=0
--env HTTP_PROXY=$http_proxy
--env HTTPS_PROXY=$http_proxy
--env NO_PROXY=$no_proxy
--env http_proxy=$http_proxy
--env https_proxy=$http_proxy
--env no_proxy=$no_proxy
-v $(pwd)/configs:/kub-generator/configs:rw,shared
-v $(pwd)/keys:/kub-generator/keys:rw,shared
-v $(pwd)/bin:/kub-generator/bin:rw,shared
-v $(pwd)/ssl:/kub-generator/ssl:rw,shared
-v $(pwd)/work:/kub-generator/work:rw,shared
-v $(pwd)/tmp:/kub-generator/tmp:rw,shared
--rm -it elik1001/coreos-kubernetes-generator:0.8.2 

**Notes on stored directory:**

*   The _configs_ directory will store the generated ignition, iso and yaml files.
*   The _ssl_ directory will store your root and kubernetes certificates for future runs.
*   The _keys_ directory will store your ssh keys for future runs.
*   The _bin_ directory will store the ct and kubectl utilities.
*   The _work_ directory will store all your selections doing first run for future runs.

#### Building your own image

Just clone the [GitHub Repository](https://github.com/elik1001/coreos-kubernetes-generator).
 
git clone https://github.com/elik1001/coreos-kubernetes-generator 

Then to build the image, just run the below.

docker build --no-cache -t coreos-kubernetes-generator:0.8.2 app

**If behind a proxy**

docker build --no-cache 
--build-arg HTTP_PROXY=$http_proxy
--build-arg HTTPS_PROXY=$http_proxy
--build-arg NO_PROXY=$no_proxy
--build-arg http_proxy=$http_proxy
--build-arg https_proxy=$http_proxy
--build-arg no_proxy=$no_proxy
-t coreos-kubernetes-generator:0.8.2 app 

#### License

[MIT License - Full License Details is available here](https://github.com/elik1001/coreos-kubernetes-generator/blob/master/LICENSE).
