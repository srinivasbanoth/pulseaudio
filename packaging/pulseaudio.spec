%bcond_with tizen_mobile

Name:             pulseaudio
Summary:          Improved Linux sound server
Version:          4.0
Release:          0
Group:            Multimedia/Audio
License:          GPL-2.0+ ; LGPL-2.1+
URL:              http://pulseaudio.org
Source0:          http://127.0.0.1/pulseaudio-4.0.tar.gz
%if %{with tizen_mobile}
Source1:          default.pa-for-gdm
Source2:          setup-pulseaudio
Source3:          sysconfig.sound-pulseaudio
Source99:         baselibs.conf
%endif
BuildRequires:    m4
BuildRequires:    libtool-ltdl-devel
BuildRequires:    libtool
BuildRequires:    intltool
BuildRequires:    fdupes
BuildRequires:    pkgconfig(speexdsp)
BuildRequires:    pkgconfig(sndfile)
BuildRequires:    pkgconfig(alsa)
BuildRequires:    pkgconfig(glib-2.0)
BuildRequires:    pkgconfig(gconf-2.0)
BuildRequires:    pkgconfig(bluez)
BuildRequires:    pkgconfig(sbc)
BuildRequires:    pkgconfig(dbus-1)
BuildRequires:    pkgconfig(xi)
BuildRequires:    pkgconfig(libudev)
BuildRequires:    pkgconfig(openssl)
BuildRequires:    pkgconfig(json)
%if %{with tizen_mobile}
BuildRequires:    pkgconfig(capi-system-power)
BuildRequires:    pkgconfig(dlog)
BuildRequires:    pkgconfig(vconf)
%endif
Requires:         udev
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires:         pulseaudio-config

%description
PulseAudio is a sound server for Linux and other Unix like operating
systems. It is intended to be an improved drop-in replacement for the
Enlightened Sound Daemon (ESOUND).

%package libs
Summary:    PulseAudio client libraries
Group:      Multimedia/Audio
Requires:   %{name} = %{version}-%{release}

%description libs
Client libraries used by applications that access a PulseAudio sound server
via PulseAudio's native interface.

%package libs-devel
Summary:    PulseAudio client development headers and libraries
Group:      Multimedia/Development
Requires:   %{name} = %{version}-%{release}

%description libs-devel
Headers and libraries for developing applications that access a PulseAudio
sound server via PulseAudio's native interface

%package utils
Summary:    Command line tools for the PulseAudio sound server
Group:      Multimedia/Audio
Requires:   %{name} = %{version}-%{release}

%description utils
These tools provide command line access to various features of the
PulseAudio sound server. Included tools are:
pabrowse - Browse available PulseAudio servers on the local network.
paplay - Playback a WAV file via a PulseAudio sink.
pacat - Cat raw audio data to a PulseAudio sink.
parec - Cat raw audio data from a PulseAudio source.
pacmd - Connect to PulseAudio's built-in command line control interface.
pactl - Send a control command to a PulseAudio server.
padsp - /dev/dsp wrapper to transparently support OSS applications.
pax11publish - Store/retrieve PulseAudio default server/sink/source
settings in the X11 root window.

%package module-bluetooth
Summary:    Bluetooth module for PulseAudio sound server
Group:      Multimedia/Audio
Requires:   %{name} = %{version}-%{release}

%description module-bluetooth
This module enables PulseAudio to work with bluetooth devices, like headset
or audio gateway

%package module-devel
Summary:    Headers and libraries for PulseAudio module development
License:    LGPL-2.0+
Group:      Multimedia/Development
Requires:   %{name}-libs-devel = %{version}-%{release}

%description module-devel
Headers and libraries for developing pulseaudio modules outside
the source tree.

%if %{with tizen_mobile}

%package config-mobile
Summary:    Configuration for PulseAudio in tizen mobile
Group:      Multimedia/Audio

%description config-mobile
Default configuration for PulseAudio in tizen mobile.

%else

%package config-ivi
Summary:    Configuration for PulseAudio in tizen ivi
Group:      Multimedia/Audio

%description config-ivi
Default configuration for PulseAudio in tizen ivi.

%endif

