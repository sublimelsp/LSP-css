"use strict";
/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
Object.defineProperty(exports, "__esModule", { value: true });
exports.getDocumentContext = void 0;
const strings_1 = require("../utils/strings");
const vscode_uri_1 = require("vscode-uri");
function getDocumentContext(documentUri, workspaceFolders) {
    function getRootFolder() {
        for (let folder of workspaceFolders) {
            let folderURI = folder.uri;
            if (!strings_1.endsWith(folderURI, '/')) {
                folderURI = folderURI + '/';
            }
            if (strings_1.startsWith(documentUri, folderURI)) {
                return folderURI;
            }
        }
        return undefined;
    }
    return {
        resolveReference: (ref, base = documentUri) => {
            if (ref[0] === '/') { // resolve absolute path against the current workspace folder
                let folderUri = getRootFolder();
                if (folderUri) {
                    return folderUri + ref.substr(1);
                }
            }
            base = base.substr(0, base.lastIndexOf('/') + 1);
            return vscode_uri_1.Utils.resolvePath(vscode_uri_1.URI.parse(base), ref).toString();
        },
    };
}
exports.getDocumentContext = getDocumentContext;
