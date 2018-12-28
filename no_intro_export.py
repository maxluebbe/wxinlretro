import collections
import os
import pickle
import sys

from xml.etree import ElementTree

import common

# Example file:
#<?xml version="1.0"?>
#<!DOCTYPE datafile PUBLIC "-//Logiqx//DTD ROM Management Datafile//EN" "http://www.logiqx.com/Dats/datafile.dtd">
#<datafile>
#	<header>
#		<name>Sega - Mega Drive - Genesis</name>
#		<description>Sega - Mega Drive - Genesis</description>
#		<version>20181222-195449</version>
#		<author>BigFred, BitLooter, C. V. Reynolds, coraz, dead_screem, Densetsu, DeriLoko3, einstein95, ElBarto, Gefflon, gigadeath, Hiccup, Jack, Money_114, omonim2007, Powerpuff, relax, RetroUprising, Rifu, Special T, sunbeam, Tauwasser, TeamEurope, Vigi, xNo, xuom2</author>
#		<homepage>No-Intro</homepage>
#		<url>http://www.no-intro.org</url>
#	</header>
#   <game name="Battletoads (World)">
#       <description>Battletoads (World)</description>
#       <rom name="Battletoads (World).md" size="524288" crc="D10E103A" md5="F1E299D6EB40E3ECEC6460D96E1E4DC9" sha1="5EF3C29B6BDD04D24552AB200D0530F647AFDB08" status="verified"/>
#   </game>
#</datafile>


def xml_to_dict(xml_filename):
    games_by_sha1 = {}
    tree = ElementTree.parse(xml_filename)
    root = tree.getroot()
    for child in root:
        if child.tag == 'game':
            for t in child:
                if t.tag == 'rom':
                    a = t.attrib
                    size_bytes = int(a['size'])
                    g = common.Game(filename=a['name'], size=size_bytes, crc=a['crc'],
                            md5=a['md5'], sha1=a['sha1'])
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