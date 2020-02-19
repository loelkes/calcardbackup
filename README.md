# calcardbackup

:de: [auf deutsch lesen...](README_GER.md)

This Bash script exports calendars and addressbooks from ownCloud/Nextcloud to .ics and .vcf files and saves them to a compressed file. Additional options are available.

## Contents
- [Requirements](#requirements)
- [Quick Installation Guide](#quick-installation-guide)
- [Upgrading *calcardbackup*](#upgrading-calcardbackup)
- [Options](#options)
- [Usage Examples](#usage-examples)
- [Nextcloud-Snap Users](#nextcloud-snap-users)
- [Synology Users](#synology-users)
- [Considerations about Encryption](#considerations-about-encryption)
- [Does this also work with a broken ownCloud/Nextcloud instance?](#does-this-also-work-with-a-broken-owncloudnextcloud-instance)
- [Links](#links)
- [About Deprecated Option -g|--get-via-http](#about-deprecated-option--g----get-via-http)

## Requirements

- local installation of ownCloud/Nextcloud >= 5.0 with MySQL/MariaDB, PostgreSQL or SQLite3
- command line client appropriate for database type
- the user running the script needs to be able to read the full path to ownClouds/Nextclouds `config.php`, to the script itself and all used configuration files
- GNU Bash >= 4.2 (check with `bash --version`)
- *optional*: package `gnupg` to encrypt backup
- *optional*: package `zip` to compress backup as zip-file  (instead of tar.gz)
- *optional*: package `curl` when using deprecated option `-g|--get-via-http`

## Quick Installation Guide

1. Clone the repository to your server (outside of webroot!) and enter the repo:  
`git clone https://codeberg.org/BernieO/calcardbackup.git`  
`cd calcardbackup`

2. Change the ownership of repo to your webserver's user (here `www-data`):  
`sudo chown -R www-data:www-data .`

3. Run the script as your webserver's user (here `www-data`) and give as first argument the path to your ownCloud/Nextcloud instance (here `/var/www/nextcloud`):  
`sudo -u www-data ./calcardbackup "/var/www/nextcloud"`

4. Check output of script - it will tell, if it needs any other options.

5. Find your backup in directory `backups/`.

There are many more options available: have a look at sections [Options](#options) and [Usage examples](#usage-examples).

#### optional: setup a cronjob for an automatic daily run

Once *calcardbackup* runs without errors, a cronjob can be setup to run it automatically each day as follows:

1. create a logfile and transfer its ownership to the webserver's user (here `www-data`):  
   `sudo touch /var/log/calcardbackup.log`  
   `sudo chown www-data:www-data /var/log/calcardbackup.log`

2. edit the cron table of the webserver's user (here `www-data`) with:  
   `sudo crontab -u www-data -e`  
   and add the following line to the end of the file (change paths to fit your setup!):
   ```text
   0 2 * * * /path/to/calcardbackup/calcardbackup "/var/www/nextcloud" > /var/log/calcardbackup.log 2>&1
   ```

Cron will now execute *calcardbackup* each day at 02:00am.  
The output of the last run is written to `/var/log/calcardbackup.log`.

## Upgrading *calcardbackup*

If you followed the instructions in the [Quick Installation Guide](#quick-installation-guide), you just need to pull the new version to upgrade to the latest version:
```text
cd /path/to/calcardbackup
sudo -u www-data git pull
```

When migrating from GitHub to Codeberg, you need to execute the following command once before pulling the new version:
```text
sudo -u www-data git remote set-url origin "https://codeberg.org/BernieO/calcardbackup.git"
```

:warning: __IMPORTANT:__ users upgrading *calcardbackup* from a version <= 0.7.2 are strongly advised to delete the file with users credentials (it is not needed anymore)!

## Options

All options can be specified in a configuration file or as command line arguments. If started with no options at all or only `-b|--batch`, the script attempts to use file `calcardbackup.conf` in the script's directory as configuration file.  
If no configuration file via option `-c|--configfile` is given, the path to your ownCloud/Nextcloud instance must be the very first argument.  
Find detailed description of all available options below.

```text
Usage: ./calcardbackup [DIRECTORY] [option [argument]] [option [argument]] [option [argument]] ...

Arguments in capital letters to options are mandatory.
Paths (FILE / DIRECTORY) are absolute paths or relative paths to working directory.

-a | --address URL
       Pass URL of ownCloud Installation to script.
       Only required when using option '-g|--get-via-http' for ownCloud < 7.0
-b | --batch
       Batch mode: print nothing to stdout, except for path to backup.
       Depending on configuration this will be:
         - absolute path of compressed backup file
       or, if run with option '-x|--uncompressed' (see below),
         - absolute path of directory containing uncompressed files
-c | --configfile FILE
       Read configuration from FILE. See 'examples/calcardbackup.conf.example'
       All other options except for '-b|--batch' will be ignored!
-d | --date FORMAT
       Use FORMAT as file name extension for backup directory or compressed backup file.
       FORMAT needs to be a format descriptor of the command date().
       The default is -%Y-%m-%d and will result in a directory or file
       named: 'calcardbackup-2017-03-23' or 'calcardbackup-2017-03-23.tar.gz'
       Check 'man date' for more info about different formats and syntax.
-e | --encrypt FILE
       Encrypt backup file with AES256 (gnupg). First line of FILE will be used as passphrase
-g | --get-via-http
       NOTE: this option is deprecated and might be removed in a future version of calcardbackup;
       it is only available to provide backwards compatibility.
       Get calendar/addressbooks via http request from the ownCloud/Nextcloud server.
       When using this option, a file with usernames and according cleartext passwords (see option
       '-u|--usersfile') is mandatory.
       This used to be the default behaviour until calcardbackup <= 0.7.2, but is not recommended
       anymore due to the security issue of cleartext passwords in a separate file.
-h | --help
       Print version number and a short help text 
-i | --include-shares
       Backup shared addressbooks/calendars, too, but only once: e.g. a shared calendar
       won't be backed up if the same calendar was already backed up for another user.
       NOTE: this option will be ignored if not used together with option '-u|--usersfile'.
-ltm | --like-time-machine N
       keep all backups for the last N days, keep only backups created on mondays for the time before.
-na | --no-addressbooks
       Do not backup addressbooks
-nc | --no-calendars
       Do not backup calendars
-o | --output DIRECTORY
       Use directory DIRECTORY to store backups.
       If this option is not given, folder 'backups/' in script's directory is created and used.
-one | --one-file-per-component
       Save each calendar component (e.g. event) and each addressbook component to a separate file
       named: USERNAME-(CALENDARNAME|ADDRESSBOOKNAME)_UID.(ics|vcf)
       In this mode, calcardbackup does not modify the data read from the database except for
       adding CR+LF at the end of the lines according to RFC5545/RFC6350.
       Use this option to investigate faulty database entries or to migrate calendars/addressbooks
       to a Radicale caldav/carddav Server or to vdirsyncer.
       NOTE: this option will be ignored if used together with deprecated option '-g|--get-via-http'
-p | --snap
       This option is mandatory if you are running nextcloud-snap
       (https://github.com/nextcloud/nextcloud-snap). With this option, calcardbackup has to be
       run with sudo (even running as root without sudo will fail!).
-r | --remove N
       Remove backups older than N days from backup folder (N needs to be a positive integer).
-s | --selfsigned
       Let cURL ignore an untrustful (e.g. selfsigned) certificate. With option -g, this is
       mandatory for backup in that case. In any case, cURL is used to retrieve status.php
       of the ownCloud/Nextcloud installation to perform some additional checks. If cURL
       can't access the URL due to an untrustful certificate, calcardbackup will run without
       executing these checks.
-u | --usersfile FILE
       Give location of FILE, which contains users to be backed up. One user per line.
       See 'examples/users.txt.example'
       NOTE: this file is mandatory when run with option '-g|--get-via-http'. In this case
       also passwords of the users to be backed up have to be given in FILE separated by a
       colon from the username. See 'examples/users.txt.example'
-x | --uncompressed
       Do not compress backup folder
-z | --zip
       Use zip to compress backup folder instead of creating a gzipped tarball (tar.gz)

NOTE:  Option '-f|--fetch-from-database' (introduced with calcardbackup 0.6.0) is set as
       default for calcardbackup >= 0.8.0, thus it has no function anymore.
```

## Usage Examples

1. `./calcardbackup /var/www/nextcloud -nc -x`  
Do not backup calendars (`-nc`) and store backed up files uncompressed (`-x`) in folder named `calcardbackup-YYYY-MM-DD` (default) under ./backups/ (default).

2. `./calcardbackup /var/www/nextcloud --no-calendars --uncompressed`  
This is exactly the same command as above but with long options instead of short options.

3. `./calcardbackup -c /etc/calcardbackup.conf`  
Use configuration file /etc/calcardbackup.conf (`-c /etc/calcardbackup.conf`). Parameters for desired behaviour have to be given in that file (see [examples/calcardbackup.conf.example](examples/calcardbackup.conf.example)).  
Don't give any other command line options in this case, because they will be ignored (except for `-b|--batch`).

4. `./calcardbackup`  
Use file calcardbackup.conf in the script's directory as configuration file.  
This is basically the same as example no.3, but with the default location of the configuration file.

5. `./calcardbackup /var/www/nextcloud -b -d .%d.%H -z -e /home/tom/key -o /media/data/backupfolder/ -u /etc/calcardbackupusers -i -r 15`  
Suppress output except for path to the backup (`-b`), use file name extension .DD.HH (`-d .%d.%H`), zip backup (`-z`), encrypt the zipped backup with using the first line in file /home/tom/key as encryption-key (`-e /home/tom/key`), save backup in folder /media/data/backupfolder/ (`-o /media/data/backupfolder/`), only back up items of usernames given in file /etc/calcardbackupusers (`-u /etc/calcardbackupusers`), include users' shared address books/calendars (`-i`) and delete all backups older than 15 days (`-r 15`).

6. `sudo ./calcardbackup /var/snap/nextcloud/current/nextcloud -p`  
This example is for [nextcloud-snap](https://github.com/nextcloud/nextcloud-snap) users. *calcardbackup* will use the cli utility from nextcloud-snap to access the database (`-p`) and backup all calendars/addressbooks found in the database.

7. `./calcardbackup /var/www/nextcloud -ltm 30 -r 180`  
Keep all backups for the last 30 days, but keep only backups created on mondays for the time before (`-ltm 30`) and remove all backups older than 180 days (`-r 180`).  
:warning: Make sure backups are also created on mondays when using option `-ltm`

## Nextcloud-Snap Users

If you are running [Nextcloud-Snap](https://github.com/nextcloud/nextcloud-snap), you have to use option `-p|--snap` to tell *calcardbackup* to use the cli utility `nextcloud.mysql-client` from the snap package.  
In order for this to work, *calcardbackup* has to be run with `sudo` (even running as root without `sudo` will fail).  
As path to Nextcloud use the path to the configuration files of nextcloud. In a standard installation this would be `/var/snap/nextcloud/current/nextcloud`. See [usage example no.6](#usage-examples).

## Synology Users

In Synology DiskStation Manager (DSM) the path to `mysql` needs to be added to the `PATH` variable before running *calcardbackup*. Example:
```text
sudo -u http PATH="$PATH:/usr/local/mariadb10/bin" ./calcardbackup "/volume1/web/nextcloud"
```

## Considerations about Encryption

If you want to use the included encryption possibility, be aware that:
- the files are encrypted by [GnuPG](https://en.wikipedia.org/wiki/GNU_Privacy_Guard), [AES256](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) with the passphrase given in a separate file
- the passphrase is stored in a file. Other users with access to the server might be able to see the passphrase.
- *calcardbackup* is designed to run without user interaction, so there can't be a rock solid encryption. I consider the offered one as sufficient in most cases though.
- if you need rock solid encryption, don't let *calcardbackup* encrypt the backup. Instead, encrypt it yourself.
- command to decrypt (you will be prompted to enter the passphrase):  
`gpg -o OUTPUT_FILE -d FILE_TO_DECRYPT.GPG`

## Does this also work with a broken ownCloud/Nextcloud instance?

__Yes, it does!__ :smiley:

*calcardbackup* only needs the database (and access to it) from an ownCloud/Nextcloud installation to be able to extract calendars/addressbooks from the database and save them as .ics and .vcf files.  
Here is how this can be accomplished:

1. create a dummy Nextcloud directory including subdirectory `config`:  
`mkdir -p /usr/local/bin/nextcloud_dummy/config`

2. create and edit file `config.php` to fit your needs as follows:  
`nano /usr/local/bin/nextcloud_dummy/config/config.php`

   - add database type according to [config.sample.php](https://github.com/nextcloud/server/blob/v14.0.3/config/config.sample.php#L90-L101)

   - for MySQL/MariaDB/PostgreSQL:
     - add according database values according to [config.sample.php](https://github.com/nextcloud/server/blob/v14.0.3/config/config.sample.php#L103-L135)

   - for SQLite3:
     - add path to the nextcloud_dummy folder as 'datadirectory' according to [config.sample.php](https://github.com/nextcloud/server/blob/v14.0.3/config/config.sample.php#L76-L82)
     - copy the SQLite3 database to the nexcloud_dummy directory (filename of the SQLite3 database must be `owncloud.db`):  
     `cp /path/to/owncloud.db /usr/local/bin/nextcloud_dummy/owncloud.db`

   - if the database belongs to an installation of ownCloud <= 8.2, the following line needs to be added:  
     `'version' => '8.0.0',`

3. run *calcardbackup* and give as first argument the path to dummy Nextcloud directory created in step 1:  
`./calcardbackup /usr/local/bin/nextcloud_dummy`

## Links

#### Related Forum Threads
- [help.nextcloud.com](https://help.nextcloud.com/t/calcardbackup-bash-script-to-backup-nextcloud-calendars-and-addressbooks-as-ics-vcf-files/11978) - Nextcloud
- [central.owncloud.org](https://central.owncloud.org/t/calcardbackup-bash-script-to-backup-owncloud-calendars-and-addressbooks-as-ics-vcf-files/7340) - ownCloud

#### Blog articles about *calcardbackup*
- [bob.gatsmas.de](https://bob.gatsmas.de/articles/calcardbackup-jetzt-erst-recht) - October 2018 (german)
- [strobelstefan.org](https://strobelstefan.org/?p=6094) - January 2019 (german)
- [newtoypia.blogspot.com](https://newtoypia.blogspot.com/2019/04/nextcloud.html) - April 2019 (taiwanese)

#### Docker Image for *calcardbackup*
- [hub.docker.com](https://hub.docker.com/r/waja/calcardbackup) - Docker Image by waja

#### ICS and VCF standard
- [RFC 5545](https://tools.ietf.org/html/rfc5545) - Internet Calendaring and Scheduling Core Object Specification (iCalendar)
- [RFC 6350](https://tools.ietf.org/html/rfc6350) - vCard Format Specification

#### Exporter Plugins from SabreDAV used by ownCloud/Nextcloud
- [ICSExportPlugin.php](https://github.com/sabre-io/dav/blob/master/lib/CalDAV/ICSExportPlugin.php) - ICS Exporter `public function mergeObjects`
- [VCFExportPlugin.php](https://github.com/sabre-io/dav/blob/master/lib/CardDAV/VCFExportPlugin.php) - VCF Exporter `public function generateVCF`

&nbsp;

---

&nbsp;

## About Deprecated Option -g | -\-get-via-http

:warning: This option is deprecated and not recommended anymore due to the necessity to give cleartext passwords in a separate file! It might be removed in a future version of *calcardbackup*.

As its default, *calcardbackup* creates calendar and addressbook backups by fetching the according data directly from the database. However, if invoked with option `-g|--get-via-http`, *calcardbackup* is using the legacy method of backing up addressbooks and calendars by downloading the according files from the ownCloud/Nextcloud webinterface. Thus, a file with usernames and passwords is necessary, passed to the script via option `-u|--usersfile FILE`.

Using this option also carries the risk of timeouts resulting in *calcardbackup* not being able to back up large addressbooks.

__To make a long story short:__ all you need to know about option `-g|--get-via-http` is to __NOT__ use it, unless you have a good reason to expose passwords of the users to be backed up.
