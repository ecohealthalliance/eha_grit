import json, contextlib, urllib2, re, os
from optparse import OptionParser

if __name__ == '__main__':

    parser = OptionParser()
    default_fudd_url = 'http://54.235.153.252/dev/canepi/api/data/search/healthmap?feed=ProMED%20Mail'
    parser.add_option('--fudd-url', dest='fudd_url', default=default_fudd_url)

    parser.add_option('-u', dest='fudd_username')
    parser.add_option('-p', dest='fudd_pw')

    default_brat_data_path = '/var/www/brat/data/promed/'
    parser.add_option('--brat-path', dest='brat_data_path', default=default_brat_data_path)

    (options, args) = parser.parse_args()

    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, options.fudd_url, options.fudd_username, options.fudd_pw)
    urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))

    req = urllib2.Request(options.fudd_url)

    with contextlib.closing(urllib2.urlopen(req)) as fudd_data:
        data = json.loads(fudd_data.read())
        features = data.get('features')

        for feature in features:
            props = feature.get('properties')
            id = props.get('healthmap_id')
            link = props.get('link')

            with contextlib.closing(urllib2.urlopen(link)) as l:
                text = l.read()
                text = re.compile(r'<style type="text/css">[^<]*?</style>').sub('', text)
                text =  re.compile(r'<.*?>').sub(' ', text)

                text_file_path = '%s%s.txt' % (options.brat_data_path, id)
                if not os.path.exists(text_file_path):
                    with open(text_file_path, 'w') as text_file:
                        text_file.write(text)
                        print 'wrote text file %s' % text_file_path

                ann_file_path = '%s%s.ann' % (options.brat_data_path, id)
                if not os.path.exists(ann_file_path):
                    with open (ann_file_path, 'w') as ann_file:
                        ann_file.write('')
                        print 'wrote ann file %s' % ann_file_path
