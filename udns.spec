%define	major	0
%define	oldlibname	%mklibname udns %{major}
%define	libname	%mklibname udns
%define	devname	%mklibname udns -d
%define	staticname	%mklibname udns -d -s

# Static library objects are not built -fPIC by default
%global	optflags %{optflags} -fPIC

Summary:	DNS resolver library for synchronous and asynchronous queries
Name:		udns
Version:	0.6
Release:	2
License:	LGPL-2.1-or-later
Group:		Networking/Other
Url:		https://www.corpit.ru/mjt/udns.html
Source0:	https://www.corpit.ru/mjt/udns/%{name}-%{version}.tar.gz
# Custom configure script is not C99-clean (pointer types for inet_ntop/pton)
Patch0:		udns-0.6-configure-c99.patch

# Custom configure script, not autotools - do not use %%configure / BuildSystem
BuildRequires:	make

%description
UDNS is a stub DNS resolver library with the ability to perform both
synchronous and asynchronous DNS queries.

This package contains the udns-dnsget and udns-rblcheck command line tools.

%package -n	%{libname}
Summary:	%{summary}
Group:		System/Libraries
%rename %{oldlibname}

%description -n	%{libname}
UDNS is a stub DNS resolver library with the ability to perform both
synchronous and asynchronous DNS queries.

This package contains the shared UDNS library.

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
This package contains the header files, pkg-config file and development
library symlink needed to compile applications that use UDNS.

%package -n	%{staticname}
Summary:	Static library for %{name}
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}

%description -n	%{staticname}
This package contains the static UDNS library. Static linking is
discouraged; prefer the shared library in %{libname}.

%prep
%autosetup -p1

%build
%set_build_flags
./configure --enable-ipv6
# shared builds the shared library and dynamically linked utilities
%make_build SOVER=%{major} staticlib shared

%install
install -Dpm0755 libudns.so.%{major} %{buildroot}%{_libdir}/libudns.so.%{major}
ln -snf libudns.so.%{major} %{buildroot}%{_libdir}/libudns.so
install -Dpm0644 libudns.a %{buildroot}%{_libdir}/libudns.a
install -Dpm0644 udns.h %{buildroot}%{_includedir}/udns.h

install -Dpm0755 dnsget_s %{buildroot}%{_bindir}/udns-dnsget
install -Dpm0755 rblcheck_s %{buildroot}%{_bindir}/udns-rblcheck

install -Dpm0644 dnsget.1 %{buildroot}%{_mandir}/man1/udns-dnsget.1
install -Dpm0644 rblcheck.1 %{buildroot}%{_mandir}/man1/udns-rblcheck.1
install -Dpm0644 udns.3 %{buildroot}%{_mandir}/man3/udns.3

mkdir -p %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/libudns.pc << EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: libudns
Description: DNS resolver library for synchronous and asynchronous queries
Version: %{version}
Libs: -L\${libdir} -ludns
Cflags: -I\${includedir}
EOF

%check
export LD_LIBRARY_PATH="$PWD${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
./dnsget_s -h
./rblcheck_s -h

%files
%license COPYING.LGPL
%doc NEWS NOTES TODO
%{_bindir}/udns-dnsget
%{_bindir}/udns-rblcheck
%{_mandir}/man1/udns-dnsget.1*
%{_mandir}/man1/udns-rblcheck.1*

%files -n %{libname}
%{_libdir}/libudns.so.%{major}*

%files -n %{devname}
%{_includedir}/udns.h
%{_libdir}/libudns.so
%{_libdir}/pkgconfig/libudns.pc
%{_mandir}/man3/udns.3*

%files -n %{staticname}
%{_libdir}/libudns.a
