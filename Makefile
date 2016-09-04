# Base the name of the software on the spec file
PACKAGE := $(shell basename *.spec .spec)
PAVER := $(shell which paver)

install:
	sudo ${PAVER} setup

reinstall:
	sudo ${PAVER} reinstall

uninstall:
	sudo ${PAVER} uninstall

clean:
	${PAVER} clean

extensions:
	sudo ${PAVER} load_extensions

rpms:
	${PAVER} make_rpm

install_rpms:
	sudo ${PAVER} install_rpms

uninstall_rpms:
	sudo ${PAVER} uninstall_rpms

debs:
	${PAVER} make_deb

uninstall_debs:
	sudo ${PAVER} uninstall_debs

start:
	sudo ${PAVER} start

