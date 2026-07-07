# Minimal Sphinx Makefile

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# User-friendly target mirroring the docs.yml/pages.yml invocation
# (``python -m sphinx -W -b html . _build/html``). ``-W`` keeps the build
# honest: any autodoc/config warning fails it.
.PHONY: html clean help

help:
	@echo "Available targets:"
	@echo "  html  - build the HTML docs with warnings-as-errors into $(BUILDDIR)/html"
	@echo "  clean - remove the $(BUILDDIR) tree"

html:
	$(SPHINXBUILD) -W -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS)

clean:
	rm -rf $(BUILDDIR)
