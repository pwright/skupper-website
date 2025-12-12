---
title: Examples
extra_headers: <link rel="stylesheet" href="index.css" type="text/css" async="async"/><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0"/>
---

# Skupper examples

These examples provide step-by-step instructions to install and use
Skupper for common multi-cluster and edge deployment scenarios.

<h2 id="featured-applications">Featured applications</h2>

<p>Skupper works with your existing application code, no changes
required.  These examples highlight Skupper's ability to deploy
conventional applications across multiple sites.
</p>

<div class="examples">

<div>
<h3><a href="https://github.com/skupperproject/skupper-example-hello-world/tree/v1">Hello World</a></h3>
<p>A minimal multi-service HTTP application deployed across sites using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-hello-world/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-patient-portal/tree/v1">Patient Portal</a></h3>
<p>A database-backed web application deployed across sites using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-patient-portal/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-trade-zoo/tree/v1">Trade Zoo</a></h3>
<p>A Kafka-based trading application deployed across sites using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-trade-zoo/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-bookinfo/tree/v1">Bookinfo</a></h3>
<p>Deploy the Istio Bookinfo application across sites using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-bookinfo/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
<a href="https://www.youtube.com/watch?v=H80GLl-KdTc"><span class="fab fa-youtube fa-lg"></span> Video</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-grpc/tree/v1">Online Boutique</a></h3>
<p>Deploy the gRPC-based Online Boutique application across sites using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-grpc/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-http-load-balancing/tree/v1">HTTP load balancing</a></h3>
<p>Use Skupper to balance HTTP requests across sites</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-http-load-balancing/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
<a href="https://www.youtube.com/watch?v=4GmXT3nj8lc"><span class="fab fa-youtube fa-lg"></span> Video</a>
</nav>
</div>
</div>

<h2 id="connectivity-scenarios">Connectivity scenarios</h2>

<p>Skupper helps you overcome tough networking obstacles.  See how
you can securely connect services in sites behind firewalls or
NAT without changing your existing networking.
</p>

<div class="examples">

<div>
<h3><a href="https://github.com/skupperproject/skupper-example-public-to-private/tree/v1">Public to private</a></h3>
<p><div style="padding-bottom: 0.8em;">
  <span class="material-symbols-outlined">cloud</span>
  <span class="material-symbols-outlined">horizontal_rule</span>
  <span class="material-symbols-outlined">business</span>
</div>
Connect from the cloud to services running on-prem
</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-public-to-private/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-private-to-private/tree/v1">Private to private</a></h3>
<p><div style="padding-bottom: 0.8em;">
  <span class="material-symbols-outlined">business</span>
  <span class="material-symbols-outlined">horizontal_rule</span>
  <span class="material-symbols-outlined">cloud</span>
  <span class="material-symbols-outlined">horizontal_rule</span>
  <span class="material-symbols-outlined">business</span>
</div>
Connect services in isolated on-prem sites
</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-private-to-private/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-dmz/tree/v1">DMZ</a></h3>
<p><div style="padding-bottom: 0.8em;">
  <span class="material-symbols-outlined">cloud</span>
  <span class="material-symbols-outlined">horizontal_rule</span>
  <span class="material-symbols-outlined">shield</span>
  <span class="material-symbols-outlined">horizontal_rule</span>
  <span class="material-symbols-outlined">business</span>
</div>
Connect services separated by firewalls and a DMZ
</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-dmz/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
</div>

<h2 id="platforms">Platforms</h2>

<p>Skupper works with services running as pods on Kubernetes, as
containers, or as ordinary processes on bare metal hosts or VMs.
</p>

<div class="examples">

<div>
<h3><a href="https://github.com/skupperproject/skupper-example-hello-world/tree/v1">Kubernetes</a></h3>
<p>Connect services running as pods in Kubernetes
</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-hello-world/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-podman/tree/v1">Podman</a></h3>
<p>Connect services running as containers
</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-podman/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-gateway/tree/v1">Bare metal or VM</a></h3>
<p>Connect services running as system processes</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-gateway/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
</div>

<h2 id="interfaces">Interfaces</h2>

