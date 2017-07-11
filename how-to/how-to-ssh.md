# SSH
SSH is a powerful utility you can use to securely connect to other computers in your network and run commands.

In this howto we'll show how you can set up mycroft to ssh into another machine, and run a command.

## create ssh keys.
 You'll need to create ssh keys on the mycroft box.  Just press enter a bunch of times.
```
ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/erm/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in id_rsa.
Your public key has been saved in id_rsa.pub.
The key fingerprint is:
a9:ad:b6:be:9e:c2:8b:7c:7f:18:4f:20:1c:1f:f0:ef erm@erm76
The key's randomart image is:
+--[ RSA 2048]----+
|    ..           |
|    ...          |
|   . o..         |
|    o o. .       |
|     . .S        |
|      .+.        |
|   .  .=E        |
| . .+ ooo        |
|  o..BO+         |
+-----------------+
```

Now copy the keys over to the box you want mycroft to run the commands on.
The `user` is the username you want mycroft to execute the command as on the remote server, and the `host` can be the ip address of the machine you want mycroft to connect to.

If you don't know what your ip is you can use `hostname -I` or `ifconfig` to find out this information.  For simplicity you can also add a hostname to your [`/etc/hosts`](http://www.tldp.org/LDP/solrhe/Securing-Optimizing-Linux-RH-Edition-v1.3/chap9sec95.html) file for that ip.  Keep in mind some routers change ip addresses, and you'll need the other ip to be static on your lan so mycroft will always be able to access it when it's on the lan.

```
# you'll be prompted for a password
ssh-copy-id user@host
```

`ssh-copy-id` Adds the contents of `~/.ssh/id_rsa.pub` to the remote box's `~/.ssh/authorized_keys` file.

Now test the connection:
```
ssh user@host
```
If you connected without being prompted for a password you're good to go.

Now we're going to need to write a few scripts on the remote/slave box with your favorite editor.
### `vlc.sh` on slave
```
#!/bin/bash
export DISPLAY=":0.0"
nohup vlc "$@" &>/dev/null
```

Remember to `chmod +x vlc.sh`

### `firefox.sh` on slave
```
#!/bin/bash
export DISPLAY=":0.0"
nohup firefox "$@" &>/dev/null
```

Remember to `chmod +x firefox.sh`

`exit` out of the ssh connection and test the commands.
```
ssh user@host /path/to/vlc.sh "rtmp://jblive.videocdn.scaleengine.net/jb-live/play/jblive.stream"
ssh user@host /path/to/firefox.sh "http://google.com"
```

From there you'll need to create the `vlc.sh` and `firefox.sh` scripts on your mycroft box.

### `vlc.sh` on master
```
#!/bin/bash
nohup ssh user@host /path/to/vlc.sh "$@" &>/dev/null
```

### `firefox.sh` on master
```
#!/bin/bash
nohup ssh user@host /path/to/firefox.sh "$@" &>/dev/null
```

Lastly edit your `mycroft.conf` file
### `mycroft.conf`
```json
"JbSkill": {
    "media_command": "/path/to/vlc.sh",
    "webpage_command": "/path/to/firefox.sh"
}
```

Restart mycroft services, and test.
`./mycroft.sh restart`
