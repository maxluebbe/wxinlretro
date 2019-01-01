import collections
import os
import pickle
import sys

from xml.etree import ElementTree

import common

# Example File:
# <?xml version="1.0" encoding="utf-16"?>
# <database version="1.0" conformance="strict" agent="NesCartDB" author="BootGod" timestamp="Mon Aug 21 23:55:50 2017">
# 	<game name="Battletoads" class="Licensed" catalog="NES-8T-USA" publisher="Tradewest" developer="Rare" region="USA" players="2" date="1991-06">
#		<cartridge system="NES-NTSC" crc="279710DC" sha1="D85C9FF489672534FBF61A15F8FA56FFF489A34B" dump="ok" dumper="bootgod" datedumped="2005-09-21">
#			<board type="NES-AOROM" pcb="NES-AOROM-03" mapper="7">
#				<prg name="NES-8T-0 PRG" size="256k" crc="279710DC" sha1="D85C9FF489672534FBF61A15F8FA56FFF489A34B"/>
#				<vram size="8k"/>
#				<chip type="74xx161"/>
#				<cic type="6113B1"/>
#			</board>
#		</cartridge>
#	</game>
# </database>

def xml_to_dict(xml_filename):
    games_by_sha1 = {}
    tree = ElementTree.parse(xml_filename)
    root = tree.getroot()
    for child in root:
        if child.tag == 'game':
            name = child.attrib['name'] + '_noheader.bin'
            for t in child:
                if t.tag == 'cartridge':
                    a = t.attrib
                    size_bytes = -1 # TODO: Sum PRG, CHR. int(a['size'])
                    md5 = ''# TODO: MD5 not available in this dataset.
                    # TODO: Break out chr/prg hashes to support partial backups.
                    g = common.Game(filename=name, size=size_bytes, crc=a['crc'],
                            md5=md5, sha1=a['sha1'])
                    games_by_sha1[g.sha1] = g
    return games_by_sha1


def main(argv):
    if len(argv) != 2:
        print('Usage: python3 %s xml_filename' % argv[0])
        return 1
    
    games_by_sha1 = xml_to_dict(argv[1])
    game_count = len(games_by_sha1)
    print("%d Games read from file." % game_count)

    file_base, _ = os.path.splitext(os.path.basename(argv[1]))
    out_file = file_base + '.p'
    pickle.dump(games_by_sha1, open(out_file, "wb"))
    print("Dictionary written to %s\n" % out_file)


if __name__ == '__main__':
    main(sys.argv)