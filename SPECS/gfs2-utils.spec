###############################################################################
###############################################################################
##
##  Copyright (C) 2004-2013 Red Hat, Inc.  All rights reserved.
##
##  This copyrighted material is made available to anyone wishing to use,
##  modify, copy, or redistribute it subject to the terms and conditions
##  of the GNU General Public License v.2.
##
###############################################################################
###############################################################################

Name: gfs2-utils
Version: 3.1.10
Release: 3%{?dist}
License: GPLv2+ and LGPLv2+
Group: System Environment/Kernel
Summary: Utilities for managing the global file system (GFS2)
%{?fedora:Requires: kernel-modules-extra}
Obsoletes: gfs2-cluster < %{version}
BuildRequires: ncurses-devel
BuildRequires: kernel-headers
BuildRequires: automake
BuildRequires: libtool
BuildRequires: zlib-devel
BuildRequires: gettext-devel
BuildRequires: bison
BuildRequires: flex
BuildRequires: libblkid-devel
BuildRequires: libuuid-devel
BuildRequires: check-devel
URL: https://fedorahosted.org/cluster/wiki/HomePage

Provides: xenserver-%{name} = %{version}-%{release}

%if 0%{?rhel} > 0
ExclusiveArch: x86_64 s390x ppc64le
%endif

# The source for this package was pulled from the upstream git tree.
# Use the following commands to generate the tarball:
# git clone git://git.fedorahosted.org/gfs2-utils.git
# cd gfs2-utils
# ./make-tarball.sh
#
#Source0: https://releases.pagure.org/gfs2-utils/gfs2-utils-%{version}.tar.gz
Source0: https://code.citrite.net/rest/archive/latest/projects/XSU/repos/gfs2-utils/archive?at=refs%2Ftags%2F%{version}&format=tar.gz&prefix=gfs2-utils-%{version}#/gfs2-utils-%{version}.tar.gz
Patch0: bz1326508-gfs2_5_Clarify_the_availability_of_the_loccookie_option.patch
Patch1: bz1436772-gfs2_grow_Disable_rgrp_alignment_when_dev_topology_is_unsuitable.patch
Patch2: bz1440269-1-mkfs_gfs2_Free_unnecessary_cached_pages_disable_readahead.patch
Patch3: bz1440269-2-mkfs_gfs2_Fix_resource_group_alignment_issue.patch
Patch4: bz1440269-3-libgfs2_Issue_one_write_per_rgrp_when_creating_them.patch


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%prep
%setup -q -n gfs2-utils-%{version}
%patch0 -p1 -b .bz1326508-gfs2_5_Clarify_the_availability_of_the_loccookie_option
%patch1 -p1 -b .bz1436772-gfs2_grow_Disable_rgrp_alignment_when_dev_topology_is_unsuitable
%patch2 -p1 -b .bz1440269-1-mkfs_gfs2_Free_unnecessary_cached_pages_disable_readahead
%patch3 -p1 -b .bz1440269-2-mkfs_gfs2_Fix_resource_group_alignment_issue
%patch4 -p1 -b .bz1440269-3-libgfs2_Issue_one_write_per_rgrp_when_creating_them

%build
./autogen.sh
%configure
make %{_smp_mflags}

%check
make check

%install
rm -rf %{buildroot}
make -C gfs2 install DESTDIR=%{buildroot}
# Don't ship gfs2_{trace,lockcapture} in this package
rm -f %{buildroot}/usr/sbin/gfs2_trace
rm -f %{buildroot}/usr/sbin/gfs2_lockcapture
rm -f %{buildroot}%{_mandir}/man8/gfs2_trace.8
rm -f %{buildroot}%{_mandir}/man8/gfs2_lockcapture.8

%clean
rm -rf %{buildroot}

%description
The gfs2-utils package contains a number of utilities for creating,
checking, modifying, and correcting any inconsistencies in GFS2
file systems.

