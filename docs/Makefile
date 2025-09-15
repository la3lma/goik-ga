# Makefile for goik-ga Documentation Generation
#
# This Makefile handles:
# - LaTeX document compilation
# - PlantUML diagram generation
# - Python figure generation with virtual environment
# - Illustration management

# Tool configurations
LATEX=pdflatex
BIBTEX=bibtex
PLANTUML=plantuml
PYTHON=python3
VENV_DIR=.venv
PYTHON_VENV=$(VENV_DIR)/bin/python

# Directory structure
PLANTUML_DIR=plantuml
PYTHON_DIR=python
ILLUSTRATIONS_DIR=illustrations

# Source files
TEX_SOURCE=main.tex
TEX_OUTPUT=main.pdf
BIB_SOURCE=refs.bib

# PlantUML source files (will be populated)
PLANTUML_SOURCES=$(wildcard $(PLANTUML_DIR)/*.puml)
PLANTUML_OUTPUTS=$(PLANTUML_SOURCES:$(PLANTUML_DIR)/%.puml=$(ILLUSTRATIONS_DIR)/%.png)

# Python source files (will be populated)
PYTHON_SOURCES=$(wildcard $(PYTHON_DIR)/*.py)
PYTHON_OUTPUTS=$(PYTHON_SOURCES:$(PYTHON_DIR)/%.py=$(ILLUSTRATIONS_DIR)/%-py.png)

# Default target
.PHONY: all clean clean-latex clean-illustrations clean-venv help
.PHONY: pdf plantuml-figures python-figures illustrations venv

all: illustrations pdf

# PDF generation with LaTeX
pdf: $(TEX_OUTPUT)

$(TEX_OUTPUT): $(TEX_SOURCE) $(BIB_SOURCE) $(PLANTUML_OUTPUTS) $(PYTHON_OUTPUTS)
	@echo "Building LaTeX documentation with illustrations..."
	$(LATEX) $(TEX_SOURCE)
	$(BIBTEX) main
	$(LATEX) $(TEX_SOURCE)
	$(LATEX) $(TEX_SOURCE)
	@echo "Documentation built: $(TEX_OUTPUT)"

# PlantUML figure generation
plantuml-figures: $(PLANTUML_OUTPUTS)

$(ILLUSTRATIONS_DIR)/%.png: $(PLANTUML_DIR)/%.puml
	@echo "Generating PlantUML diagram: $@"
	@mkdir -p $(ILLUSTRATIONS_DIR)
	$(PLANTUML) -tpng -o ../$(ILLUSTRATIONS_DIR) $<

# Python virtual environment setup
venv: $(VENV_DIR)/pyvenv.cfg

$(VENV_DIR)/pyvenv.cfg:
	@echo "Creating Python virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	$(PYTHON_VENV) -m pip install --upgrade pip
	$(PYTHON_VENV) -m pip install matplotlib numpy scipy Pillow
	@echo "Virtual environment created with scientific Python packages"

# Python figure generation
python-figures: venv $(PYTHON_OUTPUTS)

$(ILLUSTRATIONS_DIR)/%-py.png: $(PYTHON_DIR)/%.py venv
	@echo "Generating Python figure: $@"
	@mkdir -p $(ILLUSTRATIONS_DIR)
	cd $(PYTHON_DIR) && ../$(PYTHON_VENV) $*.py && mv $*-py.png ../$(ILLUSTRATIONS_DIR)/

# Generate all illustrations
illustrations: plantuml-figures python-figures

# Cleaning targets
clean: clean-latex clean-illustrations

clean-latex:
	@echo "Cleaning LaTeX intermediate files..."
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.pdf

clean-illustrations:
	@echo "Cleaning generated illustrations..."
	rm -rf $(ILLUSTRATIONS_DIR)/*.png

clean-venv:
	@echo "Cleaning Python virtual environment..."
	rm -rf $(VENV_DIR)

clean-all: clean clean-venv
	@echo "All build artifacts cleaned"

# Help target
help:
	@echo "Available targets:"
	@echo "  all              - Generate all illustrations and build PDF"
	@echo "  pdf              - Build LaTeX documentation PDF"
	@echo "  illustrations    - Generate all illustrations (PlantUML + Python)"
	@echo "  plantuml-figures - Generate PlantUML diagrams"
	@echo "  python-figures   - Generate Python figures"
	@echo "  venv             - Set up Python virtual environment"
	@echo "  clean            - Clean LaTeX files and illustrations"
	@echo "  clean-latex      - Clean LaTeX intermediate files only"
	@echo "  clean-illustrations - Clean generated illustrations only"
	@echo "  clean-venv       - Clean Python virtual environment"
	@echo "  clean-all        - Clean everything including venv"
	@echo "  help             - Show this help"

# Check if required tools are available
check-tools:
	@echo "Checking for required tools..."
	@which $(LATEX) > /dev/null || (echo "pdflatex is not installed or not in PATH" && exit 1)
	@which $(BIBTEX) > /dev/null || (echo "bibtex is not installed or not in PATH" && exit 1)
	@which $(PLANTUML) > /dev/null || (echo "plantuml is not installed or not in PATH" && exit 1)
	@which $(PYTHON) > /dev/null || (echo "python3 is not installed or not in PATH" && exit 1)
	@echo "All required tools are available"