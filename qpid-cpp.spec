# Define pkgdocdir for releases that don't define it already
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%global _perldocdir %{_docdir}/perl-qpid-messaging-%{version}
%global pythonx python2

%{!?__python2:%global __python2 %{__python}}
%{!?__python2:%global python2_sitelib %{python_sitelib}}
%{!?__python2:%global python2_sitearch %{python_sitearch}}
%{!?__python2:%global pythonx python}

%global _pythondocdir %{_docdir}/%{pythonx}-qpid-messaging-%{version}

# We ship a .pc file but don't need to depend on pkg-config
%global __requires_exclude pkg-config
%global __provides_exclude_from ^(%{python2_sitearch}/.*\\.so|%{_libdir}/.libqmf*)$
%global proton_min_ver 0.21.0

Name:          qpid-cpp
Version:       1.38.0
Release:       2%{?dist}
Summary:       Libraries for Qpid C++ client applications
License:       ASL 2.0
URL:           http://qpid.apache.org

Source0:       http://www.apache.org/dist/qpid/cpp/%{version}/%{name}-%{version}.tar.gz
Source1:       licenses.xml

%global _pkglicensedir %{_licensedir}/%{name}-%{version}
%{!?_licensedir:%global license %doc}
%{!?_licensedir:%global _pkglicensedir %{_pkgdocdir}}

%global _rdma 0
%if (0%{?rhel} && 0%{?rhel} == 6)
%ifnarch s390 s390x 
%global _rdma 1
%endif
%else
%ifnarch %{arm}
%global _rdma 1
%endif
%endif

BuildRequires: boost-devel
BuildRequires: boost-filesystem
BuildRequires: boost-program-options
BuildRequires: cmake
BuildRequires: cyrus-sasl
BuildRequires: cyrus-sasl-devel
BuildRequires: cyrus-sasl-lib
%if (0%{?rhel} && 0%{?rhel} < 7)
BuildRequires: db4-devel
%endif
BuildRequires: doxygen
BuildRequires: gcc-c++
BuildRequires: libaio-devel
%if 0%{?fedora}
BuildRequires: libdb4-cxx-devel
%endif
%if (0%{?rhel} && 0%{?rhel} == 7)
BuildRequires: libdb-cxx-devel
%endif
%if %{_rdma}
BuildRequires: libibverbs-devel
BuildRequires: librdmacm-devel
%endif
BuildRequires: libuuid-devel
BuildRequires: make
BuildRequires: nspr-devel
BuildRequires: nss-devel
%if 0%{?fedora}
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl-generators
%endif
BuildRequires: pkgconfig
BuildRequires: %{pythonx}
BuildRequires: %{pythonx}-devel
BuildRequires: %{pythonx}-setuptools
BuildRequires: qpid-proton-c-devel >= %{proton_min_ver}
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: swig
%if 0%{?fedora} < 28 || (0%{?rhel} && 0%{?rhel} < 7)
BuildRequires: xerces-c-devel
BuildRequires: xqilla-devel
%endif

# Filter bogus libcqpid_perl.so() Provides, this is intentional rpm-build
# feature, bug #1309664
%global __provides_exclude_from %{?__provides_exclude_from:%{__provides_exclude_from}|}^%{perl_vendorarch}/auto/.*\\.so$


%description

Run-time libraries for AMQP client applications developed using Qpid
C++. Clients exchange messages with an AMQP message broker using
the AMQP protocol.


%package client
Summary:   Libraries for Qpid C++ client applications
%if 0%{?fedora}
Provides:  qpid(cpp-client)%{?_isa} = %{version}-%{release}
%endif
Obsoletes: %{name}-client-ssl

Requires:  boost-filesystem
Requires:  boost-program-options
Requires:  boost-system
Requires:  qpid-proton-c%{?_isa} >= %{proton_min_ver}

%if (0%{?rhel} && 0%{?rhel} < 7)
Requires:  initscripts
Requires(post):/sbin/chkconfig
Requires(preun):/sbin/chkconfig
Requires(preun):/sbin/service
Requires(postun):/sbin/service
%endif

%description client
Run-time libraries for AMQP client applications developed using Qpid
C++. Clients exchange messages with an AMQP message broker using
the AMQP protocol.

