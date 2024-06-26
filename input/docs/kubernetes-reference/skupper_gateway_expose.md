---
title: skupper gateway expose
---
### skupper gateway expose

Expose a process to the service network (ensure gateway and cluster service)

#### Synopsis

Expose a process to the service network (ensure gateway and cluster service)

```
skupper gateway expose <address> <host> <port...> [flags]
```

#### Options

```
      --aggregate string   The aggregation strategy to use. One of 'json' or 'multipart'. If specified requests to this service will be sent to all registered implementations and the responses aggregated.
      --event-channel      If specified, this service will be a channel for multicast events.
  -h, --help               help for expose
      --protocol string    The protocol to gateway (tcp, http or http2). (default "tcp")
      --type string        The gateway type one of: 'service', 'docker', 'podman' (default "service")
```

#### Options inherited from parent commands

```
  -c, --context string      The kubeconfig context to use
      --kubeconfig string   Path to the kubeconfig file to use
  -n, --namespace string    The Kubernetes namespace to use
      --platform string     The platform type to use [kubernetes, podman]
```

#### SEE ALSO

* [skupper gateway](skupper_gateway.html)	 - Manage skupper gateway definitions

<!-- ###### Auto generated by spf13/cobra on 29-May-2024
 -->