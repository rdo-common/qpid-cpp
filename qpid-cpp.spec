
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?ruby_sitelib: %global ruby_sitelib %(ruby -rrbconfig  -e 'puts Config::CONFIG["sitelibdir"]')}
%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"]')}

%global qpid_svnrev 829175
%global rhm_svnrev 3684

Name:          qpid-cpp
Version:       0.5.%{qpid_svnrev}
Release:       4%{?dist}
Summary:       Libraries for Qpid C++ client applications
Group:         System Environment/Libraries
License:       ASL 2.0 and LGPLv2
URL:           http://qpid.apache.org
Source0:       qpidc-%{version}.tar.gz
Source1:       rhm-0.5.%{rhm_svnrev}.tar.gz
Source2:       qpidd.pp
Patch0:        so_number.patch
Patch1:        qmf.patch
Patch2:        bz538355.patch
Patch3:        xqilla.patch
Patch4:        db4.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: boost-devel
BuildRequires: boost-program-options
BuildRequires: boost-filesystem
BuildRequires: doxygen
BuildRequires: e2fsprogs-devel
BuildRequires: libuuid-devel
BuildRequires: libtool
BuildRequires: pkgconfig
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: python
BuildRequires: python-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: cyrus-sasl-lib
BuildRequires: cyrus-sasl
BuildRequires: libibverbs-devel
BuildRequires: librdmacm-devel
BuildRequires: nss-devel
BuildRequires: nspr-devel
BuildRequires: xqilla-devel
BuildRequires: xerces-c-devel
BuildRequires: corosynclib-devel >= 1.0.0-1
BuildRequires: clusterlib-devel >= 3.0.0-20
BuildRequires: swig

%ifarch i386 i586 i686 x86_64
#RHM
BuildRequires: db4-devel
BuildRequires: libaio-devel
#/RHM
%endif

%description
Run-time libraries for AMQP client applications developed using Qpid
C++. Clients exchange messages with an AMQP message broker using
the AMQP protocol.

%package client
Summary: Libraries for Qpid C++ client applications
Requires: boost
Obsoletes: qpidc < %{version}-4
Provides: qpidc = %{version}-4
License: ASL 2.0

Requires(post):/sbin/chkconfig
Requires(preun):/sbin/chkconfig
Requires(preun):/sbin/service
Requires(postun):/sbin/service

%description client
Run-time libraries for AMQP client applications developed using Qpid
C++. Clients exchange messages with an AMQP message broker using
the AMQP protocol.

%package client-devel
Summary: Header files and documentation for developing Qpid C++ clients
Group: Development/System
Requires: qpid-cpp-client = %{version}-%{release}
Requires: boost-devel
Requires: boost-program-options
Requires: boost-filesystem
Requires: e2fsprogs-devel
Requires: libuuid-devel
Requires: python
Obsoletes: qpidc-devel < %{version}-4
Provides: qpidc-devel = %{version}-4
License: ASL 2.0

%description client-devel
Libraries, header files and documentation for developing AMQP clients
in C++ using Qpid.  Qpid implements the AMQP messaging specification.

%package client-devel-docs
Summary: AMQP client development documentation
Group: Documentation
BuildArch: noarch
Obsoletes: qpidc-devel-docs < %{version}-4
Provides: qpidc-devel-docs = %{version}-4
License: ASL 2.0

%description client-devel-docs
This package includes the AMQP clients development documentation in HTML
format for easy browsing.

%package server
Summary: An AMQP message broker daemon
Group: System Environment/Daemons
Requires: qpid-cpp-client = %{version}-%{release}
Requires: cyrus-sasl
Obsoletes: qpidd < %{version}-4
Provides: qpidd = %{version}-4
Requires(post): policycoreutils
Requires(post): selinux-policy-minimum
Requires(post): /usr/sbin/semodule
Requires(postun): /usr/sbin/semodule
License: ASL 2.0

%description server
A message broker daemon that receives stores and routes messages using
the open AMQP messaging protocol.

%package server-devel
Summary: Libraries and header files for developing Qpid broker extensions
Group: Development/System
Requires: qpid-cpp-client-devel = %{version}-%{release}
Requires: qpid-cpp-server = %{version}-%{release}
Requires: boost-devel
Requires: boost-program-options
Requires: boost-filesystem
Obsoletes: qpidd-devel < %{version}-4
Provides: qpidd-devel = %{version}-4
License: ASL 2.0

