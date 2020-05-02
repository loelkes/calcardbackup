# calcardbackup

This is a **WORK IN PROGRESS**, there is no working version available at the moment.

This python script exports calendars from ownCloud/Nextcloud to .ics files. It is inspired by the bash version from BernieO available at [codeberg.org/BernieO/calcardbackup](https://codeberg.org/BernieO/calcardbackup).

The bash version is also available in the branch *bash*. Not all features and options are available in the python version.

## Motivations
The bash script is impressive. Nice work. But:
- There's no easy way of using a separate database user. I don't want to give scripts write access and prefer creating read-only users for backups.
- IMHO encryption, compression and handling of old backups should be done with existing tools such as rsnapshot on an encrypted filesystems/containers. Implementing it in the script increase maintenance effort.
- IMHO Python is a better option for such task than bash.
- No possiblity for backups up via CalDAV with app passwords for user without access to the database.

## Contents
- [Requirements](#requirements)
- [Quick Installation Guide](#quick-installation-guide)
- [Upgrading *calcardbackup*](#upgrading-calcardbackup)
- [Options](#options)
- [Does this also work with a broken ownCloud/Nextcloud instance?](#does-this-also-work-with-a-broken-owncloud-nextcloud-instance)
- [Links](#links)

## Requirements

- ownCloud/Nextcloud >= 5.0 with MySQL/MariaDB. PostgreSQL or SQLite3 might be supported in later version.
- python >=  3.6

## Quick Installation Guide

1. Clone the repository and enter the repo:
`git clone https://github.com/loelkes/calcardbackup`
`cd calcardbackup`

2. Create a virtual environment (optional but recommended):
```
python3 -m venv venv
source venv/bin/activate
python setup.py install
```

3. Change settings to match your nextcloud/owncloud config
```
cp configsample.ini config.ini
vim config.ini
```

4. Run the script with `python -m calcardbackup -c config.ini`

5. Find your backup in directory `backups/`.

There are many more options available: have a look at sections [Options](#options).

#### optional: setup a cronjob for an automatic daily run

Once *calcardbackup* runs without errors, a cronjob can be setup to run it automatically each day at as follows:

1. Edit the cron table of the user with:
   `sudo crontab -e`
   and add the following line to the end of the file (change paths to fit your setup!):
   ```
   0 2 * * * /path/to/venv/bin/python -m calcardbackup -c /path/to/config.ini
   ```

Cron will now execute *calcardbackup* each day at 02:00am.
The output of the last run is written to `/var/log/calcardbackup.log`.

## Upgrading *calcardbackup*

If you followed the instructions in the [Quick Installation Guide](#quick-installation-guide), you just need to pull the new version to upgrade to the latest version:
```
cd /path/to/calcardbackup
git pull
python setup.py install
```

## Options

All options can be specified in a configuration file. Some can be overwritten at execution witg command line arguments. If started with no options at all the script attempts to use file `config.ini` in the script's directory as configuration file.

* See `python -m calcardbackup -h` for all available CLI options.
* See `configsample.ini` for all available config options.

## Does this also work with a broken ownCloud/Nextcloud instance?

__Yes, it does!__ :smiley:

*calcardbackup* only needs the database (and access to it) from an ownCloud/Nextcloud installation to be able to extract calendars/addressbooks from the database and save them as .ics and .vcf files.
Here is how this can be accomplished:

## Links

#### Related Forum Threads
- [help.nextcloud.com](https://help.nextcloud.com/t/calcardbackup-bash-script-to-backup-nextcloud-calendars-and-addressbooks-as-ics-vcf-files/11978) - Nextcloud
- [central.owncloud.org](https://central.owncloud.org/t/calcardbackup-bash-script-to-backup-owncloud-calendars-and-addressbooks-as-ics-vcf-files/7340) - ownCloud

#### Blog articles about *calcardbackup*
- [bob.gatsmas.de](https://bob.gatsmas.de/articles/calcardbackup-jetzt-erst-recht) - October 2018 (german)
- [strobelstefan.org](https://strobelstefan.org/?p=6094) - January 2019 (german)
- [newtoypia.blogspot.com](https://newtoypia.blogspot.com/2019/04/nextcloud.html) - April 2019 (taiwanese)

#### ICS and VCF standard
- [RFC 5545](https://tools.ietf.org/html/rfc5545) - Internet Calendaring and Scheduling Core Object Specification (iCalendar)
- [RFC 6350](https://tools.ietf.org/html/rfc6350) - vCard Format Specification

#### Exporter Plugins from SabreDAV used by ownCloud/Nextcloud
- [ICSExportPlugin.php](https://github.com/sabre-io/dav/blob/master/lib/CalDAV/ICSExportPlugin.php) - ICS Exporter `public function mergeObjects`
- [VCFExportPlugin.php](https://github.com/sabre-io/dav/blob/master/lib/CardDAV/VCFExportPlugin.php) - VCF Exporter `public function generateVCF`
