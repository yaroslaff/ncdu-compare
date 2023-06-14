# ncdu-compare
Compare ncdu export files and shows differences to find out what consumes most space.

## Installation

~~~
# from pypi
pip3 install ncdu-compare

# ... or from git
pip3 install git+https://github.com/yaroslaff/ncdu-compare.git
~~~

## Example usage

~~~bash
# measure current /var/log 
$ ncdu /var/log/ -0o /tmp/1

# create extra 1M file... and just wait
$ sudo dd if=/dev/zero of=/var/log/zzz.log bs=1M count=1
1+0 records in
1+0 records out
1048576 bytes (1.0 MB, 1.0 MiB) copied, 0.00229604 s, 457 MB/s

# measure /var/log again
$ ncdu /var/log/ -0o /tmp/2

# see top usage
$ ncdu-compare /tmp/1 /tmp/2 | sort -n | tail -n 5
575 FILE /var/log/auth.log (273797 > 274372)
12209 FILE /var/log/daemon.log (62452009 > 62464218)
12286 FILE /var/log/syslog (63463377 > 63475663)
1048576 FILE /var/log/zzz.log (0 > 1048576)
1074015 DIR /var/log (3895153251 > 3896227266)
~~~

## Invalid unicode filenames
Sometimes ncdu can produce invalid JSON files (see https://dev.yorhel.nl/ncdu/jsonfmt). When loading ncdu files ncdu-compare uses (default) 'replace' mode to handle unicode errors. You can  override it with `-e`/`--error` options, e.g. `--error ignore`. More at python doc to [open()](https://docs.python.org/3/library/functions.html#open).

## See also

My other project [Plus Size](https://github.com/yaroslaff/pluss) to detect changes in short-time (e.g. fast growing log files)

[ncdu-diff](https://github.com/lilydjwg/ncdu-diff) C + Python ncdu fork that can compare and diff results

