RESUME=Martin_Bruchanov_Resume
PACKAGE=http://lmtx.pragma-ade.nl/install-lmtx/context-linux-64.zip
DESTDIR=$$HOME/bin/context

all: pdf #txt

$(RESUME)_CZ.pdf: Makefile $(RESUME).ctex header.ctex Makefile
	context $(RESUME).ctex
	mv -v $(RESUME).pdf $@

$(RESUME)_CA.pdf: Makefile $(RESUME).ctex header.ctex Makefile
	CANADA=1 context $(RESUME).ctex
	mv -v $(RESUME).pdf $@

$(RESUME).txt: $(RESUME).pdf
	pdftotext -layout $(RESUME).pdf
	sed -i.bak -e 's/ \.//g' -e '/Page [1-9].*/d' $(RESUME).txt
	# Remove double empty lines
	sed -i.bak -e '/^$$/N;/^\n$$/D' $(RESUME).txt
	# Remove ASCII linefeed control sequences
	sed -i.bak -e 's/\o14//g' -e 's/\o12//g' $(RESUME).txt

.PHONY: pdf txt clean veryclean install check_inkscape

pdf: $(RESUME)_CZ.pdf $(RESUME)_CA.pdf

txt: $(RESUME).txt

clean:
#	@rm -v -f $(RESUME).{tuc,log,txt.bak}
	@rm -v -f $(addprefix $(RESUME)., tuc log txt.bak)

veryclean: clean
#	@rm -v -f $(RESUME).{pdf,txt}
	rm -v -f $(addprefix $(RESUME), _CA.pdf _CZ.pdf txt)

install: check_inkscape
	mkdir -p $(DESTDIR)
	( cd $(DESTDIR) && \
		wget $(PACKAGE) && \
		unzip `basename $(PACKAGE)` && \
		sh install.sh )
	echo "export PATH=$(DESTDIR)/tex/texmf-linux-64/bin:\$$PATH" >> ~/.bashrc

check_inkscape:
	@inkscape --version || echo "Inkscape is not installed, needed for proper SVG support."
