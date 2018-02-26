# Migration scripts Bepress (CSV) -> OJS

The script in this repository was used to migrate from a Bepress installation to a OJS installation for the journal "Journal of Privacy and Confidentiality".

While not perfect, the script successfully created reasonable entries for all articles previously hosted under Bepress. Any shortcomings are primarily shortcomings of the available metadata:

- page numbers were not created (not contained in the CSV file)
- email adresses and affiliations were missing for all authors in the CSV file
- some articles did not have abstracts
- Not all keywords were migrated (this might be a bug in the script)

We ultimately filled these in manually, drawing on the migrated PDFs (which contained almost all of the missing info).

This script is not maintained by us, since we have completed the migration - YMMV.

Lars Vilhuber @larsvilhuber
