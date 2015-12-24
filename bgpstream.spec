%global _hardened_build 1

Summary: BGPStream
Name: bgpstream
Version: 1.0.0
Release: 2%{?dist}
License: GPLv2+
Group: System/Libraries
Prefix: /usr
Source0: http://www.caida.org/~chiara/bgpstream-doc/bgpstream-1.0.0.tar.gz
URL: http://www.caida.org/~chiara/bgpstream-doc/bgpstream/index.html

BuildRequires: mariadb-devel
BuildRequires: sqlite-devel
BuildRequires: libtrace-devel
BuildRequires: gcc
BuildRequires: make

Requires: libtrace
Requires: mariadb
Requires: mariadb-libs
Requires: sqlite

%description
BGP Stream, a software framework for the historical analysis and real-time 
monitoring of BGP data.

%package devel
Summary: BGPStream development headers
Group: System/Libraries
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
* Thu Dec 24 2015 John Siegrist <john@complects.com> - 1.0.0-2
- Update Package build dependencies and fixed RPath build error.

* Tue Jun 02 2015 Arun Babu Neelicattu <arun.neelicattu@gmail.com> - 1.0.0-1
- Initial specfile

