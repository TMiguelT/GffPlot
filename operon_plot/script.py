import dnaplotlib as dpl
import matplotlib.pyplot as plt
from matplotlib import gridspec
from dataclasses import dataclass
from pathlib import Path
import matplotlib

import argparse


@dataclass
class Region:
    contig: str
    start: int
    end: int

    @staticmethod
    def parse(region_str: str) -> 'Region':
        """
        Takes a string of the form "chr:start-end"
        """
        contig, region = region_str.split(':')
        start, end = region.split('-')

        return Region(
            contig=contig,
            start=int(start),
            end=int(end)
        )


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('region', help='The genomic region to plot, in the format chr:start-end', type=Region.parse)
    parser.add_argument('gff', help='Path to a GFF file from which to read the gene annotations', type=Path)
    return parser


def main(gff: Path, region: Region):
    # import gffutils
    # db = gffutils.create_db(str(gff), dbfn='test.db', force=True, keep_order=True, merge_strategy='merge',
    #                         sort_attribute_values=True)
    # print(list(db.region(region=(region.contig, region.start, region.end), completely_within=False)))
    cmap = matplotlib.cm.get_cmap('tab10')

    # Load the design from a GFF file
    design = dpl.load_design_from_gff(str(gff), region.contig, region=[region.start - 1, region.end])
    for i, gene in enumerate(design):
        gene['opts']['label'] = gene['name']#gene['opts'].get('old_locus_tag')#
        if i % 2 == 0:
            gene['opts']['label_y_offset'] = -5
        else:
            gene['opts']['label_y_offset'] = 5
        gene['opts']['label_size'] = 4
        gene['opts']['color'] = matplotlib.colors.rgb2hex(cmap(i % cmap.N))

    # Create the DNAplotlib renderer
    dr = dpl.DNARenderer(scale=8, linewidth=0.8)
    # part_renderers = dr.SBOL_part_renderers()
    part_renderers = dr.trace_part_renderers()

    # Create the figure
    fig = plt.figure(figsize=(5.0, 0.6))
    gs = gridspec.GridSpec(1, 1)
    ax_dna = plt.subplot(gs[0])

    # Redender the DNA to axis
    start, end = dr.renderDNA(ax_dna, design, part_renderers)
    dna_len = end - start
    ax_dna.set_xlim([start - 20, end + 20])
    ax_dna.set_ylim([-8, 8])
    ax_dna.plot([start - 20, end + 20], [0, 0], color=(0, 0, 0), linewidth=0.5, zorder=1)
    ax_dna.axis('off')
    plt.subplots_adjust(hspace=.08, left=.12, right=.99, top=0.99, bottom=0.02)
    # ax_dna.set_xlim([start, end])
    # ax_dna.set_ylim([-15, 15])
    # ax_dna.set_aspect('equal')
    # ax_dna.axis('off')

    # Update subplot spacing
    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)

    # Save the figure
    fig.savefig(gff.with_suffix('.png'), dpi=300)

    # Clear the plotting cache
    plt.close('all')


if __name__ == '__main__':
    args = get_parser().parse_args()
    main(
        gff=args.gff,
        region=args.region
    )
