%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}
%{!?_httpd_apxs: %{expand: %%global _httpd_apxs %%{_sbindir}/apxs}}

Name:           mod_qos
Version:        10.13
Release:        2%{?dist}
Summary:        Quality of service module for Apache

Group:          System Environment/Daemons
License:        GPLv2
URL:            http://opensource.adnovum.ch/mod_qos/
Source0:        http://downloads.sourceforge.net/project/mod-qos/%{name}-%{version}.tar.gz
Source1:        mod_qos.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel pcre-devel openssl-devel
Requires:       httpd-mmn = %{_httpd_mmn}

%description
The mod_qos module may be used to determine which requests should be served and 
which shouldn't in order to avoid resource over-subscription. The module 
collects different attributes such as the request URL, HTTP request and response
headers, the IP source address, the HTTP response code, history data (based on 
user session and source IP address), the number of concurrent requests to the 
server (total or requests having similar attributes), the number of concurrent 
TCP connections (total or from a single source IP), and so forth.

Counteractive measures to enforce the defined rules are: request blocking, 
dynamic timeout adjustment, request delay, response throttling, and dropping of 
TCP connections. 


%prep
%setup -q -n %{name}-%{version}

%build
%{_httpd_apxs} -Wc,"%{optflags}" -c apache2/mod_qos.c


%install
rm -rf $RPM_BUILD_ROOT
install -Dpm 755 apache2/.libs/mod_qos.so \
    $RPM_BUILD_ROOT%{_libdir}/httpd/modules/mod_qos.so
install -Dpm 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/mod_qos.conf

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc doc README.TXT
%{_libdir}/httpd/modules/mod_qos.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_qos.conf


%changelog
* Tue Jan  8 2013 Christof Damian <christof@damian.net> - 10.13-2
- add conf file

* Tue Jan  8 2013 Christof Damian <christof@damian.net> - 10.13-1
- initial package

