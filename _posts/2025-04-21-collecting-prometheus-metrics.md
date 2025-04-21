---
title: "Collecting Prometheus Metrics Across Docker Services While Maintaining Network Separation"
date: 2025-04-21
---

## Problem Description

In a Docker environment, we have multiple services running in separate networks.
However, we want to collect metrics from these services using a single Prometheus container, without exposing services to each other.
We can't / don't want to modify the services to expose their metrics to the Prometheus network (e.g. a push gateway, firewall rules, etc.).

Suppose we have a docker compose:

```yaml
services:
  my_app:
    image: my_app
    ports: "80:8080"
```

Now, if you want to collect metrics from this app using Prometheus, you can do so by adding a new service to the same compose file:

```yaml
services:
  my_app:
    image: my_app
    ports: "80:8080"
  prom:
    image: prometheus
    ports: "9090:9090"
```

This is fine, and we can access the app and Prometheus on their respective ports, but it doesn't scale easily to many apps - we would end up with a prometheus instance for each app.
If we want to have a _single_ instance of Prometheus, a naive solution would be to have a single network for all the apps and Prometheus.
But this is not a good idea, as it would expose all the apps to each other.

## A Solution

One solution to this problem is to add a reverse proxy configuration to each service, which exposes _just_ the metrics endpoint to the Prometheus network.

### compose-prometheus.yml

```yaml
services:
  prom:
    image: prometheus
    ports: "9090:9090"
    networks:
      - prometheus
networks:
  prometheus:
    name: prometheus
```

### compose-my_app.yml

```yaml
# compose-my_app.yml
services:
  my_app:
    image: my_app
    ports: "80:8080"
    networks:
     - internal

  prom_nginx:
    image: nginx:alpine
    hostname: my_app_metrics
    container_name: my_app_metrics
    networks:
      - internal
      - prometheus
    restart: always
    configs:
      - source: prom_nginx_config
        target: /etc/nginx/nginx.conf

configs:
  prom_nginx_config:
    content: |
      worker_processes 1;
      events {
        worker_connections 1024;
      }
      http {
        server {
          listen 80;
          location /metrics {
            proxy_pass http://my_app:8081/metrics;
          }
          location / {
            return 403;
          }
        }
      }

networks:
  internal:
    name: my_app_internal
  prometheus:
    external: true
```

Here, we introduce a new service, `prom_nginx`, which is a reverse proxy for the metrics endpoint of `my_app`.
In this scenario, `my_app` exposes metrics on port 8081, and the main application on 8080.
As such, the metrics are only exposed to the Prometheus network and not to the end users of the app.
Moreover, Prometheus has access only to the metrics endpoint, and not to the main application.
Nginx is a bridge between the two networks, exposing just that metrics endpoint (and nothing else).
This can easily scale to many applications, each with their own Nginx bridge.

The Nginx container is configured using the `configs` directive, which avoids the need to create and mount an Nginx config file for each service's compose file - the nginx container and config block can be copy-pasted for each service, with minor edits.

### prometheus.yml

The prometheus config will look like:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'my_app'
    static_configs:
      - targets: ['my_app_metrics:80']
  - job_name: 'my_app2'
    static_configs:
      - targets: ['my_app2_metrics:80']
```