%description server-devel
Libraries and header files for developing extensions to the
Qpid broker daemon.

%package -n qmf
Summary: The QPID Management Framework
Group: System Environment/Daemons
Requires: qpid-cpp-client = %{version}-%{release}
License: ASL 2.0

%description -n qmf
An extensible managememt framework layered on QPID messaging.

%package -n qmf-devel
Summary: Header files and tools for developing QMF extensions
Group: Development/System
Requires: qmf = %{version}-%{release}
Requires: qpid-cpp-client-devel = %{version}-%{release}
License: ASL 2.0

%description -n qmf-devel
Header files and code-generation tools needed for developers of QMF-managed
components.

%package -n ruby-qmf
Summary: The QPID Management Framework bindings for ruby
Group: System Environment/Libraries
Requires: qpid-cpp-client = %{version}-%{release}
License: ASL 2.0

%description -n ruby-qmf
An extensible managememt framework layered on QPID messaging, bindings
for ruby.

%package server-acl
Summary: ACL based security for the Qpid daemon
Group: System Environment/Libraries
Requires: qpid-cpp-server = %{version}-%{release}
Obsoletes: qpidd-acl < %{version}-4
Provides: qpidd-acl = %{version}-4
License: ASL 2.0

%description server-acl
A Qpid daemon plugin to support ACL-based access control.

%package client-rdma
Summary: RDMA Protocol support (including Infiniband) for Qpid clients
Group: System Environment/Libraries
Requires: qpid-cpp-client = %{version}-%{release}
Obsoletes: qpidc-rdma < %{version}-4
Provides: qpidc-rdma = %{version}-4
License: ASL 2.0

%description client-rdma
A client plugin and support library to support RDMA protocols (including
Infiniband) as the transport for Qpid messaging.

%package server-rdma
Summary: RDMA Protocol support (including Infiniband) for the Qpid daemon
Group: System Environment/Libraries
Requires: qpid-cpp-server = %{version}-%{release}
Requires: qpid-cpp-client-rdma = %{version}-%{release}
Obsoletes: qpidd-rdma < %{version}-4
Provides: qpidd-rdma = %{version}-4
License: ASL 2.0

%description server-rdma
A Qpid daemon plugin to support RDMA protocols (including Infiniband) as the
transport for AMQP messaging.

%package client-ssl  
Summary: SSL support for Qpid clients
Group: System Environment/Libraries
Requires: qpid-cpp-client = %{version}-%{release}
Obsoletes: qpidc-ssl < %{version}-4
Provides: qpidc-ssl = %{version}-4
License: ASL 2.0

%description client-ssl
A client plugin and support library to support SSL as the transport
for Qpid messaging.

%package server-ssl
Summary: SSL support for the Qpid daemon
Group: System Environment/Libraries
Requires: qpid-cpp-server = %{version}-%{release}
Requires: qpid-cpp-client-ssl = %{version}-%{release}
Obsoletes: qpidd-ssl < %{version}-4
Provides: qpidd-ssl = %{version}-4
License: ASL 2.0

%description server-ssl
A Qpid daemon plugin to support SSL as the transport for AMQP
messaging.

%package server-xml
Summary: XML extensions for the Qpid daemon
Group: System Environment/Libraries
Requires: qpid-cpp-server = %{version}-%{release}
Requires: xqilla
Requires: xerces-c
Obsoletes: qpidd-xml < %{version}-4
Provides: qpidd-xml = %{version}-4
License: ASL 2.0

%description server-xml
A Qpid daemon plugin to support extended XML-based routing of AMQP
messages.

%package server-cluster
Summary: Cluster support for the Qpid daemon
Group: System Environment/Daemons
Requires: qpid-cpp-server = %{version}-%{release}
Requires: qpid-cpp-client = %{version}-%{release}
Requires: corosync >= 1.0.0-1
Requires: clusterlib >= 3.0.0-20
Obsoletes: qpidd-cluster < %{version}-4
Provides: qpidd-cluster = %{version}-4
License: ASL 2.0

%description server-cluster
A Qpid daemon plugin enabling broker clustering using openais

