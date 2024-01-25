---
title: Using Skupper podman
---
# Using Skupper podman

Skupper podman allows you to create a site using containers, without requiring Kubernetes.
Typically, you create a site on a Linux host, allowing you to link to and from other sites, regardless of whether those sites are running in podman or Kubernetes.

**📌 NOTE**\
This is a preview feature and may change before becoming fully supported by [skupper.io](https://skupper.io).

## About Skupper podman

Skupper podman is available with the following precedence:

* **`skupper --platform podman <command>`**\
Use this option to avoid changing mode, for example, if you are working on Kubernetes and podman simultaneously.
* **`export SKUPPER_PLATFORM=podman`**\
Use this command to use Skupper podman for the current session, for example, if you have two terminals set to different contexts. To set the environment to target Kubernetes sites:

  ```bash
  $ export SKUPPER_PLATFORM=kubernetes
  ```
* **`skupper switch podman`**\
If you enter this command, all subsequent command target podman rather than Kubernetes for all terminal sessions.

To determine which mode is currently active:
```bash
$ skupper switch

podman
```

To switch back to target Kubernetes sites: `skupper switch kubernetes`

## Creating a site using Skupper podman

* The latest `skupper` CLI is installed.
* Podman is installed, see https://podman.io/

  By default, Podman v4 uses Netavark which works with Skupper.
  If you are using CNI, for example, if you upgrade from Podman v3, you must also install the `podman-plugins` package.
  For example, `dnf install podman-plugins` for RPM based distributions.

  **📌 NOTE**\
  CNI will be deprecated in the future in preference of Netavark.
* Podman service endpoint.

  Use `systemctl status podman.socket` to make sure the Podman API Socket is running.

  Use `systemctl --user enable --now podman.socket` to start the  Podman API Socket.

  See [Podman socket activation](https://github.com/containers/podman/blob/main/docs/tutorials/socket_activation.md) for information about enabling this endpoint.
  1. Set your session to use Skupper podman:

     ```bash
     $ export SKUPPER_PLATFORM=podman
     ```

     To verify the `skupper` mode:

     ```bash
     $ skupper switch

     podman
     ```
  2. Create a Skupper site:

     The simplest Skupper site allows you to link to other sites, but does not support linking _to_ the current site.

     ```bash
     $ skupper init --ingress none

     It is recommended to enable lingering for <username>, otherwise Skupper may not start on boot.
     Skupper is now installed for user '<username>'.  Use 'skupper status' to get more information.
     ```

     If you require that other sites can link to the site you are creating:

     ```bash
     $ skupper init --ingress-host <machine-address>

     It is recommended to enable lingering for <username>, otherwise Skupper may not start on boot.
     Skupper is now installed for user '<username>'.  Use 'skupper status' to get more information.
     ```

     For more information, see the [Skupper Podman CLI reference](../podman-reference/skupper.html) documentation.
  3. Check the status of your site:

     ```bash
     $ skupper status
     Skupper is enabled for "<username>" with site name "<machine-name>-<username>" in interior mode. It is not connected to any other sites. It has no exposed services.
     ```

     **📌 NOTE**\
     You can only create one site per user. If you require a host to support many sites, create a user for each site.

## Linking sites using Skupper podman

The general flow for linking podman sites is the same as for Kubernetes sites:

1. Generate a token on one site:

   ```bash
   $ skupper token create <filename>
   ```
2. Create a link from the other site:

   ```bash
   $ skupper link create <filename>
   ```

After you have linked to a network, you can check the link status:
```bash
$ skupper link status
```

## Working with services using Skupper podman

The general flow for working with services is the same for Kubernetes and Podman sites.

**📌 NOTE**\
Services exposed on Kubernetes are not automatically available to Podman sites.
This is the equivalent to Kubernetes sites created using `skupper init --enable-service-sync false`.

In this variation of the [hello world](https://github.com/skupperproject/skupper-example-hello-world) example, the `backend` service is exposed on Kubernetes site and a Podman site is linked.
You deploy the `frontend` as a container and that container can access the `backend` service.

1. Create a Podman site and link it to a Kubernetes site.
2. Check the service from the Podman site:

   ```bash
   $ skupper service status

   No services defined
   ```

   This result is expected because services exposed on Kubernetes are not automatically available to Podman sites.
3. Create a service on the Podman site matching the service exposed on the Kubernetes site:

   ```bash
   $ skupper service create backend 8080
   ```
4. Validate the service from the Podman site by checking the backend API health URL:

   ```bash
   $ podman run -it --rm --network=skupper --name=myubi ubi8/ubi curl backend:8080/api/health

   OK
   ```

   This command runs a container using the `skupper` network and returns the results from `http://backend:8080/api/health`
5. Run the frontend as a container:

   ```bash
   $ podman run -dp 8080:8080 --name hello-world-frontend --network skupper quay.io/skupper/hello-world-frontend
   ```
6. Check your service network is working as expected by navigating to http://localhost:8080 and click **Say hello**.

   Each of the backend replicas respond, for example `Hi, Perfect Parrot. I am Kind Hearted Component (backend-7c84887f9f-wxhxp).`

   <dl><dt><strong>📌 NOTE</strong></dt><dd>

   In this scenario, running the `skupper service status` command on the Podman site does not provide much detail about the service:

   ```bash
   $ skupper service status
   Services exposed through Skupper:
   ╰─ backend (tcp port 8080)
   ```

   </dd></dl>

In this variation of the [hello world](https://github.com/skupperproject/skupper-example-hello-world) example, the `backend` service is exposed on Podman site and consumed from a `frontend` on a Kubernetes site.

1. Create a Podman site and link it to a Kubernetes site.
2. Create and expose a frontend deployment on the Kubernetes site:

   ```bash
   $ kubectl create deployment frontend --image quay.io/skupper/hello-world-frontend
   $ kubectl expose deployment/frontend --port 8080 --type LoadBalancer
   ```
3. Run the backend as a container:

   ```bash
   $ podman run -d --name hello-world-backend --network skupper quay.io/skupper/hello-world-backend
   ```
4. Expose the `backend` from the Podman site.

   ```bash
   $ skupper expose host hello-world-backend --address backend --port 8080
   ```
5. From the Kubernetes site, create the `backend` service:

   ```bash
   $ skupper service create backend 8080
   ```
6. Check your service network is working as expected by navigating to your cluster URL, port 8080, and clicking **Say hello**.

For more information, see the [Skupper Podman CLI reference](../podman-reference/skupper.html) documentation.
