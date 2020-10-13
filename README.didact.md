# Getting started with Skupper

## Overview

To show Skupper in action, we need an application to work with.  This
guide uses an HTTP Hello World application with a frontend service and
a backend service.  The frontend uses the backend to process requests.
In this scenario, the frontend is deployed in the `west`
namespace, and the backend is deployed in the `east` namespace.

<img style="margin: 2em; width: 80%;" src="/images/hello-world-entities.svg"/>

While these instructions use this particular application for
demonstration purposes, the steps are the same for any Skupper
deployment.

## Prerequisites

You must have access to at least two Kubernetes namespaces.  In the
steps below, replace `west` and `east` with your chosen namespaces.

Each namespace can reside on **any cluster you choose**, and **you are
not limited to two**.  You can have one on your laptop, another on
Amazon, another on Google, and so on.  For convenience, you can have
them all on one cluster.

Skupper works with any flavor of Kubernetes.  Here are some of your
options for setting up Kubernetes clusters:

<ul class="column-list">
  <li><a href="minikube.html">Minikube</a></li>
  <li><a href="https://aws.amazon.com/eks/getting-started/">Amazon Elastic Kubernetes Service</a></li>
  <li><a href="https://docs.microsoft.com/en-us/azure/aks/intro-kubernetes">Azure Kubernetes Service</a></li>
  <li><a href="https://cloud.google.com/kubernetes-engine/docs/quickstart">Google Kubernetes Engine</a></li>
  <li><a href="https://cloud.ibm.com/docs/containers?topic=containers-getting-started">IBM Kubernetes Service</a></li>
  <li><a href="https://www.openshift.com/learn/get-started/">Red Hat OpenShift</a> or <a href="https://www.okd.io/">OKD</a></li>
  <li><a href="https://kubernetes.io/docs/concepts/cluster-administration/cloud-providers/">More providers</a></li>
  <!-- <li><a href="eks.html">Amazon Elastic Kubernetes Service</a></li> -->
  <!-- <li><a href="aks.html">Azure Kubernetes Service</a></li> -->
  <!-- <li><a href="gke.html">Google Kubernetes Engine</a></li> -->
  <!-- <li><a href="openshift.html">Red Hat OpenShift</a> or <a href="okd.html">OKD</a></li> -->
</ul>


