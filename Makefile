# Makefile for goik-ga - Geometric Algebra Kinematics

# Go settings
GOCMD=go
GOBUILD=$(GOCMD) build
GOTEST=$(GOCMD) test
GOCLEAN=$(GOCMD) clean
GOGET=$(GOCMD) get
GOFMT=$(GOCMD) fmt
GOMOD=$(GOCMD) mod
GOVET=$(GOCMD) vet

# LaTeX settings
LATEX=pdflatex
BIBTEX=bibtex
DOCS_DIR=docs
DOCS_SOURCE=$(DOCS_DIR)/main.tex
DOCS_OUTPUT=$(DOCS_DIR)/main.pdf

# Example settings
EXAMPLE_DIR=examples/hexapod_leg
EXAMPLE_BINARY=$(EXAMPLE_DIR)/hexapod_leg

# Packages
PACKAGES=./pga ./cga
ALL_PACKAGES=./...

.PHONY: all build test clean fmt vet tidy deps example doc pdf help

# Default target
all: build test example pdf

# Build all packages
build:
	@echo "Building Go packages..."
	$(GOBUILD) -v $(PACKAGES)

# Run tests
test:
	@echo "Running tests..."
	$(GOTEST) -v $(ALL_PACKAGES)

# Build and run the hexapod leg example
example:
	@echo "Building and running hexapod leg example..."
	cd $(EXAMPLE_DIR) && $(GOBUILD) -o hexapod_leg .

# Run the example
run-example: example
	@echo "Running hexapod leg example..."
	cd $(EXAMPLE_DIR) && ./hexapod_leg

# Format Go code
fmt:
	@echo "Formatting Go code..."
	$(GOFMT) $(ALL_PACKAGES)

# Run go vet
vet:
	@echo "Running go vet..."
	$(GOVET) $(ALL_PACKAGES)

# Tidy go modules
tidy:
	@echo "Tidying go modules..."
	$(GOMOD) tidy

# Download dependencies
deps:
	@echo "Downloading dependencies..."
	$(GOMOD) download

# Build documentation PDF
pdf: $(DOCS_OUTPUT)

$(DOCS_OUTPUT): $(DOCS_SOURCE) $(DOCS_DIR)/refs.bib
	@echo "Building LaTeX documentation..."
	cd $(DOCS_DIR) && $(LATEX) main.tex
	cd $(DOCS_DIR) && $(BIBTEX) main
	cd $(DOCS_DIR) && $(LATEX) main.tex
	cd $(DOCS_DIR) && $(LATEX) main.tex
	@echo "Documentation built: $(DOCS_OUTPUT)"

# Alias for documentation
doc: pdf

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	$(GOCLEAN) $(ALL_PACKAGES)
	rm -f $(EXAMPLE_BINARY)
	cd $(DOCS_DIR) && rm -f *.aux *.bbl *.blg *.log *.out *.toc *.pdf

# Clean LaTeX intermediate files only
clean-latex:
	@echo "Cleaning LaTeX intermediate files..."
	cd $(DOCS_DIR) && rm -f *.aux *.bbl *.blg *.log *.out *.toc

# Check for required tools
check-tools:
	@echo "Checking for required tools..."
	@which $(GOCMD) > /dev/null || (echo "Go is not installed or not in PATH" && exit 1)
	@which $(LATEX) > /dev/null || (echo "pdflatex is not installed or not in PATH" && exit 1)
	@which $(BIBTEX) > /dev/null || (echo "bibtex is not installed or not in PATH" && exit 1)
	@echo "All required tools are available"

# Development workflow
dev: fmt vet test build example
	@echo "Development build complete"

# Release workflow
release: clean tidy fmt vet test build pdf
	@echo "Release build complete"

# Benchmark tests (if any exist)
bench:
	@echo "Running benchmarks..."
	$(GOTEST) -bench=. $(ALL_PACKAGES)

# Coverage report
coverage:
	@echo "Generating coverage report..."
	$(GOTEST) -coverprofile=coverage.out $(ALL_PACKAGES)
	$(GOCMD) tool cover -html=coverage.out -o coverage.html
	@echo "Coverage report generated: coverage.html"

# Help
help:
	@echo "Available targets:"
	@echo "  all          - Build everything (packages, tests, example, PDF)"
	@echo "  build        - Build Go packages"
	@echo "  test         - Run tests"
	@echo "  example      - Build hexapod leg example"
	@echo "  run-example  - Build and run hexapod leg example"
	@echo "  pdf/doc      - Build LaTeX documentation PDF"
	@echo "  fmt          - Format Go code"
	@echo "  vet          - Run go vet"
	@echo "  tidy         - Tidy go modules"
	@echo "  deps         - Download dependencies"
	@echo "  clean        - Clean all build artifacts"
	@echo "  clean-latex  - Clean LaTeX intermediate files only"
	@echo "  check-tools  - Check for required tools"
	@echo "  dev          - Development workflow (fmt, vet, test, build, example)"
	@echo "  release      - Release workflow (clean, tidy, fmt, vet, test, build, pdf)"
	@echo "  bench        - Run benchmarks"
	@echo "  coverage     - Generate test coverage report"
	@echo "  help         - Show this help"