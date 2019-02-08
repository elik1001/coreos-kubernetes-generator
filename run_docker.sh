:
# Run Docker image
docker run \
-e PYTHONUNBUFFERED=0 \
-v $(pwd)/configs:/kub-generator/configs:rw,shared \
-v $(pwd)/keys:/kub-generator/keys:rw,shared \
-v $(pwd)/bin:/kub-generator/bin:rw,shared \
-v $(pwd)/ssl:/kub-generator/ssl:rw,shared \
-v $(pwd)/work:/kub-generator/work:rw,shared \
-v $(pwd)/tmp:/kub-generator/tmp:rw,shared \
--rm -it elik1001/coreos-kubernetes-generator:0.8.5

# Behind a proxy, use the below.
docker run \
-e PYTHONUNBUFFERED=0 \
--env HTTP_PROXY=$http_proxy \
--env HTTPS_PROXY=$http_proxy \
--env NO_PROXY=$no_proxy \
--env http_proxy=$http_proxy \
--env https_proxy=$http_proxy \
--env no_proxy=$no_proxy \
-v $(pwd)/configs:/kub-generator/configs:rw,shared \
-v $(pwd)/keys:/kub-generator/keys:rw,shared \
-v $(pwd)/bin:/kub-generator/bin:rw,shared \
-v $(pwd)/ssl:/kub-generator/ssl:rw,shared \
-v $(pwd)/work:/kub-generator/work:rw,shared \
-v $(pwd)/tmp:/kub-generator/tmp:rw,shared \
--rm -it elik1001/coreos-kubernetes-generator:0.8.5
