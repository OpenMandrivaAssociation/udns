%define	major 0
%define libname %mklibname udns %{major}
%define develname %mklibname udns -d

Summary:	DNS Resolver Library
Name:		udns
Version:	0.0.9
Release:	%mkrel 2
Group:		Networking/Other
License:	LGPL
URL:		http://www.corpit.ru/mjt/udns.html
Source0:	http://www.corpit.ru/mjt/udns/%{name}_%{version}.tar.gz
BuildConflicts:	%{name}-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
UDNS is a stub DNS resolver library with ability to perform both syncronous and
asyncronous DNS queries.

%package -n	%{libname}
Summary:	DNS Resolver Library
Group:          System/Libraries

%description -n	%{libname}
UDNS is a stub DNS resolver library with ability to perform both syncronous and
asyncronous DNS queries.

This package contains the shared UDNS library.

%package -n	%{develname}
Summary:	Static library and header files for the libmemcached library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
UDNS is a stub DNS resolver library with ability to perform both syncronous and
asyncronous DNS queries.

This package contains the static UDNS library and its header files.

%prep

%setup -q -n %{name}-%{version}

%build

./configure

make CFLAGS="%{optflags}" SOVER="%{major}" staticlib sharedlib
ln -snf libudns.so.%{major} libudns.so

gcc %{optflags} -DHAVE_CONFIG_H -o udns-rblcheck rblcheck.c -L. -ludns
gcc %{optflags} -DHAVE_CONFIG_H -o udns-dnsget dnsget.c -L. -ludns
#gcc %{optflags} -DHAVE_CONFIG_H -o udns-ex-rdns ex-rdns.c -L. -ludns

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man3

install -m0755 libudns.so.%{major} %{buildroot}%{_libdir}/
ln -snf libudns.so.%{major} %{buildroot}%{_libdir}/libudns.so
install -m0644 libudns.a %{buildroot}%{_libdir}/
install -m0644 udns.h %{buildroot}%{_includedir}/

install -m0755 udns-rblcheck %{buildroot}%{_bindir}/
install -m0755 udns-dnsget %{buildroot}%{_bindir}/

install -m0644 dnsget.1 %{buildroot}%{_mandir}/man1/udns-dnsget.1
install -m0644 rblcheck.1 %{buildroot}%{_mandir}/man1/udns-rblcheck.1
install -m0644 udns.3 %{buildroot}%{_mandir}/man3/

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/udns-rblcheck
%{_bindir}/udns-dnsget
%{_mandir}/man1/udns-dnsget.1*
%{_mandir}/man1/udns-rblcheck.1*

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING.LGPL NEWS NOTES TODO
%{_libdir}/libudns.so.%{major}

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libudns.so
%{_libdir}/libudns.a
%{_mandir}/man3/udns.3*
