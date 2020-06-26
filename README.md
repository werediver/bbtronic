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

## Building

`bbtronic` can be packaged as a single executable file (thanks to [pex](https://github.com/pantsbuild/pex)) by running the build script:

```
$ ./mk.sh
``` 

The build script generates a single file `bin/bbtronic`, which you can link or copy into `~/bin/` or other appropriate directory _that is included in your `PATH` environment variable_.

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

# Dependencies

`bbtronic` depends on [requests](https://github.com/psf/requests) package to perform HTTP requests.
