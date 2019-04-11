Miniapp for create/list/remove [MailHog](https://github.com/mailhog/MailHog) containers.

```sh
docker run \
  -d \
  -p 5000:5000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  ksisu/mailhog-mgr
```

```sh
docker run \
  -d \
  -p 5000:5000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e DOMAIN=lvh.me
  ksisu/mailhog-mgr
```
