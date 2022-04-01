%global service networking-l2gw
%global plugin networking-l2gw-tempest-plugin
%global module networking_l2gw_tempest_plugin
%global with_doc 1
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate isort pylint astroid
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%{!?upstream_version: %global upstream_version %{commit}}
%global commit 82e3d07ea410e1489c6a83e5a4b9557d52643d41
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# DO NOT REMOVE ALPHATAG
%global alphatag .%{shortcommit}git

%{?dlrn: %global tarsources %{plugin}-%{upstream_version}}
%{!?dlrn: %global tarsources %{plugin}}

%global common_desc \
Tempest Plugin for Neutron L2GW This project defines a tempest plugin \
containing tests used to verify the functionality of the Neutron L2GW service \
plugin. The plugin will automatically load these tests into tempest.

Name:       python-%{service}-tests-tempest
Version:    0.1.0
Release:    4%{?alphatag}%{?dist}
Summary:    Tempest Plugin for Neutron L2 Gateway
License:    Apache-2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}
Source0:    http://opendev.org/x/%{plugin}/archive/%{upstream_version}.tar.gz#/%{module}-%{shortcommit}.tar.gz
BuildArch:  noarch
BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python3-%{service}-tests-tempest
Summary:    Tempest Plugin for Neutron L2 Gateway

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

Requires:   python3-neutron-tests-tempest
Requires:   python3-tempest >= 1:18.0.0

%description -n python3-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:    python-%{service}-tests-tempest documentation

%description -n python-%{service}-tests-tempest-doc
It contains the documentation for the Neutron L2GW tempest plugin.
%endif

%prep
%autosetup -n %{tarsources} -S git


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
  %pyproject_buildrequires -t -e docs
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
* Thu Apr 18 2024 RDO <dev@lists.rdoproject.org> 0.1.0-4
- Rebuild in Caracal

* Fri Apr 01 2022 RDO <dev@lists.rdoproject.org> 0.1.0-3
- Update to post 0.1.0 (82e3d07ea410e1489c6a83e5a4b9557d52643d41)

