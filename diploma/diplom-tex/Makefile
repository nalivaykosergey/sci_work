main:
	pdflatex --shell-escape main.tex; pybtex main; pdflatex --shell-escape main.tex; pdflatex --shell-escape main.tex
	
clean:
	rm -f *.{log,aux,bbl,out,toc}