%package perftest
Summary: Simple benchmarking tools
Group: System Environment/Tools
Requires: qpid-cpp-client = %{version}-%{release}
Obsoletes: qpidc-perftest < %{version}-4
Provides: qpidc-perftest = %{version}-4
License: ASL 2.0

%description perftest
Tools for performing testing and benchmarking of MRG-Messaging

%ifarch i386 i586 i686 x86_64
#RHM
%package server-store
Summary: Red Hat persistence extension to the Qpid messaging system
Group: System Environment/Libraries
Requires: qpid-cpp-server = %{version}-%{release}
Requires: db4
Obsoletes: rhm < 0.5.%{rhm_svnrev}-4
Provides: rhm = 0.5.%{rhm_svnrev}-4
License: LGPLv2

%description server-store
Red Hat persistence extension to the Qpid AMQP broker: persistent message
storage using either a libaio-based asynchronous journal, or synchronously
with Berkeley DB.
#/RHM
%endif

%pre server
getent group qpidd >/dev/null || groupadd -r qpidd
getent passwd qpidd >/dev/null || \
  useradd -r -M -g qpidd -d %{_localstatedir}/lib/qpidd -s /sbin/nologin \
    -c "Owner of Qpidd Daemons" qpidd
exit 0

%prep
%setup -q -n qpidc-%{version}
%patch0
%patch1
%patch2
%patch3 -p1
install -d selinux
install %{SOURCE2} selinux

%setup -q -T -D -b 1 -n rhm-0.5.%{rhm_svnrev}
%patch4 -p1

# fix spurious-executable-perm warnings
find ../ \( -name '*.h' -o -name '*.cpp' \) -executable | xargs chmod a-x

%global perftests "perftest topic_listener topic_publisher latencytest client_test txtest"

%build
pushd ../qpidc-0.5.829175/cpp
./bootstrap
CXXFLAGS="%{optflags} -DNDEBUG -O3" \
%configure --disable-static --with-cpg --without-graphviz --without-help2man
ECHO=echo make #%{?_smp_mflags}

# Make perftest utilities
pushd src/tests
for ptest in %{perftests}; do
  ECHO=echo make $ptest
done
popd
popd

%ifarch i386 i586 i686 x86_64
#RHM
pushd ../rhm-0.5.%{rhm_svnrev}
export CXXFLAGS="%{optflags} -DNDEBUG" 
./bootstrap
%configure --disable-static --disable-rpath --disable-dependency-tracking --with-qpid-checkout=%{_builddir}/qpidc-%{version}
make dist
make #%{?_smp_mflags}
popd
#/RHM
%endif

%install
rm -rf %{buildroot}
mkdir -p -m0755 %{buildroot}/%_bindir
pushd %{_builddir}/qpidc-%{version}/cpp
make install DESTDIR=%{buildroot}
install -Dp -m0755 etc/qpidd %{buildroot}%{_initrddir}/qpidd
install -d -m0755 %{buildroot}%{_localstatedir}/lib/qpidd
install -d -m0755 %{buildroot}%{_libdir}/qpidd
install -d -m0755 %{buildroot}/var/run/qpidd
# Install perftest utilities
pushd src/tests/
for ptest in %{perftests}; do
  libtool --mode=install install -m755 $ptest %{buildroot}/%_bindir
