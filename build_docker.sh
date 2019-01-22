:
# Build image
docker build --no-cache \
-t kube-generate:0.8.2 app

# If behind a proxy
# docker build --no-cache --build-arg HTTP_PROXY=$http_proxy \
# --build-arg HTTPS_PROXY=$http_proxy --build-arg NO_PROXY=$no_proxy \
# --build-arg http_proxy=$http_proxy --build-arg https_proxy=$http_proxy \
# --build-arg no_proxy=$no_proxy -t kube-generate:0.8.2 app
