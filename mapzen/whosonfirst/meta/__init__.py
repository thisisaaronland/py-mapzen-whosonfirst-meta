import os
import logging
import hashlib
import geojson
import csv

import atomicwrites

import mapzen.whosonfirst.utils

def update_metafile(source_meta, dest_meta, updated, **kwargs):

    features = {}

    for path in updated:

        path = os.path.abspath(path)

        # See what's going on here - it is something between not
        # awesome and wildly inefficient. It is possible and likely
        # and just generally more better that we can and will
        # simply parse the filename and extract the ID accordingly.
        # The thing is that we need (want) to pass a file to the
        # dump_row function in order to generate a file_hash which 
        # a bunch of other services use for detecting changes.
        # So, in the meantime this is what we're doing...
        # (20151111/thisisaaronland)

        feature = mapzen.whosonfirst.utils.load_file(path)

        props = feature['properties']
        wofid = props['wof:id']
        
        features[wofid] = path
        
    source_fh = open(source_meta, 'r')
    reader = csv.DictReader(source_fh)

    writer = None

    with atomicwrites.atomic_write(dest_meta, mode='wb', overwrite=True) as dest_fh:

        for row in reader:

            id = row['id']
            id = int(id)

            if features.get(id, False):

                logging.debug("update row for %s in %s" % (id, dest_meta))
                
                path = features[id]
                row = mapzen.whosonfirst.meta.dump_file(path, **kwargs)

                del(features[id])

            if not writer:
                fn = fieldnames()
                writer = csv.DictWriter(dest_fh, fieldnames=fn)
                writer.writeheader()

            writer.writerow(row)

        for wofid, path in features.items():

            row = mapzen.whosonfirst.meta.dump_file(path, **kwargs)
            writer.writerow(row)

    # https://github.com/whosonfirst/py-mapzen-whosonfirst-meta/issues/2

    perms = kwargs.get('perms', 0644)

    if perms != None:
        os.chmod(dest_meta, perms)

def defaults():

    defaults = {
        'id': 0,
        'parent_id': -1,
        'name': '',
        'placetype': '',
        'fullname': '',
        'source': '',
        'path' : '',
        'lastmodified': 0,
        'iso': '',		# deprecated in favour of PREFIX_country (20160127/thisisaaronland)
        'iso_country': '',
        'wof_country': '',
        'bbox': '',
        'file_hash': '',
        'geom_hash': '',
        'geom_latitude': 0,
        'geom_longitude': 0,
        'lbl_latitude': 0,
        'lbl_longitude': 0,
        'supersedes': '',
        'superseded_by': '',
        'inception': '',
        'cessation': '',
        'deprecated': '',	# deprecated date, not deprecated (20160127/thisisaaronland)
        'country_id': 0,
        'region_id': 0,
        'locality_id': 0,
        }

    return defaults

def fieldnames():

    stub = defaults()
    fieldnames = stub.keys()
    fieldnames.sort()

    return fieldnames

def dump_file(path, **kwargs):

        try:
            fh = open(path, 'r')
            feature = geojson.load(fh)
        except Exception, e:
            logging.error("failed to load %s, because %s" % (path, e))
            return None

        props = feature['properties']
        placetype = props.get('wof:placetype', None)

        out = defaults()

        hash = hash_filehandle(fh)
        out['file_hash'] = hash

        wofid = props.get('wof:id', None)

        if wofid == None:
            logging.warning("feature is missing an wof:id property!")
            return None

            # fname = os.path.basename(path)
            # wofid = fname.replace(".geojson", "")
            
        out['id'] = wofid

        out['parent_id'] = props.get('wof:parent_id', -1)
        
        name = props.get('wof:name', None)
        
        if not name:
            name = props.get('name', None)
            
        if not name:
            name = ""
            
        name = name.encode('utf8')
        out['name'] = name

        out['placetype'] = props.get('wof:placetype')

        source = None

        for k in ('src:geom', 'wof:source', 'wof:datasource'):

            if props.get(k):
                source = props[k]
                break

        if not source:
            logging.warning("%s is missing a source property" % path)
            source = ""

        out['source'] = source
        
        if kwargs.get('paths', 'absolute') == 'relative':
            path = mapzen.whosonfirst.utils.id2relpath(wofid)
            
        out['path'] = path

        bbox = feature.get('bbox', None)
        
        if bbox:
            bbox = map(str, bbox)
            bbox = ",".join(bbox)
            out['bbox'] = bbox

        supersedes = props.get('wof:supersedes', [])
        superseded_by = props.get('wof:superseded_by', [])

        out['supersedes'] = ",".join(map(str, supersedes))
        out['superseded_by'] = ",".join(map(str, superseded_by))
        
        out['iso'] = props.get('iso:country', '')		# deprecated (20160127/thisisaaronland)
        out['iso_country'] = props.get('iso:country', '')
        out['wof_country'] = props.get('iso:country', '')

        out['lastmodified'] = props.get('wof:lastmodified', 0)
        out['geom_hash'] = props.get('wof:geomhash', '')

        out['geom_latitude'] = props.get('geom:latitude', 0)
        out['geom_longitude'] = props.get('geom:longitude', 0)
        out['lbl_latitude'] = props.get('lbl:latitude', 0)
        out['lbl_longitude'] = props.get('lbl:longitude', 0)

        out['inception'] = props.get('edtf:inception', '')
        out['cessation'] = props.get('edtf:cessation', '')
        out['deprecated'] = props.get('edtf:deprecated', '')

	# this should never happen but still does so rather than shout at the sky
        # we'll just try to handle it gracefully (20161109/thisisaaronland)

        parent_id = props.get('wof:parent_id', -1)
        parent_hier = None

        hiers = props.get('wof:hierarchy', [])

        if len(hiers) == 1:
            parent_hier = hiers[0]

        elif parent_id != -1:

            for h in hiers:

                for ignore, id in h.items():
                    if id == parent_id:
                        parent_hier = h
                        break

                if parent_hier:
                    break

        else:
            pass

        if parent_hier:
            out['country_id'] = parent_hier.get('country_id', 0)
            out['region_id'] = parent_hier.get('region_id', 0)
            out['locality_id'] = parent_hier.get('locality_id', 0)

        return out

def hash_file(path):
    fh = open(path, 'r')
    return hash_filehandle(fh)

def hash_filehandle(fh):
    fh.seek(0)
    hash = hashlib.md5(fh.read()).hexdigest()
    return hash
