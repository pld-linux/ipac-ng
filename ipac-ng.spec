Summary:	IP accounting package for Linux
Summary(pl):	Pakiet zbieraj±cy informacje o ruchu IP
Name:		ipac-ng
Version:	1.19
Release:	0.2
License:	GPL
Group:		Networking/Daemons
Group(cs):	SÌªovÈ/DÈmoni
Group(da):	NetvÊrks/DÊmoner
Group(de):	Netzwerkwesen/Server
Group(es):	Red/Servidores
Group(fr):	RÈseau/Serveurs
Group(is):	Net/P˙kar
Group(it):	Rete/Demoni
Group(no):	Nettverks/Daemoner
Group(pl):	Sieciowe/Serwery
Group(pt):	Rede/Servidores
Group(ru):	Û≈‘ÿ/‰≈ÕœŒŸ
Group(sl):	Omreæni/Streæniki
Group(sv):	N‰tverk/Demoner
Group(uk):	Ì≈“≈÷¡/‰≈ÕœŒ…
URL:		http://sourceforge.net/projects/ipac-ng/
Source0:	http://prdownloads.sourceforge.net/ipac-ng/%{name}-%{version}.tar.bz2
BuildRequires:	autoconf
BuildRequires:	byacc
BuildRequires:	gdbm-devel
BuildRequires:	perl
BuildRequires:	postgresql-backend-devel
BuildRequires:	openssl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _sysconfdir     /etc/%{name}

%define		_htmldir	/home/httpd/html/stat
%define		_cgidir		/home/httpd/cgi-bin/stat

%description
ipac is a package which is designed to gather, summarize and nicely
output the IP accounting data. ipac make summaries and graphs as ascii
text and/or images with graphs.

%description -l pl
ipac to pakiet przeznaczony do zbierania, podliczania i ≥adnego
przedstawiania danych o ruchu IP. ipac tworzy zestawienia i wykresy
jako tekst ASCII lub obrazki z wykresami.

%prep
%setup -q -n %{name}-%{version}

%build
autoconf
%configure \
	--enable-classic=no

%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_htmldir},%{_cgidir},/var/lib/ipac}

install contrib/sample_configs/ipac-ng/ipac.conf $RPM_BUILD_ROOT%{_sysconfdir}/ipac.conf
install html/stat/index.html $RPM_BUILD_ROOT%{_htmldir}/index.html
install html/cgi-bin/.htaccess $RPM_BUILD_ROOT%{_cgidir}/.htaccess
install html/cgi-bin/* $RPM_BUILD_ROOT%{_cgidir}
touch $RPM_BUILD_ROOT/var/lib/ipac/flag

gzip -9nf README README-NG README-NG.RUS postgre.readme

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ipac.conf
%attr(755,root,root) %{_sbindir}/ipacsum
%attr(755,root,root) %{_sbindir}/fetchipac
%attr(644,http,http) %{_htmldir}/index.html
%attr(644,root,root) %{_cgidir}/.htaccess
%attr(755,root,root) %{_cgidir}/*
%attr(664,http,http) /var/lib/ipac/flag
%dir /var/lib/ipac
%dir %{_cgidir}
%dir %{_htmldir}
%doc *.gz contrib/* ipac-ng.sql
%{_mandir}/man8/*
