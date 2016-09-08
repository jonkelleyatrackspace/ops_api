# Base the name of the software on the spec file
PACKAGE := $(shell basename *.spec .spec)
PAVER := $(shell which paver)

install:
	${PAVER} install

install_all:
	${PAVER} install_all

reinstall:
	sudo ${PAVER} reinstall

uninstall:
	sudo ${PAVER} uninstall

clean:
	${PAVER} clean

clean_all:
	${PAVER} clean_all

rpms:
	${PAVER} make_rpm

install_rpms:
	sudo ${PAVER} install_rpms

uninstall_rpms:
	sudo ${PAVER} uninstall_rpms

debs:
	${PAVER} make_deb

install_debs:
	sudo ${PAVER} install_debs

uninstall_debs:
	sudo ${PAVER} uninstall_debs

start:
	sudo ${PAVER} start

