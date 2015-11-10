# https://pythonhosted.org/setuptools/setuptools.html#namespace-packages
__import__('pkg_resources').declare_namespace(__name__)

import logging
import geojson

def defaults():

    defaults = {
        'id': 0,
        'parent_id': -1,
        'name': '',
        'fullname': '',
        'source': '',
        'path' : '',
        'lastmodified': 0,
        'iso': '',
        'bbox': '',
        'file_hash': '',
        'geom_hash': '',
        'geom_latitude': 0,
        'geom_longitude': 0,
        'lbl_latitude': 0,
        'lbl_longitude': 0,
        'supersedes': '',
        'superseded_by': '',
        }

    return defaults

def dump_file(path):

        try:
            fh = open(path, 'r')
            feature = geojson.load(fh)
        except Exception, e:
            logging.error("failed to load %s, because %s" % (path, e))
            return None

        props = feature['properties']
        placetype = props.get('wof:placetype', None)

        out = defaults

        hash = hash_filehandle(fh)
        out['file_hash'] = hash

        wofid = props.get('wof:id', None)

        if wofid == None:
            logging.warning("%s is missing an wof:id property, using filename" % path)
            fname = os.path.basename(path)
            wofid = fname.replace(".geojson", "")
            
        out['id'] = wofid

        out['parent_id'] = props.get('wof:parent_id', -1)
        
        name = props.get('wof:name', None)
        
        if not name:
            name = props.get('name', None)
            
        if not name:
            name = ""
            
        name = name.encode('utf8')
        out['name'] = name

        source = None

        for k in ('src:geom', 'wof:source', 'wof:datasource'):

            if props.get(k):
                source = props[k]
                break

        if not source:
            logging.warning("%s is missing a source property" % path)
            source = ""

        out['source'] = source
        
        path = path.replace(options.source, "")
        path = path.lstrip("/")
            
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
        
        out['iso'] = props.get('iso:country', '')
        out['lastmodified'] = props.get('wof:lastmodified', 0)
        out['geom_hash'] = props.get('wof:geomhash', '')

        out['geom_latitude'] = props.get('geom:latitude', 0)
        out['geom_longitude'] = props.get('geom:longitude', 0)
        out['lbl_latitude'] = props.get('lbl:latitude', 0)
        out['lbl_longitude'] = props.get('lbl:longitude', 0)

        return out
