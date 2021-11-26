## Det her skal gøres:

- Lav en ordentlig hjemmeside
- Start Github actions CI som skal tjekke at alle opskrifter er korrekt formatteret:
  - En opskrift skal have felterne:
    - Navn
    - beskrivelse
    - Fremgangsmetode
    - Tid
    - køkken
    - ingredienser
    - der skal være et billede under "opskriftsgrotten/opskrifter/billeder" der hedder det samme som opskriftfilen... eller også så bare lav et script der google opskriftnavnet og henter det første billede på google, idk
  - Constraints er:
    - et køkken skal være beskrevet under opskriftsgrotten/metainformation/køkkener.json
    - en ingrediens skal være beskrevet under opskriftsgrotten/metainformation/ingerdienser.json
    - Ingen duplicates i ingredienser/køkken
  - En CI robot som autoformatterer alle JSON filer så det ikke bliver kaos