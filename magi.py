import os
from dataclasses import dataclass
import json

os.chdir(os.path.dirname(os.path.realpath(__file__)))

OUTDIR = None


@dataclass
class Opskrift:
    filnavn: str = ""
    navn: str = ""
    banner: str = ""
    ingredienser: list = lambda: []
    tid: str = ""
    køkkener: list = lambda: []
    basename: str = ""

    def skriv_til_md(self, udgangsFilnavn):
        with open(udgangsFilnavn, 'w') as f:
            f.write(f'## {self.navn}\n\n')
            f.write(
                f'![KOKKEN HAR VIST GLEMT AT TAGE ET BILLEDE AF MADEN! måske er det ikke instaworthy? hvem ved, kig tilbage i fremtiden.]({self.banner})\n'
            )
            f.write(f'### Tid: {self.tid}\n')
            køkkener = ','.join(self.køkkener)
            f.write(f'### Køkkener: {køkkener}\n')
            f.write(f'### Ingredienser:\n')
            [f.write(f'* {ingrediens}\n') for ingrediens in self.ingredienser]
            f.write(f'### Beskrivelse:\n')
            with open(os.path.splitext(self.filnavn)[0] + ".md") as desc:
                f.write(desc.read())


def parseRecipe(path):
    # open the file
    with open(path, 'r') as f:
        data = json.loads(f.read())
        opskrift = Opskrift()
        opskrift.filnavn = path
        opskrift.basename = os.path.basename(path)
        opskrift.basename = os.path.splitext(opskrift.basename)[0]
        opskrift.banner = data['banner']
        opskrift.navn = data['navn']
        opskrift.ingredienser = data['ingredienser']
        if 'tid' in data:
            opskrift.tid = data['tid']
        opskrift.tid = data['tid']
        if 'køkkener' in data:
            opskrift.køkkener = data['køkkener']
        else:
            opskrift.køkkener = ["N/A"]
        print(opskrift.køkkener)
        return opskrift


def createCookbook():
    with open(os.path.join(OUTDIR, 'README.md'), 'w') as f:
        f.write(f'# Trøffelheltenes opskriftsgrotte\n\n')

        path = os.path.join('opskriftsgrotten', "opskrifter")
        opskrifter = []
        for opskrift in os.listdir(path):
            if opskrift.endswith('.json'):
                opskrift = parseRecipe(os.path.join(path, opskrift))
                opskrift.skriv_til_md(
                    os.path.join(OUTDIR, opskrift.basename + ".md"))
                opskrifter.append(opskrift)

        f.write(f'## Opskrifter:\n')
        [
            f.write(f'* [{opskrift.navn}]({opskrift.basename}.md)\n')
            for opskrift in opskrifter
        ]


if __name__ == '__main__':
    # argparser with an optional buildsite argument
    import argparse
    parser = argparse.ArgumentParser(
        description='Create a cookbook from the opskriftsgrotten')
    parser.add_argument('--buildsite',
                        action='store_true',
                        help='Build the site')
    args = parser.parse_args()

    if args.buildsite:
        OUTDIR = 'docs'
    else:
        OUTDIR = 'udgangsmappe'

    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)

    createCookbook()
