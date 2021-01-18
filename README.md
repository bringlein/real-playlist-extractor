Real Playlist Metadata Readout
===============================

A python script to extract meta data of Blu-Ray Real Playlist (`.rpls`) folder.

Background
-------------

RPLS is used by some vendors for the BDAV [(Blu-ray Disc Audio/Visual)](https://en.wikipedia.org/wiki/Blu-ray#Application_format) format of Blu-Ray discs to store the metadata of the recorded videos.

BDAV is intended to be used by consumer to safe recorded videos, including from personal camcorders. 
But it is also used by some DVR/AVR vendors (e.g. Panasonic) as file system for the external HDD.


The BDAV [file structure](https://en.wikipedia.org/wiki/Blu-ray#Directory_and_file_structure) is as follows:
```
BDAV/
├── info.bdav
├── menu.something
├── CLIPINF
│   ├── 00001.clpi
│   ├── 00002.clpi
│   ├── 00003.clpi
│   ├── .....
├── PLAYLIST
│   ├── 00001.rpls
│   ├── 00002.rpls
│   ├── 00003.rpls
│   ├── .....
└── STREAM
    ├── 00001.m2ts
    ├── 00002.m2ps
    ├── 00003.m2ps
    ├── .....
```

- `PLAYLIST` contains the metadata of the videos
- `STREAM`  contains the videos
- (`CLIPINF` some scene information etc...not relevant for this script).


The file file names *do not match*! I.e. it is *not* required that `0001.rpls` belongs to `0001.m2ps`! 

However, the `.rpls` file contains the name of the `STREAM` file that it describes. Hence, a short script can extract the name (and other metadata) of the `.rpls` files and match it to the video files. 


The script `main.py` extracts the title of the playlist file, matches it to the corresponding video file, stores the title as id3 tag in the file, and finally renames the file.

Usage
-------

```
$ python3.8 main.py /path/to/BDAV/PLAYLIST /path/to/BDAV/STREAM/or-other-video-folder /path/to/processed-and-renamed-output-dir
```
For further details, please see my blog.

### License

Apache 2.0


### Requirements

python 3.8 (other python 3.4+ versions may work as well).


