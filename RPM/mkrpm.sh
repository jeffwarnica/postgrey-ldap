#!/bin/sh

RPMBUILD_ROOT=/home/jwarnica/rpmbuild/
VER=`grep Version: postgreyldap.spec|sed 's/Version:\s*//'`

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR=`dirname $DIR`
echo $ROOT_DIR

UP_DIR=`dirname $ROOT_DIR`

rm -rf /tmp/postgreyldap-$VER

cp -arv $ROOT_DIR /tmp/postgreyldap-$VER

cd /tmp

tar cjvf $RPMBUILD_ROOT/SOURCES/postgreyldap-$VER.tar.bz2 postgreyldap-$VER

cd $DIR

cp * $RPMBUILD_ROOT/SOURCES

cp postgreyldap.spec $RPMBUILD_ROOT/SPECS

rpmbuild -ba $RPMBUILD_ROOT/SPECS/postgreyldap.spec
