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
BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python3-%{service}-tests-tempest
Summary:    Tempest Plugin for Neutron L2 Gateway
%{?python_provide:%python_provide python3-%{service}-tests-tempest}

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-pbr

Requires:   python3-pbr >= 4.0.0
Requires:   python3-babel >= 2.3.4
Requires:   python3-neutron-lib >= 1.30.0
Requires:   python3-neutronclient >= 6.7.0
Requires:   python3-neutron-tests-tempest
Requires:   python3-ovsdbapp >= 0.10.0
Requires:   python3-tempest >= 1:18.0.0

%description -n python3-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:    python-%{service}-tests-tempest documentation

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-reno

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
%{py3_build}

# Generate Docs
%if 0%{?with_doc}
sphinx-build -W -b html doc/source doc/build/html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%files -n python3-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
