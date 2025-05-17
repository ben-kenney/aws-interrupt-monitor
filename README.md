# Background

Running an EC2 spot instance is very cheap, but you can be booted with 2 minutes of warning if somebody bids more than you. This script will monitor if there is a kill message sent for your server and will notify you using the `ntfy` service.

## Run

Run the following docker command:

```bash
docker run -d \
  -e NTFY_TOPIC="my_topic" \
  -e NTFY_SERVER="https://ntfy.server.url" \
  -e NTFY_SECRET="my_secret" \
  -e POLL_INTERVAL="15" \
  -e VM_HOSTNAME="$(hostname)" \
  bak7/aws-interrupt-monitor:latest
```

or download from git and run docker compose

Create an `.env`:

```
NTFY_TOPIC="my_topic"
NTFY_SERVER="https://ntfy.server.url"
NTFY_SECRET="my_secret"
POLL_INTERVAL="15"
```

then

```bash
git clone https://github.com/ben-kenney/aws-interrupt-monitor.git && cp .env aws-interrupt-monitor/ && cd aws-interrupt-monitor && VM_HOSTNAME=$(hostname) docker compose up -d
```

## Build instructions:

```
docker build -t bak7/aws-interrupt-monitor .
docker push bak7/aws-interrupt-monitor:latest
```