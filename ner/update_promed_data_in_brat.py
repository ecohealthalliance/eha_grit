import json, contextlib, urllib2, re, os

if __name__ == '__main__':
    default_fudd_url = 'http://54.235.153.252/dev/canepi/api/data/search/healthmap?feed=ProMED%20Mail'
    fudd_url = raw_input('fudd URL (%s):' % default_fudd_url) or default_fudd_url
    fudd_username = raw_input('fudd username:')
    fudd_pw = raw_input('fudd password:')

    default_brat_data_path = '../brat-v1.3_Crunchy_Frog/data/promed/'
    brat_data_path = raw_input('brat data path (%s):' % default_brat_data_path) or default_brat_data_path

    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, fudd_url, fudd_username, fudd_pw)
    urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))

    req = urllib2.Request(fudd_url)

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

                text_file_path = '%s%s.txt' % (brat_data_path, id)
                if not os.path.exists(text_file_path):
                    with open(text_file_path, 'w') as text_file:
                        text_file.write(text)
                        print 'wrote text file %s' % text_file_path

                ann_file_path = '%s%s.ann' % (brat_data_path, id)
                if not os.path.exists(ann_file_path):
                    with open (ann_file_path, 'w') as ann_file:
                        ann_file.write('')
                        print 'wrote ann file %s' % ann_file_path
