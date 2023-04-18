#!/bin/bash

pdfjam `find plots/variables/dnntuples/pfcand_el_*.pdf | grep -v combined | sort -V` --nup 3x2 --column true --columnstrict true --landscape --outfile plots/variables/dnntuples/pfcand_el_combined.pdf
pdfjam `find plots/variables/dnntuples/pfcand_mu_*.pdf | grep -v combined | sort -V` --nup 3x2 --column true --columnstrict true --landscape --outfile plots/variables/dnntuples/pfcand_mu_combined.pdf
