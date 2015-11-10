# py-mapzen-whosonfirst-meta

Simple Python utilities for working with Who's On First meta files.

**THIS IS WORK IN PROGRESS**

## Usage

TBW

## Utilities

### wof-dump-meta

A simple utility to dump one or more WOF files to `STDOUT` as "meta" files.

```
$> /usr/local/bin/wof-dump-meta /usr/local/mapzen/whosonfirst-data/data/857/848/31/85784831.geojson
bbox,file_hash,fullname,geom_hash,geom_latitude,geom_longitude,id,iso,lastmodified,lbl_latitude,lbl_longitude,name,parent_id,path,source,superseded_by,supersedes
"-73.6318442408,45.5000240857,-73.5891723633,45.5275166771",2e5920fdd2c3f2d8048e02a76a3ff8af,,3ab0096772e41bb5f866bdf993665683,45.515446291578,-73.61104958857936,85784831,,1447127503,45.5162582006,-73.6072397139,Outremont,101736545,/usr/local/mapzen/whosonfirst-data/data/857/848/31/85784831.geojson,quattroshapes,,
```

See the way those paths are absolute? To specifify relative paths pass in the `-r` and the `-s /path/to/trim` flags, like this:

```
$> /usr/local/bin/wof-dump-meta -r -s /usr/local/mapzen/whosonfirst-data/data /usr/local/mapzen/whosonfirst-data/data/857/848/31/85784831.geojson
bbox,file_hash,fullname,geom_hash,geom_latitude,geom_longitude,id,iso,lastmodified,lbl_latitude,lbl_longitude,name,parent_id,path,source,superseded_by,supersedes
"-73.6318442408,45.5000240857,-73.5891723633,45.5275166771",2e5920fdd2c3f2d8048e02a76a3ff8af,,3ab0096772e41bb5f866bdf993665683,45.515446291578,-73.61104958857936,85784831,,1447127503,45.5162582006,-73.6072397139,Outremont,101736545,857/848/31/85784831.geojson,quattroshapes,,
```

## See also

* https://github.com/whosonfirst/whosonfirst-data