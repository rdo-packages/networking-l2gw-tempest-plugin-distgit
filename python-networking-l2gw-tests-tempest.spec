# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility
%global service networking-l2gw
%global plugin networking-l2gw-tempest-plugin
%global module networking_l2gw_tempest_plugin
%global with_doc 1
%{!?upstream_version: %global upstream_version %{commit}}
%global commit a3af33b319e5605791b0c95b7bbfdd81a814877c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# DO NOT REMOVE ALPHATAG
%global alphatag .%{shortcommit}git

%global common_desc \
Tempest Plugin for Neutron L2GW This project defines a tempest plugin \
containing tests used to verify the functionality of the Neutron L2GW service \
plugin. The plugin will automatically load these tests into tempest.

Name:       python-%{service}-tests-tempest
Version:    0.1.0
Release:    1%{alphatag}%{?dist}
Summary:    Tempest Plugin for Neutron L2 Gateway
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}
Source0:    https://github.com/openstack/%{plugin}/archive/%{upstream_version}.tar.gz#/%{name}-%{shortcommit}.tar.gz
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
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-reno

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
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
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
* Tue Oct 8 2019 RDO <dev@lists.rdoproject.org> 0.1.0-1.a3af33bgit
- Update to post 0.1.0 (a3af33b319e5605791b0c95b7bbfdd81a814877c)
