%global service networking-l2gw
%global plugin networking-l2gw-tempest-plugin
%global module networking_l2gw_tempest_plugin
%global with_doc 1
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Tempest Plugin for Neutron L2GW This project defines a tempest plugin
containing tests used to verify the functionality of the Neutron L2GW service
plugin. The plugin will automatically load these tests into tempest.

Name:       python-%{service}-tests-tempest
Version:    XXX
Release:    XXX
Summary:    Tempest Plugin for Neutron L2 Gateway
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}
Source0:    https://files.pythonhosted.org/packages/source/n/%{plugin}/%{plugin}-%{version}.tar.gz
BuildArch:  noarch

%description
%{common_desc}

%package -n python2-%{service}-tests-tempest
Summary:    Tempest Plugin for Neutron L2 Gateway
%{?python_provide:%python_provide python2-%{service}-tests-tempest}

BuildRequires:  python-psycopg2
BuildRequires:  python-setuptools
BuildRequires:  python-subunit
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python-PyMySQL
BuildRequires:  python-coverage
BuildRequires:  python-ddt
BuildRequires:  python2-devel
BuildRequires:  python-flake8-import-order
BuildRequires:  python-hacking
BuildRequires:  python-mock
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-oslotest
BuildRequires:  python-pbr
BuildRequires:  python-sphinx
BuildRequires:  python-testresources
BuildRequires:  tempest
 
Requires:   python-pbr >= 2.0.0
Requires:   python-babel >= 2.3.4
Requires:   python-neutron-lib >= 1.9.0
Requires:   python-neutronclient >= 6.3.0
Requires:   python-ovsdbapp >= 0.4.0
Requires:   python-setuptools

%description -n python2-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:    python-%{service}-tests-tempest documentation

BuildRequires:  python-sphinx >= 1.6.2

%description -n python-%{service}-tests-tempest-doc
It contains the documentation for the Neutron L2GW tempest plugin.
%endif

%prep
%autosetup -n %{module}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{plugin}.egg-info

%build
%py2_build

# Generate Docs
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%py2_install

%files -n python2-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{module}
%{python2_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Tue Dec 21 2017 Ricardo Noriega <rnoriega@redhat.com>
- Initial package.
