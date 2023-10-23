#!/bin/sh
# run a command as (non-existent) user, using libnss-wrapper (nss_wrapper in alpine)

NSS_UID="$(id -u)"
NSS_GID="$(id -g)"

HOME_DIR=/tmp/user
PASSWD=/var/tmp/passwd
GROUP=/var/tmp/group

if [ ! -d "${HOME_DIR}" ]; then
  mkdir "${HOME_DIR}"
fi
if [ ! -f "${PASSWD}" ]; then
  echo "user::${NSS_UID}:${NSS_GID}::${HOME_DIR}:" > "$PASSWD"
fi
if [ ! -f "${GROUP}" ]; then
  echo "user::${NSS_GID}:" > "${GROUP}"
fi

LD_PRELOAD=libnss_wrapper.so NSS_WRAPPER_PASSWD="${PASSWD}" NSS_WRAPPER_GROUP="${GROUP}" HOME="${HOME_DIR}" exec "$@"
