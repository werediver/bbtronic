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

## Usage

You can list the open pull-requests by using the `list` command:

```
$ bbtronic list server1/PROJ/repo
```

It shows IDs and titles of the open pull-requests, so that you can proceed with other commands, the key of which is `automerge`:

```
$ bbtronic automerge server1/PROJ/repo/1234
```

It periodically checks whether the pull-request is ready to be merged and merges it as soon as possible.
