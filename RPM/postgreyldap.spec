#
# spec file for package postgreyLDAP
#
# Copyright (c) 2012 Jeff Warnica, NS, Canada
#
# Based on postgrey.spec by SUSE
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

#

# norootforbuild


Name:           postgreyldap
Requires:       perl >= 5.6.0, perl-IO-Multiplex perl-Net-Server perl-ldap perl-Config-Simple
BuildRequires:  postfix
%if 0%{?suse_version} >= 1000
Suggests:       cron
%endif
PreReq:         %insserv_prereq, %fillup_prereq /usr/sbin/useradd
License:        GPL-2.0+
Group:          Productivity/Networking/Email/Utilities
Summary:        PostfixLDAP LDAP Backed greylisting policy server
Version:        0.0.8
Release:        1
Url:            https://github.com/jeffwarnica/postgrey-ldap
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        http://postgrey.schweikert.ch/pub/%name-%{version}.tar.bz2
Source1:        %{name}.init
Source2:        %{name}.sysconfig
Source3:        %{name}.README.SUSE

%description
PostgreyLDAP is a Postfix policy server implementing greylisting, 
which is backed by an LDAP database, allowing shared greylisting across
mail servers. When a request for delivery of a mail is received by 
Postfix via SMTP, the triplet CLIENT_IP / SENDER / RECIPIENT is built. 
If it is the first time that this triplet is seen, or if the triplet 
was first seen less than 5 minutes, then the mail gets rejected with
a temporary error. Hopefully spammers or viruses will not try again 
later, as it is however required per RFC.

Being LDAP backed, the greylist databae can be shared across multiple
mail servers. While SQL databases would provide the same, with 
SuSE/YaST it is very likely that mail servers are using LDAP already, 
and not necessarally an SQL server


Authors:
--------
    Jeff Warnica <jeff@coherentnetworksolutions.com>
    David Schweikert <david@schweikert.ch>

%prep
%setup -q

%build
pod2man -s 8 postgreyldap > postgreyldap.8

%install
# the binaries
install -d %{buildroot}/%{_sbindir}
install -m 0755 postgreyldap %{buildroot}/%{_sbindir}/%{name}
#install -m 0755 contrib/postgreyreport %{buildroot}/%{_sbindir}/postgreyreport
# manual
install -d %{buildroot}/%{_mandir}/man8
install -m 0644 %{name}.8 %{buildroot}%{_mandir}/man8/%{name}.8
#install -m 0644 postgreyreport.8 %{buildroot}%{_mandir}/man8/postgreyreport.8
# configuration
install -D -m 0644 config.dist $RPM_BUILD_ROOT/etc/postfix/postgreyldap.conf
#install -d %{buildroot}/%{_sysconfdir}/%{name}
#install -m 0644 postgrey_whitelist_clients %{buildroot}/%{_sysconfdir}/%{name}/whitelist_clients
#install -m 0644 postgrey_whitelist_recipients %{buildroot}/%{_sysconfdir}/%{name}/whitelist_recipients
touch whitelist_clients.local
install -m 0644 whitelist_clients.local %{buildroot}/%{_sysconfdir}/%{name}
# init file and configuration
install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/init.d/%{name}
ln -sf /etc/init.d/%{name} $RPM_BUILD_ROOT/usr/sbin/rc%{name}
install -D -m 644 %{SOURCE2} %{buildroot}/var/adm/fillup-templates/sysconfig.%{name}
# queue directory
install -d %{buildroot}/%{_var}/lib/%{name}
# directory for socket
install -d -m 0775 %{buildroot}/%{_var}/spool/postfix/%{name}


%pre
/usr/sbin/useradd --system -g nogroup -s /bin/false -c "Postgrey Daemon" -d /var/lib/%{name} %{name} 2> /dev/null || :

%preun
%stop_on_removal %{name}

%post
%{fillup_and_insserv %{name}}

%postun
%restart_on_update %{name}
%{insserv_cleanup}
%verifyscript

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/%{name}
%config(noreplace) /etc/postfix/postgreyldap.conf
#%config(noreplace) %{_sysconfdir}/%{name}/whitelist_recipients
#%config(noreplace) %{_sysconfdir}/%{name}/whitelist_clients
#%config(noreplace) %{_sysconfdir}/%{name}/whitelist_clients.local
%config %attr(0755,root,root) /etc/init.d/%{name}
%{_sbindir}/%{name}
%{_sbindir}/rc%{name}
%dir %attr(0755,postgreyldap,postfix) %{_var}/lib/%{name}
/var/adm/fillup-templates/sysconfig.%{name}
%dir %attr(0770,postgreyldap,postfix) %{_var}/spool/postfix/%{name}
%doc %{_mandir}/man?/*
#%doc Changes COPYING README README.SUSE examples %{name}_daily_greylist.crontab
%doc COPYING README ldap/schema4ldapadd.ldif ldap/indexes.ldif ldap/schema.ldif ldap/README.ldap ldap/postgrey_whitelist_recipients ldap/access.ldif ldap/postgrey_whitelist_clients ldap/whitelist2ldap.pl


%changelog
* Tue May 17 2012 jeff@coherentnetworksolutions.com
- Update to package, including reconnect to dead LDAP servers

* Tue Apr 3 2012 jeff@coherentnetworksolutions.com
- Initial creation of RPM (fork of postgreyldap)
