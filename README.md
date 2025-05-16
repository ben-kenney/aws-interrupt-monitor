# Background

Running an EC2 spot instace is very cheap, but you can be booted with 2 minutes of warning if somebody bids more than you. This script will monitor if there is a kill message sent for your server and will notify you using the `ntfy` service.