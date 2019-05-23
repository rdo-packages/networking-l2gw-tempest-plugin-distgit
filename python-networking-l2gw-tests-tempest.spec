# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%global service networking-l2gw
%global plugin networking-l2gw-tempest-plugin
%global module networking_l2gw_tempest_plugin
%global with_doc 1
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Tempest Plugin for Neutron L2GW This project defines a tempest plugin \
containing tests used to verify the functionality of the Neutron L2GW service \
plugin. The plugin will automatically load these tests into tempest.

Name:       python-%{service}-tests-tempest
Version:    XXX
Release:    XXX
Summary:    Tempest Plugin for Neutron L2 Gateway
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}
Source0:    https://files.pythonhosted.org/packages/source/n/%{plugin}/%{plugin}-%{version}.tar.gz
BuildArch:  noarch
BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python%{pyver}-%{service}-tests-tempest
Summary:    Tempest Plugin for Neutron L2 Gateway
%{?python_provide:%python_provide python%{pyver}-%{service}-tests-tempest}

BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr

Requires:   python%{pyver}-pbr >= 3.1.1
Requires:   python%{pyver}-babel >= 2.3.4
Requires:   python%{pyver}-neutron-lib >= 1.13.0
Requires:   python%{pyver}-neutronclient >= 6.7.0
Requires:   python%{pyver}-neutron-tests-tempest
Requires:   python%{pyver}-ovsdbapp >= 0.10.0
Requires:   python%{pyver}-tempest >= 1:18.0.0

%description -n python%{pyver}-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:    python-%{service}-tests-tempest documentation

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-oslo-sphinx

%description -n python-%{service}-tests-tempest-doc
It contains the documentation for the Neutron L2GW tempest plugin.
%endif

%prep
%autosetup -n %{plugin}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{plugin}.egg-info

%build
%{pyver_build}

# Generate Docs
%if 0%{?with_doc}
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%files -n python%{pyver}-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/networking-l2gw-tempest-plugin/commit/?id=ae15928cc5da93f25c7bb0a5a922b64f679077b4
