#!/usr/bin/env python
# Copyright (C) 2012 Yunfei Zu <zuyunfei@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import distutils.core
import svnhistory

if __name__ == '__main__':
	distutils.core.setup(
		name='svnhistory',
		description='svn history browser',
        # long_description=svnhistory.__doc__,
		version=svnhistory.__version__,
		author=svnhistory.__author__,
		author_email=svnhistory.__email__,
		license=svnhistory.__license__,
		url='',
        scripts=['data/svnhistory'],
        # data_files=[],
        # package_data={},
		packages=('svnhistory',
                  'svnhistory.ui')
        )
