Summary:	ipac-ng
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
BuildRequires:	perl
BuildRequires:	postgresql-backend-devel
BuildRequires:	byacc
BuildRequires:	gdbm-devel
BuildRequires:	openssl-devel
BuildRequires:	autoconf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _sysconfdir     /etc/%{name}

%description
ipac is a package which is designed to gather, summarize and nicely
output the IP accounting data. ipac make summaries and graphs as ascii
text and/or images with graphs.

%prep
%setup -q -n %{name}-%{version}
autoconf
%configure \
	--enable-classic=no 

%build
%{__make} DESTDIR=$RPM_BUILD_ROOT all

%install
rm -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

install -d $RPM_BUILD_ROOT{%{_sysconfdir},/var/www/cgi-bin,/var/www/html/stat,/var/lib/ipac}

install contrib/sample_configs/ipac-ng/ipac.conf $RPM_BUILD_ROOT%{_sysconfdir}/ipac.conf
install html/stat/index.html $RPM_BUILD_ROOT/var/www/html/stat/index.html
install html/cgi-bin/.htaccess $RPM_BUILD_ROOT/var/www/cgi-bin/.htaccess
install -m 755 html/cgi-bin/* $RPM_BUILD_ROOT/var/www/cgi-bin
touch $RPM_BUILD_ROOT/var/lib/ipac/flag

gzip -9nf README README-NG README-NG.RUS postgre.readme

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/%{name}-%{version}

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ipac.conf
%attr(755,root,root)%{_sbindir}/ipacsum
%attr(755,root,root)%{_sbindir}/fetchipac
%attr(644,nobody,nobody)/var/www/html/stat/index.html
%attr(644,root,root)/var/www/cgi-bin/.htaccess
%attr(755,nobody,nobody)/var/www/cgi-bin/*
%attr(664,apache,nobody)/var/lib/ipac/flag
%dir /var/lib/ipac
%dir /var/www/cgi-bin
%dir /var/www/html/stat
%doc *.gz contrib/* ipac-ng.sql
%{_mandir}/man8/*
