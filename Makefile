Martin_Bruchanov_Sys_Eng_Resume.txt: Martin_Bruchanov_Sys_Eng_Resume.pdf Makefile
	pdftotext -layout Martin_Bruchanov_Sys_Eng_Resume.pdf
	sed -i.bak -e 's/ \.//g' -e '/Page [1-9].*/d' Martin_Bruchanov_Sys_Eng_Resume.txt 
	sed -i.bak -e 's/\o14//g' -e '/^$$/N;/^\n$$/D' Martin_Bruchanov_Sys_Eng_Resume.txt 
