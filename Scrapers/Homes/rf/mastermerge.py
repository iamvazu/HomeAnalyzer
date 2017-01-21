#-------------------------------------------------------------------------------
# Name:        master merge
# Purpose:
#
# Author:      Lord Azu
#
# Created:     04/01/2017
# Copyright:   (c) Lord Azu 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#cut and pasted from SO
import glob

interesting_files = glob.glob("*.csv")



def main():
    header_saved = False
    with open('Masterfile.csv','w') as fout:
        for filename in interesting_files:
            try:
                with open(filename) as fin:
                    header = next(fin)
                    if not header_saved:
                        try:
                            fout.write(header)
                            header_saved = True
                        except Exception as e:
                            print (e)

                    for line in fin:
                        fout.write(line)
            except Exception as e:
                print (e)


if __name__ == '__main__':
    main()
