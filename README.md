# Ansible playbook for che-rjs1.che.pitt.edu

Although Ansible is often used to configure several machines, these
playbooks here apply to a single research lab Ubuntu Server.

## Using the container sandbox for testing

You can test the playbooks using a container.  Canonical does not have
a Docker image specifically for their Ubuntu Server, but one can
trivially create an Ubuntu Server image by installing the
`ubuntu-server` package into an `ubuntu` image.  This is what the
`Dockerfile` in this repository does.

However using Docker for your container is not a great idea because of
its unnecessary root escalation and a long history of poor security
practices.  Instead, on a Linux operating system you probably want to
setup the safer, rootless
[containerd](https://github.com/containerd/containerd) package from
the Linux Foundation (that provides `nerdctl`) and on macOS you may
want to setup the recent
[container](https://github.com/apple/container) package from Apple.

```shell
alias docker=nerdctl            # on GNU/Linux
alias docker=container          # on macOS

docker image ls                 # does not list ubuntu-server:24.04
docker build -t ubuntu-server:24.04
docker image ls                 # should now list ubuntu-server:24.04
```

We need to share the files from this Git repository inside the
container to run `ansible-playbook` on them.  Therefore, mount this
directory as read-only at an unprivileged location inside the
container and start the container:

```shell
container \
    run \
    --mount source=.,destination=/home/ubuntu/che-rjs1,readonly \
    -it ubuntu-server:24.04
```

Then inside the container:

```shell
apt -y update
apt -y install ansible
su - ubuntu
cd che-rjs1/
ansible-playbook network.yaml	# or whatever playbook interests you.
```
