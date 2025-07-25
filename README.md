# Ansible playbook for che-rjs1.che.pitt.edu

Although Ansible is often used to configure several machines, these
playbooks here apply to a single research lab Ubuntu Server.

## Setup

1. Clone this repository

    ```shell
    git clone https://github.com/ImmuSystems-Lab/che-rjs1
    cd che-rjs1/
    ```

2. Install ansible with jmespath if not already in your PATH:

    ```shell
	pipx ensurepath
    pipx install --include-deps ansible
    pipx inject anisble --include-deps jmespath
    ```

3. Run one or more playbooks from this directory:

    ```shell
    # Allow root-privilege for select commands in the playbook.
    sudo true

    # Run the playbook
    ansible-playbook users.yaml
    ```

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
apt -y install ansible sudo
gpasswd -a ubuntu sudo
echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
echo "127.0.0.1 $(cat /etc/hostname)" >> /etc/hosts
su - ubuntu
cd che-rjs1/
# Reset `sudo` timeout for select commands in ansible-playbook(s) that
# require root privilege escalation.
sudo true

# Run whatever playbooks interest you below.

# Install packages used by this playbook.
sudo apt -y install grub2-common linux-generic
sudo cp -a /usr/share/grub/default/grub /etc/default/grub
sudo mkdir -p /boot/grub
sudo update-grub
ansible-playbook grub.yaml

# Install packages used by this playbook.
sudo apt -y install netplan.io
ansible-playbook network.yaml

# Install packages used by this playbook.
sudo apt -y install cloud-init openssh-server
ansible-playbook ssh.yaml

ansible-playbook users.yaml
```