%package module-raop
Summary: PA module-raop
Group:   Multimedia/Audio

%description module-raop
PA module-raop.

%package module-filter
Summary: PA module-filter
Group:   Multimedia/Audio

%description module-filter
PA module-filter.

%package module-combine-sink
Summary: PA module-combine-sink
Group:   Multimedia/Audio

%description module-combine-sink
PA module-combine-sink.

%package module-augment-properties
Summary: PA module-augment-properties
Group:   Multimedia/Audio

%description module-augment-properties
PA module-augment-properties.

%package module-dbus-protocol
Summary: PA module-dbus-protocol
Group:   Multimedia/Audio

%description module-dbus-protocol
PA module-dbus-protocol.

%package module-null-source
Summary: PA module-null-source
Group:   Multimedia/Audio

%description module-null-source
PA module-null-source.

%package module-switch-on-connect
Summary: PA module-swich-on-connect
Group:   Multimedia/Audio

%description module-switch-on-connect
PA module-swich-on-connect.

%package localization
Summary:    PA localization files
Group:      Multimedia/Audio
Requires:   %{name} = %{version}-%{release}

%description localization
PA localization files.

%package vala-bindings
Summary:    PA Vala bindings
Group:      Multimedia/Audio
Requires:   %{name} = %{version}-%{release}

%description vala-bindings
PA Vala bindings.

%prep
%setup -q -T -b0
echo "%{version}" > .tarball-version

%if %{with tizen_mobile}
%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
export LD_AS_NEEDED=0
cp src/daemon/default.pa.in.mobile src/daemon/default.pa.in
cp src/daemon/system.pa.in.mobile src/daemon/system.pa.in
cp src/daemon/daemon.conf.in.mobile src/daemon/daemon.conf.in
cp src/pulse/client.conf.in.mobile src/pulse/client.conf.in
./bootstrap.sh
%configure \
--disable-static \
--disable-rpath \
--enable-dlog \
--enable-pmapi \
--enable-spolicy \
--enable-systemd \
--with-system-user=pulse \
--with-system-group=pulse \
--with-access-group=pulse-access \
--with-udev-rules-dir=/usr/lib/udev/rules.d \
--disable-hal
make %{?_smp_mflags} V=1

%else
%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
export LD_AS_NEEDED=0
cp src/daemon/default.pa.in.ivi src/daemon/default.pa.in
cp src/daemon/system.pa.in.ivi src/daemon/system.pa.in
cp src/daemon/daemon.conf.in.ivi src/daemon/daemon.conf.in
cp src/pulse/client.conf.in.ivi src/pulse/client.conf.in
CPUS="`cat /proc/cpuinfo  | grep ^processor | wc -l`"
JOBS="-j$(($CPUS + 1))"
./bootstrap.sh
%configure --disable-static \
--enable-alsa \
--disable-ipv6 \
--disable-oss-output \
--disable-oss-wrapper \
--disable-x11 \
--disable-hal \
--disable-hal-compat \
--disable-lirc \
--disable-avahi \
--disable-jack \
--disable-xen \
--without-fftw \
--enable-bluez \
--enable-systemd \
--with-system-user=pulse \
--with-system-group=pulse \
--with-access-group=pulse-access

make $JOBS
%endif

%if %{with tizen_mobile}
%install
%make_install
%find_lang %{name}
install %{SOURCE2} %{buildroot}%{_bindir}
chmod 755 %{buildroot}%{_bindir}/setup-pulseaudio
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
touch %{buildroot}%{_sysconfdir}/profile.d/pulseaudio.sh
touch %{buildroot}%{_sysconfdir}/profile.d/pulseaudio.csh
mkdir -p %{buildroot}%{_localstatedir}/lib/gdm/.pulse
cp $RPM_SOURCE_DIR/default.pa-for-gdm %{buildroot}%{_localstatedir}/lib/gdm/.pulse/default.pa
ln -s esdcompat %{buildroot}%{_bindir}/esd
rm -rf %{buildroot}%{_sysconfdir}/xdg/autostart/pulseaudio-kde.desktop