done
popd
pushd docs/api
make html
popd
rm -f %{buildroot}%_libdir/*.a
rm -f %{buildroot}%_libdir/*.l
rm -f %{buildroot}%_libdir/*.la
rm -f %{buildroot}%_libdir/librdmawrap.so
rm -f %{buildroot}%_libdir/libsslcommon.so
rm -f %{buildroot}%_libdir/qpid/client/*.la
rm -f %{buildroot}%_libdir/qpid/daemon/*.la

# disable auth by default
echo "auth=no" >> %{buildroot}/etc/qpidd.conf

install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{_builddir}/qpidc-%{version}/selinux/qpidd.pp %{buildroot}%{_datadir}/selinux/packages
install -pm 644 %{_builddir}/qpidc-%{version}/cpp/bindings/qmf/ruby/qmf.rb %{buildroot}%{ruby_sitelib}
install -pm 755 %{_builddir}/qpidc-%{version}/cpp/bindings/qmf/ruby/.libs/qmfengine.so %{buildroot}%{ruby_sitearch}

rm -f %{buildroot}%_libdir/_*
rm -fr %{buildroot}%_libdir/qpid/tests
rm -fr %{buildroot}%_libexecdir/qpid/tests
rm -f %{buildroot}%{ruby_sitearch}/qmfengine.la
popd

%ifarch i386 i586 i686 x86_64
#RHM
pushd %{_builddir}/rhm-0.5.%{rhm_svnrev}
make install DESTDIR=%{buildroot}
install -d -m0775 %{buildroot}%{_localstatedir}/rhm
install -d -m0755 %{buildroot}%{_libdir}/qpid/daemon
rm -f %{buildroot}%_libdir/qpid/daemon/*.a
rm -f %{buildroot}%_libdir/qpid/daemon/*.la
rm -f %{buildroot}%_libdir/*.a
rm -f %{buildroot}%_libdir/*.la
rm %{buildroot}%_sysconfdir/rhmd.conf
popd
#/RHM
%endif

%clean
rm -rf %{buildroot}

%check
#pushd %{_builddir}/%{name}-%{version}/cpp
# LANG=C needs to be in the environment to deal with a libtool issue
# temporarily disabling make check due to libtool issues
# needs to be re-enabled asap
#LANG=C ECHO=echo make check
#popd

%ifarch i386 i586 i686 x86_64
#RHM
#pushd %{_builddir}/rhm-0.5.%{rhm_svnrev}
#make check
#popd
#/RHM
%endif

%files client
%defattr(-,root,root,-)
%doc ../qpidc-%{version}/cpp/LICENSE
%doc ../qpidc-%{version}/cpp/NOTICE
%doc ../qpidc-%{version}/cpp/README 
%doc ../qpidc-%{version}/cpp/INSTALL
%doc ../qpidc-%{version}/cpp/RELEASE_NOTES 
%doc ../qpidc-%{version}/cpp/DESIGN
%_libdir/libqpidcommon.so.3
%_libdir/libqpidcommon.so.3.0.0
%_libdir/libqpidclient.so.3
%_libdir/libqpidclient.so.3.0.0
%dir %_libdir/qpid
%dir %_libdir/qpid/client
%dir %_sysconfdir/qpid
%config(noreplace) %_sysconfdir/qpid/qpidc.conf

%files client-devel
%defattr(-,root,root,-)
%dir %_includedir/qpid
%_includedir/qpid/*.h
%_includedir/qpid/amqp_0_10
%_includedir/qpid/client
%_includedir/qpid/console
%_includedir/qpid/framing
%_includedir/qpid/sys
%_includedir/qpid/log
%_includedir/qpid/management
%_includedir/qpid/messaging
%_includedir/qpid/agent
%_includedir/qmf
%_libdir/libqpidcommon.so
%_libdir/libqpidclient.so
%_datadir/qpidc/examples

%files server
%defattr(-,root,root,-)
%_datadir/selinux/packages/qpidd.pp
%_libdir/libqpidbroker.so.3
%_libdir/libqpidbroker.so.3.0.0
%_libdir/qpid/daemon/replicating_listener.so
%_libdir/qpid/daemon/replication_exchange.so
%_libdir/qpid/daemon/watchdog.so
%_sbindir/qpidd
%_libexecdir/qpid/qpidd_watchdog
%config(noreplace) %_sysconfdir/qpidd.conf
%config(noreplace) %_sysconfdir/sasl2/qpidd.conf
%{_initrddir}/qpidd
%dir %_libdir/qpid/daemon
%attr(755, qpidd, qpidd) %_localstatedir/lib/qpidd
%attr(755, qpidd, qpidd) /var/run/qpidd
# qpidd.sasldb contains sasl credentials, needs to be readable only by root
%attr(600, qpidd, qpidd) %config(noreplace) %_localstatedir/lib/qpidd/qpidd.sasldb
%doc %_mandir/man1/qpidd.*

%files server-devel
%defattr(-,root,root,-)
%defattr(-,root,root,-)
%_libdir/libqpidbroker.so
%_includedir/qpid/broker

%files -n qmf
%defattr(-,root,root,-)
%_libdir/libqmf.so.1
%_libdir/libqmf.so.1.0.0
%_libdir/libqmfengine.so.1
%_libdir/libqmfengine.so.1.0.1
%_libdir/libqmfconsole.so.3
%_libdir/libqmfconsole.so.3.0.0

%files -n qmf-devel
%defattr(-,root,root,-)
%_libdir/libqmf.so
%_libdir/libqmfengine.so
%_libdir/libqmfconsole.so
%_bindir/qmf-gen
%{python_sitelib}/qmfgen

%files -n ruby-qmf
%defattr(-,root,root,-)
%{ruby_sitelib}/qmf.rb
%{ruby_sitearch}/qmfengine.so

%files server-acl
%defattr(-,root,root,-)
%_libdir/qpid/daemon/acl.so

%files client-rdma
%defattr(-,root,root,-)
%_libdir/librdmawrap.so.0
%_libdir/librdmawrap.so.0.0.0
%_libdir/qpid/client/rdmaconnector.so
%config(noreplace) %_sysconfdir/qpid/qpidc.conf

%files server-rdma
%defattr(-,root,root,-)
%_libdir/qpid/daemon/rdma.so

%files client-ssl
%defattr(-,root,root,-)
%_libdir/libsslcommon.so.3
%_libdir/libsslcommon.so.3.0.0
%_libdir/qpid/client/sslconnector.so

%files server-ssl
%defattr(-,root,root,-)
%_libdir/qpid/daemon/ssl.so

%files server-xml
%defattr(-,root,root,-)
%_libdir/qpid/daemon/xml.so

%files server-cluster
%defattr(-,root,root,-)
%_libdir/qpid/daemon/cluster.so

%files perftest
%defattr(755,root,root,-)
%_bindir/perftest
%_bindir/topic_listener
%_bindir/topic_publisher
%_bindir/latencytest
%_bindir/client_test
%_bindir/txtest

%files client-devel-docs
%defattr(-,root,root,-)
%doc ../qpidc-%{version}/cpp/docs/api/html

%ifarch i386 i586 i686 x86_64
%files server-store
%defattr(-,root,root,-)
%doc ../rhm-0.5.%{rhm_svnrev}/README 
%{_libdir}/qpid/daemon/msgstore.so*
# /var/rhm needs to be group writable so that journal files can be updated properly
%attr(0775,qpidd,qpidd) %dir %_localstatedir/rhm
%endif

%post client -p /sbin/ldconfig

%postun client -p /sbin/ldconfig

%post server
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add qpidd
/sbin/ldconfig
/usr/sbin/semodule -i %_datadir/selinux/packages/qpidd.pp

%preun server
# Check that this is actual deinstallation, not just removing for upgrade.
if [ $1 = 0 ]; then
        /sbin/service qpidd stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del qpidd
fi

%postun server
if [ "$1" -ge "1" ]; then
        /sbin/service qpidd condrestart >/dev/null 2>&1 || :
fi
/sbin/ldconfig

/usr/sbin/semodule -r qpidd

%post client-rdma -p /sbin/ldconfig

%postun client-rdma -p /sbin/ldconfig

%post client-ssl -p /sbin/ldconfig

%postun client-ssl -p /sbin/ldconfig

%post -n qmf -p /sbin/ldconfig

%postun -n qmf -p /sbin/ldconfig

%changelog
* Mon Feb  8 2010 Nuno Santos <nsantos@nsantos-laptop> - 0.5.829175-4
- Package rename

* Wed Dec  2 2009 Nuno Santos <nsantos@redhat.com> - 0.5.829175-3
- Patch for BZ538355

* Tue Nov  3 2009 Nuno Santos <nsantos@redhat.com> - 0.5.829175-2
- Add patch for qmf fixes

* Fri Oct 23 2009 Nuno Santos <nsantos@redhat.com> - 0.5.829175-1
- Rebased to svn rev 829175

* Thu Oct 15 2009 Nuno Santos <nsantos@redhat.com> - 0.5.825677-1
- Rebased to svn rev 825677

* Tue Sep 29 2009 Nuno Santos <nsantos@redhat.com> - 0.5.819819-1
- Rebased to svn rev 819819 for F12 beta

* Thu Sep 24 2009 Nuno Santos <nsantos@redhat.com> - 0.5.818599-1
- Rebased to svn rev 818599
- rhm-cpp-server-store obsoletes rhm top-level package

* Fri Sep 19 2009 Nuno Santos <nsantos@redhat.com> - 0.5.817349
- Rebased to svn rev 817349

* Wed Jul 29 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.5.790661-3
- Update BuildRequires and Requires to use latest stable versions of
  corosync and clusterlib.
- Unbreak perftests define (and fix vim spec syntax coloring).

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.790661-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  2 2009 Nuno Santos <nsantos@redhat.com> - 0.5.790661-1
- Rebased to svn rev 790661; .so lib numbers bumped

* Fri Jun 26 2009 Nuno Santos <nsantos@redhat.com> - 0.5.788782-1
- Rebased to svn rev 788782

* Mon Jun 22 2009 Nuno Santos <nsantos@redhat.com> - 0.5.787286-1
- Rebased to svn rev 787286

* Wed Jun 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.5.752600-8
- update BuildRequires to use corosynclib-devel in correct version.
- update BuildRequires to use clusterlib-devel instead of the obsoleted
  cmanlib-devel.
- drop Requires on cmanlib. This should come in automatically as part
  of the rpm build process.
- re-align package version to -8. -7 didn't have a changelog entry?
- add patch to port Cluster/Cpg to newest Cpg code.
- change patch tag to use patch0.

* Mon May  4 2009 Nuno Santos <nsantos@redhat.com> - 0.5.752600-5
- patch for SASL credentials refresh

* Wed Apr  1 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 0.5.752600-5
- Fix unowned examples directory in -devel pkg.

* Mon Mar 16 2009 Nuno Santos <nsantos@localhost.localdomain> - 0.5.752600-4
- BZ483925 - split docs into a separate noarch subpackage

* Mon Mar 16 2009 Nuno Santos <nsantos@redhat.com> - 0.5.752600-3
- Disable auth by default; fix selinux requires

* Wed Mar 11 2009 Nuno Santos <nsantos@redhat.com> - 0.5.752600-1
- Rebased to svn rev 752600

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.738618-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.738618-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Nuno Santos <nsantos@redhat.com> - 0.4.738618-2
- Rebased to svn rev 738618

* Tue Jan 20 2009 Nuno Santos <nsantos@redhat.com> - 0.4.734452-3
- BZ474614 and BZ474613 - qpidc/rhm unowned directories

* Thu Jan 15 2009 Nuno Santos <nsantos@redhat.com> - 0.4.734452-1
- Rebased to svn rev 734452

* Tue Dec 23 2008 Nuno Santos <nsantos@redhat.com> - 0.4.728142-1
- Rebased to svn rev 728142
- Re-enable cluster, now using corosync

* Tue Dec  2 2008 Nuno Santos <nsantos@redhat.com> - 0.3.722557-1
- Rebased to svn rev 722557
- Temporarily disabled cluster due to openais version incompatibility

* Wed Nov 26 2008 Nuno Santos <nsantos@redhat.com> - 0.3.720979-1
- Rebased to svn rev 720979

* Fri Nov 21 2008  Mick Goulish <mgoulish@redhat.com>
- updated to 719552

* Thu Nov 20 2008  Mick Goulish <mgoulish@redhat.com>
- updated to 719323
- For subpackage qpidd-cluster, added dependency to cman-devel.
- For subpackage qpidd-cluster, added dependency to qpidc.
- added BuildRequires cman-devel

* Fri Nov 14 2008 Justin Ross <jross@redhat.com> - 0.3.714072-1
- Update to svn rev 714072
- Enable building --with-cpg

* Wed Nov 12 2008 Justin Ross <jross@redhat.com> - 0.3.713378-1
- Update to svn rev 713378

* Fri Nov  7 2008 Justin Ross <jross@redhat.com> - 0.3.712127-1
- Update to svn rev 712127

* Thu Nov  6 2008 Nuno Santos <nsantos@redhat.com> - 0.3.711915-2
- Removed extraneous openais-devel dependency

* Thu Nov  6 2008 Justin Ross <jross@redhat.com> - 0.3.711915-1
- Update to svn rev 711915

* Tue Nov  4 2008 Nuno Santos <nsantos@redhat.com> - 0.3.709187-2
- Remove extraneous dependency

* Thu Oct 30 2008 Nuno Santos <nsantos@redhat.com> - 0.3.709187-1
- Rebsed to svn rev 709187

* Tue Oct 28 2008 Nuno Santos <nsantos@redhat.com> - 0.3.708576-1
- Rebased to svn rev 708576

* Mon Oct 27 2008 Nuno Santos <nsantos@redhat.com> - 0.3.708210-1
- Rebased to svn rev 708210; address make check libtool issue

* Fri Oct 24 2008 Justin Ross <jross@redhat.com> - 0.3.707724-1
- Update to revision 707724

* Thu Oct 23 2008 Justin Ross <jross@redhat.com> - 0.3.707468-1
- Don't use silly idenity defines
- Add new ssl and rdma subpackages
- Move cluster and xml plugins into their own subpackages
- Reflect new naming of plugins

* Wed Aug 21 2008 Justin Ross <jross@redhat.com> - 0.2.687156-1
- Update to source revision 687156 of the qpid.0-10 branch

* Wed Aug 14 2008 Justin Ross <jross@redhat.com> - 0.2.685273-1
- Update to source revision 685273 of the qpid.0-10 branch

* Wed Aug  6 2008 Justin Ross <jross@redhat.com> - 0.2.683301-1
- Update to source revision 683301 of the qpid.0-10 branch

* Thu Jul 15 2008 Justin Ross <jross@redhat.com> - 0.2.676581-1
- Update to source revision 676581 of the qpid.0-10 branch
- Work around home dir creation problem
- Use a license string that rpmlint likes

* Thu Jul 10 2008 Nuno Santos <nsantos@redhat.com> - 0.2.667603-3
- BZ453818: added additional tests to -perftest

* Thu Jun 13 2008 Justin Ross <jross@redhat.com> - 0.2.667603-1
- Update to source revision 667603

* Thu Jun 12 2008 Justin Ross <jross@redhat.com> - 0.2.667253-1
- Update to source revision 667253

* Thu Jun 12 2008 Nuno Santos <nsantos@redhat.com> - 0.2.666138-5
- add missing doc files

* Wed Jun 11 2008 Justin Ross <jross@redhat.com> - 0.2.666138-3
- Added directories for modules and pid files to install script

* Wed May 28 2008 David Sommerseth <dsommers@redhat.com> - 0.2.663761-1
- Added perftest utilities

* Thu May 22 2008 Nuno Santos <nsantos@redhat.com> - 0.2.656926-4
- Additional build flags for i686

* Tue May 20 2008 Nuno Santos <nsantos@redhat.com> - 0.2.656926-3
- BZ 432872: remove examples, which are being packaged separately

* Tue May 20 2008 Justin Ross <jross@redhat.com> -0.2.656926-2
- Drop build requirements for graphviz and help2man

* Wed May 14 2008 Nuno Santos <nsantos@redhat.com> - 0.2-34
- Bumped for Beta 4 release

* Fri May  9 2008 Matthew Farrellee <mfarrellee@redhat> - 0.2-33
- Moved qpidd.conf from qpidc package to qpidd package
- Added BuildRequires xqilla-devel and xerces-c-devel to qpidd for XML Exchange
- Added BuildRequires openais-devel to qpidd for CPG
- Added missing Requires xqilla-devel to qpidd-devel

* Thu May  8 2008 Matthew Farrellee <mfarrellee@redhat> - 0.2-32
- Added sasl2 config file for qpidd
- Added cyrus-sasl dependencies

* Wed May  7 2008 Matthew Farrellee <mfarrellee@redhat> - 0.2-31
- Added python dependency, needed by managementgen

* Wed May  7 2008 Matthew Farrellee <mfarrellee@redhat> - 0.2-30
- Added management-types.xml to qpidc-devel package

* Tue May  6 2008 Matthew Farrellee <mfarrellee@redhat> - 0.2-29
- Added managementgen to the qpidc-devel package

* Mon Apr 14 2008 Nuno Santos <nsantos@redhat.com> - 0.2-28
 - Fix home dir permissions
 - Bumped for Fedora 9

* Mon Mar 31 2008 Nuno Santos <nsantos@redhat.com> - 0.2-25
- Create user qpidd, start qpidd service as qpidd

* Mon Feb 18 2008 Rafael Schloming <rafaels@redhat.com> - 0.2-24
- Bug fix for TCK issue in Beta 3

* Thu Feb 14 2008 Rafael Schloming <rafaels@redhat.com> - 0.2-23
- Bumped to pull in fixes for Beta 3

* Tue Feb 12 2008 Alan Conway <aconway@redhat.com> - 0.2-22
- Added -g to compile flags for debug symbols.

* Tue Feb 12 2008 Alan Conway <aconway@redhat.com> - 0.2-21
- Create /var/lib/qpidd correctly.

* Mon Feb 11 2008 Rafael Schloming <rafaels@redhat.com> - 0.2-20
- bumped for Beta 3

* Mon Jan 21 2008 Gordon Sim <gsim@redhat.com> - 0.2-18
- bump up rev for recent changes to plugin modules & mgmt

* Thu Jan 03 2008 Nuno Santos <nsantos@redhat.com> - 0.2-17
- add missing header file SessionManager.h

* Thu Jan 03 2008 Nuno Santos <nsantos@redhat.com> - 0.2-16
- limit builds to i386 and x86_64 archs

* Thu Jan 03 2008 Nuno Santos <nsantos@redhat.com> - 0.2-15
- add ruby as a build dependency

* Tue Dec 18 2007 Nuno Santos <nsantos@redhat.com> - 0.2-14
- include fixes from Gordon Sim (fragmentation, lazy-loading, staging) 
  and Alan Conway (exception handling in the client).

* Thu Dec 6 2007 Alan Conway <aconway@redhat.com> - 0.2-13
- installcheck target to build examples in installation.

* Thu Nov 8 2007 Alan Conway <aconway@redhat.com> - 0.2-10
- added examples to RPM package.

* Thu Oct 9 2007 Alan Conway <aconway@redhat.com> - 0.2-9
- added config(noreplace) for qpidd.conf

* Thu Oct 4 2007 Alan Conway <aconway@redhat.com> - 0.2-8
- Added qpidd.conf configuration file.
- Updated man page to detail configuration options.

* Thu Sep 20 2007 Alan Conway <aconway@redhat.com> - 0.2-7
- Removed apr dependency.

* Wed Aug 1 2007 Alan Conway <aconway@redhat.com> - 0.2-6
- added --disable-cluster flag

* Tue Apr 17 2007 Alan Conway <aconway@redhat.com> - 0.2-5
- Add missing Requires: e2fsprogs-devel for qpidc-devel.

* Tue Apr 17 2007 Alan Conway <aconway@redhat.com> - 0.2-4
- longer broker_start timeout to avoid failures in plague builds.

* Tue Apr 17 2007 Alan Conway <aconway@redhat.com> - 0.2-3
- Add missing Requires: apr in qpidc.

* Mon Apr 16 2007 Alan Conway <aconway@redhat.com> - 0.2-2
- Bugfix for memory errors on x86_64.

* Thu Apr 12 2007 Alan Conway <aconway@redhat.com> - 0.2-1
- Bumped version number for rhm dependencies.

* Wed Apr 11 2007 Alan Conway <aconway@redhat.com> - 0.1-5
- Add qpidd-devel sub-package.

* Mon Feb 19 2007 Jim Meyering <meyering@redhat.com> - 0.1-4
- Address http://bugzilla.redhat.com/220630:
- Remove redundant "cppunit" build-requires.
- Add --disable-static.

* Thu Jan 25 2007 Alan Conway <aconway@redhat.com> - 0.1-3
- Applied Jim Meyerings fixes from http://mail-archives.apache.org/mod_mbox/incubator-qpid-dev/200701.mbox/<87hcugzmyp.fsf@rho.meyering.net>

* Mon Dec 22 2006 Alan Conway <aconway@redhat.com> - 0.1-1
- Fixed all rpmlint complaints (with help from David Lutterkort)
- Added qpidd --daemon behaviour, fix init.rc scripts

* Fri Dec  8 2006 David Lutterkort <dlutter@redhat.com> - 0.1-1
- Initial version based on Jim Meyering's sketch and discussions with Alan
  Conway
