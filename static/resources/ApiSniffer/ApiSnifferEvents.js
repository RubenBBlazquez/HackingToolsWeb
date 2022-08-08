const AUTHORIZATION_TYPES = {
    BEARER: 'Bearer Token',
    BASIC: 'Basic Auth',
    NONE: 'None Auth',
    DIGEST: 'Digest Auth'
}

document.addEventListener("DOMContentLoaded", () => {
    initSavedAuthorizationsDatatable();
    setSelectorAuthorizationTypesEvent();
    setVisibilityToAuthorizationTable();
})

document.getElementById('getExampleFileButton').addEventListener('click', () => {
    getDefaultDownloadFileLink()
});

document.getElementById("setEndpointsFile").addEventListener("click", () => {
    const inputEndpointsFile = document.getElementById('inputEndpointsFile')
    inputEndpointsFile.click()
})

const authCollapse = document.getElementById('authorizationCollapse')
authCollapse.addEventListener('hidden.bs.collapse', () => collapseSavedAuthenticationSelector())

let numberOfAuthorizations = 0
document.getElementById('saveAuthorizationConfig').addEventListener('click', () => savedAuthenticationAction())

document.getElementById('endpointsCollapseButton').addEventListener('click', () => setHTMLElementsFromNewEndpoint())
document.getElementById('saveEndpoint').addEventListener('click', () => addNewEndpoint())

const setSavedAuthenticationEvents = (numberOfAuthorizations) => {
    const handler = () => {
        const removeSavedAuth = document.getElementById(`removeAuthSaved${numberOfAuthorizations}`);
        removeSavedAuth.addEventListener('click', () => {
            deleteRowFromDatatable(authorizationsDatatable, numberOfAuthorizations - 1)
            updateAuthenticationNumberEvents(numberOfAuthorizations-1)
            numberOfAuthorizations -= 1;
        })

        const editSavedAuth = document.getElementById(`editAuthSaved${numberOfAuthorizations}`)
        editSavedAuth.addEventListener('click', () => {
            editSavedAuthentication(numberOfAuthorizations)
        })
    }

    setTimeout(handler, 500);
    clearTimeout(handler)
}

const updateAuthenticationNumberEvents = (deletedAuthNumber) => {
    const INDEX_SAVED_AUTH = 0;
    const ACTION_SAVED_AUTH = 3;

    for (let authNumber = deletedAuthNumber + 1; authNumber < numberOfAuthorizations; authNumber++) {
        const auth = getInformationFromDatatable(authorizationsDatatable, authNumber-1)

        if (auth) {
            auth[INDEX_SAVED_AUTH] = auth[INDEX_SAVED_AUTH] - 1
            auth[ACTION_SAVED_AUTH] = auth[ACTION_SAVED_AUTH].replace(`removeAuthSaved${authNumber+1}`,`removeAuthSaved${authNumber}`)
            auth[ACTION_SAVED_AUTH] = auth[ACTION_SAVED_AUTH].replace(`editAuthSaved${authNumber+1}`,`editAuthSaved${authNumber}`)
        }

        updateRowDatatable(authorizationsDatatable, authNumber - 1, auth)
        setSavedAuthenticationEvents(authNumber)
    }
}