%define module vt6656
%define name dkms-%{module}
%define uversion 1.19_12
%define version %(echo %{uversion} | sed "s,_,.,")
%define release %mkrel 2
%define dkms_ver %{version}-%{release}
%define sname VT6656_Linux_src_v%{uversion}_x86

Summary: VIA VT6656 wireless USB driver
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://www.viaarena.com/Driver/%{sname}.zip
Patch0: VT6656_Linux_src_v1.19_12_x86-netdev_priv.patch
Patch1: VT6656_linux_src_v1.19.16_x86-fsugid.patch
Patch2: VT6656_linux_src_v1.19.16_x86-noinfo.patch
License: GPL
Group: System/Kernel and hardware
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Url: http://www.viaarena.com/
BuildArch: noarch
Requires(post): dkms
Requires(preun): dkms

%description
This is a driver for the VIA VT6656 wireless USB chipset

%prep
%setup -q -n %{sname}
%patch0 -p1 -b .netdev_priv
%patch1 -p1 -b .fsugid
%patch2 -p1 -b .noinfo

cat > dkms.conf <<EOF
PACKAGE_NAME=%{module}
PACKAGE_VERSION=%{dkms_ver}
BUILT_MODULE_NAME[0]=vntwusb
DEST_MODULE_NAME[0]=%{module}
DEST_MODULE_LOCATION[0]=/kernel/drivers/net/wireless
AUTOINSTALL=yes
EOF

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/src/%{module}-%{dkms_ver}/
pushd driver
tar c . | tar x -C %{buildroot}/usr/src/%{module}-%{dkms_ver}/
popd
tar c include dkms.conf | tar x -C %{buildroot}/usr/src/%{module}-%{dkms_ver}/

%clean
rm -rf %{buildroot}

%post
set -x
/usr/sbin/dkms --rpm_safe_upgrade add -m %{module} -v %{dkms_ver}
/usr/sbin/dkms --rpm_safe_upgrade build -m %{module} -v %{dkms_ver}
/usr/sbin/dkms --rpm_safe_upgrade install -m %{module} -v %{dkms_ver}
:

%preun
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{module} -v %{dkms_ver} --all
:

%files
%defattr(-,root,root)
/usr/src/%{module}-%{dkms_ver}
