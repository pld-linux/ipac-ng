%bcond_with default_ipchains	# use ipchains as default accouting agent
%include        /usr/lib/rpm/macros.perl
Summary:	IP accounting package for Linux
Summary(pl):	Pakiet zbieraj±cy informacje o ruchu IP
Name:		ipac-ng
Version:	1.30
Release:	1
Epoch:		0
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/ipac-ng/%{name}-%{version}.tar.bz2
# Source0-md5:	89eab6631528b1a946e7b9dec6ee8799
# Source0-size:	159033
Source1:	%{name}.init
Source2:	%{name}.cron
Patch0:		%{name}-hardcode-path.patch
URL:		http://sourceforge.net/projects/ipac-ng/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gdbm-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	perl-base
BuildRequires:	postgresql-devel
BuildRequires:	postgresql-backend-devel
BuildRequires:	rpm-perlprov >= 3.0.3-16
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Obsoletes:	ipac-ng-cgi
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _sysconfdir     /etc/%{name}

%description
ipac is a package which is designed to gather, summarize and nicely
output the IP accounting data. ipac make summaries and graphs as ascii
text and/or images with graphs.

%description -l pl
ipac to pakiet przeznaczony do zbierania, podliczania i ³adnego
przedstawiania danych o ruchu IP. ipac tworzy zestawienia i wykresy
jako tekst ASCII lub obrazki z wykresami.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	--enable-default-access=files \
	--enable-default-storage=gdbm \
	--enable-default-agent=%{?with_default_ipchains:ipchains}%{!?with_default_ipchains:iptables}
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,cron.d}
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_htmldir},%{_cgidir},/var/lib/ipac}

install contrib/sample_configs/ipac.conf $RPM_BUILD_ROOT%{_sysconfdir}/ipac.conf
install contrib/sample_configs/rules.conf.%{?with_default_ipchains:ipchains}%{!?with_default_ipchains:iptables} $RPM_BUILD_ROOT%{_sysconfdir}/rules.conf

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
%doc doc/* contrib/* CHANGELOG README TODO
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not size mtime md5) %attr(640,root,root) /etc/cron.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.conf
%attr(755,root,root) %{_sbindir}/ipac*
%attr(755,root,root) %{_sbindir}/fetchipac
%dir /var/lib/ipac
%attr(664,http,http) /var/lib/ipac/flag
%{_mandir}/man?/*
