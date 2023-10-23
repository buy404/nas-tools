#!/bin/sh

DOCKER_BUILD_SHELL_PATH=$(cd "$(dirname "$0")";pwd)

cd ${DOCKER_BUILD_SHELL_PATH}

if [ ! -f NAStool_Update_Key ]; then
  echo "SSH私钥文件缺失，无法构建：${DOCKER_BUILD_SHELL_PATH}/NAStool_Update_Key"
  exit 1
fi

if [ -f ../package_list.txt ]; then
  cp -a ../package_list.txt ./
fi
if [ -f ../requirements.txt ]; then
  cp -a ../requirements.txt ./
fi
if [ -f ../version.py ]; then
  cp -a ../version.py ./
fi

APP_VERSION=$(cat version.py | awk '{print substr($3,2,length($3)-2)}')

rm -f Dockerfile-wdmcheng
cp -a Dockerfile-wdmcheng-tpl Dockerfile-wdmcheng
sed -i "s/__APP_VERSION__/${APP_VERSION}/g" Dockerfile-wdmcheng

DOCKER_BUILDKIT=1 docker build -f Dockerfile-wdmcheng -t wdmcheng/nas-tools:${APP_VERSION}-enhanced \
  --secret id=nastool_deploy_readonly_key,src=${DOCKER_BUILD_SHELL_PATH}/NAStool_Update_Key .
