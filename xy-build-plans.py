#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--mode", required=True)
args = parser.parse_args()

template = """
[buildPlans.{font-id}]
family = "{font-name}"           # Font menu family name
spacing = "{spacing}"            # Optional; Values: `normal`, `term`, `fontconfig-mono`, or `fixed`
serifs = "{serif}"               # Optional; Values: `sans` or `slab`
noCvSs = true                  # Disables cv## and ss## OpenType features
noLigation = true               # Disables ligations.
exportGlyphNames = false       # Set this to true for ligature support in Kitty (increased file size)

[buildPlans.{font-id}.variants.design]
percent = 'dots'
asterisk = 'hex-low'
brace = 'straight'

[buildPlans.{font-id}.variants.italic]
g = 'double-storey'

###################################################################################################
# Configure ligations

# [buildPlans.{font-id}.ligations]
# inherits = "default-calt"   # Optional; inherits an existing ligation set
# disables = []               # Optional; disable specific ligation groups, overrides inherited ligation set
# enables  = []               # Optional; enable specific ligation groups, overrides inherited ligation set

# End ligation section
###################################################################################################

###################################################################################################
# Override default building weights
# When buildPlans.<plan name>.weights is absent, all weights would built and mapped to
# default values.
# IMPORTANT : Currently "menu" and "css" property only support numbers between 0 and 1000.
#             and "shape" properly only supports number between 100 and 900 (inclusive).
#             If you decide to use custom weights you have to define all the weights you
#             plan to use otherwise they will not be built.
[buildPlans.{font-id}.weights.regular]
shape = {weight-regular}  # Weight for glyph shapes.
menu  = 400  # Weight for the font's names.
css   = 400  # Weight for webfont CSS.

[buildPlans.{font-id}.weights.book]
shape = {weight-book}
menu  = 450  # Use 450 here to name the font's weight "Book"
css   = 450

[buildPlans.{font-id}.weights.bold]
shape = {weight-bold}
menu  = 700
css   = 700

# End weight section
###################################################################################################

###################################################################################################
# Override default building slope sets
# Format: <upright|italic|oblique> = <"normal"|"italic"|"oblique">
# When this section is absent, all slopes would be built.

[buildPlans.{font-id}.slopes.upright]
angle = 0             # Angle in degrees. Valid range [0, 15]
shape = "upright"     # Slope grade used for shape selection.  `upright` | `oblique` | `italic`
menu  = "upright"     # Slope grade used for naming.           `upright` | `oblique` | `italic`
css   = "normal"      # Slope grade used for webfont CSS.      `normal`  | `oblique` | `italic`

[buildPlans.{font-id}.slopes.oblique]
angle = 9.4
shape = "oblique"
menu  = "oblique"
css   = "oblique"

[buildPlans.{font-id}.slopes.italic]
angle = 9.4
shape = "italic"
menu  = "italic"
css   = "italic"

# End slope section
###################################################################################################

###################################################################################################
# Override default building widths
# When buildPlans.<plan name>.widths is absent, all widths would built and mapped to
# default values.
# IMPORTANT : Currently "shape" property only supports numbers between 434 and 664 (inclusive),
#             while "menu" only supports integers between 1 and 9 (inclusive).
#             The "shape" parameter specifies the unit width, measured in 1/1000 em. The glyphs'
#             width are equal to, or a simple multiple of the unit width.
#             If you decide to use custom widths you have to define all the widths you plan to use,
#             otherwise they will not be built.

[buildPlans.{font-id}.widths.normal]
shape = 500        # Unit Width, measured in 1/1000 em.
menu  = 5          # Width grade for the font's names.
css   = "normal"   # "font-stretch' property of webfont CSS.

[buildPlans.{font-id}.widths.extended]
shape = 600
menu  = 7
css   = "expanded"

# End width section
###################################################################################################

###################################################################################################
# Collect plans

[collectPlans.{font-id}]
release = true
from = ["{font-id}"]
"""

default_fields = {
    "font-id": None,
    "font-name": None,
    "serif": "sans",
    # FIXME: `fixed` does not work in st for some reason after 2022-10-01.
    "spacing": "term",
    "weight-regular": "400",
    "weight-book": "450",
    "weight-bold": "700",
}

instances = [
    {
        "font-id": "iosevka-xy-mono",
        "font-name": "Iosevka XY Mono",
    },
    {
        "font-id": "iosevka-xy-mono-ui",
        "font-name": "Iosevka XY Mono UI",
        "weight-regular": "350",
        "weight-book": "350",
        "weight-bold": "600",
    },
]

if args.mode == "generate-build-plans":
    output = "private-build-plans.toml"
    f = open(output, "w")
    for instance in instances:
        final_instance = {}
        for k in default_fields:
            final_instance[k] = instance.get(k, default_fields[k])
            pass
        f.write(template.format(**final_instance))
        pass
elif args.mode == "print-build-targets":
    sys.stdout.write(" ".join("super-ttc::{}".format(instance["font-id"]) for instance in instances))
elif args.mode == "print-package-paths":
    sys.stdout.write(" ".join("{}.ttc".format(instance["font-id"]) for instance in instances))
else:
    sys.stderr.write("Unknown mode {}\n".format(args.mode))
    sys.exit(1)
    pass