%files client
%license %{_pkglicensedir}/LICENSE.txt
%license %{_pkglicensedir}/licenses.xml
%doc NOTICE.txt
%doc README.md
%doc INSTALL.txt
%{_libdir}/libqpidcommon.so.*
%{_libdir}/libqpidclient.so.*
%{_libdir}/libqpidtypes.so.*
%{_libdir}/libqpidmessaging.so.*
%dir %{_libdir}/qpid
%if %{_rdma}
%dir %{_libdir}/qpid/client
%exclude %{_libdir}/qpid/client/rdmaconnector.so*
%endif
%dir %{_sysconfdir}/qpid
%config(noreplace) %{_sysconfdir}/qpid/qpidc.conf

%post client -p /sbin/ldconfig

%postun client -p /sbin/ldconfig


%package client-devel
Summary:   Header files, documentation and testing tools for developing Qpid C++ clients
%if 0%{?fedora}
Provides:  qpid(cpp-client-devel)%{?_isa} = %{version}-%{release}
Requires:  qpid(cpp-client)%{?_isa} = %{version}-%{release}
%endif
Requires:  %{name}-client = %{version}-%{release}
Requires:  boost-devel
Requires:  boost-filesystem
Requires:  boost-program-options
Requires:  libuuid-devel
Requires:  %{pythonx}

%description client-devel
Libraries and header files for developing AMQP clients in C++ using Qpid.
Qpid implements the AMQP messaging specification.

