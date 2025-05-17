# Background

Running an EC2 spot instance is very cheap, but you can be booted with 2 minutes of warning if somebody bids more than you. This script will monitor if there is a kill message sent for your server and will notify you using the [ntfy](https://ntfy.sh/) service.

AWS has [instructions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-instance-termination-notices.html) for how to monitor for this kill signal which involves a simple poll to their api:

```
TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"` \
    && curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/spot/instance-action
```

If there is no kill signal then this curl request will return a 404 response, but if there is a kill request, then it will return

```bash
{"action": "terminate", "time": "2017-09-18T08:22:00Z"}
```
or
```bash
{"action": "stop", "time": "2017-09-18T08:22:00Z"}
```

This script converts the curl command into python and runs it every few seconds to monitor for a kill signal.

## How to run the script
Run the following docker command which will pull the image/script from [dockerhub](https://hub.docker.com/r/bak7/aws-interrupt-monitor/tags):

```bash
docker run -d \
  -e NTFY_SERVER="https://ntfy.server.url" \
  -e NTFY_TOPIC="my_topic" \
  -e NTFY_SECRET="my_secret" \
  -e POLL_INTERVAL="15" \
  -e VM_HOSTNAME="$(hostname)" \
  bak7/aws-interrupt-monitor:latest
```

The environment variables `NTFY_SERVER` and `NTFY_TOPIC` make up the endpoint of your `ntfy` server and `NTFY_SECRET` is the secret token that is placed in the header data of the ntfy request. `VM_HOSTNAME` can be anything, but is useful to identify the EC2 instance hostname.

The above command is useful if you want to add it to your AWS EC2 template under user data so that it automatically starts as the server is started. Otherwise it can be run by hand.

Alternatively, the script can be run from docker compose in the following way:


Clone the repo:

```bash
git clone https://github.com/ben-kenney/aws-interrupt-monitor.git
```

Create the `.env` file inside the `aws-interrupt-monitor`:

```
NTFY_TOPIC="my_topic"
NTFY_SERVER="https://ntfy.server.url"
NTFY_SECRET="my_secret"
POLL_INTERVAL="15"
```

Launch the docker compose file:

```bash
VM_HOSTNAME=$(hostname) docker compose up -d
```

## Build instructions

If you want to build the container instead of downloading from dockerhub: `docker compose -f docker-compose-build.yaml up -d`.

If you want to upload to your own dockerhub repository:

```bash
docker build -t bak7/aws-interrupt-monitor .
docker push bak7/aws-interrupt-monitor:latest
```

replace `bak7` with your dockerhub username.