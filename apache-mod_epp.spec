# TODO:
# - example/minimal configuration file
%define		mod_name	epp
%define 	apxs		/usr/sbin/apxs
%include	/usr/lib/rpm/macros.perl
Summary:	An EPP (Extensible Provisioning Protocol) implementation for Apache2
Summary(pl.UTF-8):   Implementacja EPP (Extensible Provisioning Protocol) dla Apache2
Name:		apache-mod_%{mod_name}
Version:	1.2
Release:	1
License:	Apache
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/aepps/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	c21073a4025d79f3ac1c293b58132ed7
Source1:	http://dl.sourceforge.net/aepps/epp-erd-20030122.tar.gz
# Source1-md5:	3d7720410e83fe6e90742119892011e2
URL:		http://aepps.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.43
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This Apache 2.0 module implements the EPP over TCP protocol as defined
in draft-ietf-provreg-epp-tcp-05.txt and the session management parts
of draft-ietf-provreg-epp-0(6|7).txt.

This is *not* a full implementation of EPP, this module just makes it
possible to write an EPP server as a set of CGI scripts.

%description -l pl.UTF-8
Ten moduł Apache 2.0 jest implementacją protokołu EPP po TCP zgodną z
dokumentem draft-ietf-provreg-epp-tcp-05.txt oraz częściami
dotyczącymi zarządzania sesją z draft-ietf-provreg-epp-0(6|7).txt.

*Nie* jest to pełna implementacja EPP, ten moduł jedynie umożliwia
pisanie serwera EPP jako zestawu skryptów CGI.

%prep
%setup -q -n mod_%{mod_name}-%{version} -a1
sed -i -e 's#MD5_DIGESTSIZE#APR_MD5_DIGESTSIZE#g' *.c

%build
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_bindir},%{_sysconfdir}/httpd.conf,%{_examplesdir}/%{name}-%{version}}

libtool --mode=install install mod_%{mod_name}.la $RPM_BUILD_ROOT%{_pkglibdir}
rm -f $RPM_BUILD_ROOT%{_pkglibdir}/*.{l,}a

install epptelnet.pl $RPM_BUILD_ROOT%{_bindir}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

echo 'LoadModule %{mod_name}_module modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/68_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README TODO epp-erd*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
%attr(755,root,root) %{_bindir}/*
%{_examplesdir}/%{name}-%{version}
