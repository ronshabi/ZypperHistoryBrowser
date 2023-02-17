# Zypper History Browser
This is a quick n' handy tool to browse and filter through Zypper's (package manager for OpenSuSE and SuSE linux) action history.

This script will query the file that holds Zypper's history, which can be found at ```/var/log/zypp/history```, Therefore it needs to run with sufficient permissions (usually as root).

## Usage
Program will query all history avaliable by default, the following flags are optional and can be used to filter:


```
--actions [install, remove, verify, source-install, update, patch info, refresh, clean]
```
Filter by action (Can be multiple choice, separated by spaces)

```
--from [Date (in IsoFormat)]
--to [Date (in IsoFormat)
```
Filter by date range (Inclusive for both *from* and *to*).

*Note that they don't have to be used together, or in any specific order*

## Author
Ron Shabi

## License
MIT