#
# TODO:
# - example/minimal configuration file
#
%include	/usr/lib/rpm/macros.perl
%define		mod_name	epp
%define 	apxs		/usr/sbin/apxs
Summary:	An EPP (Extensible Provisioning Protocol) implementation for Apache2
Summary(pl):	Implementacja EPP (Extensible Provisioning Protocol) dla Apache2
Name:		apache-mod_%{mod_name}
Version:	1.1
Release:	1
License:	Apache
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/aepps/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	157780266ea623b752b999e7b15b42c6
# XXX: to be added to docs?
#Source1:	http://dl.sourceforge.net/aepps/epp-erd-20030122.tar.gz
URL:		http://aepps.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.43
BuildRequires:	rpm-perlprov
Requires(post,preun):	%{apxs}
Requires:	apache >= 2.0.43
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR)

%description
This Apache 2.0 module implements the EPP over TCP protocol as defined
in draft-ietf-provreg-epp-tcp-05.txt and the session management parts
of draft-ietf-provreg-epp-0(6|7).txt.

This is *not* a full implementation of EPP, this module just makes it
possible to write an EPP server as a set of CGI scripts.

%description -l pl
Ten modu³ Apache 2.0 jest implementacj± protoko³u EPP po TCP zgodn± z
dokumentem draft-ietf-provreg-epp-tcp-05.txt oraz czê¶ciami
dotycz±cymi zarz±dzania sesj± z draft-ietf-provreg-epp-0(6|7).txt.

*Nie* jest to pe³na implementacja EPP, ten modu³ jedynie umo¿liwia
pisanie serwera EPP jako zestawu skryptów CGI.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT

install -D .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so
install -D epptelnet.pl $RPM_BUILD_ROOT%{_bindir}/epptelnet.pl
install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -r examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_pkglibdir}/*
%{_examplesdir}/%{name}-%{version}
