#SERIAL 201601291542
# Base the name of the software on the spec file
PACKAGE := $(shell basename *.spec .spec)
# Override this arch if the software is arch specific
ARCH = noarch

# Variables for clean build directory tree under repository
BUILDDIR = ./build
ARTIFACTDIR = ./artifacts
SDISTDIR = ${ARTIFACTDIR}/sdist
WHEELDIR = ${ARTIFACTDIR}/wheels
RPMBUILDDIR = ${BUILDDIR}/rpm-build
RPMDIR = ${ARTIFACTDIR}/rpms
DEBBUILDDIR = ${BUILDDIR}/deb-build
DEBDIR = ${ARTIFACTDIR}/debs

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

