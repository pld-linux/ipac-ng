%bcond_with default_ipchains	# use ipchains as default accouting agent
%include        /usr/lib/rpm/macros.perl
Summary:	IP accounting package for Linux
Summary(pl):	Pakiet zbieraj�cy informacje o ruchu IP
Name:		ipac-ng
Version:	1.27pl1
Release:	2
Epoch:		0
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/ipac-ng/%{name}-%{version}.tar.bz2
# Source0-md5:	9ac8ded2b1690605017d41da04a7d90f
Source1:	%{name}.init
Source2:	%{name}.cron
Patch0:		%{name}-hardcode-path.patch
Patch1:		%{name}-miscfix.patch
Patch2:		%{name}-new-ipt.patch
URL:		http://sourceforge.net/projects/ipac-ng/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	gdbm-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	perl
BuildRequires:	postgresql-devel
BuildRequires:	postgresql-backend-devel
BuildRequires:	rpm-perlprov >= 3.0.3-16
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _sysconfdir     /etc/%{name}
%define		_htmldir	/home/services/httpd/html/stat
%define		_cgidir		/home/services/httpd/cgi-bin/stat

%description
ipac is a package which is designed to gather, summarize and nicely
output the IP accounting data. ipac make summaries and graphs as ascii
text and/or images with graphs.

%description -l pl
ipac to pakiet przeznaczony do zbierania, podliczania i �adnego
przedstawiania danych o ruchu IP. ipac tworzy zestawienia i wykresy
jako tekst ASCII lub obrazki z wykresami.

%package cgi
Summary:	IP accounting package for Linux - CGI scripts
Summary(pl):	Pakiet zbieraj�cy informacje o ruchu IP - skrypty CGI
Group:		Networking/Daemons
# perlprov doesn't catch these
Requires:	perl-CGI
Requires:	perl-DBI
Requires:	perl-GD
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description cgi
ipac is a package which is designed to gather, summarize and nicely
output the IP accounting data. ipac make summaries and graphs as ascii
text and/or images with graphs. CGI scripts for web visualisation.

%description cgi -l pl
ipac to pakiet przeznaczony do zbierania, podliczania i �adnego
przedstawiania danych o ruchu IP. ipac tworzy zestawienia i wykresy
jako tekst ASCII lub obrazki z wykresami. Skrypty CGI do wizualizacji
statystyk na stronach WWW.

%prep
%setup -q -n %{name}-1.27
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	--enable-auth-server=127.0.0.1 \
	--enable-classic=no \
	--enable-default-access=files \
	--enable-default-storage=gdbm \
	--enable-default-agent=%{?with_default_ipchains:ipchains}%{!?with_default_ipchains:iptables}
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,cron.d}
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_htmldir},%{_cgidir},/var/lib/ipac}

install contrib/sample_configs/ipac.conf $RPM_BUILD_ROOT%{_sysconfdir}/ipac.conf
install contrib/sample_configs/rules.conf.%{?with_default_ipchains:ipchains}%{!?with_default_ipchains:iptables} $RPM_BUILD_ROOT%{_sysconfdir}/rules.conf

sed -e s'#/cgi-bin/#/cgi-bin/stat/#g' html/stat/index.html > $RPM_BUILD_ROOT%{_htmldir}/index.html
install html/cgi-bin/.htaccess $RPM_BUILD_ROOT%{_cgidir}/.htaccess
install html/cgi-bin/* $RPM_BUILD_ROOT%{_cgidir}
touch $RPM_BUILD_ROOT/var/lib/ipac/flag

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ipac-ng
if [ -f /var/lock/subsys/ipac-ng ]; then
	/etc/rc.d/init.d/ipac-ng restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/ipac-ng start\" to setup ipac-ng rules."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/ipac-ng ]; then
		/etc/rc.d/init.d/ipac-ng stop 1>&2
	fi
	/sbin/chkconfig --del ipac-ng
fi

%files
%defattr(644,root,root,755)
%doc README README-NG README-NG.RUS postgre.readme contrib/* ipac-ng.sql
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not size mtime md5) %attr(640,root,root) /etc/cron.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.conf
%attr(755,root,root) %{_sbindir}/ipac*
%attr(755,root,root) %{_sbindir}/fetchipac
%dir /var/lib/ipac
%attr(664,http,http) /var/lib/ipac/flag
%{_mandir}/man?/*

%files -n %{name}-cgi
%defattr(644,root,root,755)
%dir %{_cgidir}
%dir %{_htmldir}
%attr(644,http,http) %{_htmldir}/index.html
%attr(644,root,root) %{_cgidir}/.htaccess
%attr(755,root,root) %{_cgidir}/*
