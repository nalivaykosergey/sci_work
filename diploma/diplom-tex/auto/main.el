(TeX-add-style-hook
 "main"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("report" "a4paper" "")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("fontenc" "T2A") ("inputenc" "utf8") ("babel" "russian") ("scrextend" "fontsize=13pt") ("xcolor" "table" "xcdraw") ("geometry" "left=30mm" "right=15mm" "bottom=20mm" "top=20mm") ("natbib" "numbers") ("hyperref" "hidelinks")))
   (add-to-list 'LaTeX-verbatim-environments-local "minted")
   (add-to-list 'LaTeX-verbatim-environments-local "lstlisting")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "href")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "lstinline")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "lstinline")
   (TeX-run-style-hooks
    "latex2e"
    "title"
    "text/abstract"
    "text/abbrev"
    "text/intro"
    "text/ch01"
    "text/ch02"
    "text/ch03"
    "text/concl"
    "text/ap01"
    "text/ap02"
    "text/ap03"
    "text/ap04"
    "report"
    "rep10"
    "fontenc"
    "inputenc"
    "babel"
    "setspace"
    "scrextend"
    "xcolor"
    "geometry"
    "sectsty"
    "amsmath"
    "listings"
    "pdflscape"
    "graphicx"
    "subfig"
    "amssymb"
    "natbib"
    "enumerate"
    "verbatim"
    "minted"
    "hyperref")
   (LaTeX-add-bibliographies
    "bib/cite"))
 :latex)

