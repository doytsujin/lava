# Upgrade LAVA

## When to upgrade

We advice to always upgrade to the latest released version. Only the latest
release will include new features and fix bugs (including security issues).

## How to upgrade

Currently, LAVA does not allow for zero-downtime upgrade.

We advice to put the instance in maintenance before any upgrade.

!!! example "Maintenance mode"

    ```shell tab="docker-compose"
    docker-compose exec lava-server lava-server manage maintenance
    ```

    ```shell tab="debian"
    lava-server manage maintenance
    ```

    ```shell tab="lavacli"
    lavacli system maintenance
    ```


### Docker

When a new version of LAVA is released, a Docker image is published on [docker
hub](https://hub.docker.com/u/lavasoftware/).

In order to upgrade, admins should just pull the latest **docker-compose
configuration**:

```shell
git pull --rebase
```

The restarting docker-compose will enough:

```shell
docker-compose up
```

??? tip "Downtime during upgrade"
    The current setup does not allow for zero-downtime upgrade without a
    management layer like [docker swarm](https://docs.docker.com/engine/swarm/)
    or [kubernetes](https://kubernetes.io/).

### Debian

When a new version of LAVA is released, a new Debian package is published on
the official [Debian repository](https://apt.lavasoftware.org/release/).

You can upgrade using **apt**:

```shell
apt-get update
apt-get upgrade
```

??? tip "Downtime during upgrade"
    Zero-downtime upgrade is not possible with the current Debian packages.
    During the upgrade, every services will be stopped while upgrading.
