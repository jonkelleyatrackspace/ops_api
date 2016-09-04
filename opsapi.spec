%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           opsapi
Version:        1.0.0
Release:        1%{?dist}
Group:          Applications/Systems
Summary:        Lightweight API framework with simple extension SDK

License:        MIT
URL:            https://github.com/jonkelleyatrackspace/ops_api
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  python-setuptools
Requires(pre):  shadow-utils
Requires:       python
Requires:       python-setuptools
Requires:       python-requests
Requires:       python-tornado
Requires:       python-pygments
Requires:       PyYAML

%define service_name %{name}d

%description
Lightweight API framework with simple extension SDK to allow rapid prototype of infrastructure-as-a-service concepts

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
%doc README.md
%doc LICENSE
%doc CHANGES.md
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/opsapi.yaml
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}*.egg-info
%attr(0755,-,-) %{_bindir}/%{name}

%changelog
* Sun Sep 4 2016 Jonathan Kelley <jon@jon-kelley.com> - 0.0.1-1
- First spec

* Sun Sep 4 2016 Jonathan Kelley <jon@jon-kelley.com> - 1.0.0-1
- First spec