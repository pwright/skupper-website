---
title: skupper unexpose
---
### skupper unexpose

Unexpose one or more network services

#### Synopsis

Unexpose one or more network services

```
skupper unexpose [host <hostname|ip>] [flags]
```

#### Examples

```

        # unexposing a service running on the local machine
        skupper unexpose host host.containers.internal --address my-service

        # unexposing a local network IP
        skupper unexpose host 10.0.0.1 --address my-service

        # unexposing a podman container connected to the same podman network
        skupper unexpose host my-container --address my-service
```

#### Options

```
      --address string   Skupper address the target was exposed as
  -h, --help             help for unexpose
```

#### Options inherited from parent commands

```
      --platform string   The platform type to use [kubernetes, podman]
```

#### SEE ALSO

* [skupper](index.html) 

<!-- ###### Auto generated by spf13/cobra on 29-May-2024
 -->