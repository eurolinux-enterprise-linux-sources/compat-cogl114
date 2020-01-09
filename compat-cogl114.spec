Name:          compat-cogl114
Version:       1.14.0
Release:       3%{?dist}
Summary:       Compat package with cogl 1.14 libraries

Group:         Development/Libraries
License:       LGPLv2+
URL:           http://www.clutter-project.org/
Source0:       http://download.gnome.org/sources/cogl/1.14/cogl-%{version}.tar.xz
# Updates to a git snapshot of the 1.4 branch of Cogl as of 2013-05-01,
# since there is no 1.4.1 yet. Fixes, among other things
# https://bugzilla.gnome.org/show_bug.cgi?id=699431
# extra BRs just because we're touching Makefile.am in this patch
Patch0: cogl-1.14.0-21-ge26464f.patch
# Don't disable copy_sub_buffer on llvmpipe
Patch1: cogl-1.14.0-swrast-copy-sub-buffer.patch

# Support for quadbuffer stereo (patches upstream as of the Cogl 1.20
# development branch)
Patch10: Add-support-for-setting-up-stereo-CoglOnscreens.patch
Patch11: CoglTexturePixmapX11-add-support-for-stereo-content.patch

BuildRequires: autoconf automake libtool gettext-devel

BuildRequires: cairo-devel
BuildRequires: gdk-pixbuf2-devel
BuildRequires: glib2-devel
BuildRequires: gobject-introspection-devel
BuildRequires: gtk-doc
BuildRequires: libXrandr-devel
BuildRequires: libXcomposite-devel
BuildRequires: libXdamage-devel
BuildRequires: libXext-devel
BuildRequires: libXfixes-devel
BuildRequires: mesa-libGL-devel
BuildRequires: pango-devel
BuildRequires: pkgconfig

%description
Compatibility package with cogl 1.14 librarires.

%package -n compat-libcogl12
Summary: Compat package with cogl 1.14 libraries
Conflicts: cogl < 1.15

%description -n compat-libcogl12
Compatibility package with cogl 1.14 librarires.

%package -n compat-libcogl-pango12
Summary: Compat package with cogl 1.14 libraries
Conflicts: cogl < 1.15
Requires: compat-libcogl12 = %{version}-%{release}

%description -n compat-libcogl-pango12
Compatibility package with cogl 1.14 librarires.

%prep
%setup -q -n cogl-%{version}
%patch0 -p1
%patch1 -p1

%patch10 -p1
%patch11 -p1

%build
CFLAGS="$RPM_OPT_FLAGS -fPIC"
autoreconf -vif
%configure --enable-cairo=yes --enable-gdk-pixbuf=yes --enable-cogl-pango=yes --enable-glx=yes --enable-gtk-doc --enable-introspection=yes

make V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_libdir}/girepository-1.0/
rm -rf %{buildroot}%{_libdir}/*.so
rm -rf %{buildroot}%{_libdir}/pkgconfig/
rm -rf %{buildroot}%{_datadir}

%post -n compat-libcogl12 -p /sbin/ldconfig
%postun -n compat-libcogl12 -p /sbin/ldconfig

%post -n compat-libcogl-pango12 -p /sbin/ldconfig
%postun -n compat-libcogl-pango12 -p /sbin/ldconfig

%files -n compat-libcogl12
%doc COPYING
%{_libdir}/libcogl.so.*

%files -n compat-libcogl-pango12
%doc COPYING
%{_libdir}/libcogl-pango.so.*

%changelog
* Fri May 22 2015 Florian Müllner <fmuellner@redhat.com> - 1.14.0-3
- Add explicit requirement to subpackage
  Related: #1184209

* Fri Nov 07 2014 Kalev Lember <kalevlember@gmail.com> - 1.14.0-2
- Add missing ldconfig calls

* Thu Nov 06 2014 Kalev Lember <kalevlember@gmail.com> - 1.14.0-1
- Cogl 1.14 compat package for el7-gnome-3-14 copr
