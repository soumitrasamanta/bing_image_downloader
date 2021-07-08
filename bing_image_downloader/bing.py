from pathlib import Path
import urllib.request
import urllib
import imghdr
import posixpath
import re
import pandas as pd
from collections import OrderedDict 
from tqdm import tqdm

'''
Python api to download image form Bing.
Author: Guru Prasad (g.gaurav541@gmail.com)
'''


class Bing:
    def __init__(
        self, 
        query, 
        limit, 
        output_dir, 
        adult, 
        timeout,  
        filters='', 
        output_filetype='jpg',
        output_info_filename='images_source_info.xlsx',
        verbose=True,
    ):
        self.download_count = 0
        self.query = query
        self.output_dir = output_dir
        self.adult = adult
        self.filters = filters
        self.output_filetype = output_filetype
        self.output_info_filename = output_info_filename
        self.verbose = verbose

        assert type(limit) == int, "limit must be integer"
        self.limit = limit
        self.len_limit = len(str(limit))
        assert type(timeout) == int, "timeout must be integer"
        self.timeout = timeout
        self.dict_image_source = OrderedDict({
            'image_filename': [None]*self.limit, 
            'url_info': [None]*self.limit
        })

        # self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        self.page_counter = 0
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}

    def save_image(self, link, file_path):
        request = urllib.request.Request(link, None, self.headers)
        image = urllib.request.urlopen(request, timeout=self.timeout).read()
        if not imghdr.what(None, image):
            print('[Error]Invalid image, not saving {}\n'.format(link))
            raise ValueError('Invalid image, not saving {}\n'.format(link))
        with open(str(file_path), 'wb') as f:
            f.write(image)

    
    def download_image(self, link):
        self.download_count += 1
        # Get the image link
        try:
            path = urllib.parse.urlsplit(link).path
            filename = posixpath.basename(path).split('?')[0]
            file_type = filename.split(".")[-1]
                
            if self.verbose:
                # Download the image
                print("[%] Downloading Image #{} from {}".format(self.download_count, link))
            output_filename = ''.join(['image', str(self.download_count).zfill(self.len_limit), '.', self.output_filetype])    
            self.save_image(link, self.output_dir.joinpath(output_filename))
            self.dict_image_source['image_filename'][self.download_count-1] = output_filename
            self.dict_image_source['url_info'][self.download_count-1] = link
            pd.DataFrame.from_dict(self.dict_image_source).to_excel(self.output_dir.joinpath(self.output_info_filename), index=False)
            if self.verbose:
                print("[%] File Downloaded !\n")

        except Exception as e:
            self.download_count -= 1
            print("[!] Issue getting: {}\n[!] Error:: {}".format(link, e))

    
    def run(self):
        while self.download_count < self.limit:
            if self.verbose:
                print('\n\n[!!]Indexing page: {}\n'.format(self.page_counter + 1))
            # Parse the page source and download pics
            request_url = 'https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(self.query) \
                          + '&first=' + str(self.page_counter) + '&count=' + str(self.limit) \
                          + '&adlt=' + self.adult + '&qft=' + ('' if self.filters is None else str(self.filters))
            request = urllib.request.Request(request_url, None, headers=self.headers)
            try:
                response = urllib.request.urlopen(request)
                html = response.read().decode('utf8')
                if html ==  "":
                    print("[%] No more images are available")
                    break
                links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)
            except:
                links = []
                print('Unable to extract data from : "{}"' .format(request_url))
            if self.verbose:
                print("[%] Indexed {} Images on Page {}.".format(len(links), self.page_counter + 1))
                print("="*70)

            for link in links:
                if((self.download_count < self.limit) and (link not in self.dict_image_source['url_info'][:self.download_count])):
                    self.download_image(link)

            self.page_counter += 1
        print('\n[%] Done. Downloaded {} "{}" images.' .format(self.download_count, self.query))
        print("="*70)
        