%files
%defattr(-,root,root,-)
%doc doc/COPYING.* doc/COPYRIGHT doc/*.txt
%doc doc/README.contributing doc/README.licence doc/README.tests
%{_sbindir}/fsck.gfs2
%{_sbindir}/gfs2_grow
%{_sbindir}/gfs2_jadd
%{_sbindir}/mkfs.gfs2
%{_sbindir}/gfs2_convert
%{_sbindir}/gfs2_edit
%{_sbindir}/tunegfs2
%{_sbindir}/gfs2_withdraw_helper
%{_sbindir}/glocktop
%{_mandir}/man8/*gfs2*
%{_mandir}/man8/glocktop*
%{_mandir}/man5/*
%{_prefix}/lib/udev/rules.d/82-gfs2-withdraw.rules

%changelog
* Tue Apr 18 2017 Andrew Price <anprice@redhat.com> - 3.1.10-3
- libgfs2: Issue one write per rgrp when creating them
- mkfs.gfs2: Fix resource group alignment issue
- mkfs.gfs2: Free unnecessary cached pages, disable readahead
  Resolves: rhbz#1440269

* Tue Mar 28 2017 Andrew Price <anprice@redhat.com> - 3.1.10-2
- gfs2_grow: Disable rgrp alignment when dev topology is unsuitable
  Resolves: rhbz#1436772

* Tue Mar 28 2017 Andrew Price <anprice@redhat.com> - 3.1.10-1
- Rebase to new upstream version 3.1.10
  Resolves: rhbz#1348601
  Resolves: rhbz#1356685
  Resolves: rhbz#1382087
  Resolves: rhbz#1405163
  Resolves: rhbz#1430399
- Make dependency on libuuid explicit

* Wed Mar 15 2017 Andrew Price <anprice@redhat.com> - 3.1.9-4
- Enable ppc64le builds
  Resolves: rhbz#1426651

* Wed Jul 20 2016 Andrew Price <anprice@redhat.com> - 3.1.9-3
- gfs2(5): Clarify the availability of the loccookie option
  Resolves: rhbz#1326508

* Wed Jul 06 2016 Andrew Price <anprice@redhat.com> - 3.1.9-2
- fsck.gfs2: "undo" functions can stop too early on duplicates
  Resolves: rhbz#1348703
- fsck.gfs2: link count checking wrong inode's formal inode number
  Resolves: rhbz#1350597
- fsck.gfs2: check formal inode number when links go from 1 to 2
  Resolves: rhbz#1350600

* Tue Jun 07 2016 Andrew Price <anprice@redhat.com> - 3.1.9-1
- Rebase to new upstream release 3.1.9
  Resolves: rhbz#1271674
  Resolves: rhbz#1162819
  Resolves: rhbz#1196321
  Resolves: rhbz#1202814
  Resolves: rhbz#1251036
  Resolves: rhbz#1257625
  Resolves: rhbz#1268045
  Resolves: rhbz#1283866
  Resolves: rhbz#1332728

* Thu Sep 17 2015 Andrew Price <anprice@redhat.com> - 3.1.8-6
- gfs2_edit savemeta: speed up is_block_in_per_node()
  Resolves: rhbz#1162216

* Thu Aug 20 2015 Andrew Price <anprice@redhat.com> - 3.1.8-5
- gfs2-utils: Fix hang on withdraw (4 patches)
- Include new withdraw helper scripts in files section
  Resolves: rhbz#1225634

* Tue Jul 07 2015 Andrew Price <anprice@redhat.com> - 3.1.8-4
- fsck.gfs2: Change duptree structure to have generic flags
- fsck.gfs2: Detect, fix and clone duplicate block refs within a dinode
  Resolves: rhbz#1236669

* Mon Apr 27 2015 Andrew Price <anprice@redhat.com> - 3.1.8-3
- mkfs.gfs2: Allow longer cluster names
  Resolves: rhbz#1202831

* Fri Apr 17 2015 Andrew Price <anprice@redhat.com> - 3.1.8-2
- fsck.gfs2: replace recent i_goal fixes with simple logic
  Resolves: rhbz#1186515

* Tue Apr 07 2015 Andrew Price <anprice@redhat.com> - 3.1.8-1
- Rebase to new upstream version 3.1.8
  Resolves: rhbz#1184482
  Resolves: rhbz#1153316
  Resolves: rhbz#1154726
  Resolves: rhbz#1162216
  Resolves: rhbz#1165285
  Resolves: rhbz#1186515
  Resolves: rhbz#1186847
  Resolves: rhbz#1194446
  Resolves: rhbz#1195394

* Thu Jan 15 2015 Andrew Price <anprice@redhat.com> - 3.1.7-6
- fsck.gfs2: fix broken i_goal values in inodes
- gfs2_convert: use correct i_goal values instead of zeros for inodes
- tests: test for incorrect inode i_goal values
- fsck.gfs2: Reprocess nodes if anything changed - addendum 1 of 2
- fsck.gfs2: addendum to fix broken i_goal values in inodes - addendum 2 of 2
  Resolves: rhbz#1178604

* Thu Nov 20 2014 Andrew Price <anprice@redhat.com> - 3.1.7-5
- Update ExclusiveArch
  Resolves: rhbz#1161936

* Tue Nov 18 2014 Andrew Price <anprice@redhat.com> - 3.1.7-4
- mkfs.gfs2: Revert default resource group size
  Resolves: rhbz#1162817
- Add ExclusiveArch
  Resolves: rhbz#1161936

* Tue Nov 18 2014 Andrew Price <anprice@redhat.com> - 3.1.7-3
- fsck.gfs2: Detect and correct corrupt journals
  Resolves: rhbz#1146160

* Mon Nov 17 2014 Andrew Price <anprice@redhat.com> - 3.1.7-2
- fsck.gfs2: Improve reporting of pass timings
  Resolves: rhbz#1154786

* Mon Sep 08 2014 Andrew Price <anprice@redhat.com> - 3.1.7-1
- Rebase to new upstream version 3.1.7
- gfs2-utils tests: Fix unit tests for RHEL7
- gfs2-utils tests: Build unit tests with consistent cpp flags
  Resolves: rhbz#1112342
  Resolves: rhbz#1017381
  Resolves: rhbz#1075135
  Resolves: rhbz#1079507
  Resolves: rhbz#1107238

* Fri Mar 07 2014 Andrew Price <anprice@redhat.com> - 3.1.6-13
- gfs2_edit: Convert fssize to bytes before reporting fs size
- mkfs.gfs2 tests: Enable debug output
  Resolves: rhbz#1059443
- libgfs2: Superblock building and writing improvements
- gfs2-utils: Ensure sb_uuid uses are guarded
- libgfs2: Add support for new leaf hint fields
  Resolves: rhbz#1063842

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.1.6-12
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.1.6-11
- Mass rebuild 2013-12-27

* Mon Nov 18 2013 Andrew Price <anprice@redhat.com> - 3.1.6-10
- libgfs2: Add lgfs2_open_mnt* functions
- Switch is_pathname_mounted callers to lgfs2_open_mnt*
- libgfs2: Remove is_pathname_mounted
  Resolves: rhbz#991204

* Wed Nov 13 2013 Andrew Price <anprice@redhat.com> - 3.1.6-9
- libgfs2: Add sd_heightsize bounds checking in read_sb (3 patches)
  Resolves: rhbz#1028388

* Tue Sep 17 2013 Andrew Price <anprice@redhat.com> - 3.1.6-8
- Don't use README.* for docs (it can pick up some patch files)
  Related: rhbz#1000066

* Tue Sep 17 2013 Andrew Price <anprice@redhat.com> - 3.1.6-7
- fsck.gfs2: Check and repair per_node contents such as quota_changeX
  Resolves: rhbz#1003059

* Fri Sep 06 2013 Andrew Price <anprice@redhat.com> - 3.1.6-6
- gfs2_tool: catch interrupts while the metafs is mounted
  Resolves: rhbz#996236

* Tue Aug 27 2013 Andrew Price <anprice@redhat.com> - 3.1.6-5
- gfs2-utils tests: Switch to autotest
  Resolves: rhbz#1000066
- fsck.gfs2: Allocate enough space for the block map (2 patches)
  Resolves: rhbz#1001583

* Tue Aug 27 2013 Andrew Price <anprice@redhat.com> - 3.1.6-4
- Install utils into /usr/sbin instead of /sbin
  Resolves: rhbz#996539

* Tue Aug 13 2013 Andrew Price <anprice@redhat.com> - 3.1.6-3
- fsck.gfs2: Add the ability to detect journal inode indirect block corruption
  Resolves: rhbz#990683
- gfs2_grow: Don't try to open an empty string
  Resolves: rhbz#991204

* Mon Jul 29 2013 Andrew Price <anprice@redhat.com> - 3.1.6-2
- Don't install gfs2_lockcapture and gfs2_trace
  Resolves: rhbz#987019
- Run test suite after build (requires check-devel build req)
- Install both of the READMEs into doc/

* Wed Jul 24 2013 Andrew Price <anprice@redhat.com> - 3.1.6-1
- New upstream release
- Drop 'file' requirement - mkfs.gfs2 now uses libblkid instead
- Drop 'ncurses' requirement - dependency is added automatically
- Drop requires chkconfig and initscripts - no longer installs daemons
- Drop fix_build_on_rawhide.patch - upstream
- Add build req on libblkid-devel

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Andrew Price <anprice@redhat.com> - 3.1.5-1
- New upstream release
  Removes mount.gfs2, gfs2_tool, gfs2_quota
- Remove rawhide_transition.patch - now obsolete
- Update BuildRequires:
  Change glibc-kernheaders to kernel-headers
  Add bison and flex
- Provide a valid url for Source0
- Add fix_build_on_rawhide.patch to fix a circular dep introduced in
  bison 2.6, and a make -j race between libgfs2 and gfs2l

* Tue Aug 14 2012 Andrew Price <anprice@redhat.com> - 3.1.4-6
- Make the kernel-modules-extra requirement Fedora-specific
  Resolves bz#847955

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 17 2012 Andrew Price <anprice@redhat.com> - 3.1.4-4
- Remove commented-out sections
- Clean up some lintian warnings
- Add dependency on kernel-modules-extra as per bz#811547

* Wed Mar 07 2012 Andrew Price <anprice@redhat.com> - 3.1.4-3
- Remove redundant postinstall scriptlet

* Thu Feb  2 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.4-2
- make sure to Obsolete gfs2-cluster

* Wed Feb 01 2012 Andrew Price <anprice@redhat.com> - 3.1.4-1
- New upstream release
  Adds gfs2_lockgather script
- Remove gfs2-cluster (commented out for now)
- Remove dependency on corosynclib-devel and systemd-units
- Add rawhide_transition.patch to stop gfs_controld from building

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Andrew Price <anprice@redhat.com> - 3.1.3-1
- New upstream release
  Bugfixes and improvements to fsck.gfs2
  Fixes various other bugs
  Improve strings and translation support
- Adds gfs2-cluster systemd unit
- Removes gfs2* init scripts

* Wed Jul 06 2011 Andrew Price <anprice@redhat.com> - 3.1.2-1
- New upstream release
  Fixes several bugs
  Improves translation support
  Adds savemeta compression
- Add zlib-devel to BuildRequires
- Add gettext-devel to BuildRequires

* Wed May 25 2011 Steven Whitehouse <swhiteho@redhat.com> - 3.1.1-3
- Update wiki URL
- Remove gfs2_tool and gfs2_quota from package

* Fri Feb 25 2011 Bob Peterson <rpeterso@redhat.com> - 3.1.1-2
- Bumping release number to keep upgrades consistent.

* Wed Feb 23 2011 Bob Peterson <rpeterso@redhat.com> - 3.1.1-1
- gfs2_edit savemeta doesn't save all leafs for big directories
- gfs2_edit improvements
- fsck.gfs2: can't repair rgrps resulting from gfs_grow->gfs2_convert
- fsck.gfs2: reports master/root dinodes as unused and fixes bitmap

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Steven Whitehouse <swhiteho@redhat.com> - 3.1.0-4
- Drop mount.gfs2 and its man page
- Only list gfs2_tool once in the files list

* Wed Dec  8 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.0-3
- Drop circular dependency on cman

* Fri Dec  3 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.0-2
- gfs2-cluster should Obsoletes/Provides gfs-pcmk

* Tue Sep 30 2010 Steven Whitehouse <swhiteho@redhat.com> - 3.1.0-1
- Bringing this package back for upstream GFS2
  Addition of gfs2tune to the utils
  Merge of gfs_controld from cman

* Thu Jan 22 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.03.11-1
- New upstream release
  Fix several bugs and drastically improve startup errors.

* Wed Dec 10 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.03.10-1
- New upstream release
  Fix several bugs and port gfs1 code to match 2.6.27 kernel.

* Fri Oct 31 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.03.09-1
- New upstream release
  Fix rhbz#468966
  Addresses several security issues similar to CVE-2008-4192 and
  CVE-2008-4579 after deep code audit from upstream
- cleanup patches to match 2.6.26 kernel in F-9

* Tue Oct 21 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.03.08-1
- New upstream release
  Fix rhbz#460376 CVE-2008-4192
  Fix rhbz#467386 CVE-2008-4579
- cleanup/update patches to match 2.6.26 kernel in F-9

* Thu Aug 14 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.03.07-1
- New upstream release
- Fix rgmanager startup locking issues
- Apply patch to include kernel headers from 2.6.26 required to build
  userland. Userland will run in 2.6.25 compatibility mode
- Apply patch to keep kernel modules at 2.6.25 (upstream is at 2.6.26)
  (this patch is purely cosmetic since we don't build kernel modules
  but keep the source in sync is Good (tm))
- Cleanup packaging for installed docs and file permissions

* Mon Jul 14 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.03.05-1
- New upstream release
- Cleanup installed doc after upstream

* Wed Jun 11 2008 Fabio M. Di Nitto <fdinitto@redhat.com> 2.03.04-1
- New upstream release
- Resolves: #446995 #318271 #447378 #445662
- Update license tags after major upstream cleanup
- Include COPYRIGHT file

* Fri May 30 2008 Fabio M. Di Nitto <fdinitto@redhat.com> 2.03.03-1
- New upstream release
- Fix several build warnings
- Update spec files to use macros
- Update Requires to use packages rather than pointing at files
- Drop BR on kernel-devel since it's not required anymore
- Update build section to use proper _sysconfdir, libdir and sbindir
- Avoid abusing cd when we can ask make to do the work for us
- Remove /usr/sbin from file section. We don't have any file there
  and we can avoid shipping stuff by mistake

* Mon Apr 14 2008 Steven Whitehouse <swhiteho@redhat.com> 2.03.00-3
- Fabbione saves the day. We can get rid of the sed stuff after all

* Mon Apr 14 2008 Steven Whitehouse <swhiteho@redhat.com> 2.03.00-1
- New upstream sources
- Eric Sandeen's solution to kernel version dep

* Wed Apr 09 2008 Steven Whitehouse <swhiteho@redhat.com> 0.1.25.2.02.01-15
- Remove obsolete chkconfig patch for initscript
- Enable parallel make
- Remove obsolete copy of gfs2_ondisk.h (this should be in glibc-kernheaders)

* Wed Apr 09 2008 Steven Whitehouse <swhiteho@redhat.com> 0.1.25.2.02.01-14
- Update URL
- Fix license spec

* Fri Mar 14 2008 Chris Feist <cfeist@redhat.com> 0.1.25.2.02.00-2
- New upstream sources.

* Tue Jan 16 2007 Chris Feist <cfeist@redhat.com> 0.1.24-1
- New upstream sources.
- Resolves: rhbz#222747

* Wed Jan 03 2007 Chris Feist <cfeist@redhat.com> 0.1.24-1
- Updated sources
- Resolves: rhbz#218560

* Thu Dec 21 2006 Chris Feist <cfeist@redhat.com> 0.1.23-1
- Updated sources
- Resolves: rhbz#218560

* Tue Dec 19 2006 Chris Feist <cfeist@redhat.com> 0.1.22-1
- New upstream sources.
- Resolves: rhbz#219878

* Tue Dec 04 2006 Chris Feist <cfeist@redhat.com> 0.1.21-1
- New upstream sources.
- Resolves: rhbz#218134 rhbz#215962

* Thu Nov 30 2006 Chris Feist <cfeist@redhat.com> 0.1.19-1
- New upstream sources.
- Resolves: rhbz#217798

* Wed Nov 29 2006 Chris Feist <cfeist@redhat.com> 0.1.18-1
- New upstream sources.
- Resolves: rhbz#217460

* Thu Oct 26 2006 Chris Feist <cfeist@redhat.com> 0.1.14-1
- New upstream sources.

* Fri Oct 13 2006 Chris Feist <cfeist@redhat.com> 0.1.12-1
- New Upstream sources.

* Fri Oct 13 2006 Chris Feist <cfeist@redhat.com> 0.1.10-1
- New Upstream sources.

* Mon Oct 09 2006 Chris Feist <cfeist@redhat.com> 0.1.9-1
- New Upstream sources.

* Mon Sep 25 2006 Chris Feist <cfeist@redhat.com> 0.1.8-1
- New Upstream sources.

* Wed Sep 13 2006 Chris Feist <cfeist@redhat.com> 0.1.7-1
- New Upstream sources.

* Thu Sep 07 2006 Chris Feist <cfeist@redhat.com> 0.1.6-2
- Fix typo in uninstall script (turn off gfs2 instead of gfs)

* Mon Aug 28 2006 Chris Feist <cfeist@redhat.com> 0.1.6-1
- New Upstream sources.

* Tue Aug 22 2006 Chris Feist <cfeist@redhat.com> 0.1.5-1
- New Upstream sources.

* Mon Aug 14 2006 Chris Feist <cfeist@redhat.com> 0.1.3-0
- New Upstream sources, use dist tag.

* Fri Jul 14 2006 Chris Feist <cfeist@redhat.com>
- Rebuild with updated sources

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com>
- rebuild

* Tue Jun 27 2006 Florian La Roche <laroche@redhat.com>
- fix typo in preun script

* Fri Jun 09 2006 Chris Feist <cfeist@redhat.com> - 0.1.0-1.fc6.3
- Initial build of gfs-utils.
