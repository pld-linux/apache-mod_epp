#
# TODO:
# - example/minimal configuration file
# - review XXX's
# - better Summary
#
%include	/usr/lib/rpm/macros.perl
%define		mod_name	epp
%define 	apxs		/usr/sbin/apxs
Summary:	An EPP (Extensible Provisioning Protocol) implementation for Apache2
#Summary(pl):	
Name:		apache-mod_%{mod_name}
Version:	1.0
Release:	1
License:	Apache
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/aepps/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	ce458a48f56cc857c808b71ec27f592d
# XXX: to be added to docs?
#Source1:	http://dl.sourceforge.net/aepps/epp-erd-20030122.tar.gz
URL:		http://aepps.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.43
BuildRequires:	rpm-perlprov
Requires(post,preun):	%{apxs}
# XXX: wouldn't requires_eq be more appropiate?
Requires:	apache >= 2.0.43
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir	/etc/httpd

%description
This Apache 2.0 module implements the EPP over TCP protocol as defined
in draft-ietf-provreg-epp-tcp-05.txt and the session management parts
of draft-ietf-provreg-epp-0(6|7).txt.

This is *not* a full implementation of EPP, this module just makes it
possible to write an EPP server as a set of CGI scripts.

# %description -l pl
# TODO

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