install -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/sound
%pre
groupadd -r pulse &>/dev/null || :
useradd -r -c 'PulseAudio daemon' \
-s /sbin/nologin -d /var/lib/pulseaudio -g pulse -G audio pulse &>/dev/null || :
groupadd -r pulse-access &>/dev/null || :

%post   -n libpulse -p /sbin/ldconfig

%postun -n libpulse -p /sbin/ldconfig

%post   -n libpulse-mainloop-glib -p /sbin/ldconfig

%postun -n libpulse-mainloop-glib -p /sbin/ldconfig

%post
/sbin/ldconfig
# Update the /etc/profile.d/pulseaudio.* files
setup-pulseaudio --auto > /dev/null

%postun -p /sbin/ldconfig

%lang_package

%else
%install
rm -rf %{buildroot}
%make_install
%find_lang %{name}

install -D -m0755 pulseaudio.sh.in.ivi %{buildroot}%{_sysconfdir}/rc.d/init.d/pulseaudio.sh

install -d  %{buildroot}/%{_libdir}/systemd/system
install -m 644 pulseaudio.service %{buildroot}/%{_libdir}/systemd/system/pulseaudio.service
mkdir -p  %{buildroot}/%{_libdir}/systemd/system/multi-user.target.wants
ln -s  ../pulseaudio.service  %{buildroot}/%{_libdir}/systemd/system/multi-user.target.wants/pulseaudio.service

rm -rf  %{buildroot}/etc/xdg/autostart/pulseaudio-kde.desktop
rm -rf  %{buildroot}/usr/bin/start-pulseaudio-kde
rm -rf %{buildroot}/%{_libdir}/pulse-%{version}/modules/module-device-manager.so

mkdir -p %{buildroot}/%{_includedir}/pulsemodule/pulse
mkdir -p %{buildroot}/%{_includedir}/pulsemodule/pulsecore

