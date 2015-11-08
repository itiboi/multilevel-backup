# multilevel-backup

[![Build Status](https://travis-ci.org/itiboi/multilevel-backup.svg?branch=master)](https://travis-ci.org/itiboi/multilevel-backup)

Simplifying the management of a multilevel backup structure with rsnapshot especially for not always-on devices.
Since rsnapshot takes only care about the actual backup process and leaves the handling and timing of multiple backup
level to the user. For simple setups, this issue can be easily solved with cron jobs, but notably with not always-on devices
the manual management can easily result in irreversible mistakes. 

### What does it do?

Multilevel-backup handles all calls to rsnapshot, the only thing needed is a valid rsnapshot config file. At every
invocation, it takes care about performing

- Only one backup a day
- Higher backup level as needed

This way, you never have to think about when to call a higher level backup just because you missed a backup.

Note: At the moment only a backup setup with the levels daily, weekly and monthly are supported.

### Requirements

Multilevel-backup has no special requirements, it just needs:

- Python >= 3.3
- Functional rsnapshot installation

### Installation

Currently, multilevel-backup is not available on PyPi. To get it, clone it with

```
$ git clone https://github.com/itiboi/multilevel-backup.git
```

and install it with

```
$ python3 ./setup.py install
```

### Usage

To perform a backup, just call

```
multilevel-backup -c path/to/rsnapshot/config
```

and relax.

If you want to execute backups automatically, just create a cron job with this call to invoke it daily (or hourly, just
as you setup requires) and multilevel-backup cares about the rest.

To do a dry run, just add  ```-d``` to the call. It prints all calls that would be invoked. 

### Help? Want feature?

If you encounter any problems, do not hesitate to create an [issue](https://github.com/itiboi/multilevel-backup/issues).
If you want to help, just [fork](https://github.com/itiboi/multilevel-backup/fork). Any help is wanted!

### License

This project is published under the terms of GPLv3. For more information see [LICENSE.txt](LICENSE.txt)