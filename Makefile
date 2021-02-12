RESUME=Martin_Bruchanov_Resume

all: pdf txt

$(RESUME).pdf: $(RESUME).ctex header.ctex Makefile
	context $(RESUME).ctex

$(RESUME).txt: $(RESUME).pdf
	pdftotext -layout $(RESUME).pdf
	sed -i.bak -e 's/ \.//g' -e '/Page [1-9].*/d' $(RESUME).txt
	# Remove double empty lines
	sed -i.bak -e '/^$$/N;/^\n$$/D' $(RESUME).txt
	# Remove ASCII linefeed control sequences
	sed -i.bak -e 's/\o14//g' -e 's/\o12//g' $(RESUME).txt

.PHONY: pdf txt clean veryclean

pdf: $(RESUME).pdf

txt: $(RESUME).txt

clean:
	@rm -f $(RESUME).{tuc,log,txt.bak}

veryclean: clean
	@rm -f $(RESUME).{pdf,txt}

