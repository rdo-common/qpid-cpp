#
# Spec file for Qpid C++ packages: qpid-cpp-server*, qpid-cpp-client* and qmf
# svn revision: $Rev$
#

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?ruby_sitelib: %global ruby_sitelib %(/usr/bin/ruby -rrbconfig  -e 'puts Config::CONFIG["sitelibdir"] ')}
%{!?ruby_sitearch: %global ruby_sitearch %(/usr/bin/ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')}

# ===========
# The following section controls which rpms are produced for which builds.
# * To set the following flags, assign the value 1 for true; 0 for false.
# * These rpms produced by these two flags are mutually exclusive - ie they
#   won't duplicate any of the rpms.
# RHEL-6:
# * MRG_core is for building only RHEL-6 OS core components .
# * MRG_non_core is for building only RHEL-6 MRG product components.
# All other OSs (RHEL4/5/Fedora):
# * The MRG product is entirely external to the OS.
# * Set both MRG_core and MRG_non_core to true.
%global MRG_core            1
%global MRG_non_core        1

# Release numbers
%global qpid_release        0.6
%global qpid_svnrev         895736
%global store_svnrev        3795
# Change this release number for each build of the same qpid_svnrev, otherwise set back to 1.
%global release_num         4

# NOTE: no more than one of these flags should be set at the same time!
# RHEL-6 builds (the default) should have all these flags set to 0.
%global fedora              1
%global rhel_5              0

# ===========

# Note: if the mix is changed between MRG_core and MRG_non_core, then
# the files that will be removed at the end of the install section will
# need to be adjusted (moved from one section to the other).
%global client              %{MRG_core}
%global server              %{MRG_core}
%global qmf                 %{MRG_core}
%global ruby_qmf            %{MRG_core}
%global client_devel        %{MRG_non_core}
%global client_devel_docs   %{MRG_non_core}
%global server_devel        %{MRG_non_core}
%global qmf_devel           %{MRG_non_core}
%global client_rdma         %{MRG_non_core}
%global server_rdma         %{MRG_non_core}
%global client_ssl          %{MRG_non_core}
%global server_ssl          %{MRG_non_core}
%global server_xml          %{MRG_non_core}
%global server_cluster      %{MRG_non_core}
%global server_store        %{MRG_non_core}

# RHEL-6: Because core packages are .el6 and non-core .el6mrg, the {core_release}
# tag is needed for dependency checks of core packages from non-core packages.
# Non-RHEL-6: {core_release} is set to same value as {release} below.
%if %{fedora} || %{rhel_5}
%global core_release        %{release_num}%{?dist}
%else
%global core_release        %{release_num}.el6
%endif

# This overrides the package name - do not change this! It keeps all package
# names consistent, irrespective of the {name} varialbe - which changes for
# core and non-core builds.
%global pkg_name qpid-cpp

Name:           qpid-cpp
Version:        %{qpid_release}.%{qpid_svnrev}
Release:        %{release_num}%{?dist}.1
Summary:        Libraries for Qpid C++ client applications
Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://qpid.apache.org
Source0:        %{name}-%{version}.tar.gz
Source1:        store-%{qpid_release}.%{store_svnrev}.tar.gz
Source2:        qpidd.pp
%if %{fedora}
Patch0:         so_number.patch
Patch1:		xqilla.patch
Patch2:		boost_system.patch
Patch3:		db4.patch
Patch4:		qpidd.patch
Patch5:		qmf.rb.patch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if %{rhel_5}
ExclusiveArch:  i386 x86_64
%else
ExclusiveArch:  i686 x86_64
%endif
Vendor:         Red Hat, Inc.

BuildRequires: boost-devel
BuildRequires: doxygen
BuildRequires: libtool
BuildRequires: pkgconfig
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: python-devel
BuildRequires: swig
BuildRequires: cyrus-sasl-devel
BuildRequires: cyrus-sasl-lib
BuildRequires: cyrus-sasl
%if %{rhel_5}
BuildRequires: e2fsprogs-devel
%else
BuildRequires: boost-program-options
BuildRequires: boost-filesystem
BuildRequires: boost-system
BuildRequires: libuuid-devel
%endif

%if %{MRG_non_core}
BuildRequires: libibverbs-devel
BuildRequires: librdmacm-devel
BuildRequires: nss-devel
BuildRequires: nspr-devel
BuildRequires: xqilla-devel
BuildRequires: xerces-c-devel
BuildRequires: db4-devel
BuildRequires: libaio-devel
%if %{rhel_5}
BuildRequires: openais-devel
BuildRequires: cman-devel
%else
BuildRequires: corosynclib-devel >= 1.0.0-1
BuildRequires: clusterlib-devel >= 3.0.0-20
%endif
%endif # MRG_non_core


%description

Run-time libraries for AMQP client applications developed using Qpid
C++. Clients exchange messages with an AMQP message broker using
the AMQP protocol.

# === Package: qpid-cpp-client ===

%if %{client}

%package -n %{pkg_name}-client
Summary: Libraries for Qpid C++ client applications
Group: System Environment/Libraries
Requires: boost
Obsoletes: qpidc < %{version}
Provides:  qpidc = %{version}-%{release_num}

Requires(post):/sbin/chkconfig
Requires(preun):/sbin/chkconfig
Requires(preun):/sbin/service
Requires(postun):/sbin/service

%description -n %{pkg_name}-client
Run-time libraries for AMQP client applications developed using Qpid
C++. Clients exchange messages with an AMQP message broker using
the AMQP protocol.

%files -n %{pkg_name}-client
%defattr(-,root,root,-)
%doc cpp/LICENSE cpp/NOTICE cpp/README cpp/INSTALL cpp/RELEASE_NOTES cpp/DESIGN
%_libdir/libqpidcommon.so.*
%_libdir/libqpidclient.so.*
%dir %_libdir/qpid
%dir %_libdir/qpid/client
%dir %_sysconfdir/qpid
%config(noreplace) %_sysconfdir/qpid/qpidc.conf

%post -n %{pkg_name}-client
/sbin/ldconfig

%postun -n %{pkg_name}-client
/sbin/ldconfig

%endif # client

# === Package: qpid-cpp-client-devel ===

%if %{client_devel}

%package -n %{pkg_name}-client-devel
Summary: Header files, documentation and testing tools for developing Qpid C++ clients
Group: Development/System
Requires: %{pkg_name}-client = %{version}-%{core_release}
Requires: boost-devel
Requires: %_includedir/uuid/uuid.h
%if ! %{rhel_5}
Requires: boost-filesystem
Requires: boost-program-options
Requires: boost-system
%endif
Requires: python
Obsoletes: qpidc-devel < %{version}
Provides:  qpidc-devel = %{version}-%{release_num}
Obsoletes: qpidc-perftest < %{version}
Provides:  qpidc-perftest = %{version}-%{release_num}

%description -n %{pkg_name}-client-devel
Libraries, header files and documentation for developing AMQP clients
in C++ using Qpid.  Qpid implements the AMQP messaging specification.

%files -n %{pkg_name}-client-devel
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
%_libdir/libqpidcommon.so
%_libdir/libqpidclient.so
%_datadir/qpidc/examples
%defattr(755,root,root,-)
%_bindir/perftest
%_bindir/topic_listener
%_bindir/topic_publisher
%_bindir/latencytest
%_bindir/client_test
%_bindir/txtest

%post -n %{pkg_name}-client-devel
/sbin/ldconfig

%postun -n %{pkg_name}-client-devel
/sbin/ldconfig

%endif # client_devel

# === Package: qpid-cpp-client-devel-docs ===

%if %{client_devel_docs}

%package -n %{pkg_name}-client-devel-docs
Summary: AMQP client development documentation
Group: Documentation
%if !%{rhel_5}
BuildArch: noarch
%endif
Obsoletes: qpidc-devel-docs < %{version}
Provides:  qpidc-devel-docs = %{version}-%{release_num}

%description -n %{pkg_name}-client-devel-docs
This package includes the AMQP clients development documentation in HTML
format for easy browsing.

%files -n %{pkg_name}-client-devel-docs
%defattr(-,root,root,-)
%doc cpp/docs/api/html

%endif # client_devel_docs

# === Package: qpid-cpp-server ===

%if %{server}

%package -n %{pkg_name}-server
Summary: An AMQP message broker daemon
Group: System Environment/Daemons
Requires: %{pkg_name}-client = %{version}-%{release}
Requires: cyrus-sasl
Requires(post): policycoreutils
Requires(post): selinux-policy-base
Requires(post): /usr/sbin/semodule
Requires(postun): /usr/sbin/semodule
Obsoletes: qpidd < %{version}
Provides: qpidd = %{version}-%{release_num}
Obsoletes: qpidd-acl < %{version}
Provides: qpidd-acl = %{version}-%{release_num}

%description -n %{pkg_name}-server
A message broker daemon that receives stores and routes messages using
the open AMQP messaging protocol.

%files -n %{pkg_name}-server
%defattr(-,root,root,-)
%_datadir/selinux/packages/qpidd.pp
%_libdir/libqpidbroker.so.*
%_libdir/qpid/daemon/replicating_listener.so
%_libdir/qpid/daemon/replication_exchange.so
%_sbindir/qpidd
%config(noreplace) %_sysconfdir/qpidd.conf
%config(noreplace) %_sysconfdir/sasl2/qpidd.conf
%{_initrddir}/qpidd
%dir %_libdir/qpid/daemon
%_libdir/qpid/daemon/acl.so
%attr(755, qpidd, qpidd) %_localstatedir/lib/qpidd
%attr(755, qpidd, qpidd) %_localstatedir/run/qpidd
%attr(600, qpidd, qpidd) %config(noreplace) %_localstatedir/lib/qpidd/qpidd.sasldb
%doc %_mandir/man1/qpidd.*

%pre -n %{pkg_name}-server
getent group qpidd >/dev/null || groupadd -r qpidd
getent passwd qpidd >/dev/null || \
  useradd -r -M -g qpidd -d %{_localstatedir}/lib/qpidd -s /sbin/nologin \
    -c "Owner of Qpidd Daemons" qpidd
exit 0

%post -n %{pkg_name}-server
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add qpidd
/sbin/ldconfig
/usr/sbin/semodule -i %_datadir/selinux/packages/qpidd.pp

%preun -n %{pkg_name}-server
# Check that this is actual deinstallation, not just removing for upgrade.
if [ $1 = 0 ]; then
        /sbin/service qpidd stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del qpidd
fi

%postun -n %{pkg_name}-server
if [ "$1" -ge "1" ]; then
        /sbin/service qpidd condrestart >/dev/null 2>&1 || :
fi
/sbin/ldconfig
/usr/sbin/semodule -r qpidd

%endif # server

# === Package: qpid-cpp-server-devel ===

%if %{server_devel}

%package -n %{pkg_name}-server-devel
Summary: Libraries and header files for developing Qpid broker extensions
Group: Development/System
Requires: %{pkg_name}-client-devel = %{version}-%{release}
Requires: %{pkg_name}-server = %{version}-%{core_release}
Requires: boost-devel
%if !%{rhel_5}
Requires: boost-filesystem
Requires: boost-program-options
Requires: boost-system
%endif
Obsoletes: qpidd-devel < %{version}
Provides: qpidd-devel = %{version}-%{release_num}

%description -n %{pkg_name}-server-devel
Libraries and header files for developing extensions to the
Qpid broker daemon.

%files -n %{pkg_name}-server-devel
%defattr(-,root,root,-)
%_libdir/libqpidbroker.so
%_includedir/qpid/broker

%post -n %{pkg_name}-server-devel
/sbin/ldconfig

%postun -n %{pkg_name}-server-devel
/sbin/ldconfig

%endif # server_devel

# === Package: qmf ===

%if %{qmf}

%package -n qmf
Summary: The QPID Management Framework
Group: System Environment/Libraries
Requires: %{pkg_name}-client = %{version}-%{release}

%description -n qmf
An extensible managememt framework layered on QPID messaging.

%files -n qmf
%defattr(-,root,root,-)
%_libdir/libqmf.so.*
%_libdir/libqmfengine.so.*
%_libdir/libqmfconsole.so.*

%post -n qmf
/sbin/ldconfig

%postun -n qmf
/sbin/ldconfig

%endif # qmf

# === Package: qmf-devel ===

%if %{qmf_devel}

%package -n qmf-devel
Summary: Header files and tools for developing QMF extensions
Group: Development/System
Requires: qmf = %{version}-%{core_release}
Requires: %{pkg_name}-client-devel = %{version}-%{release}

%description -n qmf-devel
Header files and code-generation tools needed for developers of QMF-managed
components.

%files -n qmf-devel
%defattr(-,root,root,-)
%_libdir/libqmf.so
%_libdir/libqmfengine.so
%_libdir/libqmfconsole.so
%_bindir/qmf-gen
%{python_sitelib}/qmfgen

%post -n qmf-devel
/sbin/ldconfig

%postun -n qmf-devel
/sbin/ldconfig

%endif # qmf_devel

# === Package: ruby-qmf ===

%if %{ruby_qmf}

%package -n ruby-qmf
Summary: The QPID Management Framework bindings for ruby
Group: System Environment/Libraries
Requires: %{pkg_name}-client = %{version}-%{release}

%description -n ruby-qmf
An extensible managememt framework layered on QPID messaging, bindings
for ruby.

%files -n ruby-qmf
%defattr(-,root,root,-)
%{ruby_sitelib}/qmf.rb
%{ruby_sitearch}/qmfengine.so

%post -n ruby-qmf
/sbin/ldconfig

%postun -n ruby-qmf
/sbin/ldconfig

%endif # ruby_qmf

# === Package: qpid-cpp-client-rdma ===

%if %{client_rdma}

%package -n %{pkg_name}-client-rdma
Summary: RDMA Protocol support (including Infiniband) for Qpid clients
Group: System Environment/Libraries
Requires: %{pkg_name}-client = %{version}-%{core_release}
Obsoletes: qpidc-rdma < %{version}
Provides: qpidc-rdma = %{version}-%{release_num}

%description -n %{pkg_name}-client-rdma
A client plugin and support library to support RDMA protocols (including
Infiniband) as the transport for Qpid messaging.

%files -n %{pkg_name}-client-rdma
%defattr(-,root,root,-)
%_libdir/librdmawrap.so.*
%_libdir/qpid/client/rdmaconnector.so
%config(noreplace) %_sysconfdir/qpid/qpidc.conf

%post -n %{pkg_name}-client-rdma
/sbin/ldconfig

%postun -n %{pkg_name}-client-rdma
/sbin/ldconfig

%endif # client_rdma

# === Package: qpid-cpp-server-rdma ===

%if %{server_rdma}

%package -n %{pkg_name}-server-rdma
Summary: RDMA Protocol support (including Infiniband) for the Qpid daemon
Group: System Environment/Libraries
Requires: %{pkg_name}-server = %{version}-%{core_release}
Requires: %{pkg_name}-client-rdma = %{version}-%{release}
Obsoletes: qpidd-rdma < %{version}
Provides: qpidd-rdma = %{version}-%{release_num}

%description -n %{pkg_name}-server-rdma
A Qpid daemon plugin to support RDMA protocols (including Infiniband) as the
transport for AMQP messaging.

%files -n %{pkg_name}-server-rdma
%defattr(-,root,root,-)
%_libdir/qpid/daemon/rdma.so

%post -n %{pkg_name}-server-rdma
/sbin/ldconfig

%postun -n %{pkg_name}-server-rdma
/sbin/ldconfig

%endif # server_rdma

# === Package: qpid-cpp-client-ssl ===

%if %{client_ssl}

%package -n %{pkg_name}-client-ssl
Summary: SSL support for Qpid clients
Group: System Environment/Libraries
Requires: %{pkg_name}-client = %{version}-%{core_release}
Obsoletes: qpidc-ssl < %{version}
Provides: qpidc-ssl = %{version}-%{release_num}

%description -n %{pkg_name}-client-ssl
A client plugin and support library to support SSL as the transport
for Qpid messaging.

%files -n %{pkg_name}-client-ssl
%defattr(-,root,root,-)
%_libdir/libsslcommon.so.*
%_libdir/qpid/client/sslconnector.so

%post -n %{pkg_name}-client-ssl
/sbin/ldconfig

%postun -n %{pkg_name}-client-ssl
/sbin/ldconfig

%endif # client_ssl

# === Package: qpid-cpp-server-ssl ===

%if %{server_ssl}

%package -n %{pkg_name}-server-ssl
Summary: SSL support for the Qpid daemon
Group: System Environment/Libraries
Requires: %{pkg_name}-server = %{version}-%{core_release}
Requires: %{pkg_name}-client-ssl = %{version}-%{release}
Obsoletes: qpidd-ssl < %{version}
Provides: qpidd-ssl = %{version}-%{release_num}

%description -n %{pkg_name}-server-ssl
A Qpid daemon plugin to support SSL as the transport for AMQP
messaging.

%files -n %{pkg_name}-server-ssl
%defattr(-,root,root,-)
%_libdir/qpid/daemon/ssl.so

%post -n %{pkg_name}-server-ssl
/sbin/ldconfig

%postun -n %{pkg_name}-server-ssl
/sbin/ldconfig

%endif # server_ssl

# === Package: qpid-cpp-server-xml ===

%if %{server_xml}

%package -n %{pkg_name}-server-xml
Summary: XML extensions for the Qpid daemon
Group: System Environment/Libraries
Requires: %{pkg_name}-server = %{version}-%{core_release}
Requires: xqilla
Requires: xerces-c
Obsoletes: qpidd-xml < %{version}
Provides: qpidd-xml = %{version}-%{release_num}

%description -n %{pkg_name}-server-xml
A Qpid daemon plugin to support extended XML-based routing of AMQP
messages.

%files -n %{pkg_name}-server-xml
%defattr(-,root,root,-)
%_libdir/qpid/daemon/xml.so

%post -n %{pkg_name}-server-xml
/sbin/ldconfig

%postun -n %{pkg_name}-server-xml
/sbin/ldconfig

%endif # server_xml

# === Package: qpid-cpp-server-cluster ===

%if %{server_cluster}

%package -n %{pkg_name}-server-cluster
Summary: Cluster support for the Qpid daemon
Group: System Environment/Daemons
Requires: %{pkg_name}-server = %{version}-%{core_release}
Requires: %{pkg_name}-client = %{version}-%{core_release}
%if %{rhel_5}
Requires: openais
Requires: cman
%else
Requires: corosync >= 1.0.0-1
Requires: clusterlib >= 3.0.0-20
%endif
Obsoletes: qpidd-cluster < %{version}
Provides: qpidd-cluster = %{version}-%{release_num}

%description -n %{pkg_name}-server-cluster
%if %{rhel_5}
A Qpid daemon plugin enabling broker clustering using openais.
%else
A Qpid daemon plugin enabling broker clustering using corosync.
%endif

%files -n %{pkg_name}-server-cluster
%defattr(-,root,root,-)
%_libdir/qpid/daemon/cluster.so
%_libdir/qpid/daemon/watchdog.so
%_libexecdir/qpid/qpidd_watchdog

%post -n %{pkg_name}-server-cluster
%if %{rhel_5}
# [RHEL-5] openais: Make the qpidd user a member of the root group, and also make
# qpidd's primary group == ais.
usermod -g ais -G root qpidd
%else
# [RHEL-6, Fedora] corosync: Set up corosync permissions for user qpidd
cat > /etc/corosync/uidgid.d/qpidd <<EOF
uidgid {
        uid: qpidd
        gid: qpidd
}
EOF
%endif
/sbin/ldconfig

%postun -n %{pkg_name}-server-cluster
/sbin/ldconfig

%endif # server_cluster

# === Package: qpid-cpp-server-store ===

%if %{server_store}

%package -n %{pkg_name}-server-store
Summary: Red Hat persistence extension to the Qpid messaging system
Group: System Environment/Libraries
License: LGPL 2.1+
Requires: %{pkg_name}-server = %{version}-%{core_release}
Requires: db4
Requires: libaio
Obsoletes: rhm < %{version}
Provides: rhm = %{version}-%{release_num}

%description -n %{pkg_name}-server-store
Red Hat persistence extension to the Qpid AMQP broker: persistent message
storage using a libaio-based asynchronous journal. (Built from store svn
r.%{store_svnrev}.)

%files -n %{pkg_name}-server-store
%defattr(-,root,root,-)
%doc ../store-%{qpid_release}.%{store_svnrev}/README 
%_libdir/qpid/daemon/msgstore.so*
%_libexecdir/qpid/jrnl.py*
%_libexecdir/qpid/resize
%_libexecdir/qpid/store_chk
%attr(0775,qpidd,qpidd) %dir %_localstatedir/rhm

%post -n %{pkg_name}-server-store
/sbin/ldconfig

%postun -n %{pkg_name}-server-store
/sbin/ldconfig

%endif # server_store

%prep
# Sanity checks on flag settings
%if ! %{MRG_core} && ! %{MRG_non_core}
echo "ERROR: Neither {MRG_core} nor {MRG_non_core} is set true (1)."
exit 1
%endif
%if %{fedora} && %{rhel_5}
echo "ERROR: Both {fedora} and {rhel_5} are true (1) at the same time."
exit 1
%endif

%setup -q -n %{name}-%{version}
%setup -q -T -D -b 1 -n %{name}-%{version}
%if %{fedora}
%patch0
%patch1
%patch2
%patch4
%patch5
pushd ../store-%{qpid_release}.%{store_svnrev}
%patch3
popd
%endif
%global perftests "perftest topic_listener topic_publisher latencytest client_test txtest"

install -d selinux
install %{SOURCE2} selinux

%build
pushd cpp
./bootstrap
CXXFLAGS="%{optflags} -DNDEBUG -O3" \

%if %{MRG_non_core}
# [MRG_non_core] - Build everything with all options
%configure --disable-static --with-swig --with-sasl --with-cpg --with-xml --with-rdma --with-ssl --without-graphviz --without-help2man
make

# Make perftest utilities
pushd src/tests
for ptest in %{perftests}; do
    make $ptest
done
popd
popd

# Store
pushd ../store-%{qpid_release}.%{store_svnrev}
export CXXFLAGS="%{optflags} -DNDEBUG -O3" 
./bootstrap
%configure --disable-static --disable-rpath --disable-dependency-tracking --with-qpid-checkout=%{_builddir}/%{name}-%{version}
make

%else # MRG_non_core
# [MRG_core] - Build without options
%configure --disable-static --with-swig --with-sasl --without-cpg --without-xml --without-rdma --without-ssl --without-graphviz --without-help2man
make
%endif # MRG_non_core
popd

%install
rm -rf %{buildroot}
mkdir -p -m0755 %{buildroot}/%_bindir
pushd %{_builddir}/%{name}-%{version}/cpp
make install DESTDIR=%{buildroot}
install -Dp -m0755 etc/qpidd %{buildroot}%{_initrddir}/qpidd
install -d -m0755 %{buildroot}%{_localstatedir}/lib/qpidd
install -d -m0755 %{buildroot}%_libdir/qpidd
install -d -m0755 %{buildroot}/var/run/qpidd

%if %{MRG_non_core}
# Install perftest utilities
pushd src/tests/
for ptest in %{perftests}; do
  libtool --mode=install install -m755 $ptest %{buildroot}/%_bindir
done
popd
pushd docs/api
make html
popd

#Store
pushd %{_builddir}/store-%{qpid_release}.%{store_svnrev}
make install DESTDIR=%{buildroot}
install -d -m0775 %{buildroot}%{_localstatedir}/rhm
install -d -m0755 %{buildroot}%_libdir/qpid/daemon
rm -f %{buildroot}%_libdir/qpid/daemon/*.a
rm -f %{buildroot}%_libdir/qpid/daemon/*.la
rm -f %{buildroot}%_libdir/*.a
rm -f %{buildroot}%_libdir/*.la
rm -f %{buildroot}%_sysconfdir/rhmd.conf
popd
%endif # MRG_non_core

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
install -m 644 %{_builddir}/%{name}-%{version}/selinux/qpidd.pp %{buildroot}%{_datadir}/selinux/packages
install -pm 644 %{_builddir}/%{name}-%{version}/cpp/bindings/qmf/ruby/qmf.rb %{buildroot}%{ruby_sitelib}
install -pm 755 %{_builddir}/%{name}-%{version}/cpp/bindings/qmf/ruby/.libs/qmfengine.so %{buildroot}%{ruby_sitearch}

rm -f  %{buildroot}%_libdir/_*
rm -fr %{buildroot}%_libdir/qpid/tests
rm -fr %{buildroot}%_libexecdir/qpid/tests
rm -f  %{buildroot}%{ruby_sitearch}/qmfengine.la
rm -fr %{buildroot}%_includedir/qmf
popd

%if ! %{MRG_core}
rm -f  %{buildroot}%_sysconfdir/qpidd.conf
rm -f  %{buildroot}%_sysconfdir/rc.d/init.d/qpidd
rm -f  %{buildroot}%_sysconfdir/sasl2/qpidd.conf
rm -f  %{buildroot}%{ruby_sitelib}/qmf.rb
rm -f  %{buildroot}%_libdir/libqmf.so.*
rm -f  %{buildroot}%_libdir/libqmfconsole.so.*
rm -f  %{buildroot}%_libdir/libqmfengine.so.*
rm -f  %{buildroot}%_libdir/libqpidbroker.so.*
rm -f  %{buildroot}%_libdir/libqpidclient.so.*
rm -f  %{buildroot}%_libdir/libqpidcommon.so.*
rm -f  %{buildroot}%_libdir/qpid/daemon/acl.so
rm -f  %{buildroot}%_libdir/qpid/daemon/replicating_listener.so
rm -f  %{buildroot}%_libdir/qpid/daemon/replication_exchange.so
rm -f  %{buildroot}%{ruby_sitearch}/qmfengine.so
rm -f  %{buildroot}%_sbindir/qpidd
rm -f  %{buildroot}%_datadir/man/man1/qpidd.1*
rm -f  %{buildroot}%_datadir/selinux/packages/qpidd.pp
rm -f  %{buildroot}%_localstatedir/lib/qpidd/qpidd.sasldb
%endif

%if ! %{MRG_non_core}
rm -rf %{buildroot}%_includedir/qpid
rm -rf %{buildroot}%_datadir/qpidc/examples
rm -rf %{buildroot}%{python_sitelib}/qmfgen
rm -f  %{buildroot}%_bindir/qmf-gen
rm -f  %{buildroot}%_libdir/libqmf.so
rm -f  %{buildroot}%_libdir/libqmfconsole.so
rm -f  %{buildroot}%_libdir/libqmfengine.so
rm -f  %{buildroot}%_libdir/libqpidbroker.so
rm -f  %{buildroot}%_libdir/libqpidclient.so
rm -f  %{buildroot}%_libdir/libqpidcommon.so
%endif

%clean
rm -rf %{buildroot}

%check
# All tests currently disabled, using 'make check' takes too long.
# TODO: Find a small smoke test that runs quickly, perhaps a special make target?

#pushd %{_builddir}/%{name}-%{version}/cpp
# LANG=C needs to be in the environment to deal with a libtool issue
# temporarily disabling make check due to libtool issues
# needs to be re-enabled asap
#LANG=C ECHO=echo make check
#popd

# Store
#pushd %{_builddir}/store-%{qpid_release}.%{store_svnrev}
#make check
#popd

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.895736-4.1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon May  3 2010 Nuno Santos <nsantos@redhat.com> - 0.6.895736-4
- Patch for qmf.rb

* Tue Apr  6 2010 Nuno Santos <nsantos@redhat.com> - 0.6.895736-3
- BZ529448 - qpidd should not require selinux-policy-minimum

* Fri Mar 19 2010 Nuno Santos <nsantos@redhat.com> - 0.6.895736-2
- BZ574880 - Add restorecon to qpid init script

* Tue Mar 2 2010 Kim van der Riet<kim.vdriet@redhat.com> - 0.6.895736-1
- Imported unified specfile from RHEL maintained by Kim van der Riet

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
