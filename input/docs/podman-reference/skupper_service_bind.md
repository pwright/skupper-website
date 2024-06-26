---
title: skupper service bind
---
### skupper service bind

Bind a target to a service

#### Synopsis

Bind a target to a service

```
skupper service bind <service-name> <target-type> <target-name> [flags]
```

#### Options

```
  -h, --help                  help for bind
      --target-port strings   The port the target is listening on (you can also use colon to map source-port to a target-port).
      --tls-trust string      K8s secret name with the CA to expose the service over TLS
```

#### Options inherited from parent commands

```
      --platform string   The platform type to use [kubernetes, podman]
```

#### SEE ALSO

* [skupper service](skupper_service.html)	 - Manage skupper service definitions

<!-- ###### Auto generated by spf13/cobra on 29-May-2024
 -->