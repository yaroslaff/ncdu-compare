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

Create ncdu snapshots with command:

~~~bash
# now
$ ncdu /some/path/ -0o /tmp/snapshot-1

# after some time, e.g. daily
$ ncdu /some/path/ -0o /tmp/snapshot-2
~~~

Compare it
~~~bash
$ ncdu-compare /tmp/snapshot-1 /tmp/snapshot-2 | sort -n | tail -n 5
~~~

Example real output (first number is growth in bytes for `sort -n`, may be negative):
~~~
2125273220 DIR /home/username/public_html/client-portal/storage/framework/cache (18.96G => 21.09G (2.13G))
2125273220 DIR /home/username/public_html/client-portal/storage/framework/cache/data (18.96G => 21.09G (2.13G))
2125741830 DIR /home/username/public_html/client-portal/storage/framework (18.97G => 21.10G (2.13G))
2153400708 DIR /home/username/public_html/client-portal/storage (19.29G => 21.44G (2.15G))
3134727368 DIR /home/username/public_html/client-portal/public/alavie/customer_folder (36.76G => 39.90G (3.13G))
3146881276 DIR /home/username/public_html/client-portal/public/alavie (52.62G => 55.77G (3.15G))
4649987199 DIR /home/username/public_html/client-portal/public (158.13G => 162.78G (4.65G))
6803387907 DIR /home/username/public_html/client-portal (177.97G => 184.78G (6.80G))
6805286889 DIR /home/username/public_html (179.92G => 186.73G (6.81G))
~~~

## Invalid unicode filenames
Sometimes ncdu can produce invalid JSON files (see https://dev.yorhel.nl/ncdu/jsonfmt). When loading ncdu files ncdu-compare uses (default) 'replace' mode to handle unicode errors. You can  override it with `-e`/`--error` options, e.g. `--error ignore`. More at python doc to [open()](https://docs.python.org/3/library/functions.html#open).

## See also

My other project [Plus Size](https://github.com/yaroslaff/pluss) to detect changes in short-time (e.g. fast growing log files)

[ncdu-diff](https://github.com/lilydjwg/ncdu-diff) C + Python ncdu fork that can compare and diff results

