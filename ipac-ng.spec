%include        /usr/lib/rpm/macros.perl
Summary:	IP accounting package for Linux
Summary(pl):	Pakiet zbieraj±cy informacje o ruchu IP
Name:		ipac-ng
Version:	1.22
Release:	1
License:	GPL
Group:		Networking/Daemons
URL:		http://sourceforge.net/projects/ipac-ng/
Source0:	http://prdownloads.sourceforge.net/ipac-ng/%{name}-%{version}.tar.bz2
BuildRequires:	autoconf
BuildRequires:	byacc
BuildRequires:	gdbm-devel
BuildRequires:	perl
BuildRequires:	postgresql-devel
BuildRequires:	postgresql-backend-devel
BuildRequires:	openssl-devel
BuildRequires:  rpm-perlprov >= 3.0.3-16
# perlprov doesn't catch these
Requires:	perl-CGI
Requires:	perl-DBI
Requires:	perl-GD
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _sysconfdir     /etc/%{name}

%define		_htmldir	/home/httpd/html/stat
%define		_cgidir		/home/httpd/cgi-bin/stat

%description
ipac is a package which is designed to gather, summarize and nicely
output the IP accounting data. ipac make summaries and graphs as ascii
text and/or images with graphs.

%description -l pl
ipac to pakiet przeznaczony do zbierania, podliczania i ³adnego
przedstawiania danych o ruchu IP. ipac tworzy zestawienia i wykresy
jako tekst ASCII lub obrazki z wykresami.

%prep
%setup -q -n %{name}-%{version}

%build
%{__aclocal}
%{__autoconf}
%configure \
	--enable-auth-server=127.0.0.1 \
	--enable-classic=no \
	--enable-default-access=files \
	--enable-default-storage=gdbm
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_htmldir},%{_cgidir},/var/lib/ipac}

install contrib/sample_configs/ipac-ng/ipac.conf $RPM_BUILD_ROOT%{_sysconfdir}/ipac.conf
sed -e s'#/cgi-bin/#/cgi-bin/stat/#g' html/stat/index.html > $RPM_BUILD_ROOT%{_htmldir}/index.html
install html/cgi-bin/.htaccess $RPM_BUILD_ROOT%{_cgidir}/.htaccess
install html/cgi-bin/* $RPM_BUILD_ROOT%{_cgidir}
touch $RPM_BUILD_ROOT/var/lib/ipac/flag

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README README-NG README-NG.RUS postgre.readme contrib/* ipac-ng.sql
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ipac.conf
%attr(755,root,root) %{_sbindir}/ipac*
%attr(755,root,root) %{_sbindir}/fetchipac
%attr(644,http,http) %{_htmldir}/index.html
%attr(644,root,root) %{_cgidir}/.htaccess
%attr(755,root,root) %{_cgidir}/*
%attr(664,http,http) /var/lib/ipac/flag
%dir /var/lib/ipac
%dir %{_cgidir}
%dir %{_htmldir}
%{_mandir}/man?/*
