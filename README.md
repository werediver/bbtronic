# bbtronic

Monitors and merges your pull-request on Bitbucket when it's ready.

## Configuration

`bbtronic` looks for a configuration file named `.bbtronic` in the current directory of one of its parent directories.

The configuration file should be of the following form:

```
[server1]
base_uri = https://server1.com
access_token = xxx

[server2]
base_uri = https://server2.com
access_token = yyy
```
