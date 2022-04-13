# Для точечного источника cartesian1.jl
# Для параллельных лучей  cartesian2.jl
# Для полярной системы координат polar.jl
PROG=polar.jl

all: clean maxwell luneburg plot

maxwell:
	@rm -fr ./Maxwell_data
	julia $(PROG) "maxwell"

luneburg:
	@rm -fr ./Luneburg_data
	julia $(PROG) "luneburg"

plot:
	python3 plot.py $(PROG)

clean:
	@rm -fr ./Luneburg_data
	@rm -fr ./Maxwell_data
	@rm -f *.pdf
	@rm -f *.png

