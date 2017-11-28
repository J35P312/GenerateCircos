import sys
import os
import argparse
#command: python generate_circos.py prefix input_variants.tab




def main(args):
    #path to the circos executable
    wd= os.path.dirname(os.path.realpath(sys.argv[0]))

    circos_path=os.path.join("{}/circos/bin/circos".format(wd))
    #path of the karyotype file
    karyotype_path=os.path.join("{}/circos/data/karyotype/karyotype.human.txt".format(wd))

    cnv  = open("{}_label_track.txt".format(args.prefix), "w")
    links  = open("{}_links.txt".format(args.prefix), "w")

    chromosomes=set([])
    i=0
    for line in open(args.tab):
        color=False
        if "\t" in line:
            content=line.strip().split("\t")
        elif "," in line:
            content=line.strip().split(",")
        elif " " in line:
            content=line.strip().split(" ")
        elif line[0] == "#":
            continue
        chromosomes.add("hs"+content[0])
        chromosomes.add("hs"+ content[2])
        if content[-1] == "l":
            links.write("var{} hs{} {} {}\n".format(i,content[0],content[1],content[1]))
            links.write("var{} hs{} {} {}\n".format(i,content[2],content[3],content[3]))        

        elif content[0] == content[2]:
            if content[-1] == "g":
                color="color=green"
            elif content[-1] == "r":
                color="color=red"
            elif content[-1] == "b":
                color="color=blue"
            elif content[-1] =="bl":
                color="color=black"
            if color:
                chromosome="hs" + content[0]
                cnv.write("{} {} {} {}\n".format(chromosome,content[1],content[3],color) )
        i+=1
    chromosomes=";".join(chromosomes)
    circos_conf="""
# circos.conf

karyotype = {}
chromosomes_display_default = no
chromosomes_units = 1000000
chromosomes = {}
show_ticks          = yes
show_tick_labels    = yes

<plots>

type            = tile
layers_overflow = collapse

<plot>
file        = {}_label_track.txt
r1          = 0.98r
r0          = 0.95r
orientation = out

layers      = 1
margin      = 0.02u
thickness   = 30
padding     = 8

stroke_thickness = 1
stroke_color     = grey
</plot>

</plots>


<ticks>
radius           = 1r
color            = black
thickness        = 10p

# the tick label is derived by multiplying the tick position
# by 'multiplier' and casting it in 'format':
#
# sprintf(format,position*multiplier)
#

multiplier       = 1e-6

# %d   - integer
# %f   - float
# %.1f - float with one decimal
# %.2f - float with two decimals
#
# for other formats, see http://perldoc.perl.org/functions/sprintf.html

format           = %d

<tick>
spacing        = 5u
size           = 15p
</tick>

<tick>
spacing        = 25u
size           = 25p
show_label     = yes
label_size     = 60p
label_offset   = 10p
format         = %d
</tick>

</ticks>

<links>

<link>
file          = {}_links.txt
radius        = 0.95r
bezier_radius = 0r
color         = black_a4
thickness     = 10
</link>

</links>


<ideogram>

<spacing>
default = 0.005r
</spacing>

# Ideogram position, fill and outline
radius           = 0.8r
thickness        = 120p
fill             = yes
stroke_color     = dgrey
stroke_thickness = 10p

# Minimum definition for ideogram labels.

show_label       = yes
# see etc/fonts.conf for list of font names
label_font       = default 
label_radius     = dims(image,radius) - 100p
label_size       = 100
label_parallel   = yes

show_bands            = yes
fill_bands            = yes
band_stroke_thickness = 2
band_stroke_color     = white
band_transparency     = 0

</ideogram>

################################################################
# The remaining content is standard and required. It is imported 
# from default files in the Circos distribution.
#
# These should be present in every Circos configuration file and
# overridden as required. To see the content of these files, 
# look in etc/ in the Circos distribution.

<image>
# Included from Circos distribution.
<<include etc/image.conf>>
</image>

# RGB/HSV color definitions, color lists, location of fonts, fill patterns.
# Included from Circos distribution.
<<include etc/colors_fonts_patterns.conf>>

# Debugging, I/O an dother system parameters
# Included from Circos distribution.
<<include etc/housekeeping.conf>>
""".format(karyotype_path,chromosomes,args.prefix,args.prefix)

    circos_conf_file=open("{}_circos.conf".format(args.prefix), "w")
    circos_conf_file.write(circos_conf)
    circos_conf_file.close()

    cnv.close()
    links.close()
    print circos_path
    print "{} -conf {}_circos.conf -outputfile {} > run.out".format(circos_path,args.prefix,args.prefix)
    os.system("{} -conf {}_circos.conf -outputfile {} > run.out".format(circos_path,args.prefix,args.prefix))



parser = argparse.ArgumentParser("""GenerateCircos - easy to use tool for generting circos plots""")
parser.add_argument('--tab',required=True,type=str, help="A bedpe file describing which links to draw, the fifth column is set to l,bl,b,g,r for link,black, blue, green, or red ")
parser.add_argument('--prefix',required=True,type=str, help="prefix of the output file")
args= parser.parse_args()
main(args)

