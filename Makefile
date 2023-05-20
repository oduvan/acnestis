CURRENT_DIR := $(shell pwd)

nox-all-docker:
	docker run --rm -it -v $(CURRENT_DIR):/src thekevjames/nox nox -f src/noxfile.py