# multilevel-backup

[![Build Status](https://travis-ci.org/itiboi/multilevel-backup.svg?branch=master)](https://travis-ci.org/itiboi/multilevel-backup) [![Coverage Status](https://coveralls.io/repos/itiboi/multilevel-backup/badge.svg?branch=master&service=github)](https://coveralls.io/github/itiboi/multilevel-backup?branch=master)

Simplifies the management of a multilevel backup structure with rsnapshot especially for not always-on devices.
Since rsnapshot takes only care about the actual backup process, the handling and timing of multiple backup level is
left to the user. For simple setups, this issue can be easily solved with cron jobs, but notably with not always-on devices
the manual management can easily result in irreversible mistakes. 

### What does it do?

Multilevel-backup handles all calls to rsnapshot, the only thing needed is a valid rsnapshot config file. At every
invocation, it takes care about performing

- Only one backup a day
- Higher backup level as needed

This way, you never have to think about when to call a higher level backup just because you missed a backup.

#### Important: Current setup limitation

At the moment only a backup setup with the intervals daily, weekly and monthly is supported. So your rsnapshot.conf file 
should contain something like this:

```
retain		daily	7   # Will be performed after 1 day difference
retain		weekly	4   # Will be performed after 7 days difference
retain		monthly	3   # Will be performed after 28 days difference
```

The interval count can differ, multilevel-backup will parse them. All difference days are referring to date difference,
so if a daily backup took place on `05.11.2015 20:00`, a second one will be performed on `06.11.2015 15:00`, although the
actual difference is less than 24 hours.

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
$ multilevel-backup -c path/to/rsnapshot/config
```

and relax.

If you want to execute backups automatically, just create a cron job with this call to invoke it daily (or different, just
as you setup requires) and multilevel-backup cares about the rest.

To do a dry run, just add  ```-d``` to the call. It prints all calls that would be invoked. 

### Help? Want feature?

If you encounter any problems, do not hesitate to create an [issue](https://github.com/itiboi/multilevel-backup/issues).
If you want to help, just [fork](https://github.com/itiboi/multilevel-backup/fork). Any help is wanted!

### License

This project is published under the terms of GPLv3. For more information see [LICENSE.txt](LICENSE.txt)