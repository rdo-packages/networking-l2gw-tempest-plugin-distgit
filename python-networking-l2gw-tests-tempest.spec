%global service networking-l2gw
%global plugin networking-l2gw-tempest-plugin
%global module networking_l2gw_tempest_plugin
%global with_doc 1
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global common_desc \
Tempest Plugin for Neutron L2GW This project defines a tempest plugin \
containing tests used to verify the functionality of the Neutron L2GW service \
plugin. The plugin will automatically load these tests into tempest.

Name:       python-%{service}-tests-tempest
Version:    XXX
Release:    XXX
Summary:    Tempest Plugin for Neutron L2 Gateway
License:    Apache-2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}
Source0:    https://files.pythonhosted.org/packages/source/n/%{plugin}/%{plugin}-%{version}.tar.gz
BuildArch:  noarch
BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python3-%{service}-tests-tempest
Summary:    Tempest Plugin for Neutron L2 Gateway

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description -n python3-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:    python-%{service}-tests-tempest documentation

%description -n python-%{service}-tests-tempest-doc
It contains the documentation for the Neutron L2GW tempest plugin.
%endif

%prep
%autosetup -n %{plugin}-%{upstream_version} -S git


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -R
%endif

%build
%pyproject_wheel

# Generate Docs
%if 0%{?with_doc}
%tox -e docs
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

%files -n python3-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.dist-info

%if 0%{?with_doc}
%files -n python-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
