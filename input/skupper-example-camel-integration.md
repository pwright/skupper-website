# Skupper Camel Integration Example

#### Twitter, Telegram and PostgreSQL integration routes deployed across Kubernetes clusters using Skupper

This example is part of a [suite of examples][examples] showing the
different ways you can use [Skupper][website] to connect services
across cloud providers, data centers, and edge sites.

[website]: https://skupper.io/
[examples]: https://skupper.io/examples/index.html

#### Contents

* [Overview](#overview)
* [Prerequisites](#prerequisites)
* [Step 1: Configure separate console sessions](#step-1-configure-separate-console-sessions)
* [Step 2: Access your clusters](#step-2-access-your-clusters)
* [Step 3: Set up your namespaces](#step-3-set-up-your-namespaces)
* [Step 4: Install Skupper in your namespaces](#step-4-install-skupper-in-your-namespaces)
* [Step 5: Check the status of your namespaces](#step-5-check-the-status-of-your-namespaces)
* [Step 6: Link your namespaces](#step-6-link-your-namespaces)
* [Step 7: Deploy and expose the database in the private cluster](#step-7-deploy-and-expose-the-database-in-the-private-cluster)
* [Step 8: Create the table to store the tweets](#step-8-create-the-table-to-store-the-tweets)
* [Step 9: Deploy Twitter Camel Integration in the public cluster](#step-9-deploy-twitter-camel-integration-in-the-public-cluster)
* [Step 10: Deploy Telegram Camel integration in the public cluster](#step-10-deploy-telegram-camel-integration-in-the-public-cluster)
* [Step 11: Test the application](#step-11-test-the-application)
* [Summary](#summary)
* [Cleaning up](#cleaning-up)
* [Next steps](#next-steps)

## Overview

In this example we can see how to integrate different Camel integration routers
that can be deployed across multiple Kubernetes clusters using Skupper.

The main idea of this project is to show a Camel integration deployed in a public cluster
which searches tweets that contain the word 'skupper'. Those results are sent to a
private cluster that has a database deployed. A third public cluster will ping the database
and send new results to a Telegram channel.

In order to run this example you will need to create a Telegram channel and a Twitter Account
to use its credentials.

It contains the following components:

* A Twitter Camel integration that searches in the Twitter feed for results containing the word `skupper` (public).

* A PostgreSQL Camel sink that receives the data from the Twitter Camel router and sends it to the database (public).

* A PostgreSQL database that contains the results (private).

* A Telegram Camel integration that polls the database and sends the results to a Telegram channel (public).

## Prerequisites

* The `kubectl` command-line tool, version 1.15 or later
([installation guide][install-kubectl])

* The `skupper` command-line tool, the latest version ([installation
guide][install-skupper])

* Access to at least one Kubernetes cluster, from any provider you
choose

* `Kamel` installation to deploy the Camel integrations per namespace.
In minikube you will need to execute the following commands:
```
minikube addons enable registry
kamel install
```

* A `Twitter Developer Account` in order to use the Twiter API (you need to add the credentials in `config.properties` file)

* Create a `Telegram` Bot and Channel to publish messages (you need to add the credentials in `config.properties` file)

## Step 1: Configure separate console sessions

Skupper is designed for use with multiple namespaces, typically on
different clusters.  The `skupper` command uses your
[kubeconfig][kubeconfig] and current context to select the namespace
where it operates.

[kubeconfig]: https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/

Your kubeconfig is stored in a file in your home directory.  The
`skupper` and `kubectl` commands use the `KUBECONFIG` environment
variable to locate it.

A single kubeconfig supports only one active context per user.
Since you will be using multiple contexts at once in this
exercise, you need to create distinct kubeconfigs.

Start a console session for each of your namespaces.  Set the
`KUBECONFIG` environment variable to a different path in each
session.

Console for _private1_:

~~~ shell
export KUBECONFIG=~/.kube/config-private1
~~~

Console for _public1_:

~~~ shell
export KUBECONFIG=~/.kube/config-public1
~~~

Console for _public2_:

~~~ shell
export KUBECONFIG=~/.kube/config-public2
~~~

## Step 2: Access your clusters

The methods for accessing your clusters vary by Kubernetes provider.
Find the instructions for your chosen providers and use them to
authenticate and configure access for each console session.  See the
following links for more information:

* [Minikube](https://skupper.io/start/minikube.html)
* [Amazon Elastic Kubernetes Service (EKS)](https://skupper.io/start/eks.html)
* [Azure Kubernetes Service (AKS)](https://skupper.io/start/aks.html)
* [Google Kubernetes Engine (GKE)](https://skupper.io/start/gke.html)
* [IBM Kubernetes Service](https://skupper.io/start/ibmks.html)
* [OpenShift](https://skupper.io/start/openshift.html)
* [More providers](https://kubernetes.io/partners/#kcsp)

## Step 3: Set up your namespaces

Use `kubectl create namespace` to create the namespaces you wish to
use (or use existing namespaces).  Use `kubectl config set-context` to
set the current namespace for each session.

Console for _private1_:

~~~ shell
kubectl create namespace private1
kubectl config set-context --current --namespace private1
~~~

Console for _public1_:

~~~ shell
kubectl create namespace public1
kubectl config set-context --current --namespace public1
~~~

Console for _public2_:

~~~ shell
kubectl create namespace public2
kubectl config set-context --current --namespace public2
~~~

## Step 4: Install Skupper in your namespaces

The `skupper init` command installs the Skupper router and service
controller in the current namespace.  Run the `skupper init` command
in each namespace.

**Note:** If you are using Minikube, [you need to start `minikube
tunnel`][minikube-tunnel] before you install Skupper.

[minikube-tunnel]: https://skupper.io/start/minikube.html#running-minikube-tunnel

Console for _private1_:

~~~ shell
skupper init
~~~

Console for _public1_:

~~~ shell
skupper init
~~~

Console for _public2_:

~~~ shell
skupper init
~~~

## Step 5: Check the status of your namespaces

Use `skupper status` in each console to check that Skupper is
installed.

Console for _private1_:

~~~ shell
skupper status
~~~

Console for _public1_:

~~~ shell
skupper status
~~~

Console for _public2_:

~~~ shell
skupper status
~~~

You should see output like this for each namespace:

~~~
Skupper is enabled for namespace "<namespace>" in interior mode. It is not connected to any other sites. It has no exposed services.
The site console url is: http://<address>:8080
The credentials for internal console-auth mode are held in secret: 'skupper-console-users'
~~~

As you move through the steps below, you can use `skupper status` at
any time to check your progress.

## Step 6: Link your namespaces

Creating a link requires use of two `skupper` commands in conjunction,
`skupper token create` and `skupper link create`.

The `skupper token create` command generates a secret token that
signifies permission to create a link.  The token also carries the
link details.  Then, in a remote namespace, The `skupper link create`
command uses the token to create a link to the namespace that
generated it.

**Note:** The link token is truly a *secret*.  Anyone who has the
token can link to your namespace.  Make sure that only those you trust
have access to it.

First, use `skupper token create` in one namespace to generate the
token.  Then, use `skupper link create` in the other to create a link.

Console for _public1_:

~~~ shell
skupper token create ~/public1.token --uses 2
~~~

Console for _public2_:

~~~ shell
skupper link create ~/public1.token
skupper link status --wait 30
skupper token create ~/public2.token
~~~

Console for _private1_:

~~~ shell
skupper link create ~/public1.token
skupper link create ~/public2.token
skupper link status --wait 30
~~~

If your console sessions are on different machines, you may need to
use `scp` or a similar tool to transfer the token.

## Step 7: Deploy and expose the database in the private cluster

Use `kubectl apply` to deploy the database in `private1`. Then expose the deployment.

Console for _private1_:

~~~ shell
kubectl create -f src/main/resources/database/postgres-svc.yaml
skupper expose deployment postgres --address postgres --port 5432 -n private1
~~~

## Step 8: Create the table to store the tweets

Console for _private1_:

~~~ shell
kubectl run pg-shell -i --tty --image quay.io/skupper/simple-pg --env="PGUSER=postgresadmin" --env="PGPASSWORD=admin123" --env="PGHOST=$(kubectl get service postgres -o=jsonpath='{.spec.clusterIP}')" -- bash
psql --dbname=postgresdb
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE tw_feedback (id uuid DEFAULT uuid_generate_v4 (),sigthning VARCHAR(255),created TIMESTAMP default CURRENT_TIMESTAMP,PRIMARY KEY(id));
~~~

## Step 9: Deploy Twitter Camel Integration in the public cluster

First, we need to deploy the `TwitterRoute` component in Kubernetes by using kamel. This component will poll Twitter
every 5000 ms for tweets that include the word `skupper`. Subsequently, it will send the results to the
`postgresql-sink`, that should be installed in the same cluster as well.
The kamelet sink will insert the results in the postgreSQL database.

Console for _public1_:

~~~ shell
src/main/resources/scripts/setUpPublic1Cluster.sh
~~~

## Step 10: Deploy Telegram Camel integration in the public cluster

In this step we will install the secret in Kubernetes that contains the database credentials, in order to be used
by the `TelegramRoute` component.
After that we will deploy `TelegramRoute` using kamel in the Kubernetes cluster. This component will poll the
database every 3 seconds and gather the results inserted during the last 3 seconds.

Console for _public2_:

~~~ shell
src/main/resources/scripts/setUpPublic2Cluster.sh
~~~

## Step 11: Test the application

To be able to see the whole flow at work, you need to post a tweet containing the word `skupper` and after that
you will see a new message in the Telegram channel with the title `New feedback about Skupper`

Console for _private1_:

~~~ shell
kubectl attach pg-shell -c pg-shell -i -t
psql --dbname=postgresdb
SELECT * FROM tw_feedback;
~~~

Sample output:

~~~
id                                    | sigthning       |          created
--------------------------------------+-----------------+----------------------------
 95655229-747a-4787-8133-923ef0a1b2ca | Testing skupper | 2022-03-10 19:35:08.412542
~~~

Console for _public1_:

~~~ shell
kamel logs twitter-route
~~~

Sample output:

~~~
"[1] 2022-03-10 19:35:08,397 INFO  [postgresql-sink-1] (Camel (camel-1) thread #0 - twitter-search://skupper) Testing skupper"
~~~

## Summary

This example locates the different camel integrations in different
namespaces, on different clusters. This means that they
have no way to communicate with the database deployed in the private cluster
unless they are exposed to the public internet.

Introducing Skupper into each namespace allows us to create a virtual
application network that can connect services in different clusters.
Any service exposed on the application network is represented as a
local service in all of the linked namespaces.

The database is located in `private1`, but the TelegramRoute integration
in `public2` can "see" it as if it were local.  When the integration pulls
the database, Skupper forwards the request to the namespace where the database is running
and routes the response back to the integration component.

## Cleaning up

To remove Skupper and the other resources from this exercise, use the
following commands.

Console for _private1_:

~~~ shell
src/main/resources/scripts/tearDownPrivate1Cluster.sh
~~~

Console for _public1_:

~~~ shell
src/main/resources/scripts/tearDownPublic1Cluster.sh
~~~

Console for _public2_:

~~~ shell
src/main/resources/scripts/tearDownPublic2Cluster.sh
~~~

## Next steps

Check out the other [examples][examples] on the Skupper website.
