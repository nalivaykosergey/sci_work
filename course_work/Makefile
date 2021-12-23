BUILDDIR = build
TMPFILES = *.{log,toc,tac,aux,dvi,ps,bbl,blg,tmp,nav,out,snm,vrb,rel,lot,lof,fls,fdb_latexmk,pyg,run.xml} *~
TMPFILES_LOCAL = *.tac *.loa default.titlelist.* split-paper.tex default.xml default.html default*.png *.4o[mftsy] *.mintedcmd *.mintedmd5
TMPDIRS_LOCAL = split-paper.d default.htmld _minted-* plantuml-images

# FILES = $(patsubst %.md, %.docx, $(wildcard *.md))
FILES += $(patsubst %.md, %.pdf, $(wildcard *.md))
#FILES = text/*.md

FILTERS = 
PDF_ENGINE =
PDF_OPTIONS =
PDF_FORMAT_OPTIONS =
EXPORT_LIST = 
TEMPLATE_TEX = --template=pandoc/templates/book.tex
CONFIG_YAML = pandoc/templates/term-paper.yaml
# CONFIG_YAML = pandoc/lang/ru.yaml pandoc/formats/pdf.yaml pandoc/templates/book.yaml pandoc/include/bibliography.yaml pandoc/include/biblatex.yaml
CONFIG_YAML += pandoc/lang/ru.yaml pandoc/formats/pdf.yaml pandoc/include/bibliography.yaml pandoc/include/biblatex.yaml
CONFIG_YAML += pandoc/formats/luatex/fonts.yaml
CONFIG_YAML += pandoc/formats/luatex/fonts-julia.yaml
RESOURCE_PATH = --resource-path ".:image:text"

# include markdown files
FILTERS += -F pandoc-include
FILTERS += --lua-filter=pandoc/filters/include-files.lua
FILTERS += --lua-filter=pandoc/filters/table-width.lua
EXPORT_LIST += export LUA_PATH="pandoc/lua/?.lua;;";
# FILTERS += -F pandoc-include
FILTERS += --lua-filter=pandoc/filters/menukeys.lua
# CONFIG_YAML += pandoc/filters/menukeys.yaml
EXPORT_LIST += export PLANTUML=/usr/share/plantuml/lib/plantuml.jar;
FILTERS += --filter=pandoc/filters/plantuml.py # Befor minted filter
FILTERS += --lua-filter=pandoc/filters/include-code-files.lua # Befor minted filter
FILTERS += --lua-filter=pandoc/filters/minted.lua
# CONFIG_YAML += pandoc/filters/minted.yaml
# FILTERS += -F pandoc-citeproc
# FILTERS += --citeproc
FILTERS += -F pandoc-crossref
# FILTERS += --lua-filter pandoc/filters/section-refs.lua -M section-refs-level=1 -M reference-section-title="Список литературы"
PDF_ENGINE += --pdf-engine=lualatex --pdf-engine-opt=--shell-escape # --pdf-engine-opt=--output-directory=build
PDF_OPTIONS += --number-sections
PDF_FORMAT_OPTIONS += --top-level-division=chapter
PDF_BIB_OPTIONS = --biblatex

%.docx: %.md
	-pandoc "$<" $(FILTERS) -o "$@"

%.pdf: %.md
	@mkdir -p $(BUILDDIR)
	-pandoc $(CONFIG_YAML) title/*.yaml "$<" $(FILTERS) $(PDF_ENGINE) $(PDF_OPTIONS) $(PDF_FORMAT_OPTIONS) $(PDF_BIB_OPTIONS) $(TEMPLATE_TEX) $(RESOURCE_PATH) -o "$@"

%.tex: %.md
	-pandoc -s $(CONFIG_YAML) title/*.yaml "$<" $(FILTERS) $(PDF_ENGINE) $(PDF_OPTIONS) $(PDF_FORMAT_OPTIONS) $(TEMPLATE_TEX) -o "$@"

%.pdf: %.docx
	-unoconv "$<" "$@"

all: main.pdf

clean:
	-@latexmk -C
	-@rm $(FILES) $(TMPFILES)
	-@rm $(TMPFILES_LOCAL)

cleanall: clean
	-@rm *.tex
	-@rm -rf out $(BUILDDIR) $(TMPDIRS_LOCAL)

distclean: cleanall
	-@find . -type d -name "auto" -exec rm -r "{}" \;
	-@find . -type f -name "*~" -delete

## 2 step compilation: md -> tex, tex -> pdf

main.tex: main.md text/*.md appendix.tex
	-$(EXPORT_LIST) \
	pandoc -s $(CONFIG_YAML) title/*.yaml "$<" $(FILTERS) $(PDF_ENGINE) $(PDF_OPTIONS) $(PDF_FORMAT_OPTIONS) $(PDF_BIB_OPTIONS) $(TEMPLATE_TEX) $(RESOURCE_PATH) -A appendix.tex -o "$@"

appendix.tex: appendix.md text/*.md
	-$(EXPORT_LIST) \
	pandoc "$<" $(FILTERS) $(PDF_OPTIONS) $(PDF_FORMAT_OPTIONS) $(PDF_BIB_OPTIONS) $(RESOURCE_PATH) -o "$@"

main.pdf: main.tex
	latexmk -pdflatex="lualatex --shell-escape %O %S" -pdf -bibtex "$<"

