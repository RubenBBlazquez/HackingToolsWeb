const AUTHORIZATION_TYPES = {
    BEARER: 'Bearer Token',
    BASIC: 'Basic Auth',
    NONE: 'None Auth',
    DIGEST: 'Digest Auth'
}

document.addEventListener("DOMContentLoaded", () => {
    initSavedAuthorizationsDatatable();
    setSelectorAuthorizationTypesEvent();
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
        removeSavedAuth.addEventListener('click', () => { deleteRowFromDatatable(authorizationsDatatable, numberOfAuthorizations - 1)})

        const editSavedAuth = document.getElementById(`editAuthSaved${numberOfAuthorizations}`)
        editSavedAuth.addEventListener('click', () => { editSavedAuthentication(numberOfAuthorizations - 1)})
    }

    setTimeout(handler, 500);
}