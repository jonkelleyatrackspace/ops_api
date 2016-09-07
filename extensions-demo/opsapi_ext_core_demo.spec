%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           opsapi_ext_core_demo
Version:        1.0.1
Release:        1%{?dist}
Group:          Applications/Systems
Summary:        A demo extension module for opsAPI

License:        MIT
URL:            https://github.com/jonkelleyatrackspace/ops_api
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  python-setuptools
Requires(pre):  shadow-utils
Requires:       python
Requires:       PyYAML

%define service_name %{name}d

%description
Collection of demo scripts to test with the opsAPI SDK.

%prep
%setup -q -n %{name}-%{version}

%build

%pre

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}
%post

%preun

%postun

%files
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}*.egg-info
%attr(0755,-,-) %{_bindir}/%{name}

%changelog
* Tue Sep 6 2016 Jonathan Kelley <jon@jon-kelley.com> - 1.0.0-1
- First release
