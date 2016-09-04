#SERIAL 201601291542
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

load_extensions:
	${PAVER} load_extensions

make_rpms:
	${PAVER} make_rpm

install_rpms:
	${PAVER} install_rpms

uninstall_rpms:
	${PAVER} uninstall_rpms

make_debs:
	${PAVER} make_deb

uninstall_debs:
	${PAVER} uninstall_debs

start:
	${PAVER} start

