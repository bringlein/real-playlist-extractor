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
- (`CLIPINF` some scene information etc...not relevant for this script)


The file file names *do not match*! I.e. it is *not* required that `0001.rpls` belongs to `0001.m2ps`! 

However, the `.rpls` file contains the name of the `STREAM` file that it describes. Hence, a short script can extract the name (and other metadata) of the `.rpls` files and match it to the video files. 


The script `main.py` does:
1. extracts the title of the playlist file,
2. matches it to the corresponding video file (i.e. extracting the file name),
3. stores the title as id3 tag in the video file,
4. and finally renames/copies the file.

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

RPLS File Format
--------------------

Sadly, I haven't found a lot of information regarding the `.rpls` file structure, but 
```
$ xxd <file>.rpls
```
did help a lot.

### Example
```
$ xxd 0042.rpls
00000000: 504c 5354 3031 3030 0000 0728 0000 0748  PLST0100...(...H
00000010: 0000 07ac 0000 060c 0000 0000 0000 0000  ................
00000020: 0000 0000 0000 0000 0000 05de 0000 1102  ................
00000030: 0200 2042 1123 1534 2800 3431 0103 01a0  .. A.#.4(.41....
00000040: 0001 0003 4156 3100 0000 0000 0000 0000  ....AV1.........
00000050: 0000 0000 0000 0000 1453 4f4d 4520 5641  .........SOME VA
00000060: 4c55 4142 4c45 2054 4954 4c45 2000 0000  LUABLE TITLE ...
00000070: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000080: 0000 0000 0000 0000 0000 0000 0000 0000  ................
....
00000710: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000720: 0000 0000 0000 0000 0000 001c 0001 0001  ................
00000730: 0000 0014 3030 3030 324d 3250 5300 0100  ....00002M2PS...
00000740: 0000 2e18 063b b4f8 0000 0060 0002 0318  .....:.....`....
00000750: 0103 0000 0009 33dc ffff ffff 0000 0000  ......3.........
....
```

So, here the title `SOME VALUABLE TITLE ` has the length of `0x14` and belongs to the file `00002`.`M2PS`.

Consequently to me the file structure appeared as follows:

| Byte address |  Content  |
| 0 -- 3 | `PLST` (header byte or so) |
| 4 -- 7 | version of file structure |
| ....   | .... |
| 88     | `length` of the title field |
| 89 -- 89 + length | the title field |
| ....   |   .... |
| 1842 -- 1846 | file name in `STREAM` folder |
| 1847 -- 1850 | file name ending |
| ....   | .... |


I've also found a [german blog entry](https://schueckvcr.com/2017/10/24/real-playlists-rpls-file-reader/) with some more file structure information, but only parts of the reported structure were valid in my case.



