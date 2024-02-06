---
title: Deployment options on Kubernetes
---
# Deployment options on Kubernetes

When you create a site on Kubernetes, there are many options you can use, for example, the number of pods for each component and the resource allocations for the associated pods.
This guide focusses on the following goals:

* [Scaling for increased traffic](#scaling-for-increased-traffic)
* [Creating a high availability site](#creating-a-high-availability-site)

## Scaling for increased traffic

For optimal network latency and throughput, you can adjust the CPU allocation for the router using the `router-cpu` option.
Adjusting other allocations does not affect network performance.

**📌 NOTE**\
Increasing the number of routers does not improve network performance.

1. Determine the router CPU allocation you require.

   By default, the router CPU allocation is `BestEffort` as described in [Pod Quality of Service Classes](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/#besteffort).

   Consider the following CPU allocation options:

   |     |     |
   | --- | --- |
   | Router CPU | Description |
   | 1 | Helps avoid issues with `BestEffort` on low resource clusters. |
   | 2 | Suitable for production environments. |
   | 5 | Maximum performance. |
2. If you are using the `skupper` CLI, set the CPU allocation for the router using the `--router-cpu` option, for example:

   ```bash
   $ skupper init --router-cpu 2
   ```
3. If you are using YAML, set the CPU allocation for the router by setting a value for `router-cpu`, for example:

   ```YAML
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: "skupper-site"
   data:
     name: "my-site"
     router-cpu: 2
   ```

## Creating a high availability site

By default, Kubernetes restarts any router that become unresponsive.
If you encounter router pod issues, consider [Scaling for increased traffic](#scaling-for-increased-traffic) before increasing the number of routers.

To address high availability concerns, increase the number of routers to 2 as follows:

1. If you are using the `skupper` CLI, set the number of routers to `2` using the `--routers` option:

   ```bash
   $ skupper init --routers 2
   ```
2. If you are using YAML, set the number of routers to `2` by setting the `routers` value:

   ```YAML
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: "skupper-site"
   data:
     name: "my-site"
     routers: 2
   ```

   Setting the number of routers to more than 2 adversely affects performance.
