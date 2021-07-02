![GitHub top language](https://img.shields.io/github/languages/top/gurugaurav/bing_image_downloader)
![GitHub](https://img.shields.io/github/license/gurugaurav/bing_image_downloader)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fgurugaurav%2Fbing_image_downloader&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
## Bing Image Downloader*

<hr>

Python library to download bulk of images form Bing.com.
This package uses async url, which makes it very fast while downloading.<br/>


### Disclaimer<br />

This program lets you download tons of images from Bing.
Please do not download or use any image that violates its copyright terms. 

### Installation <br />

```bash
python -m pip install git+https://github.com/soumitrasamanta/bing_image_downloader.git
```

### Usage <br />
```python
from bing_image_downloader import downloader
query = 'cat'
downloader.download(query, limit=10,  output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60, output_filetype='jpg', output_info_filename=query+'_images_source_info.xlsx', verbose=True)

```

`query` : String to be searched.<br />
`limit` : (optional, default is `100`) Number of images to download.<br />
`output_dir` : (optional, default is `'dataset'`) Name of output dir.<br />
`adult_filter_off` : (optional, default is `True`) Enable of disable adult filteration.<br />
`force_replace` : (optional, default is `False`) Delete folder if present and start a fresh download.<br />
`timeout` : (optional, default is `60`) timeout for connection in seconds.<br />
`output_filetype` : (optional, default is `jpg`) output image file type.<br />
`output_info_filename` : (optional, default is `'query_images_source_info.xlsx'`) to save images source in a xlsx file.<br />
`verbose` : (optional, default is `True`) Enable downloaded message.<br />


## *Updated version of https://github.com/gurugaurav/bing_image_downloader



