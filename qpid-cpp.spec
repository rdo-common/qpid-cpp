# qpid-cpp

# Define pkgdocdir for releases that don't define it already
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# The following macros are no longer used for installation but only for cleanup
%{!?ruby_sitelib: %global ruby_sitelib %(/usr/bin/ruby -rrbconfig  -e 'puts Config::CONFIG["sitelibdir"] ')}
%{!?ruby_sitearch: %global ruby_sitearch %(/usr/bin/ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')}

# LIBRARY VERSIONS
%global QPIDCOMMON_VERSION_INFO             5:0:0
%global QPIDTYPES_VERSION_INFO              3:0:2
%global QPIDBROKER_VERSION_INFO             5:0:0
%global QPIDCLIENT_VERSION_INFO             5:0:0
%global QPIDMESSAGING_VERSION_INFO          4:0:1
%global RDMAWRAP_VERSION_INFO               5:0:0
%global SSLCOMMON_VERSION_INFO              5:0:0

Name:          qpid-cpp
Version:       0.24
Release:       6%{?dist}
Summary:       Libraries for Qpid C++ client applications
License:       ASL 2.0
URL:           http://qpid.apache.org

Source0:       http://www.apache.org/dist/qpid/%{version}/qpid-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: boost-devel
BuildRequires: libtool
BuildRequires: doxygen
BuildRequires: pkgconfig
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: python
BuildRequires: python-devel
BuildRequires: perl
BuildRequires: perl-devel
BuildRequires: swig
BuildRequires: cyrus-sasl-devel
BuildRequires: cyrus-sasl-lib
BuildRequires: cyrus-sasl
BuildRequires: boost-program-options
BuildRequires: boost-filesystem
BuildRequires: libuuid-devel
%ifnarch s390 s390x %{arm}
BuildRequires: libibverbs-devel
BuildRequires: librdmacm-devel
%endif
BuildRequires: nss-devel
BuildRequires: nspr-devel
BuildRequires: xqilla-devel
BuildRequires: xerces-c-devel
BuildRequires: libdb-devel
BuildRequires: libdb4-cxx-devel
BuildRequires: libaio-devel
BuildRequires: qpid-proton-c-devel%{?_isa} >= 0.5


Patch1: 01-NO-JIRA-qpidd.service-file-for-use-on-Fedora.patch
Patch2: 02-QPID-4670-Move-to-proton-0.5-remove-dummy-string-in-.patch
Patch3: 03-QPID-5122-cleaner-encoding-of-index-for-delivery-tag.patch
Patch4: 04-QPID-5123-Changes-to-Fedora-19-packaging-of-libdb4-p.patch
Patch5: 05-QPID-5016-Zero-rmgr-struct-element-with-correct-size.patch
Patch6: 06-QPID-5126-Fix-for-building-legacy-store-on-ARM-platf.patch
Patch7: 07-QPID-4582-Get-legacystore-unit-tests-working.patch
Patch8: 08-QPID-4582-Fixed-unit-legacystore-unit-test-to-remove.patch
Patch9: 09-QPID-5129-Alignment-issues-on-ARM.patch


%description

Run-time libraries for AMQP client applications developed using Qpid
C++. Clients exchange messages with an AMQP message broker using
the AMQP protocol.



%package -n qpid-cpp-client
Summary:   Libraries for Qpid C++ client applications

# Remove with 0.28
Provides:      qpid-cpp-client-ssl = %{version}
Obsoletes:     qpid-cpp-client-ssl <= 0.24

Requires:  boost
Requires:  chkconfig
Requires:  initscripts
Requires:  qpid-proton-c%{?_isa} >= 0.5

%description -n qpid-cpp-client
Run-time libraries for AMQP client applications developed using Qpid
C++. Clients exchange messages with an AMQP message broker using
the AMQP protocol.

%files -n qpid-cpp-client
%defattr(-,root,root,-)
%doc cpp/DESIGN
# %doc cpp/INSTALL
%doc cpp/LICENSE
%doc cpp/NOTICE
%doc cpp/README.txt
%doc cpp/RELEASE_NOTES
%{_libdir}/libqpidcommon.so*
%{_libdir}/libqpidclient.so*
%{_libdir}/libqpidtypes.so*
%{_libdir}/libqpidmessaging.so*
%dir %{_libdir}/qpid
%{_libdir}/qpid/client/*
%dir %{_sysconfdir}/qpid
%config(noreplace) %{_sysconfdir}/qpid/qpidc.conf

%post -n qpid-cpp-client -p /sbin/ldconfig

%postun -n qpid-cpp-client -p /sbin/ldconfig



%package -n qpid-cpp-client-devel
Summary:   Header files, documentation and testing tools for developing Qpid C++ clients

Requires:  qpid-cpp-client%{?_isa} = %{version}-%{release}
Requires:  boost-devel
Requires:  boost-filesystem
Requires:  boost-program-options
Requires:  libuuid-devel
Requires:  python

%description -n qpid-cpp-client-devel
Libraries, header files and documentation for developing AMQP clients
in C++ using Qpid.  Qpid implements the AMQP messaging specification.

%files -n qpid-cpp-client-devel
%defattr(-,root,root,-)
%dir %{_includedir}/qpid
%{_includedir}/qpid/*.h
%{_includedir}/qpid/qpid.i
%{_includedir}/qpid/swig_perl_typemaps.i
%{_includedir}/qpid/swig_python_typemaps.i
%{_includedir}/qpid/swig_ruby_typemaps.i
%{_includedir}/qpid/amqp_0_10
%{_includedir}/qpid/client
%{_includedir}/qpid/console
%{_includedir}/qpid/framing
%{_includedir}/qpid/sys
%{_includedir}/qpid/log
%{_includedir}/qpid/management
%{_includedir}/qpid/messaging
%{_includedir}/qpid/agent
%{_includedir}/qpid/types
%{_libdir}/libqpidcommon.so
%{_libdir}/libqpidclient.so
%{_libdir}/libqpidtypes.so
%{_libdir}/libqpidmessaging.so
%{_libdir}/pkgconfig/qpid.pc
%{_datadir}/qpid
%defattr(755,root,root,-)
%{_bindir}/qpid-perftest
%{_bindir}/qpid-topic-listener
%{_bindir}/qpid-topic-publisher
%{_bindir}/qpid-latency-test
%{_bindir}/qpid-client-test
%{_bindir}/qpid-txtest
# %{_datadir}/qpid/examples
%{_libexecdir}/qpid/tests

%post -n qpid-cpp-client-devel -p /sbin/ldconfig

%postun -n qpid-cpp-client-devel -p /sbin/ldconfig



%package -n qpid-cpp-client-devel-docs
Summary:   AMQP client development documentation

BuildArch: noarch

%description -n qpid-cpp-client-devel-docs
This package includes the AMQP clients development documentation in HTML
format for easy browsing.

%files -n qpid-cpp-client-devel-docs
%defattr(-,root,root,-)
%doc %{_pkgdocdir}



%package -n qpid-cpp-server
Summary:   An AMQP message broker daemon

# Remove with 0.28
Provides:      qpid-cpp-server-ssl = %{version}
Obsoletes:     qpid-cpp-server-ssl <= 0.24

Requires:  qpid-cpp-client%{?_isa} = %{version}-%{release}
Requires:  cyrus-sasl
Requires:  qpid-proton-c%{?_isa} >= 0.5

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description -n qpid-cpp-server
A message broker daemon that receives stores and routes messages using
the open AMQP messaging protocol.

%files -n qpid-cpp-server
%defattr(-,root,root,-)
%{_libdir}/libqpidbroker.so*
%{_sbindir}/qpidd
%{_unitdir}/qpidd.service
# TODO: Delete with 0.26
%ghost %config %{_sysconfdir}/qpidd.conf
%config(noreplace) %{_sysconfdir}/qpid/qpidd.conf
%config(noreplace) %{_sysconfdir}/sasl2/qpidd.conf
%{_libdir}/qpid/daemon/*
%attr(755, qpidd, qpidd) %{_localstatedir}/lib/qpidd
%ghost %attr(755, qpidd, qpidd) /var/run/qpidd
#%attr(600, qpidd, qpidd) %config(noreplace) %{_localstatedir}/lib/qpidd/qpidd.sasldb
%doc %{_mandir}/man1/qpidd*

%pre -n qpid-cpp-server
getent group qpidd >/dev/null || groupadd -r qpidd
getent passwd qpidd >/dev/null || \
  useradd -r -M -g qpidd -d %{_localstatedir}/lib/qpidd -s /sbin/nologin \
    -c "Owner of Qpidd Daemons" qpidd
exit 0

%post -n qpid-cpp-server
if [ $1 -eq 1 ]; then
    # Initial installation
    /bin/systemctl --no-reload enable qpidd.service >/dev/null 2>&1 || :
    # BZ#1012001 remove with 0.26
    /usr/bin/ln -s %{_sysconfdir}/qpid/qpidd.conf %{_sysconfdir}/qpidd.conf
fi

%preun -n qpid-cpp-server
if [ $1 -eq 0 ]; then
   # Package removal, not upgrade
   /bin/systemctl --no-reload disable qpidd.service > /dev/null 2>&1 || :
   /bin/systemctl stop qpidd.service > /dev/null 2>&1 || :
fi

%postun -n qpid-cpp-server
if [ $1 -ge 1 ]; then
   # Package upgrade, not uninstall
   /bin/systemctl stop qpidd.service > /dev/null 2>&1 || :
   /bin/systemctl start qpidd.service > /dev/null 2>&1 || :
   if [ ! -f %{_sysconfdir}/qpidd.conf ]; then
       # BZ#1012001 remove with 0.26
       /usr/bin/ln -s %{_sysconfdir}/qpid/qpidd.conf %{_sysconfdir}/qpidd.conf
   fi
fi
/sbin/ldconfig



%package -n qpid-cpp-server-ha
Summary: Provides extensions to the AMQP message broker to provide high availability

Requires: qpid-cpp-server%{?_isa} = %{version}-%{release}
Requires: qpid-qmf%{?_isa}

%description -n qpid-cpp-server-ha
%{summary}.

%files -n qpid-cpp-server-ha
%{_bindir}/qpid-ha
%{_initrddir}/qpidd-primary
%{_libdir}/qpid/daemon/ha.so

%post -n qpid-cpp-server-ha
/sbin/chkconfig --add qpidd-primary
/sbin/ldconfig

%preun -n qpid-cpp-server-ha
if [ $1 = 0 ]; then
  /sbin/service qpidd-primary stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del qpidd-primary
fi

%postun -n qpid-cpp-server-ha
if [ $1 -ge 1 ]; then
  /sbin/service qpidd-primary condrestart >/dev/null 2>&1 || :
fi
/sbin/ldconfig



%ifnarch s390 s390x %{arm}
%package -n qpid-cpp-client-rdma
Summary:   RDMA Protocol support (including Infiniband) for Qpid clients

Requires:  qpid-cpp-client%{?_isa} = %{version}-%{release}

%description -n qpid-cpp-client-rdma
A client plugin and support library to support RDMA protocols (including
Infiniband) as the transport for Qpid messaging.

%files -n qpid-cpp-client-rdma
%defattr(-,root,root,-)
%{_libdir}/librdmawrap.so*
%{_libdir}/qpid/client/rdmaconnector.so*
%config(noreplace) %{_sysconfdir}/qpid/qpidc.conf

%post -n qpid-cpp-client-rdma -p /sbin/ldconfig

%postun -n qpid-cpp-client-rdma -p /sbin/ldconfig



%package -n qpid-cpp-server-rdma
Summary:   RDMA Protocol support (including Infiniband) for the Qpid daemon

Requires:  qpid-cpp-server%{?_isa} = %{version}-%{release}
Requires:  qpid-cpp-client-rdma%{?_isa} = %{version}-%{release}

%description -n qpid-cpp-server-rdma
A Qpid daemon plugin to support RDMA protocols (including Infiniband) as the
transport for AMQP messaging.

%files -n qpid-cpp-server-rdma
%defattr(-,root,root,-)
%{_libdir}/qpid/daemon/rdma.so

%post -n qpid-cpp-server-rdma -p /sbin/ldconfig

%postun -n qpid-cpp-server-rdma -p /sbin/ldconfig
%endif



%package -n qpid-cpp-server-xml
Summary:   XML extensions for the Qpid daemon

Requires:  qpid-cpp-server%{?_isa} = %{version}-%{release}
Requires:  xqilla
Requires:  xerces-c

%description -n qpid-cpp-server-xml
A Qpid daemon plugin to support extended XML-based routing of AMQP
messages.

%files -n qpid-cpp-server-xml
%defattr(-,root,root,-)
%{_libdir}/qpid/daemon/xml.so

%post -n qpid-cpp-server-xml -p /sbin/ldconfig

%postun -n qpid-cpp-server-xml -p /sbin/ldconfig



%package -n qpid-cpp-server-store
Summary:   Red Hat persistence extension to the Qpid messaging system
License:   LGPLv2+

Requires:  qpid-cpp-server%{?_isa} = %{version}
Requires:  db4
Requires:  libaio

%description -n qpid-cpp-server-store
Red Hat persistence extension to the Qpid AMQP broker: persistent message
storage using either a libaio-based asynchronous journal, or synchronously
with Berkeley DB.

%files -n qpid-cpp-server-store
%defattr(-,root,root,-)
%{_libdir}/qpid/daemon/store.so

%post -n qpid-cpp-server-store -p /sbin/ldconfig

%postun -n qpid-cpp-server-store -p /sbin/ldconfig


%package -n qpid-tools
Summary:   Management and diagnostic tools for Apache Qpid

BuildArch: noarch

Requires:  python-qpid >= 0.8
Requires:  python-qpid-qmf

%description -n qpid-tools
Management and diagnostic tools for Apache Qpid brokers and clients.

%files -n qpid-tools
%defattr(-,root,root,-)
%{_bindir}/qpid-cluster
%{_bindir}/qpid-cluster-store
%{_bindir}/qpid-config
%{_bindir}/qpid-printevents
%{_bindir}/qpid-queue-stats
%{_bindir}/qpid-route
%{_bindir}/qpid-stat
%{_bindir}/qpid-tool
%doc LICENSE NOTICE
%if "%{python_version}" >= "2.6"
%{python_sitelib}/qpid_tools-*.egg-info
%endif



%prep
%setup -q -n qpid-%{version}

%patch1 -p2
%patch2 -p2
%patch3 -p2
%patch4 -p2
%patch5 -p2
%patch6 -p2
%patch7 -p2
%patch8 -p2
%patch9 -p2

%global perftests "qpid-perftest qpid-topic-listener qpid-topic-publisher qpid-latency-test qpid-client-test qpid-txtest"

%global rh_qpid_tests_failover "failover_soak run_failover_soak"

%global rh_qpid_tests_clients "replaying_sender resuming_receiver declare_queues"

%build
pushd cpp
%cmake -DDOC_INSTALL_DIR:PATH=%{_pkgdocdir} .
make %{?_smp_mflags}
make docs-user-api

pushd ../python
./setup.py build
popd
pushd ../tools
./setup.py build
popd

popd

%install
mkdir -p -m0755 %{buildroot}/%{_bindir}
mkdir -p -m0755 %{buildroot}/%{_unitdir}

pushd python
%{__python} setup.py install \
   --skip-build \
   --install-purelib %{python_sitearch} \
   --root %{buildroot}
popd

pushd tools
%{__python} setup.py install \
    --skip-build \
    --install-purelib %{python_sitelib} \
    --root %{buildroot}
popd

pushd cpp
make install DESTDIR=%{buildroot}/

# clean up items we're not installing
rm -f %{buildroot}/%{_libdir}/libqpidbroker.so
rm -f %{buildroot}/%{_libdir}/libcqpid_perl.so
rm -f %{buildroot}/%{_libdir}/ruby/cqmf2.so
rm -f %{buildroot}/%{_libdir}/ruby/cqpid.so
rm -f %{buildroot}/%{_libdir}/ruby/qmfengine.so
rm -f %{buildroot}/%{ruby_sitelib}
rm -rf %{buildroot}/%{_libdir}/perl5

# install systemd files
mkdir -p %{buildroot}/%{_unitdir}
install -pm 644 %{_builddir}/qpid-%{version}/cpp/etc/qpidd.service %{buildroot}/%{_unitdir}
rm -f %{buildroot}/%{_initrddir}/qpidd
rm -f %{buildroot}/%{_sysconfdir}/init.d/qpidd.service

# install perftests utilities
mkdir -p %{buildroot}/%{_bindir}
pushd src/tests
for ptest in %{perftests}; do
  libtool --mode=install install -m755 $ptest %{buildroot}/%{_bindir}
done
popd

# Remove with 0.26
touch %{buildroot}/%{_sysconfdir}/qpidd.conf
mkdir -p %{buildroot}/%{_localstatedir}/run
touch %{buildroot}/%{_localstatedir}/run/qpidd

popd

# clean up leftover ruby files
rm -rf %{buildroot}/usr/local/%{_lib}/ruby/site_ruby

%clean
rm -rf %{buildroot}


%check


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig



%files
%exclude %{_bindir}/qmf-gen
%exclude %{_bindir}/qmf-tool
%exclude %{_libdir}/libqmf*
%exclude %{_includedir}/qmf
%exclude %{python_sitelib}/qmfgen
%{_libdir}/pkgconfig/qmf2.pc
%exclude %{python_sitelib}/qpidtoollibs
%exclude %{python_sitearch}/qmf
%exclude %{python_sitearch}/cqpid.py*
%exclude %{python_sitearch}/_cqpid.so
%exclude %{python_sitearch}/qmf.py*
%exclude %{python_sitearch}/qmfengine.py*
%exclude %{python_sitearch}/_qmfengine.so
%exclude %{python_sitearch}/qmf2.py*
%exclude %{python_sitearch}/cqmf2.py*
%exclude %{python_sitearch}/_cqmf2.so
%exclude %{_bindir}/qpid-python-test
%exclude %{python_sitearch}/mllib
%exclude %{python_sitearch}/qpid
%exclude %{python_sitearch}/*.egg-info
%exclude %{ruby_vendorlibdir}/qmf*
%exclude %{ruby_vendorarchdir}/cqpid.so
%exclude %{ruby_vendorarchdir}/*qmf*


%changelog
* Fri Nov  1 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-6
- Removed the following subpackages:
- - qpid-qmf
- - qpid-qmf-devel
- - python-qpid-qmf
- - ruby-qpid-qmf
- Updated all QMF dependencies to not require the specific release.
- Removed the QMF header files from qpid-cpp-devel

* Thu Oct 10 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-5
- QPID-4582: Fix the legacy store when building on ARM
- QPID-5215: Legacy store tests
- Resolves: BZ#1010397

* Thu Sep 26 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-4.1
- Provide a symlink from /etc/qpid/qpidd.conf to /etc/qpidd.conf:
-  * this will be removed with the 0.26 release
-  * for upgrades any existing file is preserved for now
- Resolves: BZ#1012001

* Mon Sep 23 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-4
- Fixed dependencies on python-qmf to be python-qpid-qmf.

* Mon Sep 23 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-3
- Add arch checks for all requires to block potential multilib errors on upgrade.
- Added virtual provides for both obsoleted -ssl packages.
- Resolves: BZ#1010999

* Fri Sep 20 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-2
- Disabled building on ARM due to failure of the legacy store to build.

* Mon Sep 16 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-1
- Rebased on Qpid 0.24.
- Relocated qpidd.conf to /etc/qpid
- Trimmed old changelog entries due to bogus date complaints.
- Added fixes to support ARM as a primary platform.
- Build depends on qpid-proton 0.5.
- QPID-4938: Stop building ssl and acl support as separate plugin modules on Unix
- Cleaner encoding of index for delivery tags - QPID-5122
- QPID-5123: Changes to Fedora 19 packaging of libdb4 prevents legacystore from building
- QPID-5016: Legacy store not correctly initialising rmgr
- QPID-5126: Fix for building legacy store on ARM platforms

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 pmachata@redhat.com - 0.22-3
- Rebuild for boost 1.54.0

* Tue Jul  2 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.22-2
- Fixed adding the soversion to shared libraries.
- Resolves: BZ#980364

* Thu Jun 13 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.22-1
- Rebased on Qpid 0.22.
- The package now uses the CMake build system from Qpid.
- No longer use a separate source for the store.
- Resolves: BZ#616080
- Resolves: BZ#966780
- Resolves: BZ#967100

* Mon Mar 25 2013 Vít Ondruch <vondruch@redhat.com> - 0.20-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.20-5
- Moved the Qpidd swig descriptors to /usr/include/qpid
- Moved the QMF swig descriptors to /usr/include/qmf

* Tue Feb 12 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.20-4
- Moved Functor and MemFuncRef out of the definition of Handler.
- Resolves: BZ#910201

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.20-3
- Rebuild for Boost-1.53.0

* Mon Jan 28 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.20-2
- Fixed memory leak in Perl bindings typemap.
- Resolves: BZ#885149

* Wed Jan 23 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.20-1
- Rebased Qpid on release 0.20.
- Rebased Store on SVN revision 4521.
- Fixed builds on ARM system by disabling RDMA support.
- Added a check in the store for ARM architecture.
- Resolves: BZ#820282

* Mon Nov 12 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18-6
- Changed qpidd.service to not start until after networking.

* Tue Oct 16 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18-5
- Install CMake file for C++ messaging examples.
- Moved qfm2.pc from qpid-qmf to qpid-qmf-devel
- Resolves: BZ#866892

* Sat Oct 13 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18-4
- Fixed building C++ messaging examples.
- Fixed ownership for /usr/share/qpidc and /usr/shar/qpidc/messaging
- Resolves: BZ#802791
- Resolves: BZ#756927

* Wed Oct 10 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18-3.2
- Fixed reference to systemctl.
- Resolves: BZ#864987

* Wed Oct 10 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18-3.1
- Added space to fix conditional.
- Resolves: BZ#864792

* Wed Sep 26 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18-3
- Removed the perl-qpid subpackage.

* Fri Sep 21 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18-2
- Added systemd support.
- Removed SysVInit support.
- Related: BZ#832724

* Wed Sep  5 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18-1
- Rebased on Qpid release 0.18.
- Added the new HA subpackage: qpid-cpp-server-ha
- Merged the qpid-cpp-server-daemon package back into qpid-cpp-server
- Resolves: BZ#854263
- qpid-cpp-server now provides qpid-cpp-server-daemon

* Mon Aug 20 2012 Dan Horák <dan[at]danny.cz> - 0.16-9
- allow build without InfiniBand eg. on s390(x)
- fix build on non-x86 64-bit arches

* Fri Aug 17 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-8
- Added the qpid-cpp-server-daemon subpackage.
  * This package delivers the SysVInit scripts needed by qpidd.

* Mon Aug 13 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-7
- QPID4095: Boost 1.50.0 has removed filesystem version 2 from the library

* Wed Aug  1 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-6.1
- Moved the QMF related swig descriptors to the qmf-devel package.

* Mon Jul 30 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-6
- Added patches for qpid-store to work with the new BDB packages.
- Added BR for libdb-devel and libdb4-cxx-devel, replacing db4-devel.

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 25 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-4
- Added the swig descriptor files to the client-devel package.

* Fri Jun 29 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-3
- Removed colons from conditions in QMF Ruby.
- Fixed string encoding for Ruby.

* Wed Jun 27 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-2
- Makes qmf/BrokerImportExport.h public.

* Mon Jun 18 2012 Rex Dieter <rdieter@fedoraproject.org> 0.16-1.5
- -server: Obsoletes -server-devel (and so it doesn't Obsoletes itself)

* Thu Jun 07 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-1.4
- Replaced the dependency on chkconfig and service binaries with packages.

* Wed Jun 06 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-1.3
- Fixed the Ruby directory macros to use the updated macros.

* Wed Jun 06 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-1.2
- Removed the qpid-cpp-server-devel subpackage.
  * qpid-cpp-server now obsoletes this as well.
- Removed macros that were defined for a shared specfile.
- Cleaned up the use of other macros.
- Cleaned up the package macros to be more consistent
- Fixed many rpmlint warnings and errors.

* Tue May 29 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-1.1
- Release 0.16 of Qpid upstream.
- Removed non-Fedora conditional areas of the specfile.
- Changed the location of qmfgen to the python sitelib directory.

* Tue Apr 17 2012 Dan Horák <dan[at]danny.cz> - 0.14-1.3
- fix build when size_t != unsigned int

* Tue Mar 20 2012 Nuno Santos <nsantos@redhat.com> - 0.14-3.1
- BZ692583 - QMF header files are in the wrong RPM

* Tue Mar 20 2012 Nuno Santos <nsantos@redhat.com> - 0.14-2.1
- BZ756927 - Spec file fixes for qpid-cpp

* Thu Feb 16 2012 Nuno Santos <nsantos@redhat.com> - 0.14-1.1
- Rebased to sync with upstream's official 0.14 release

* Wed Jan 18 2012 Nuno Santos <nsantos@redhat.com> - 0.12-7.1
- Added missing subpackage dependency

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-6.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
