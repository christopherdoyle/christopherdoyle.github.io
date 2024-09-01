---
title: "Self-hosted backups with autorestic, ntfy, and B2"
date: 2024-09-01
---

## Overview

We will use [autorestic](https://autorestic.vercel.app/), a wrapper for [restic](https://restic.net/), to backup data to [Backblaze B2](https://www.backblaze.com/cloud-storage); cron to automate the backups; and self-hosted [ntfy.sh](https://ntfy.sh/) for backup push notifications.
We will backup the directory `/apps` on our server.
This assumes you are already running a publicly accessible server with a domain name `domain.com`, and you have docker, nginx, and certbot setup.

## B2

Create a container in B2, or use an existing container, and create an API key with read-write access to that container.
The backups will be encrypted, but the B2 container should be set to private access only.
You can enable encryption at host in the B2 container, this would add an extra layer of encryption, but it is not necessary.

Create a new API key for the container, with access to just that container.

## Setting up autorestic

autorestic is a couple of binaries and a config file.
Run the install command on [autorestic's quick start](https://autorestic.vercel.app/quick) page on the server to install.
Now create a config file like this in `/apps/.autorestic.yml`.

```yaml
version: 2

locations:
  apps:
    from: /apps
    to: remote
    cron: '5 */6 * * *'  # At 5 minutes past the hour, every 6 hours

backends:
  remote:
    type: b2
    path: 'b2-container-name:/path/in/container'
    env:
      B2_ACCOUNT_ID: ...
      B2_ACCOUNT_KEY: ...
    key: ...
    requirekey: true
```

Fill in the B2 API ID and Key.
The "key" field is your encryption password for the backups.
This is the absolute minimum that you need to store from this configuration file in order to restore the backup.
Store the key (or the entire config file) in a password manager, or write it down.
You can also store the key in a separate file (and your password manager), and the B2 key in a `.env` file, which keeps the compose file secret-free, allowing you to store it in a public/private repo as a backup.

At this point, autorestic should work.
Run `autorestic check` to check the config.
Then run `autorestic backup -a` to initiate the first full backup.

## ntfy initial setup

ntfy is an open-source notification pub-sub server with clients for the browser, Android, and iOS.
The iOS app is not great and the configuration can be a little finicky.
We will self-host ntfy in docker, but you can also use their free tier at ntfy.sh up to some limits.

Create a CNAME record `ntfy` targetting the domain root (`@`/`domain.com`).
This will host the web app and the pub-sub service.

Now:

```bash
mkdir -p /apps/ntfy/{config,data}
cd /apps/ntfy
wget https://raw.githubusercontent.com/binwiederhier/ntfy/main/server/server.yml -O config/server.yml
```

Create a compose file `/apps/ntfy/compose.yaml` with the following content:

```yaml
services:
  ntfy:
    image: binwiederhier/ntfy
    container_name: ntfy
    command:
      - serve
    environment:
      - TZ=UTC
    volumes:
      - ./config:/etc/ntfy
      - ./data:/var/lib/ntfy
    ports:
      - 8000:80
    healthcheck: # optional: remember to adapt the host:port to your environment
        test: ["CMD-SHELL", "wget -q --tries=1 http://localhost:80/v1/health -O - | grep -Eo '\"healthy\"\\s*:\\s*true' || exit 1"]
        interval: 60s
        timeout: 10s
        retries: 3
        start_period: 40s
    restart: unless-stopped
```

Set 8000 to some free port on the host.

Now edit the `server.yml` file and set at least the following fields:

```yaml
base-url: https://ntfy.domain.com/
listen-http: "80"
cache-file: /var/lib/ntfy/cache.db
auth-file: /var/lib/ntfy/auth.db
auto-default-access: "deny-all"
behind-proxy: true
attachment-cache-dir: /var/lib/ntfy/attachments
enable-signup: false
enable-login: true
upstream-base-url: "https://ntfy.sh"
```

You can now run `docker compose up -d` to start the server.
It should start successfully, but it won't be accessible until we set up nginx.

## nginx

Create a file `/etc/nginx/sites-available/ntfy` with content:

```yaml
server {
  server_name ntfy.domain.com

  location / {
    proxy_set_header   X-Real-IP $remote_addr;
    proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header   Host $host;
    proxy_pass         http://localhost:8000/;
    proxy_http_version 1.1;
    proxy_set_header   Upgrade $http_upgrade;
    proxy_set_header   Connection "upgrade";
  }
}
```

8000 should be the same port as in the docker compose file.

Enable the site with `ln -s /etc/nginx/sites-available/ntfy /etc/nginx/sites-enabled`.
Then use `certbot` to generate certificates and update the config file.
Finally run `nginx -t` to check the config, before `systemctl reload nginx` to reload the config.

At this point, `https://ntfy.domain.com` should be available.
The website is really just a local web app.
You'll notice the config was set to "deny-all" and "require login", but the web app is fully accessible without any login at all.
This is totally fine, you'll find that if you try to publish and subscribe to anything, it will prompt for a login.

## ntfy users

For the logins, we should set up users as required.
We will create one user for autorestic, and one user for you, "bob".
Since we are running ntfy in docker, we will use docker exec to open a shell and run the commands there.
You can also run `docker exec ntfy ntfy` to invoke `ntfy` directly.

```bash
docker exec -it ntfy /bin/sh
ntfy user add --role=user bob
ntfy access bob autorestic read-only
ntfy user add --role=user autorestic
ntfy access autorestic autorestic write-only
ntfy token add autorestic
```

You could also just set up one user, even a user with `--role=admin`, and use that for everything.
These are specific permissions, giving bob read access to the autorestic topic; and autorestic user write access.
The last command creates a token, save the value, we will use it later.

## ntfy push

Lastly, we want to set up ntfy to be able to push in browser.
Run `ntfy webpush keys` to generate a config, and copy it.
Exit the docker exec and edit the `server.yml` file, and paste the fields in.
`web-push-email-address` must be set, e.g. `admin@domain.com`.

Now restart ntfy with `docker compose restart`.
You should be able to enable ntfy notifications in the browser now, there is a banner at the top-left prompting you to enable them when you access the web app.

## ntfy iOS

You can subscribe to the 'autorestic' channel in the web apps, or the android app, easily.

iOS is a bit weird.
Download the [iOS](https://apps.apple.com/us/app/ntfy/id1625396347) app and install it.
Then go the the global settings and set `https://ntfy.domain.com` as the default server.
Then subscribe to the `autorestic` channel, you will need to enter your username ("bob") and password.

I found that any other order of operations did not work.
Setting the server when subscribing to the channel was not sufficient, and setting the global setting after subscribing did not work either!
Notifications would only appear when manually refreshing, and not get pushed out.

## set up ntfy in autorestic

Go back to `.autorestic.yml` and edit the location like so:

```yaml
locations:
  apps:
    from: /apps
    to: remote
    cron: '5 */6 * * *'
    hooks:
      success:
        - 'curl -H "Authorization: Bearer tk_XXXX" -H "Title: Backup successful" -H "Tags: +1" -d "" https://ntfy.domain.com/autorestic'
      failure:
        - 'curl -H "Authorization: Bearer tk_XXXX" -H "Title: Backup failure" -H "Tags: rotating_light" -H "Priority: high" -d "" https://ntfy.domain.com/autorestic'
```

Where `tf_XXXX` is the token created earlier for the `autorestic` user.
I needed quotes around the entire curl line otherwise YAML complained, not sure why.
Run `autorestic check` to check the config.

You can, and probably should, use the curl command directly to test the notification.
There are more headers and settings in the documentation if you like.
When you run the curl command, you should get a successful response back, and a notification should appear on your phone/web.

## crontab

The cron settings in the autorestic YAML and for its internal timekeeping.
This is the frequency you want to backup the location at.
You can have multiple locations, each with their own schedule.

A crontab job should be set up to invoke the cron frontend of autorestic, for example:

```
*/5 * * * * autorestic -c /apps/.autorestic.yml --ci cron
```

This is running every 5 minutes, but this just means we're asking autorestic to check the schedules every five minutes.

After autorestic has been run once, it will create a `/apps/.autorestic.lock.yml` file.
This is a miniature database that stores the unix timestamp of the last run, and is used to track the cron jobs.

## Conclusion

You now have fully automated backups of the `/apps` directory to B2.
The backups are encrypted and incremental, and you receive notifications on successful and failed jobs pushed to your phone, all on self-hosted and open source infrastructure.

## But wait. Backups do not exist until they have been tested.

Yeah you should really check they work.
Install `autorestic` on another server or computer, and copy the contents of the YML config file into `.autorestic.yml`.

Now run `autorestic restore -l apps --from remote --to apps`.
This will initiate the restore process into an apps directory (must be empty).
Note that our `/apps` directory includes ntfy, so you could also run `docker compose up -d apps/ntfy` as a final check.
