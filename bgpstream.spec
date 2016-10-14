%global _hardened_build 1

Summary: BGPStream Core package provides BGPReader tool and libBGPStream library
Name: bgpstream
Version: 1.1.0
Release: 1%{?dist}
License: GPLv2+
Group: Applications/Internet
Prefix: /usr
Source0: https://github.com/CAIDA/bgpstream/releases/download/v1.1.0/bgpstream-1.1.0.tar.gz
URL: https://bgpstream.caida.org/

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: libcurl-devel
BuildRequires: libtrace-devel
BuildRequires: libwandio-devel
BuildRequires: make
BuildRequires: mariadb-devel
BuildRequires: sqlite-devel

Requires: libtrace
Requires: libwandio
Requires: mariadb
Requires: mariadb-libs
Requires: sqlite

%description
BGP Stream, a software framework for the historical analysis and real-time 
monitoring of BGP data.

%package devel
Summary: Development files for BGPStream API
Group: Development/Libraries
Provides: %{name}-devel

%description devel
This package contains necessary header files for BGPStream development.

%package tools
Summary: BGPStream tools
Group: System Environment/Tools
Provides: %{name}-tools

%description tools
Helper utilities for use with the BGPStream library.

%prep
%setup -q

%build
./configure --prefix %{_prefix} --libdir=%{_libdir} CPPFLAGS='-I/usr/include/mysql' LDFLAGS='-L/usr/lib64/mysql'

# https://fedoraproject.org/wiki/RPath_Packaging_Draft
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc COPYING
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%exclude %{_libdir}/*.la

%files tools
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/*

%changelog
* Fri Oct 14 2016 John Siegrist <john@complects.com> - 1.1.0-1
- Update package version to 1.1.0.
- Merged in changes from alternate spec file by Clinton Work <clinton@scripty.com>.

* Tue Mar 29 2016 John Siegrist <john@complects.com> - 1.0.0-3
- Update sources URL to retrieve from Github.

* Thu Dec 24 2015 John Siegrist <john@complects.com> - 1.0.0-2
- Update Package build dependencies and fixed RPath build error.

* Tue Jun 02 2015 Arun Babu Neelicattu <arun.neelicattu@gmail.com> - 1.0.0-1
- Initial specfile

