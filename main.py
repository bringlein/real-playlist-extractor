# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import os
import sys
import glob
import string
from datetime import datetime


_album_name_ = "My Recordings"


def copy_and_rename_mp4(nr, source_mp4, new_name, target_dir):
    new_file_name = nr + "_" + new_name.replace(" ", "_").replace(".", "-") + ".m4v"
    new_path = os.path.join(target_dir, new_file_name)
    today = datetime.today().strftime('%Y-%m-%d')
    # if you want to convert the files instead of copying, alter the string below
    # e.g. for m2ts/m2ps to mp4 use the following:  -vcodec libx264 -preset veryfast -crf 20 -acodec ac3 -vf "yadif"
    cmd = '/usr/bin/ffmpeg -loglevel quiet -i {} -codec copy -metadata title=\"{}\" -metadata album=\"{}\" ' \
          '-metadata copy_date=\"{}\" {}'.format(
        source_mp4, new_name, _album_name_, today, new_path)
    print(cmd)
    os.system(cmd)


def extract_rpls_metadata(file_path):
    bytes = open(file_path, "rb").read()

    length_byte = 0
    text_start_byte = 0
    if bytes[87] == 0 and bytes[88] > 0:
        # could be vendor specific, adapt if necessary
        length_byte = 88
        text_start_byte = 89
    else:
        print("INVALID RPL FORMAT of file {}\n".format(file_path))
        exit(2)

    name = bytes[text_start_byte:(text_start_byte+bytes[length_byte])]
    # name_orig = name.decode("utf-8")
    name_orig = name.decode("latin-1")

    # check for expected chars
    if bytes[0x732] != 0 and bytes[0x733] != 0x14:
        print("FATAL: {} has not expected bytes at addresses 0x732 and 0x733!\n".format(file_path))
        exit(5)

    # could be vendor specific, adapt if necessary
    file_name_length = 9
    fc = bytes[0x734:0x734+file_name_length].decode("utf-8")
    # ft = fc[-4:].lower()
    # video_file_name = fc[:-4] + "." + ft
    mp4_file_name = fc[:-4] + ".mp4"

    print("found {} for {} in {}".format(name_orig, mp4_file_name, os.path.basename(file_path)))

    # printable = set(string.printable)
    valid_chars = "-_.() %s%säöüïß" % (string.ascii_letters, string.digits)

    # make sure only "safe" characters are used for the metadata / filename
    ret = ''.join(filter(lambda x: x in valid_chars, name_orig))
    return ret, mp4_file_name


def main(rpls_dir, mp4_dir, target_dir):
    # print("working on {}".format(rpls_dir))
    rpl_files = glob.glob(rpls_dir + "/*.rpls")
    rpl_files.sort()
    print(rpl_files)

    mp4_files = glob.glob(mp4_dir + "/*.mp4")
    mp4_files.sort()
    print(mp4_files)

    if len(rpl_files) != len(mp4_files):
        print("ERROR: content of directories aren't matching!\n")
        exit(1)

    for i in range(0, len(rpl_files)):
        cur_rpl = rpl_files[i]
        new_name, mp4_file_name = extract_rpls_metadata(cur_rpl)
        cur_mp4 = os.path.join(mp4_dir, mp4_file_name)
        if cur_mp4 in mp4_files:
            di = mp4_files.index(cur_mp4)
            del mp4_files[di]
        else:
            print("FATAL: extracted file that does not exist: {} from {}.\n".format(cur_mp4, cur_rpl))
            exit(6)
        copy_and_rename_mp4("{:04d}".format(i), cur_mp4, new_name, target_dir)

    print("\n\tDONE.\n")
    if len(mp4_files) > 0:
        print("The following mp4 files were not processed:\n {}".format(mp4_files))
    else:
        print("All files of {} were processed.".format(mp4_dir))


if __name__ == '__main__':
    # usage: python3.8 main.py /path/to/BDAV/PLAYLIST /path/to/BDAV/STREAM/or-other-video-folder /path/to/processed-and-renamed-output-dir
    main(sys.argv[1], sys.argv[2], sys.argv[3])