%files client-devel
%dir %{_includedir}/qpid
%{_includedir}/qpid/*.h
%{_includedir}/qpid/qpid.i
%{_includedir}/qpid/swig_perl_typemaps.i
%{_includedir}/qpid/swig_python_typemaps.i
%{_includedir}/qpid/swig_ruby_typemaps.i
%{_includedir}/qpid/client
%{_includedir}/qpid/framing
%{_includedir}/qpid/sys
%{_includedir}/qpid/messaging
%{_includedir}/qpid/types
%{_libdir}/libqpidcommon.so
%{_libdir}/libqpidclient.so
%{_libdir}/libqpidtypes.so
%{_libdir}/libqpidmessaging.so
%{_libdir}/pkgconfig/qpid.pc
%{_libdir}/cmake/Qpid/QpidConfig.cmake
%{_libdir}/cmake/Qpid/QpidConfigVersion.cmake
%{_datadir}/qpid/examples/messaging
%defattr(755,root,root,-)
%{_libexecdir}/qpid/tests/qpid-perftest
%{_libexecdir}/qpid/tests/qpid-topic-listener
%{_libexecdir}/qpid/tests/qpid-topic-publisher
%{_libexecdir}/qpid/tests/qpid-latency-test
%{_libexecdir}/qpid/tests/qpid-client-test
%{_libexecdir}/qpid/tests/qpid-txtest
%{_libexecdir}/qpid/tests/qpid-ping
%{_libexecdir}/qpid/tests/qpid-txtest2
%{_libexecdir}/qpid/tests/receiver
%{_libexecdir}/qpid/tests/sender
%{_bindir}/qpid-send
%{_bindir}/qpid-receive

%post client-devel -p /sbin/ldconfig

%postun client-devel -p /sbin/ldconfig


%package client-docs
Summary:   AMQP client development documentation
BuildArch: noarch
Obsoletes: %{name}-client-devel-docs

%description client-docs
This package includes the AMQP clients development documentation in HTML
format for easy browsing.

%files client-docs
%doc %{_pkgdocdir}
%license %{_pkglicensedir}/LICENSE.txt
%license %{_pkglicensedir}/licenses.xml


%package server
Summary:   An AMQP message broker daemon
%if 0%{?fedora}
Provides:  qpid(cpp-server)%{?_isa} = %{version}-%{release}
Requires:  qpid(cpp-client)%{?_isa} = %{version}-%{release}
%endif
Requires:  %{name}-client = %{version}-%{release}
Requires:  cyrus-sasl
Requires:  qpid-proton-c%{?_isa} >= %{proton_min_ver}
%if 0%{?fedora} || (0%{?rhel} && 0%{?rhel} >= 7)
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif
Obsoletes: %{name}-server-ssl
Obsoletes: %{name}-server-devel

%description server
A message broker daemon that receives stores and routes messages using
the open AMQP messaging protocol.

%files server
%{_libdir}/libqpidbroker.so*
%{_sbindir}/qpidd
%if 0%{?fedora} || (0%{?rhel} && 0%{?rhel} >= 7)
%{_unitdir}/qpidd.service
%else
%{_initrddir}/qpidd
%endif
%config(noreplace) %{_sysconfdir}/qpid/qpidd.conf
%config(noreplace) %{_sysconfdir}/sasl2/qpidd.conf
%dir %{_libdir}/qpid/daemon
%{_libdir}/qpid/daemon/amqp.so
%attr(755, qpidd, qpidd) %dir %{_localstatedir}/lib/qpidd
%attr(755, qpidd, qpidd) %dir %{_localstatedir}/run/qpidd
%doc %{_mandir}/man1/*

%pre server
# Only needed for Fedora & Epel builds
rm -fr /var/run/qpidd
#
getent group qpidd >/dev/null || groupadd -r qpidd
getent passwd qpidd >/dev/null || \
  useradd -r -M -g qpidd -d %{_localstatedir}/lib/qpidd -s /sbin/nologin \
    -c "Owner of Qpidd Daemons" qpidd
exit 0

%post server
%if (0%{?rhel} && 0%{?rhel} < 7)
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add qpidd
/sbin/ldconfig
%else
%systemd_post qpidd.service
%endif 

%preun server
%if (0%{?rhel} && 0%{?rhel} < 7)
# Check that this is actual deinstallation, not just removing for upgrade.
if [ $1 = 0 ]; then
  /sbin/service qpidd stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del qpidd
fi
%else
%systemd_preun qpidd.service
%endif

%postun server
%if (0%{?rhel} && 0%{?rhel} < 7)
if [ "$1" -ge "1" ]; then
  /sbin/service qpidd condrestart >/dev/null 2>&1 || :
fi
%else
%systemd_postun_with_restart qpidd.service
%endif
/sbin/ldconfig


%package server-ha
Summary: Provides extensions to the AMQP message broker to provide high availability
%if 0%{?fedora}
Provides: qpid(cpp-server-ha)%{?_isa} = %{version}-%{release}
Requires: qpid(cpp-server)%{?_isa} = %{version}-%{release}
%endif
Requires: %{name}-server = %{version}-%{release}
Requires: %{name}-client = %{version}-%{release}
Obsoletes: %{name}-server-cluster

%if 0%{?fedora} || (0%{?rhel} && 0%{?rhel} >= 7)
# for systemd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%endif

%description server-ha
%{summary}.

%files server-ha
%if 0%{?fedora} || (0%{?rhel} && 0%{?rhel} >= 7)
%{_unitdir}/qpidd-primary.service
%else
%{_initrddir}/qpidd-primary
%endif
%{_libdir}/qpid/daemon/ha.so

%post server-ha
%if 0%{?fedora} || (0%{?rhel} && 0%{?rhel} >= 7)
%systemd_post qpidd-primary.service
%else
/sbin/chkconfig --add qpidd-primary
%endif
/sbin/ldconfig

%preun server-ha
%if 0%{?fedora} || (0%{?rhel} && 0%{?rhel} >= 7)
%systemd_preun qpidd-primary.service
%else
if [ $1 = 0 ]; then
  /sbin/service qpidd-primary stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del qpidd-primary
fi
%endif

%postun server-ha
%if 0%{?fedora} || (0%{?rhel} && 0%{?rhel} >= 7)
%systemd_postun_with_restart qpidd-primary.service
%else
if [ $1 -ge 1 ]; then
  /sbin/service qpidd-primary condrestart >/dev/null 2>&1 || :
fi
%endif
/sbin/ldconfig


%if %{_rdma}
%package client-rdma
Summary:  RDMA Protocol support (including Infiniband) for Qpid clients
%if 0%{?fedora}
Provides: qpid(cpp-client-rdma)%{?_isa} = %{version}-%{release}
Requires: qpid(cpp-client)%{?_isa} = %{version}-%{release}
%endif
Requires: %{name}-client = %{version}-%{release}

%description client-rdma
A client plugin and support library to support RDMA protocols (including
Infiniband) as the transport for Qpid messaging.

%files client-rdma
%{_libdir}/librdmawrap.so*
%{_libdir}/qpid/client/rdmaconnector.so*
%config(noreplace) %{_sysconfdir}/qpid/qpidc.conf

%post client-rdma -p /sbin/ldconfig

%postun client-rdma -p /sbin/ldconfig


%package server-rdma
Summary:   RDMA Protocol support (including Infiniband) for the Qpid daemon
%if 0%{?fedora}
Provides: qpid(cpp-server-rdma)%{?_isa} = %{version}-%{release}
Requires: qpid(cpp-server)%{?_isa} = %{version}-%{release}
Requires: qpid(cpp-client-rdma)%{?_isa} = %{version}-%{release}
%endif
Requires: %{name}-server = %{version}-%{release}
Requires: %{name}-client = %{version}-%{release}
Requires: %{name}-client-rdma = %{version}-%{release}

%description server-rdma
A Qpid daemon plugin to support RDMA protocols (including Infiniband) as the
transport for AMQP messaging.

%files server-rdma
%{_libdir}/qpid/daemon/rdma.so

%post server-rdma -p /sbin/ldconfig

%postun server-rdma -p /sbin/ldconfig
%endif

%if 0%{?fedora} < 28 || (0%{?rhel} && 0%{?rhel} < 7)
%package server-xml
Summary:  XML extensions for the Qpid daemon
%if 0%{?fedora}
Provides: qpid(cpp-server-xml)%{?_isa} = %{version}-%{release}
Requires: qpid(cpp-server)%{?_isa} = %{version}-%{release}
%endif
Requires: %{name}-server = %{version}-%{release}
Requires: xqilla
Requires: xerces-c

%description server-xml
A Qpid daemon plugin to support extended XML-based routing of AMQP
messages.

%files server-xml
%{_libdir}/qpid/daemon/xml.so

%post server-xml -p /sbin/ldconfig

%postun server-xml -p /sbin/ldconfig
%endif


%package server-linearstore
Summary: Red Hat persistence extension to the Qpid messaging sytem
%if 0%{?fedora}
Provides: qpid(cpp-server-lineastore)%{?_isa} = %{version}-%{release}
Requires: qpid(cpp-server)%{?_isa} = %{version}-%{release}
%endif
Requires: %{name}-server = %{version}-%{release}
Requires: %{name}-client = %{version}-%{release}
%if 0%{?fedora}
Requires: libdb4
%endif
%if (0%{?rhel} && 0%{?rhel} == 7)
Requires: libdb
%endif
%if (0%{?rhel} && 0%{?rhel} < 7)
Requires: db4
%endif
Requires: libaio
Obsoletes: %{name}-server-store
Conflicts: %{name}-server-store

%description server-linearstore
Red Hat persistence extension to the Qpid AMQP broker: persistent message
storage using a libaio-based asynchronous journal.

%files server-linearstore
%{_libdir}/qpid/daemon/linearstore.so
%{_libdir}/liblinearstoreutils.so

%post server-linearstore -p /sbin/ldconfig
%postun server-linearstore -p /sbin/ldconfig

%if 0%{?fedora}
%package -n perl-qpid-messaging
Summary:  Perl bindings for the Qpid messaging framework

Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: qpid-cpp-client = %{version}-%{release}

%description -n perl-qpid-messaging
%{summary}.

%files -n perl-qpid-messaging
%{perl_vendorarch}/*
%doc %{_perldocdir}


%package -n %{pythonx}-qpid-messaging
Summary: Python bindings for the Qpid messaging framework
Requires: %{pythonx}
Requires: qpid(cpp-client)%{?_isa} = %{version}-%{release}
Requires: %{pythonx}-qpid

%if 0%{?fedora}
%{?python_provide:%python_provide python2-qpid-messaging}
%endif

%{?filter_setup:
  %filter_provides_in %{python2_sitearch}/.*\.so$
  %filter_setup}

%description -n %{pythonx}-qpid-messaging
%{summary}.

%files -n %{pythonx}-qpid-messaging
%{python2_sitearch}/qpid_messaging.py*
%{python2_sitearch}/_qpid_messaging.so
%{_pythondocdir}/examples

%endif


%package -n qpid-tools
Summary:  Management and diagostic tools for Apache Qpid
BuildArch: noarch

Requires:  %{pythonx}-qpid
Requires:  %{pythonx}-qpid-qmf = %{version}-%{release}

%description -n qpid-tools
Management and diagnostic tools for Apache Qpid brokers and clients.

%files -n qpid-tools
%{_bindir}/qpid-config
%{_bindir}/qpid-ha
%{_bindir}/qpid-printevents
%{_bindir}/qpid-queue-stats
%{_bindir}/qpid-route
%{_bindir}/qpid-stat
%{_bindir}/qpid-tool
%{python2_sitelib}/qpidtoollibs
%{_libexecdir}/qpid-qls-analyze
%dir %{_datadir}/qpid-tools
%dir %{_datadir}/qpid-tools/python
%{_datadir}/qpid-tools/python/qlslibs
%{python2_sitelib}/qpid_tools-*.egg-info


%package -n qpid-qmf
Summary: The QPID Management Framework

%if 0%{?fedora}
Requires:  qpid(cpp-client)%{?_isa}
%endif

Requires:  qpid-cpp-client%{?_isa} = %{version}-%{release} 

%description -n qpid-qmf
The Qpid Management Framework is a general-purpose management bus built on Qpid
messaging. It takes advantage of the scalability, security, and rich
capabilities of Qpid to provide flexible and easy-to-use manageability to a
large set of applications.

%files -n qpid-qmf
%{_libdir}/libqmf2.so.*

%post -n qpid-qmf -p /sbin/ldconfig

%postun -n qpid-qmf -p /sbin/ldconfig


%package -n qpid-qmf-devel
Summary:   Header files and tools for developing QMF extensions
Requires:  qpid-qmf%{?_isa} = %{version}-%{release}
%if 0%{?fedora}
Requires:  qpid(cpp-client-devel)%{?_isa}
%endif
Requires:  qpid-cpp-client-devel%{?_isa} = %{version}-%{release}

%description -n qpid-qmf-devel
Header files and code-generation tools needed for developers of QMF-managed
components.

%files -n qpid-qmf-devel
%{_includedir}/qmf
%{_libdir}/libqmf2.so
%{_bindir}/qmf-gen
%{python2_sitelib}/qmfgen
%{_libdir}/pkgconfig/qmf2.pc

%post -n qpid-qmf-devel -p /sbin/ldconfig

%postun -n qpid-qmf-devel -p /sbin/ldconfig


%package -n %{pythonx}-qpid-qmf
Summary:   The QPID Management Framework bindings for python

Requires:  qpid-qmf%{?_isa} = %{version}-%{release}
Requires:  %{name}-client%{?_isa} = %{version}-%{release}

%if 0%{?fedora}
%{?python_provide:%python_provide python2-qpid-qmf}
%endif

%description -n %{pythonx}-qpid-qmf

An extensible management framework layered on QPID messaging, bindings
for python.

%files -n %{pythonx}-qpid-qmf
%{python2_sitelib}/qmf

%post -n %{pythonx}-qpid-qmf -p /sbin/ldconfig

%postun -n %{pythonx}-qpid-qmf -p /sbin/ldconfig


%prep
%setup -q -n qpid-cpp-%{version}

%build

CXX11FLAG="-std=c++11"
%if (0%{?rhel} && 0%{?rhel} <= 6)
CXX11FLAG="-w -std=c++0x"
%endif

%if 0%{?fedora}
export ADDFLAGS="-Wno-error=maybe-uninitialized -Wno-error=catch-value= -Wno-error=cast-function-type -Wno-error=ignored-qualifiers -Wno-error=class-memaccess"
%cmake -DDOC_INSTALL_DIR:PATH=%{_pkgdocdir} \
       -DBUILD_LEGACYSTORE=false \
       -DBUILD_LINEARSTORE=true \
       -DPERL_PFX_ARCHLIB=%{perl_vendorarch} \
       -DBUILD_BINDING_RUBY=true \
       "-DCMAKE_CXX_FLAGS=$CXXFLAGS $CXX11FLAG $ADDFLAGS" \
       .
%endif
%if 0%{?rhel}
%cmake  -DDOC_INSTALL_DIR:PATH=%{_pkgdocdir} \
        -DBUILD_LEGACYSTORE=false \
        -DBUILD_LINEARSTORE=true \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DCMAKE_EXE_LINKER_FLAGS="-Wl,-z,relro,-z,now" \
        -DCMAKE_SHARED_LINKER_FLAGS="-Wl,-z,relro" \
        -DCMAKE_MODULE_LINKER_FLAGS="-Wl,-z,relro" \
       "-DCMAKE_CXX_FLAGS=$CXXFLAGS $CXX11FLAG" \
        .
%endif

make %{?_smp_mflags}
make docs-user-api

%install
rm -rf %{buildroot}

pushd management/python

%{__python2} setup.py install \
    --install-purelib %{python2_sitelib} \
    --root %{buildroot}

popd

chmod +x %{buildroot}/%{python2_sitelib}/qpidtoollibs/disp.py

mkdir -p -m0755 %{buildroot}/%{_bindir}
mkdir -p -m0755 %{buildroot}/%{_unitdir}

%if 0%{?fedora}
# install examples
mkdir -p -m0755 %{buildroot}%{_perldocdir}/examples
mkdir -p -m0755 %{buildroot}%{_pythondocdir}/examples

pushd bindings/qpid/examples/python
install -pm 644 * %{buildroot}%{_perldocdir}/examples
install -pm 644 * %{buildroot}%{_pythondocdir}/examples
popd
%endif

%make_install

# enable auth by default
echo "auth=yes" >> %{buildroot}/etc/qpid/qpidd.conf

%if 0%{?fedora} || (0%{?rhel} && 0%{?rhel} >= 7)
# install systemd files
mkdir -p %{buildroot}/%{_unitdir}
install -pm 644 %{_builddir}/qpid-cpp-%{version}/etc/fedora/qpidd.service \
    %{buildroot}/%{_unitdir}
install -pm 644 %{_builddir}/qpid-cpp-%{version}/etc/fedora/qpidd-primary.service \
    %{buildroot}/%{_unitdir}
%endif

install -d -m0755 %{buildroot}%{_localstatedir}/lib/qpidd
install -d -m0755 %{buildroot}%_libdir/qpid
install -d -m0755 %{buildroot}/var/run/qpidd

# Set executable bit on shared libraries to ensure the binaries are stripped
chmod +x %{buildroot}/%{python2_sitearch}/*so

# QMF Python management
install -d %{_builddir}/qpid-cpp-%{version}/managementgen/qmfgen \
           %{buildroot}/%{python2_sitelib}

%if 0%{?fedora} || (0%{?rhel} && 0%{?rhel} >= 7)
rm -f %{buildroot}/%{_initrddir}/qpidd*
%endif
rm -f %{buildroot}/%{_libdir}/qpid/daemon/store.so*

%if 0%{?rhel} && 0%{?rhel} <= 6
install -pm 644 %{SOURCE1} %{buildroot}%{_pkgdocdir}
%else
install -dm 755 %{buildroot}%{_pkglicensedir}
install -pm 644 %{SOURCE1} %{buildroot}%{_pkglicensedir}
install -pm 644 %{buildroot}%{_pkgdocdir}/LICENSE.txt %{buildroot}%{_pkglicensedir}
rm -f %{buildroot}%{_pkgdocdir}/LICENSE.txt
%endif

# clean up leftover examples files:
rm -f %{buildroot}/%{_datadir}/qpid/examples/README.txt
rm -f %{buildroot}/%{_datadir}/qpid/examples/qmf2/agent.cpp
rm -f %{buildroot}/%{_datadir}/qpid/examples/qmf2/event_driven_list_agents.cpp
rm -f %{buildroot}/%{_datadir}/qpid/examples/qmf2/list_agents.cpp
rm -f %{buildroot}/%{_datadir}/qpid/examples/qmf2/print_events.cpp

# clean up leftover ruby files
%if (0%{?rhel} && 0%{?rhel} <= 6)
rm -fr %{buildroot}/usr/%{_lib}/ruby/site_ruby
%else
rm -rf %{buildroot}/usr/local/%{_lib}/ruby/site_ruby
%endif

# clean up rhel build
%if 0%{?rhel}
rm -f  %{buildroot}/%{python2_sitearch}/_qpid_messaging.so
rm -f  %{buildroot}/%{python2_sitearch}/qpid_messaging.py*
# These bits will be build if perl-devel package is installed
rm -fr %{buildroot}%_libdir/perl5
%endif

rm %{buildroot}/%{_bindir}/*.bat

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%changelog
* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.38.0-2
- Perl 5.28 rebuild

* Fri May 11 2018 Irina Boverman <iboverma@redhat.com> - 1.38.0-1
- Removed ruby-qpid-qmf subpackage (per upstream changes)
- Rebased to 1.38.0

* Tue Mar 13 2018 Irina Boverman <iboverma@redhat.com> - 1.37.0-6
- Updated compiler flags
- Renuilt against qpid-proton 0.21.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.37.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Jonathan Wakely <jwakely@redhat.com> - 1.37.0-5
- Rebuilt for Boost 1.66

* Fri Jan 05 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.37.0-4
- F-28: rebuild for ruby25

* Fri Dec 1 2017 Irina Boverman <iboverma@redhat.com> - 1.37.0-3
- Updated python requirements
- Updated licensing

* Thu Nov 30 2017 Irina Boverman <iboverma@redhat.com> - 1.37.0-2
- Updated dependencies
- Changed package names from python-* to python2-*

* Wed Nov 29 2017 Irina Boverman <iboverma@redhat.com> - 1.37.0-1
- Rebased to 1.37.0

* Thu Nov 16 2017 Irina Boverman <iboverma@redhat.com> - 1.36.0-8
- Rebuilt against qpid-proton 0.18.1

* Fri Aug 25 2017 Adam Williamson <awilliam@redhat.com> - 1.36.0-7
- Disable RDMA on 32-bit ARM (#1484155)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.36.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.36.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Kalev Lember <klember@redhat.com> - 1.36.0-4
- Rebuilt for Boost 1.64

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.36.0-3
- Rebuild due to bug in RPM (RHBZ #1468476)

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.36.0-2
- Perl 5.26 rebuild

* Mon May  1 2017 Irina Boverman <iboverma@redhat.com> - 1.36.0-1
- Rebased to 1.36.0

* Mon Feb 20 2017 Irina Boverman <iboverma@redhat.com> - 1.35.0-4
- Added qpid-tools and python-qpid-qmf sub-packages previously built
  as separate packages
- Moved qmf from python_sitearch to python_sitelib
- Removed qpid-cpp-server-devel
- Renamed qpid-cpp-client-devel-docs to qpid-cpp-client-docs
- Added GCC7 flag -Wno-implicit-fallthrough

* Thu Sep  8 2016 Irina Boverman <iboverma@redhat.com> - 1.35.0-1
- Rebased to 1.35.0

* Mon Aug  8 2016 Irina Boverman <iboverma@redhat.com> - 0.34-12
- Added "-std=c++11" flag

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-11
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jun 24 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-10
- Rebuilt against qpid-proton 0.13.0-1

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-9
- Perl 5.24 rebuild

* Wed Mar 23 2016 Petr Pisar <ppisar@redhat.com> - 0.34-8
- Do not provide private libraries (bug #1309664)
- Rebuilt against qpid-proton 0.12.1-1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 0.34-6
- Rebuilt for Boost 1.60

* Tue Dec  1 2015 Irina Boverman <iboverma@redhat.com> - 0.34-5
- Resolves: BZ#1286881

* Thu Sep 03 2015 Jonathan Wakely <jwakely@redhat.com> - 0.34-4
- Rebuilt for Boost 1.59

* Wed Sep  2 2015 Irina Boverman <iboverma@redhat.com> - 0.34-3
- Rebuilt against qpid-proton-0.10-1

* Sun Aug 30 2015 Jonathan Wakely <jwakely@redhat.com> 0.34-2
- Patched and rebuilt for Boost 1.59
- Rebased to 0.34
- Rebuilt against qpid-proton-0.10-1
- Added qpid-cpp-server-devel
- Added qpid-send and qpid-qpid-receive to qpid-client-devel sub-package
- Removed python-qpid-common, python-qpid, qpid-tools and qpid-server-store sub-packages
  Note: python-qpid-common and python-qpid will be 
        added to python-qpid package
        qpid-tools will be added to qpid-tools package

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.32-7
- rebuild for Boost 1.58

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-5
- Perl 5.22 rebuild

* Wed May 27 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.32-4
- Removed qpid-send and qpid-receive from qpid-cpp-client-devel.
* Fri May 22 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.32-3
- Include the qpid.tests module in python-qpid
- Resolves: BZ#1224260

* Mon Apr 13 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.32-2
- Re-add patch that fixes builds on aarch64/ppc64le

* Tue Apr  7 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.32-1.1
- Bumped the release to force a build against Proton 0.9 in F22.

* Mon Apr  6 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.32-1
- Rebased on Qpid 0.32.
- Added build flag to enable building the legacy store.
- Added the perl-qpid-messaging subpackage.
- Added the python-qpid-messaging subpackage.
- Added the python-qpid subpackage.

* Wed Feb 25 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.30-12
- Added qpidtoollibs to the qpid-tools package.

* Fri Feb 20 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.30-11
- Fixed path to qpid-ha in the systemd service descriptor.

* Wed Feb 04 2015 Petr Machata <pmachata@redhat.com> - 0.30-10
- Bump for rebuild.

* Mon Feb  2 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.30-9
- Resolves: BZ#1186308

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 0.30-8
- Rebuild for boost 1.57.0

* Thu Jan 22 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.30-7
- Apply patch 10.

* Wed Jan 21 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.30-6
- Resolves: BZ#1184488

* Fri Jan 16 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.30-5
- Resolves: BZ#1181721

* Wed Oct 29 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.30-4
- QPID-6170: Fixes builds on aarch64 and ppc64le architectures.

* Thu Oct  2 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.30-1
- Rebased on Qpid 0.30.
- Upstream tarball filename changed from qpid-##.#.tar.gz to qpid-cpp-##.#.tar.gz.
- qpid-tools moved out to a separate package.
- Moved qpid-send and qpid-receive to the qpid-cpp-client-devel package.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.28-7
- Removed ssl package references.

* Thu Aug 14 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.28-6
- Renamed the virtual provides to conform with project needs.

* Thu Jul 10 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.28-5
- Removed parameterized ldconfig.
- Removed comments between subpackages.
- * This is what appears to have caused the (post)install error messages.

* Thu Jul  3 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.28-4
- Parameterized ldconfig location based on RHEL/Fedora release.

* Tue Jun 10 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.28-3
- Fixes alignment issues on ARM platforms.
- Resolves: BZ#1106272

* Sat Jun  7 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.28-2
- Remove arm conditionals as we now have the dependencies
- Fix aarch64 defines (it's not arm64)

* Wed Jun  4 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.28-1
- Rebased on Qpid 0.28.

* Tue Jun  3 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26-9
- Fixed dependency of server-ha on qpid(server).

* Wed May 28 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26-8
- Fixed a few typos that slipped into the specfile for virtual packages.

* Tue May 27 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26-7
- Added virtual packages for all binary subpackages.
- Updated requires to be for virtual packages.

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.26-6
- Rebuild for boost 1.55.0

* Thu May 22 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26-5
- Removed the architecture macro from the virtual provides.

* Wed May 21 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26-4
- Added virtual packages for qpid-cpp-client and -client-devel.y

* Wed May  7 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26-3
- Changed qpid-cpp-server-ha to use systemd macros for pre/post/postun
- Resoves: BZ#1094928

* Fri Feb 21 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26-2
- QPID-5499: Fix for building with -Werror=format-security enabled.
- * This was previously for files include in qpid-cpp-client-devel.

* Thu Feb 20 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26-1
- Rebased on Qpid 0.26.
- Updated qpid-cpp-server-ha to be a systemd service.
- Removed qpid-cpp-server dependency on qpid-cpp-server-store.
- * The package was mistakenly including store libraries.
- Added BR for gcc-c++.
- Removed -n option from all subpackages.
- Removed clean and check sections.
- Updated package to use systemd macros correctly.
- Removed unnecessary BRs.
- Cleaned up the deletes after the build finishes.

* Wed Jan 22 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.24-9
- Set qpidd service to start after the network service.
- QPID-5499: Updated the Swig descriptors.
- Resolves: BZ#1055660
- Resolves: BZ#1037295

* Wed Nov 27 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-8
- Removed rdma.so from the -server subpackage.
- Resolves: BZ#1035323

* Wed Nov 27 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-7
- Removed rdmaconnector.so from the -client subpackage.
- Resolves: BZ#1035323

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