These instructions require `kubectl` version 1.15 or later.  See the
[kubectl installation
guide](https://kubernetes.io/docs/tasks/tools/install-kubectl/) for
more information.

[Check if the kubectl command line is available](didact://?commandId=vscode.didact.cliCommandSuccessful&text=kubectl-requirements-status$$kubectl "Tests to see if `kubectl` returns a result"){.didact}

*Status: unknown*{#kubectl-requirements-status}

## Step 1: Install the Skupper command-line tool in your environment

The `skupper` command-line tool is the primary entrypoint for
installing and configuring the Skupper infrastructure.  You need to
install the `skupper` command only once for each development
environment.

### Download and extract the command

To get the latest release of the Skupper command for your platform,
download it from GitHub and extract the executable using `tar` or
`unzip`.

<div class="code-label">Linux</div>

    curl -fL https://github.com/skupperproject/skupper/releases/download/{{skupper_release}}/skupper-cli-{{skupper_release}}-linux-amd64.tgz | tar -xzf -

<div class="code-label">Mac</div>

    curl -fL https://github.com/skupperproject/skupper/releases/download/{{skupper_release}}/skupper-cli-{{skupper_release}}-mac-amd64.tgz | tar -xzf -

This produces an executable file named `skupper` in your current
directory.

To download artifacts for other platforms, see [Skupper
releases](/releases/index.html).

### Place the command on your path

The subsequent steps assume `skupper` is on your path.  As an example,
this is how you might install it in your home directory:

    mkdir -p $HOME/bin
    export PATH=$PATH:$HOME/bin
    mv skupper $HOME/bin

### Check the command

To test your installation, run the `skupper --version` command.  You
should see output like this:

    $ skupper --version
    skupper version {{skupper_release}}


[Check if the skupper command line is available](didact://?commandId=vscode.didact.cliCommandSuccessful&text=skupper-requirements-status$$skupper "Tests to see if `skupper` returns a result"){.didact}

*Status: unknown*{#skupper-requirements-status}

## Step 2: Configure access to multiple namespaces

Skupper is designed for use with multiple namespaces, typically on
different clusters.  The `skupper` command uses your kubeconfig and
current context to select the namespace where it operates.

To avoid getting your wires crossed, you must use a distinct
kubeconfig or context for each namespace.  The easiest way is to use
separate console sessions.

### Configure separate console sessions

Start a console session for each of your namespaces.  Set the
`KUBECONFIG` environment variable to a different path in each session.


[Start console session West](didact://?commandId=vscode.didact.startTerminalWithName&text=West "Create a new terminal window called 'West'"){.didact} to start a new terminal with the name `West`.


<div class="code-label session-2">Console for West</div>

    export KUBECONFIG=$HOME/.kube/config-west

<div class="code-label session-1">Console for East</div>

    export KUBECONFIG=$HOME/.kube/config-east





# Didact Terminal Commands

Didact has several built-in commands to help with managing Terminal creation, use, and termination. 

* `vscode.didact.startTerminalWithName` - Creates a new terminal with the given name or an unnamed terminal if no name is given.
* `vscode.didact.sendWestAString` - Looks for a terminal with the given name or creates one and then sends the text provided.
* `vscode.didact.sendWestCtrlC` - Looks for a terminal with the given name and sends an explicit `Ctrl+C` to try and halt whatever process is currently running.
* `vscode.didact.closeWest` - Looks for a terminal with the given name and sends a kill command. This works the same as if you select the terminal and use the `workbench.action.terminal.kill` command from the Command Palette.

Here are some examples of these commands in action.

## Starting a New Terminal with a Name

[Execute this](didact://?commandId=vscode.didact.startTerminalWithName&text=West "Create a new terminal window called 'West'"){.didact} to start a new terminal with the name `West`. If you execute the link a second time, it will throw an error and say that `Didact was unable to call command vscode.didact.startTerminalWithName: Error: Terminal West already exists`.

You can also create an unnamed terminal, but you won't have a consistent name to refer to it by later. [Execute this](didact://?commandId=vscode.didact.startTerminalWithName "Create a new terminal window"){.didact} to start a new terminal without a specific name.

## Sending Messages to the Terminal

You can then use the name of the terminal you have already created. This does not work if you create an unnamed terminal. The code searches for the terminal name and creates it if it doesn't already exist.

[Execute this](didact://?commandId=vscode.didact.sendWestAString&text=West$$ping%20localhost "Call `ping localhost` in the terminal window called 'West'"){.didact} to ping the localhost in our existing terminal window. 

Or you can give it a new name and combine the 'start' with the 'text'. [Execute this](didact://?commandId=vscode.didact.sendWestAString&text=SecondTerminal$$ping%20localhost "Call `ping localhost` in a second terminal window"){.didact} to start a new terminal called 'SecondTerminal' and ping the localhost there. 

## Stopping a Long-running Process in the Terminal with Ctrl+C

[Execute this](didact://?commandId=vscode.didact.sendWestCtrlC&text=SecondTerminal "Send `Ctrl+C` to the terminal window."){.didact} to send `Ctrl+C` to the second terminal and stop the ping. Note that it doesn't stop the first terminal if it's also running a ping command.

## Closing/Killing an Open Terminal Window

Note that again, you must use a named terminal.

[Execute this](didact://?commandId=vscode.didact.closeWest&text=West "Kill the first terminal window."){.didact} to close to the first terminal we opened.

[Execute this](didact://?commandId=vscode.didact.closeWest&text=SecondTerminal "Kill the second terminal window."){.didact} to close to the second terminal.

If no terminal is found with the specific name, it will show the user an error. [Execute this](didact://?commandId=vscode.didact.closeWest&text=NonexistentTerminal "Try and kill a terminal window that doesn't exist."){.didact} to close a terminal that doesn't exist. Since it can't find the terminal, it will pop up an error.