cp %{buildroot}/%{_includedir}/pulse/*.h %{buildroot}/%{_includedir}/pulsemodule/pulse

fdupes  %{buildroot}/%{_datadir}
fdupes  %{buildroot}/%{_includedir}

# get rid of *.la files
rm -f %{buildroot}/%{_libdir}/*.la
rm -f %{buildroot}/%{_libdir}/pulseaudio/*.la

# put the default configuration file in place
install -m 644 src/default.pa %{buildroot}/%{_sysconfdir}/pulse

%post
/sbin/ldconfig
ln -s  /etc/rc.d/init.d/pulseaudio.sh /etc/rc.d/rc3.d/S20pulseaudio
ln -s  /etc/rc.d/init.d/pulseaudio.sh /etc/rc.d/rc4.d/S20pulseaudio

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
rm -f %{_sysconfdir}/rc.d/rc3.d/S20pulseaudio
rm -f %{_sysconfdir}/rc.d/rc4.d/S20pulseaudio
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%post module-bluetooth -p /sbin/ldconfig
%postun module-bluetooth -p /sbin/ldconfig

%lang_package

%endif

%files
%defattr(-,root,root,-)
%license LICENSE GPL LGPL
%dir %{_sysconfdir}/pulse/
%{_bindir}/esdcompat
%{_bindir}/pulseaudio
%dir %{_libexecdir}/pulse
%{_libexecdir}/pulse/*
%{_libdir}/libpulsecore-%{version}.so
%{_libdir}/libpulse-mainloop-glib.so.*
/lib/udev/rules.d/90-pulseaudio.rules
%{_bindir}/pamon
%config(noreplace) /etc/dbus-1/system.d/pulseaudio-system.conf
# cmake stuff
%{_libdir}/cmake/PulseAudio/PulseAudioConfig.cmake
%{_libdir}/cmake/PulseAudio/PulseAudioConfigVersion.cmake
# list all modules
%{_libdir}/pulse-%{version}/modules/libalsa-util.so
%{_libdir}/pulse-%{version}/modules/libcli.so
%{_libdir}/pulse-%{version}/modules/libprotocol-cli.so
%{_libdir}/pulse-%{version}/modules/libprotocol-http.so
%{_libdir}/pulse-%{version}/modules/libprotocol-native.so
%{_libdir}/pulse-%{version}/modules/libprotocol-simple.so
%{_libdir}/pulse-%{version}/modules/librtp.so
%{_libdir}/pulse-%{version}/modules/module-alsa-sink.so
%{_libdir}/pulse-%{version}/modules/module-alsa-source.so
%{_libdir}/pulse-%{version}/modules/module-always-sink.so
%{_libdir}/pulse-%{version}/modules/module-console-kit.so
%{_libdir}/pulse-%{version}/modules/module-device-restore.so
%{_libdir}/pulse-%{version}/modules/module-stream-restore.so
%{_libdir}/pulse-%{version}/modules/module-cli-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-cli-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-cli.so
%{_libdir}/pulse-%{version}/modules/module-combine.so
%{_libdir}/pulse-%{version}/modules/module-default-device-restore.so
%{_libdir}/pulse-%{version}/modules/module-detect.so
%{_libdir}/pulse-%{version}/modules/module-esound-sink.so
%{_libdir}/pulse-%{version}/modules/module-http-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-http-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-intended-roles.so
%{_libdir}/pulse-%{version}/modules/module-ladspa-sink.so
%{_libdir}/pulse-%{version}/modules/module-match.so
%{_libdir}/pulse-%{version}/modules/module-mmkbd-evdev.so
%{_libdir}/pulse-%{version}/modules/module-native-protocol-fd.so
%{_libdir}/pulse-%{version}/modules/module-native-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-native-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-null-sink.so
%{_libdir}/pulse-%{version}/modules/module-pipe-sink.so
%{_libdir}/pulse-%{version}/modules/module-pipe-source.so
%{_libdir}/pulse-%{version}/modules/module-position-event-sounds.so
%{_libdir}/pulse-%{version}/modules/module-remap-sink.so
%{_libdir}/pulse-%{version}/modules/module-remap-source.so
%{_libdir}/pulse-%{version}/modules/module-rescue-streams.so
%{_libdir}/pulse-%{version}/modules/module-rtp-recv.so
%{_libdir}/pulse-%{version}/modules/module-rtp-send.so
%{_libdir}/pulse-%{version}/modules/module-simple-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-simple-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-sine.so
%{_libdir}/pulse-%{version}/modules/module-tunnel-sink.so
%{_libdir}/pulse-%{version}/modules/module-tunnel-source.so
%{_libdir}/pulse-%{version}/modules/module-suspend-on-idle.so
%{_libdir}/pulse-%{version}/modules/module-volume-restore.so
%{_libdir}/pulse-%{version}/modules/module-alsa-card.so
%{_libdir}/pulse-%{version}/modules/module-card-restore.so
%{_libdir}/pulse-%{version}/modules/module-sine-source.so
%{_libdir}/pulse-%{version}/modules/module-loopback.so
%{_libdir}/pulse-%{version}/modules/module-rygel-media-server.so
%{_libdir}/pulse-%{version}/modules/module-echo-cancel.so
%{_libdir}/pulse-%{version}/modules/module-virtual-sink.so
%{_libdir}/pulse-%{version}/modules/module-virtual-source.so
%{_libdir}/pulse-%{version}/modules/libprotocol-esound.so
%{_libdir}/pulse-%{version}/modules/module-esound-compat-spawnfd.so
%{_libdir}/pulse-%{version}/modules/module-esound-compat-spawnpid.so
%{_libdir}/pulse-%{version}/modules/module-esound-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-esound-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-gconf.so
%{_libdir}/pulse-%{version}/modules/module-udev-detect.so
%{_libdir}/pulse-%{version}/modules/module-role-cork.so
%{_libdir}/pulse-%{version}/modules/module-switch-on-port-available.so
%{_libdir}/pulse-%{version}/modules/module-virtual-surround-sink.so
%if %{with tizen_mobile}
%{_libdir}/pulse-%{version}/modules/module-policy.so
%endif
%{_libdir}/pulse-%{version}/modules/module-role-ducking.so
%{_libdir}/pulse-%{version}/modules/module-systemd-login.so
%{_libdir}/systemd/system/pulseaudio.service
%{_libdir}/systemd/system/multi-user.target.wants/pulseaudio.service
%config(noreplace) /etc/bash_completion.d/pulseaudio-bash-completion.sh

%files libs
%defattr(-,root,root,-)
%{_libdir}/libpulse.so.*
%{_libdir}/libpulse-simple.so.*
%{_libdir}/pulseaudio/libpulsecommon-*.so

%files libs-devel
%defattr(-,root,root,-)
%{_includedir}/pulse/*
%{_libdir}/libpulse.so
%{_libdir}/libpulse-simple.so
%{_libdir}/pkgconfig/libpulse-simple.pc
%{_libdir}/pkgconfig/libpulse.pc
%{_datadir}/vala/vapi/libpulse.vapi
%{_libdir}/pkgconfig/libpulse-mainloop-glib.pc
%{_libdir}/libpulse-mainloop-glib.so

%files utils
%defattr(-,root,root,-)
%doc %{_mandir}/man1/*
%doc %{_mandir}/man5/*
%{_bindir}/pacat
%{_bindir}/pacmd
%{_bindir}/pactl
%{_bindir}/paplay
%{_bindir}/parec
%{_bindir}/pamon
%{_bindir}/parecord
%{_bindir}/pasuspender

%files module-bluetooth
%defattr(-,root,root,-)
%{_libdir}/pulse-%{version}/modules/module-bluetooth-proximity.so
%{_libdir}/pulse-%{version}/modules/module-bluetooth-device.so
%{_libdir}/pulse-%{version}/modules/module-bluetooth-discover.so
%{_libdir}/pulse-%{version}/modules/module-bluetooth-policy.so
%{_libdir}/pulse-%{version}/modules/libbluetooth-util.so

%files module-raop
%defattr(-,root,root,-)
%{_libdir}/pulse-%{version}/modules/libraop.so
%{_libdir}/pulse-%{version}/modules/module-raop*.so

%files module-filter
%defattr(-,root,root,-)
%{_libdir}/pulse-%{version}/modules/module-filter-*.so

%files module-combine-sink
%defattr(-,root,root,-)
%{_libdir}/pulse-%{version}/modules/module-combine-sink.so

%files module-augment-properties
%defattr(-,root,root,-)
%{_libdir}/pulse-%{version}/modules/module-augment-properties.so

%files module-dbus-protocol
%defattr(-,root,root,-)
%{_libdir}/pulse-%{version}/modules/module-dbus-protocol.so

%files module-null-source
%defattr(-,root,root,-)
%{_libdir}/pulse-%{version}/modules/module-null-source.so

%files module-switch-on-connect
%defattr(-,root,root,-)
%{_libdir}/pulse-%{version}/modules/module-switch-on-connect.so

%if %{with tizen_mobile}

%files config-mobile
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/pulse/daemon.conf
%config(noreplace) %{_sysconfdir}/pulse/default.pa
%config(noreplace) %{_sysconfdir}/pulse/client.conf
%config(noreplace) %{_sysconfdir}/pulse/system.pa
%{_datadir}/pulseaudio/alsa-mixer/paths/*
%{_datadir}/pulseaudio/alsa-mixer/profile-sets/*
%config(noreplace) %{_sysconfdir}/rc.d/init.d/pulseaudio.sh

%else

%files config-ivi
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/pulse/daemon.conf
%config(noreplace) %{_sysconfdir}/pulse/default.pa
%config(noreplace) %{_sysconfdir}/pulse/client.conf
%config(noreplace) %{_sysconfdir}/pulse/system.pa
%{_datadir}/pulseaudio/alsa-mixer/paths/*
%{_datadir}/pulseaudio/alsa-mixer/profile-sets/*
%config(noreplace) %{_sysconfdir}/rc.d/init.d/pulseaudio.sh

%endif

%files module-devel
%defattr(-,root,root)
%{_includedir}/pulsemodule/pulsecore/*.h
%{_includedir}/pulsemodule/pulse/*.h
%{_libdir}/pkgconfig/pulseaudio-module-devel.pc

%files localization
%defattr(-,root,root,-)
%{_datadir}/locale/*/LC_MESSAGES/pulseaudio.mo

%files vala-bindings
%defattr(-,root,root,-)
%{_datadir}/vala/vapi/*

%docs_package
