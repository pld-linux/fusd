#
# Conditional build:
# _without_dist_kernel	- without sources of distribution kernel
#
Summary:	a Linux Framework for User-Space Devices
Name:		fusd
Version:	1.10
%define _rel	1
Release:	%{_rel}
License:	BSD
Group:		Development/Libraries
Source0:	ftp://ftp.circlemud.org/pub/jelson/fusd/%{name}-%{version}.tar.gz
# Source0-md5:	b61edee0962a3c2b62d87ad9ea4d46f8
URL:		http://www.circlemud.org/~jelson/software/fusd/
%{!?_without_dist_kernel:BuildRequires:	kernel-headers}
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FUSD (pronounced fused) is a Linux framework for proxying device file
callbacks into user-space, allowing device files to be implemented by
daemons instead of kernel code. Despite being implemented in
user-space, FUSD devices can look and act just like any other file
under /dev which is implemented by kernel callbacks.

%package -n kernel-misc-kfusd
Summary:	Linux kernel FUSD modules
Summary(pl):	Modu造 FUSD dla j康ra Linuksa
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod

%description -n kernel-misc-kfusd
Linux kernel FUSD modules.

%description -n kernel-misc-kfusd -l pl
Modu造 FUSD dla j康ra Linuksa.

%package -n kernel-smp-misc-kfusd
Summary:	Linux SMP kernel FUSD modules
Summary(pl):	Modu造 SMP FUSD dla j康ra Linuksa
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-misc-kfusd
Linux SMP kernel FUSD modules.

%description -n kernel-smp-misc-kfusd -l pl
Modu造 SMP FUSD dla j康ra Linuksa.

%prep
%setup -q
tar xzf doc/*.tar.gz

%build
sed -i -e 's#CC := .*#CC := %{kgcc}#g' make.include
sed -i -e 's#CFLAGS := .*#CFLAGS := -fPIC %{rpmcflags}#g' make.include
sed -i -e 's#KERNEL_HOME := .*#KERNEL_HOME := %{_kernelsrcdir}#g' Makefile
%{__make}
mv obj.* obj.UP
%{__make} clean
sed -i -e 's#CFLAGS := .*#CFLAGS := -fPIC %{rpmcflags} -DCONFIG_SMP#g' make.include
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/%{name}}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

install obj.UP/libfusd.a	$RPM_BUILD_ROOT%{_libdir}
install include/*.h		$RPM_BUILD_ROOT%{_includedir}/%{name}
install obj.UP/kfusd.*o		$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/
install obj.*-linux/kfusd.*o	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-misc-kfusd
%depmod %{_kernel_ver}

%postun -n kernel-misc-kfusd
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-kfusd
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-misc-kfusd
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc ChangeLog README fusd/* examples
%{_includedir}/%{name}
%{_libdir}/*.a

%files -n kernel-misc-kfusd
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/kfusd*

%files -n kernel-smp-misc-kfusd
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/kfusd*
