Summary:	ipac-ng
Name:		ipac-ng
Version:	1.19
Release:	0.1
License:	GPL
Group:		Networking/Daemons
URL:		http://sourceforge.net/projects/ipac-ng/
Source0:	http://prdownloads.sourceforge.net/ipac-ng/%{name}-%{version}.tar.bz2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:		perl, postgresql-backend-devel, byacc, gdbm-devel, openssl-devel
Requires:	apache, iptables, postgresql, gdbm

%description
ipac is a package which is designed to gather, summarize and nicely
output the IP accounting data. ipac make summaries and graphs as ascii
text and/or images with graphs.

%prep
%setup -q -n %{name}-%{version}
CXXFLAGS="$RPM_OPT_FLAGS" \
./configure \
--prefix=%{_prefix} \
--mandir=%{_mandir} \
--with-postgresql-inc=/usr/include/postgresql \
--enable-classic=no 

%build
%{__make} DESTDIR=$RPM_BUILD_ROOT all

%install
rm -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/ipac-ng
install -d $RPM_BUILD_ROOT/var/www/cgi-bin
install -d $RPM_BUILD_ROOT/var/www/html/stat
install -d $RPM_BUILD_ROOT/var/lib/ipac
install contrib/sample_configs/ipac-ng/ipac.conf $RPM_BUILD_ROOT%{_sysconfdir}/ipac-ng/ipac.conf
install html/stat/index.html $RPM_BUILD_ROOT/var/www/html/stat/index.html
install html/cgi-bin/.htaccess $RPM_BUILD_ROOT/var/www/cgi-bin/.htaccess
install -m 755 html/cgi-bin/* $RPM_BUILD_ROOT/var/www/cgi-bin
touch $RPM_BUILD_ROOT/var/lib/ipac/flag

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/%{name}-%{version}

%post
echo " * Installation complete. Please, read files in" %{_defaultdocdir}/%{name}-%{version}

%files
%defattr(644,root,root,755)
%config %{_sysconfdir}/ipac-ng/ipac.conf
%attr(755,root,root)%{_sbindir}/ipacsum
%attr(755,root,root)%{_sbindir}/fetchipac
%attr(644,nobody,nobody)/var/www/html/stat/index.html
%attr(644,root,root)/var/www/cgi-bin/.htaccess
%attr(755,nobody,nobody)/var/www/cgi-bin/*
%attr(664,apache,nobody)/var/lib/ipac/flag
%dir /var/lib/ipac
%dir /var/www/cgi-bin
%dir /var/www/html/stat
%doc %attr(644,root,root)CHANGES COPYING README README-NG README-NG.RUS TODO UPDATE contrib/* postgre.readme ipac-ng.sql
%{_mandir}/man8/*.8.gz
