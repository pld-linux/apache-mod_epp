# TODO:
# - example/minimal configuration file
#
%include	/usr/lib/rpm/macros.perl
%define		mod_name	epp
%define 	apxs		/usr/sbin/apxs
Summary:	An EPP (Extensible Provisioning Protocol) implementation for Apache2
Summary(pl):	Implementacja EPP (Extensible Provisioning Protocol) dla Apache2
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
%setup -q -n mod_%{mod_name}-%{version} -a1
sed -i -e 's#MD5_DIGESTSIZE#APR_MD5_DIGESTSIZE#g' *.c

%build
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/httpd/httpd.conf,%{_examplesdir}/%{name}-%{version}}

libtool --mode=install install -D mod_%{mod_name}.la $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so
install -D epptelnet.pl $RPM_BUILD_ROOT%{_bindir}/epptelnet.pl

cp -r examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

echo 'LoadModule %{mod_name}_module modules/mod_%{mod_name}.so' > $RPM_BUILD_ROOT/etc/httpd/httpd.conf/68_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache HTTP daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README TODO epp-erd*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_pkglibdir}/*.so
%{_examplesdir}/%{name}-%{version}
%config %{_sysconfdir}/httpd.conf/*.conf
