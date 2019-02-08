:
# Build image
docker build --no-cache \
-t elik1001/coreos-kubernetes-generator:0.8.5 app

# If behind a proxy
# docker build --no-cache --build-arg HTTP_PROXY=$http_proxy \
# --build-arg HTTPS_PROXY=$http_proxy --build-arg NO_PROXY=$no_proxy \
# --build-arg http_proxy=$http_proxy --build-arg https_proxy=$http_proxy \
# --build-arg no_proxy=$no_proxy -t elik1001/coreos-kubernetes-generator:0.8.5 app
