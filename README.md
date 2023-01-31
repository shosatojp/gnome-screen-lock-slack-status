# GNOME Screen Lock Slack Status

This app sets slack status depending on GNOME screen lock status.

## Usage

1. create slack app with permission to write status and get user token
2. edit `.env` file

`DOCKER_UID` is your user id.

```
SLACK_USER_TOKEN=xoxp-*****
DOCKER_UID=1000
```

3. compose up

```sh
docker compose up
```
