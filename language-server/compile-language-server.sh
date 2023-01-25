#!/usr/bin/env bash

GITHUB_REPO_URL="https://github.com/microsoft/vscode"
GITHUB_REPO_NAME=$(echo "${GITHUB_REPO_URL}" | command grep -oE '[^/]*$')

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_DIR="${SCRIPT_DIR}"
SRC_DIR="${REPO_DIR}/${GITHUB_REPO_NAME}/extensions/css-language-features/server"
DIST_DIR="${REPO_DIR}/css-language-features/server"


# -------- #
# clean up #
# -------- #

pushd "${REPO_DIR}" || exit

rm -rf \
    "${DIST_DIR}" \
    "package-lock.json" \
    "package.json" \
    --

popd || exit


# ------------------------- #
# download the source codes #
# ------------------------- #

pushd "${REPO_DIR}" || exit

echo 'Enter commit SHA, branch or tag (for example 2.1.0) to build'
read -rp 'SHA, branch or tag (default: main): ' ref

# use the "main" branch by default
if [ "${ref}" = "" ]; then
    ref="main"
fi

temp_zip="src-${ref}.zip"
curl -L "${GITHUB_REPO_URL}/archive/${ref}.zip" -o "${temp_zip}"
unzip -z "${temp_zip}" | tr -d '\r' > update-info.log
unzip "${temp_zip}"  # ignore errors as there are some special file names that cause them
rm -f "${temp_zip}" || exit
mv "${GITHUB_REPO_NAME}-"* "${GITHUB_REPO_NAME}"

popd || exit


# ------------ #
# prepare deps #
# ------------ #

pushd "${SRC_DIR}" || exit

npm install

# @see https://github.com/microsoft/vscode/blob/main/extensions/package.json
npm install -D typescript@^4.9.4

popd || exit


# ------- #
# compile #
# ------- #

pushd "${SRC_DIR}" || exit

# we only need the server for Node.js environment
cat << EOF > tsconfig.mod.json
{
    "extends": "./tsconfig.json",
    "compilerOptions": {
        "outDir": "./out"
    },
    "include": [
        "src/node/cssServerMain.ts"
    ]
}
EOF

npx tsc --newLine LF -p tsconfig.mod.json

popd || exit


# -------------------- #
# collect output files #
# -------------------- #

pushd "${REPO_DIR}" || exit

mkdir -p "${DIST_DIR}"

cp -rf "${SRC_DIR}/out" "${DIST_DIR}"
cp "${SRC_DIR}/package.json" .
cp "${SRC_DIR}/package-lock.json" .

popd || exit


# -------- #
# clean up #
# -------- #

pushd "${REPO_DIR}" || exit

rm -rf "${GITHUB_REPO_NAME}"

popd || exit
