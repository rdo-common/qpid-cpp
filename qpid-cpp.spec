# qpid-cpp

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# The following macros are no longer used for installation but only for cleanup
%{!?ruby_sitelib: %global ruby_sitelib %(/usr/bin/ruby -rrbconfig  -e 'puts Config::CONFIG["sitelibdir"] ')}
%{!?ruby_sitearch: %global ruby_sitearch %(/usr/bin/ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')}

# Release numbers
%global qpid_svnrev  1430909
%global store_svnrev 4521
# Change this release number for each build of the same qpid_svnrev, otherwise set back to 1.

# LIBRARY VERSIONS
%global QPIDCOMMON_VERSION_INFO             5:0:0
%global QPIDTYPES_VERSION_INFO              3:0:2
%global QPIDBROKER_VERSION_INFO             5:0:0
%global QPIDCLIENT_VERSION_INFO             5:0:0
%global QPIDMESSAGING_VERSION_INFO          4:0:1
%global QMF_VERSION_INFO                    4:0:0
%global QMF2_VERSION_INFO                   1:0:0
%global QMFENGINE_VERSION_INFO              4:0:0
%global QMFCONSOLE_VERSION_INFO             5:0:0
%global RDMAWRAP_VERSION_INFO               5:0:0
%global SSLCOMMON_VERSION_INFO              5:0:0

# Single var with all lib version params (except store) for make
%global LIB_VERSION_MAKE_PARAMS QPIDCOMMON_VERSION_INFO=%{QPIDCOMMON_VERSION_INFO} QPIDBROKER_VERSION_INFO=%{QPIDBROKER_VERSION_INFO} QPIDCLIENT_VERSION_INFO=%{QPIDCLIENT_VERSION_INFO} QPIDMESSAGING_VERSION_INFO=%{QPIDMESSAGING_VERSION_INFO} QMF_VERSION_INFO=%{QMF_VERSION_INFO} QMFENGINE_VERSION_INFO=%{QMFENGINE_VERSION_INFO} QMFCONSOLE_VERSION_INFO=%{QMFCONSOLE_VERSION_INFO} RDMAWRAP_VERSION_INFO=%{RDMAWRAP_VERSION_INFO} SSLCOMMON_VERSION_INFO=%{SSLCOMMON_VERSION_INFO}

Name:           qpid-cpp
Version:        0.20
Release:        3%{?dist}
Summary:        Libraries for Qpid C++ client applications
License:        ASL 2.0
URL:            http://qpid.apache.org

Source0:        http://www.apache.org/dist/qpid/%{version}/qpid-%{version}.tar.gz
Source1:        store-%{version}.%{store_svnrev}.tar.gz

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

Patch1: 01-Add-support-for-ARM-processors.patch
Patch2: 02-Fixed-db4-on-Fedora.patch
# BZ#885149
Patch3: 03-QPID-4493-Fixes-a-memory-leak-in-the-Perl-language-b.patch

%description

Run-time libraries for AMQP client applications developed using Qpid
C++. Clients exchange messages with an AMQP message broker using
the AMQP protocol.



%package -n qpid-cpp-client
Summary:   Libraries for Qpid C++ client applications

Requires:  boost
Requires:  chkconfig
Requires:  initscripts

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
%{_libdir}/libqpidcommon.so.*
%{_libdir}/libqpidclient.so.*
%{_libdir}/libqpidtypes.so.*
%{_libdir}/libqpidmessaging.so.*
%dir %{_libdir}/qpid
%dir %{_libdir}/qpid/client
%dir %{_sysconfdir}/qpid
%config(noreplace) %{_sysconfdir}/qpid/qpidc.conf

%post -n qpid-cpp-client -p /sbin/ldconfig

%postun -n qpid-cpp-client -p /sbin/ldconfig



%package -n qpid-cpp-client-devel
Summary:   Header files, documentation and testing tools for developing Qpid C++ clients

Requires:  qpid-cpp-client = %{version}-%{release}
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
%{_includedir}/qpid.i
%{_includedir}/swig_perl_typemaps.i
%{_includedir}/swig_python_typemaps.i
%{_includedir}/swig_ruby_typemaps.i
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
%{_includedir}/qmf
%{_libdir}/libqpidcommon.so
%{_libdir}/libqpidclient.so
%{_libdir}/libqpidtypes.so
%{_libdir}/libqpidmessaging.so
%{_libdir}/pkgconfig/qpid.pc
%{_datadir}/qpidc
%defattr(755,root,root,-)
%{_bindir}/qpid-perftest
%{_bindir}/qpid-topic-listener
%{_bindir}/qpid-topic-publisher
%{_bindir}/qpid-latency-test
%{_bindir}/qpid-client-test
%{_bindir}/qpid-txtest

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
%doc cpp/docs/api/html



%package -n qpid-cpp-server
Summary:   An AMQP message broker daemon
Obsoletes: qpid-cpp-server-devel <= %{version}-%{release}
Obsoletes: qpid-cpp-server-daemon < %{version}-%{release}
Provides:  qpid-cpp-server-daemon = %{version}-%{release}

Requires:  qpid-cpp-client = %{version}-%{release}
Requires:  cyrus-sasl

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description -n qpid-cpp-server
A message broker daemon that receives stores and routes messages using
the open AMQP messaging protocol.

%files -n qpid-cpp-server
%defattr(-,root,root,-)
%{_libdir}/libqpidbroker.so.*
%{_sbindir}/qpidd
%{_unitdir}/qpidd.service
%config(noreplace) %{_sysconfdir}/qpidd.conf
%config(noreplace) %{_sysconfdir}/sasl2/qpidd.conf
%dir %{_libdir}/qpid/daemon
%{_libdir}/qpid/daemon/acl.so
%attr(755, qpidd, qpidd) %{_localstatedir}/lib/qpidd
%ghost %attr(755, qpidd, qpidd) /var/run/qpidd
#%attr(600, qpidd, qpidd) %config(noreplace) %{_localstatedir}/lib/qpidd/qpidd.sasldb
%doc %{_mandir}/man1/qpidd.*

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
fi
/sbin/ldconfig



%package -n qpid-cpp-server-ha
Summary: Provides extensions to the AMQP message broker to provide high availability

Requires: qpid-cpp-server = %{version}-%{release}
Requires: qpid-qmf = %{version}-%{release}

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



%package -n qpid-qmf
Summary:   The QPID Management Framework

Provides:  qmf = %{version}-%{release}
Obsoletes: qmf < %{version}-%{release}

Requires:  qpid-cpp-client = %{version}-%{release}
Requires:  python-qpid >= %{version}

%description -n qpid-qmf
An extensible management framework layered on QPID messaging.

%files -n qpid-qmf
%defattr(-,root,root,-)
%{_libdir}/libqmf.so.*
%{_libdir}/libqmf2.so.*
%{_libdir}/libqmfengine.so.*
%{_libdir}/libqmfconsole.so.*

%post -n qpid-qmf -p /sbin/ldconfig

%postun -n qpid-qmf -p /sbin/ldconfig



%package -n qpid-qmf-devel
Summary:   Header files and tools for developing QMF extensions

Provides:  qmf-devel = %{version}-%{release}
Obsoletes: qmf-devel < %{version}-%{release}

Requires:  qpid-qmf = %{version}-%{release}
Requires:  qpid-cpp-client-devel = %{version}-%{release}

%description -n qpid-qmf-devel
Header files and code-generation tools needed for developers of QMF-managed
components.

%files -n qpid-qmf-devel
%defattr(-,root,root,-)
%{_libdir}/libqmf.so
%{_libdir}/libqmf2.so
%{_libdir}/libqmfengine.so
%{_libdir}/libqmfconsole.so
%{_includedir}/qmfengine.i
%{_includedir}/qmf2.i
%{_bindir}/qmf-gen
%{python_sitelib}/qmfgen
%{_libdir}/pkgconfig/qmf2.pc

%post -n qpid-qmf-devel -p /sbin/ldconfig

%postun -n qpid-qmf-devel -p /sbin/ldconfig



%package -n python-qpid-qmf
Summary:   The QPID Management Framework bindings for python

Provides:  python-qmf = %{version}-%{release}
Obsoletes: python-qmf < %{version}-%{release}

Requires:  qpid-qmf = %{version}-%{release}

# removes private-shared-object-provides warning
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}

%description -n python-qpid-qmf
An extensible management framework layered on QPID messaging, bindings
for python.

%files -n python-qpid-qmf
%defattr(-,root,root,-)
%{python_sitelib}/qpidtoollibs
%{python_sitearch}/qmf
%{python_sitearch}/cqpid.py*
%{python_sitearch}/_cqpid.so
%{python_sitearch}/qmf.py*
%{python_sitearch}/qmfengine.py*
%{python_sitearch}/_qmfengine.so
%{python_sitearch}/qmf2.py*
%{python_sitearch}/cqmf2.py*
%{python_sitearch}/_cqmf2.so
%{_bindir}/qpid-python-test
%exclude %{python_sitearch}/mllib
%exclude %{python_sitearch}/qpid
%exclude %{python_sitearch}/*.egg-info

%post -n python-qpid-qmf -p /sbin/ldconfig

%postun -n python-qpid-qmf -p /sbin/ldconfig



%package -n ruby-qpid-qmf
Summary:   The QPID Management Framework bindings for ruby

Provides:  ruby-qmf = %{version}-%{release}
Obsoletes: ruby-qmf < %{version}-%{release}

Requires:  qpid-qmf = %{version}-%{release}


%description -n ruby-qpid-qmf
An extensible management framework layered on QPID messaging, bindings
for ruby.

%files -n ruby-qpid-qmf
%defattr(-,root,root,-)
%{ruby_vendorlibdir}/qmf.rb
%{ruby_vendorlibdir}/qmf2.rb
%{ruby_vendorarchdir}/qmfengine.so
%{ruby_vendorarchdir}/cqpid.so
%{ruby_vendorarchdir}/cqmf2.so

%post -n ruby-qpid-qmf -p /sbin/ldconfig

%postun -n ruby-qpid-qmf -p /sbin/ldconfig



%ifnarch s390 s390x %{arm}
%package -n qpid-cpp-client-rdma
Summary:   RDMA Protocol support (including Infiniband) for Qpid clients

Requires:  qpid-cpp-client = %{version}-%{release}

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

Requires:  qpid-cpp-server = %{version}-%{release}
Requires:  qpid-cpp-client-rdma = %{version}-%{release}

%description -n qpid-cpp-server-rdma
A Qpid daemon plugin to support RDMA protocols (including Infiniband) as the
transport for AMQP messaging.

%files -n qpid-cpp-server-rdma
%defattr(-,root,root,-)
%{_libdir}/qpid/daemon/rdma.so

%post -n qpid-cpp-server-rdma -p /sbin/ldconfig

%postun -n qpid-cpp-server-rdma -p /sbin/ldconfig
%endif



%package -n qpid-cpp-client-ssl
Summary:   SSL support for Qpid clients

Requires:  qpid-cpp-client = %{version}-%{release}

%description -n qpid-cpp-client-ssl
A client plugin and support library to support SSL as the transport
for Qpid messaging.

%files -n qpid-cpp-client-ssl
%defattr(-,root,root,-)
%{_libdir}/libsslcommon.so.*
%{_libdir}/qpid/client/sslconnector.so

%post -n qpid-cpp-client-ssl -p /sbin/ldconfig

%postun -n qpid-cpp-client-ssl -p /sbin/ldconfig



%package -n qpid-cpp-server-ssl
Summary:   SSL support for the Qpid daemon

Requires:  qpid-cpp-server = %{version}-%{release}
Requires:  qpid-cpp-client-ssl = %{version}-%{release}

%description -n qpid-cpp-server-ssl
A Qpid daemon plugin to support SSL as the transport for AMQP
messaging.

%files -n qpid-cpp-server-ssl
%defattr(-,root,root,-)
%{_libdir}/qpid/daemon/ssl.so

%post -n qpid-cpp-server-ssl -p /sbin/ldconfig

%postun -n qpid-cpp-server-ssl -p /sbin/ldconfig



%package -n qpid-cpp-server-xml
Summary:   XML extensions for the Qpid daemon

Requires:  qpid-cpp-server = %{version}-%{release}
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

Obsoletes: rhm

Requires:  qpid-cpp-server = %{version}
Requires:  db4
Requires:  libaio

%description -n qpid-cpp-server-store
Red Hat persistence extension to the Qpid AMQP broker: persistent message
storage using either a libaio-based asynchronous journal, or synchronously
with Berkeley DB.

%files -n qpid-cpp-server-store
%defattr(-,root,root,-)
%doc ../store-%{version}.%{store_svnrev}/README
%{_libdir}/qpid/daemon/msgstore.so*
%{python_sitearch}/qpidstore/__init__.py*
%{python_sitearch}/qpidstore/jerr.py*
%{python_sitearch}/qpidstore/jrnl.py*
%{python_sitearch}/qpidstore/janal.py*
%{_libexecdir}/qpid/resize
%{_libexecdir}/qpid/store_chk
%attr(0775,qpidd,qpidd) %dir %{_localstatedir}/rhm

%post -n qpid-cpp-server-store -p /sbin/ldconfig

%postun -n qpid-cpp-server-store -p /sbin/ldconfig


%package -n qpid-tools
Summary:   Management and diagnostic tools for Apache Qpid

BuildArch: noarch

Requires:  python-qpid >= 0.8
Requires:  python-qmf = %{version}

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
%{_bindir}/qmf-tool
%doc LICENSE NOTICE
%if "%{python_version}" >= "2.6"
%{python_sitelib}/qpid_tools-*.egg-info
%endif



%prep
%setup -q -n qpid-%{version}
%setup -q -T -D -b 1 -n qpid-%{version}

%patch3 -p2

# qpid-store
pushd ../store-%{version}.%{store_svnrev}
%patch1 -p1
%patch2 -p1
popd

%global perftests "qpid-perftest qpid-topic-listener qpid-topic-publisher qpid-latency-test qpid-client-test qpid-txtest"

%global rh_qpid_tests_failover "failover_soak run_failover_soak"

%global rh_qpid_tests_clients "replaying_sender resuming_receiver declare_queues"

%build
pushd cpp
./bootstrap

CXXFLAGS="%{optflags} -DNDEBUG -O3 -Wno-unused-result" \
%configure --disable-static --with-swig --with-sasl --with-ssl --without-help2man \
--with-swig \
%ifnarch s390 s390x %{arm}
--with-rdma \
%else
--without-rdma \
%endif
--without-cpg \
--with-xml
ECHO=echo make %{LIB_VERSION_MAKE_PARAMS} %{?_smp_mflags}

# Make perftest utilities
pushd src/tests
for ptest in %{perftests}; do
  ECHO=echo make $ptest
done

popd

pushd ../python
./setup.py build
popd
pushd ../tools
./setup.py build
popd
pushd ../extras/qmf
./setup.py build
popd

# Store
pushd ../../store-%{version}.%{store_svnrev}
export CXXFLAGS="%{optflags} -DNDEBUG"
./bootstrap
%configure --disable-static --disable-rpath --disable-dependency-tracking --with-qpid-checkout=%{_builddir}/qpid-%{version}
make %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}
mkdir -p -m0755 %{buildroot}/%{_bindir}
mkdir -p -m0755 %{buildroot}/%{_unitdir}

(cd python; %{__python} setup.py install --skip-build --install-purelib %{python_sitearch} --root %{buildroot})
(cd extras/qmf; %{__python} setup.py install --skip-build --install-purelib %{python_sitearch} --root %{buildroot})
pushd %{_builddir}/qpid-%{version}/cpp
make install DESTDIR=%{buildroot}

install -d -m0755 %{buildroot}%{_localstatedir}/lib/qpidd
install -d -m0755 %{buildroot}%{_libdir}/qpidd
install -d -m0755 %{buildroot}/var/run/qpidd

#install the daemon files in the right location
mkdir -p %{buildroot}/%{_initrddir}
install %{buildroot}/%{_sysconfdir}/init.d/qpidd %{buildroot}/%{_initrddir}/qpidd
rm -f %{buildroot}/%{_sysconfdir}/init.d/qpidd
install %{buildroot}/%{_sysconfdir}/init.d/qpidd-primary %{buildroot}/%{_initrddir}/qpidd-primary
rm -f %{buildroot}/%{_sysconfdir}/init.d/qpidd-primary

# Install perftest utilities
pushd src/tests/
for ptest in %{perftests}; do
  libtool --mode=install install -m755 $ptest %{buildroot}/%{_bindir}
done

popd
pushd docs/api
make html
popd

pushd ../tools
./setup.py install --skip-build --root $RPM_BUILD_ROOT
popd

# remove things we don't want to package
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.l
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/libqpidbroker.so
rm -f %{buildroot}%{_libdir}/libsslcommon.so
rm -f %{buildroot}%{_libdir}/qpid/client/*.la
rm -f %{buildroot}%{_libdir}/qpid/daemon/*.la
rm -f %{buildroot}%{_libdir}/libcqpid_perl.so
rm -rf %{buildroot}%{ruby_sitearch}
rm -rf %{buildroot}%{ruby_sitelib}
rm -rf %{buildroot}%{_libdir}/perl5

# this should be fixed in the examples Makefile (make install)
rm -f %{buildroot}%{_datadir}/qpidc/examples/Makefile
rm -f %{buildroot}%{_datadir}/qpidc/examples/README.txt
rm -rf %{buildroot}%{_datadir}/qpidc/examples/direct
rm -rf %{buildroot}%{_datadir}/qpidc/examples/failover
rm -rf %{buildroot}%{_datadir}/qpidc/examples/fanout
rm -rf %{buildroot}%{_datadir}/qpidc/examples/pub-sub
rm -rf %{buildroot}%{_datadir}/qpidc/examples/qmf-console
rm -rf %{buildroot}%{_datadir}/qpidc/examples/request-response
rm -rf %{buildroot}%{_datadir}/qpidc/examples/tradedemo
rm -rf %{buildroot}%{_datadir}/qpidc/examples/xml-exchange

# install systemd files
install -pm 644 %{_builddir}/qpid-%{version}/cpp/etc/qpidd.service %{buildroot}/%{_unitdir}
rm -f %{buildroot}/%{_initrddir}/qpidd
rm -f %{buildroot}/%{_sysconfdir}/init.d/qpidd.service

install -d %{buildroot}%{python_sitearch}
install -pm 644 %{_builddir}/qpid-%{version}/cpp/bindings/qpid/python/cqpid.py %{buildroot}%{python_sitearch}
install -pm 644 %{_builddir}/qpid-%{version}/cpp/bindings/qpid/python/.libs/_cqpid.so %{buildroot}%{python_sitearch}
install -pm 644 %{_builddir}/qpid-%{version}/cpp/bindings/qmf/python/*.py %{buildroot}%{python_sitearch}
install -pm 644 %{_builddir}/qpid-%{version}/cpp/bindings/qmf/python/.libs/_qmfengine.so %{buildroot}%{python_sitearch}
install -pm 644 %{_builddir}/qpid-%{version}/cpp/bindings/qmf2/python/*.py %{buildroot}%{python_sitearch}
install -pm 644 %{_builddir}/qpid-%{version}/cpp/bindings/qmf2/python/.libs/_cqmf2.so %{buildroot}%{python_sitearch}

chmod +x %{buildroot}%{python_sitelib}/qpidtoollibs/disp.py
chmod +x %{buildroot}%{python_sitearch}/*.so

# remove on 64-bit arches
%ifarch x86_64 ppc64 s390x sparc64
rm -rf %{buildroot}%{python_sitelib}/cqmf2.py*
rm -rf %{buildroot}%{python_sitelib}/cqpid.py*
rm -rf %{buildroot}%{python_sitelib}/qmf.py*
rm -rf %{buildroot}%{python_sitelib}/qmf2.py*
rm -rf %{buildroot}%{python_sitelib}/qmfengine.py*
%endif
rm -rf %{buildroot}%{python_sitearch}/_cqmf2.la
rm -rf %{buildroot}%{python_sitearch}/_cqpid.la
rm -rf %{buildroot}%{python_sitearch}/_qmfengine.la
rm -rf %{buildroot}%{python_sitearch}/.libs

install -d %{buildroot}%{ruby_vendorlibdir}
install -d %{buildroot}%{ruby_vendorarchdir}
install -pm 644 %{_builddir}/qpid-%{version}/cpp/bindings/qmf/ruby/qmf.rb %{buildroot}%{ruby_vendorlibdir}
install -pm 644 %{_builddir}/qpid-%{version}/cpp/bindings/qmf2/ruby/qmf2.rb %{buildroot}%{ruby_vendorlibdir}
install -pm 755 %{_builddir}/qpid-%{version}/cpp/bindings/qpid/ruby/.libs/cqpid.so %{buildroot}%{ruby_vendorarchdir}
install -pm 755 %{_builddir}/qpid-%{version}/cpp/bindings/qmf/ruby/.libs/qmfengine.so %{buildroot}%{ruby_vendorarchdir}
install -pm 755 %{_builddir}/qpid-%{version}/cpp/bindings/qmf2/ruby/.libs/cqmf2.so %{buildroot}%{ruby_vendorarchdir}

rm -f %{buildroot}%{_libdir}/_*
rm -rf %{buildroot}%{_libdir}/qpid/tests
rm -rf %{buildroot}%{_libexecdir}/qpid/tests
popd

#Store
pushd %{_builddir}/store-%{version}.%{store_svnrev}
make install DESTDIR=%{buildroot}
install -d -m0775 %{buildroot}%{_localstatedir}/rhm
install -d -m0755 %{buildroot}%{_libdir}/qpid/daemon
rm -f %{buildroot}%{_libdir}/qpid/daemon/*.a
rm -f %{buildroot}%{_libdir}/qpid/daemon/*.la
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_sysconfdir}/rhmd.conf
popd

# install swig definition files
pushd %{_builddir}/qpid-%{version}
install -p -m 644 cpp/bindings/qpid/qpid.i %{buildroot}%{_includedir}
install -p -m 644 cpp/bindings/qmf/qmfengine.i %{buildroot}%{_includedir}
install -p -m 644 cpp/bindings/qmf2/qmf2.i %{buildroot}%{_includedir}
install -p -m 644 cpp/bindings/swig_perl_typemaps.i %{buildroot}%{_includedir}
install -p -m 644 cpp/bindings/swig_python_typemaps.i %{buildroot}%{_includedir}
install -p -m 644 cpp/bindings/swig_ruby_typemaps.i %{buildroot}%{_includedir}
popd

%clean
rm -rf %{buildroot}


%check


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%changelog
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

* Fri Jun 07 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-1.4
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

* Thu Dec 08 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.12-6.2
- Fixed the Boost.Singleton issue (thanks to Petr Machata's patch: #761045)

* Wed Dec 07 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.12-5.2
- Rebuilt for Boost-1.48

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4.2
- Rebuilt for glibc bug#747377

* Thu Oct 20 2011 Nuno Santos <nsantos@redhat.com> - 0.12-4.1
- BZ747351 - python-qpid-qmf has namespace collision

* Thu Sep 22 2011 Nuno Santos <nsantos@redhat.com> - 0.12-3.1
- BZ705208 - [RFE] qpid needs package config files for dependency usage by autotools

* Tue Sep 20 2011 Nuno Santos <nsantos@redhat.com> - 0.12-2.1
- Updated patch for qmf-related issues fixed post-0.12

* Tue Aug 30 2011 Nuno Santos <nsantos@redhat.com> - 0.12-1.1
- Rebased to sync with upstream's official 0.12 release

* Sun Aug 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.10-4.1
- Rebuilt for rpm (#728707)

* Thu Jul 21 2011 Jaroslav Reznik <jreznik@redhat.com> - 0.10-4
- Rebuilt for boost 1.47.0

* Tue Jun 14 2011 Nuno Santos <nsantos@redhat.com> - 0.10-3
- BZ709948 - package the perl bindings (patch from jpo@di.uminho.pt)

* Mon May  2 2011 Nuno Santos <nsantos@redhat.com> - 0.10-1
- Rebased to sync with upstream's official 0.10 release

* Sun Apr 17 2011 Kalev Lember <kalev@smartlink.ee> - 0.8-8
- Rebuilt for boost 1.46.1 soname bump

* Thu Mar 10 2011 Kalev Lember <kalev@smartlink.ee> - 0.8-7
- Rebuilt with xerces-c 3.1

* Tue Feb 22 2011 Nuno Santos <nsantos@redhat.com> - 0.8-6
- BZ661736 - renaming qmf subpackage to qpid-qmf

* Mon Feb 14 2011 Nuno Santos <nsantos@redhat.com> - 0.8-5
- Updated qmf patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Nuno Santos <nsantos@redhat.com> - 0.8-4
- BZ671520 - SELinux is preventing /usr/bin/updatedb from 'getattr' accesses on the directory /var/run/qpidd

* Mon Feb  7 2011 Nuno Santos <nsantos@redhat.com> - 0.8-3
- Updated qmf-related patch, includes previous size_t-related patch
- New patch to deal with updated boost
- BZ665366 - qpidd post install is blowing away default SELinux policy

* Thu Jan 21 2011 Dan Horák <dan[at]danny.cz> - 0.8-2
- fix build with different size_t - https://issues.apache.org/jira/browse/QPID-2996

* Mon Jan 10 2011 Nuno Santos <nsantos@redhat.com> - 0.8-1
- Rebased to sync with upstream's official 0.8 release, based on svn rev 1037942

* Tue Dec 21 2010 Dan Horák <dan[at]danny.cz> - 0.7.946106-4.1
- don't build with InfiniBand support on s390(x)
- don't limit architectures in Fedora

* Mon Nov 29 2010 Nuno Santos <nsantos@redhat.com> - 0.7.946106-4
- BZ656680 - Update Spec File to use ghost macro on files in /var/run

* Tue Jul 27 2010 Nuno Santos <nsantos@redhat.com> - 0.7.946106-2
- Patch for autoconf swig version comparison macro

* Tue Jul 22 2010 Nuno Santos <nsantos@redhat.com> - 0.7.946106-1
- Rebased to sync with mrg

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
