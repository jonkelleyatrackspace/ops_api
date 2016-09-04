# Base the name of the software on the spec file
PACKAGE := $(shell basename *.spec .spec)
PAVER := $(shell which paver)

install:
	${PAVER} setup

reinstall:
	${PAVER} reinstall

uninstall:
	${PAVER} uninstall

clean:
	${PAVER} clean

extensions:
	${PAVER} load_extensions

rpms:
	${PAVER} make_rpm

install_rpms:
	${PAVER} install_rpms

uninstall_rpms:
	${PAVER} uninstall_rpms

debs:
	${PAVER} make_deb

uninstall_debs:
	${PAVER} uninstall_debs

start:
	${PAVER} start