<p>Skupper provides a command-line interface for interactive
control and a YAML interface for declarative configuration.  The
Skupper web console helps you observe your application network.
</p>

<div class="examples">

<div>
<h3><a href="https://github.com/skupperproject/skupper-example-hello-world/tree/v1">Command line</a></h3>
<p>Hello World deployed across sites using the Skupper CLI
</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-hello-world/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-yaml/tree/v1">YAML</a></h3>
<p>Hello World deployed across sites using Skupper YAML</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-yaml/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-console/tree/v1">Web console</a></h3>
<p>Explore an application network using the Skupper web console</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-console/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
</div>

<h2 id="administration">Administration</h2>

<p>Skupper gives administrators tools to manage Skupper networks in
large organizations.
</p>

<div class="examples">

<div>
<h3><a href="https://github.com/skupperproject/skupper-example-policy/tree/v1">Policy</a></h3>
<p>Use Skupper cluster policy to restrict site linking and service exposure</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-policy/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-ansible/tree/v1">Ansible</a></h3>
<p>Use Skupper Ansible to automate network deployment</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-ansible/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
</div>

<h2 id="database-examples">Database examples</h2>

<p>With Skupper you can locate your data wherever you need it to
be, while accessing it from wherever your services are running.
</p>

<div class="examples">

<div>
<h3><a href="https://github.com/skupperproject/skupper-example-mongodb-replica-set/tree/v1">MongoDB</a></h3>
<p>Deploy a MongoDB replica set across sites using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-mongodb-replica-set/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-mysql/tree/v1">MySQL</a></h3>
<p>Access a MySQL database in a private data center from the public cloud</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-mysql/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-postgresql/tree/v1">PostgreSQL</a></h3>
<p>Access a PostgreSQL database in a private data center from the public cloud</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-postgresql/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
<a href="https://www.youtube.com/watch?v=Oa0aVpb0v7U"><span class="fab fa-youtube fa-lg"></span> Video</a>
</nav>
</div>
</div>

<h2 id="messaging-examples">Messaging examples</h2>

<p>Skupper helps you access message queues and connect event-driven
applications spread across isolated network locations.
</p>

<div class="examples">

<div>
<h3><a href="https://github.com/skupperproject/skupper-example-activemq/tree/v1">ActiveMQ</a></h3>
<p>Access an ActiveMQ message broker using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-activemq/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-kafka/tree/v1">Kafka</a></h3>
<p>Access a Kafka cluster using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-kafka/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
<a href="https://www.youtube.com/watch?v=W7aUOgCTyOg"><span class="fab fa-youtube fa-lg"></span> Video</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-rabbitmq/tree/v1">RabbitMQ</a></h3>
<p>Access a RabbitMQ message broker using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-rabbitmq/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
</div>

<h2 id="protocol-examples">Protocol examples</h2>

<p>Skupper supports any TCP-based protocol.  These examples show
how you can access services based on widely used internet
protocols.
</p>

<div class="examples">

<div>
<h3><a href="https://github.com/skupperproject/skupper-example-tcp/tree/v1">TCP</a></h3>
<p>Access a TCP server using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-tcp/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
<a href="https://www.youtube.com/watch?v=ZQo9cB0-1go"><span class="fab fa-youtube fa-lg"></span> Video</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-http/tree/v1">HTTP</a></h3>
<p>Access an HTTP server using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-http/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-ftp/tree/v1">FTP</a></h3>
<p>Access an FTP server using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-ftp/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
</div>

<h2 id="more-examples">More examples</h2>

<div class="examples">

<div>
<h3><a href="https://github.com/skupperproject/skupper-example-camel-integration/tree/v1">Camel</a></h3>
<p>Using Skupper to access private on-prem data from Camel</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-camel-integration/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-iperf/tree/v1">iPerf</a></h3>
<p>Perform real-time network throughput measurements using iPerf3</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-iperf/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-prometheus/tree/v1">Prometheus</a></h3>
<p>Gather Prometheus metrics from endpoints deployed across multiple clusters</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-prometheus/tree/v1"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
</div>

