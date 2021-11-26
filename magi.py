import os
from dataclasses import dataclass
import json

os.chdir(os.path.dirname(os.path.realpath(__file__)))

OUTDIR = None

@dataclass
class Opskrift:
    filnavn: str = ""
    navn: str = ""
    ingredienser: list = lambda: []
    beskrivelse: str = ""
    tid: str = ""
    køkken: str = ""
    kommentarer: str = ""
    fremgangsmetode: str = ""

    def skriv_til_md(self, udgangsFilnavn):
        with open(udgangsFilnavn, 'w') as f:
            f.write(f'## {self.navn}\n\n')
            f.write(f'### Beskrivelse: {self.beskrivelse}\n')
            f.write(f'### Tid: {self.tid}\n')
            f.write(f'### Køkken: {self.køkken}\n')
            f.write(f'### Ingredienser:\n')
            [f.write(f'* {ingrediens}\n') for ingrediens in self.ingredienser]
            f.write(f'### Fremgangsmetode:\n')
            f.write(f'{self.fremgangsmetode}\n')
            f.write(f'### Kommentarer:\n')
            f.write(f'{self.kommentarer}')


def parseRecipe(path):
    # open the file
    with open(path, 'r') as f:
        data = json.loads(f.read())
        opskrift = Opskrift()
        opskrift.filnavn = os.path.basename(path)
        opskrift.filnavn = os.path.splitext(opskrift.filnavn)[0]
        opskrift.navn = data['navn']
        opskrift.ingredienser = data['ingredienser']
        opskrift.beskrivelse = data['beskrivelse']
        if 'tid' in data:
            opskrift.tid = data['tid']
        opskrift.tid = data['tid']
        if 'køkken' in data:
            opskrift.køkken = data['køkken']
        if 'kommentarer' in data:
            opskrift.kommentarer = data['kommentarer']
        return opskrift


def createCookbook():
    with open(os.path.join(OUTDIR, 'README.md'), 'w') as f:
        f.write(f'# Trøffelheltenes opskriftsgrotte\n\n')

        path = os.path.join('opskriftsgrotten', "opskrifter")
        opskrifter = []
        for opskrift in os.listdir(path):
            if opskrift.endswith('.json'):
                opskrift = parseRecipe(os.path.join(path, opskrift))
                opskrift.skriv_til_md(os.path.join(OUTDIR, opskrift.filnavn + ".md"))
                opskrifter.append(opskrift)

        f.write(f'## Opskrifter:\n')
        [f.write(f'* [{opskrift.navn}]({opskrift.filnavn}.md)\n') for opskrift in opskrifter]


if __name__ == '__main__':
    # argparser with an optional buildsite argument
    import argparse
    parser = argparse.ArgumentParser(description='Create a cookbook from the opskriftsgrotten')
    parser.add_argument('--buildsite', action='store_true', help='Build the site')
    args = parser.parse_args()

    if args.buildsite:
        OUTDIR = 'docs'
    else:
        OUTDIR = 'udgangsmappe'

    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)

    createCookbook()
