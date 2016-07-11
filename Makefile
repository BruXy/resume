RESUME=Martin_Bruchanov_Resume

$(RESUME).pdf: $(RESUME).ctex header.ctex Makefile
	context $(RESUME).ctex

$(RESUME).txt: $(RESUME).pdf 
	pdftotext -layout $(RESUME).pdf
	sed -i.bak -e 's/ \.//g' -e '/Page [1-9].*/d' $(RESUME).txt 
	sed -i.bak -e 's/\o14//g' -e '/^$$/N;/^\n$$/D' $(RESUME).txt 

.PHONY: pdf txt

pdf: $(RESUME).pdf

txt: $(RESUME).txt

