const AUTHORIZATION_TYPES = {
    BEARER: 'Bearer Token',
    BASIC: 'Basic Auth',
    NONE: 'None Auth',
    DIGEST: 'Digest Auth'
}

document.addEventListener("DOMContentLoaded", async () => {
    initSavedAuthorizationsDatatable();
    initSavedEndpointsDatatable();
    initEndpointsAlreadySniffedDatatable()
    setSelectorAuthorizationTypesEvent();
    setVisibilityToSavedAuthorizationTabs()
    await getEndpointsAlreadySniffed()
    setEndpointsSniffedViewerEvents()
})

document.getElementById('getExampleFileButton').addEventListener('click', () => {
    getDefaultDownloadFileLink()
});

document.getElementById("setEndpointsFile").addEventListener("click", () => {
    const inputEndpointsFile = document.getElementById('inputEndpointsFile')
    inputEndpointsFile.click()
})

document.getElementById('inputEndpointsFile').addEventListener('change', setEndpointsFromFile);

const authCollapse = document.getElementById('authorizationCollapse')
authCollapse.addEventListener('hidden.bs.collapse', () => collapseSavedAuthenticationSelector())

document.getElementById('saveAuthorizationConfig').addEventListener('click', () => savedAuthenticationAction())

document.getElementById('endpointsCollapseButton').addEventListener('click', () => setHTMLElementsFromNewEndpoint())
document.getElementById('saveEndpoint').addEventListener('click', () => savedEndpointAction())

document.getElementById('sendData').addEventListener('click', startApiSniffer)

document.getElementById('addFilter').addEventListener('click', compoundAddCustomFiltersStructure);

const setSavedAuthenticationEvents = (numberOfAuthorizations) => {
    const handler = () => {
        const removeSavedAuth = document.getElementById(`removeAuthSaved${numberOfAuthorizations}`);
        removeSavedAuth.addEventListener('click', () => {
            deleteRowFromDatatable(authorizationsDatatable, numberOfAuthorizations - 1)
            updateAuthenticationNumberEvents(numberOfAuthorizations - 1)
            setVisibilityToSavedEndpointsTabs();
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

const setSavedEndpointsEvents = (numberOfEndpoint) => {
    const handler = () => {
        const removeSavedEndpoint = document.getElementById(`removeSavedEndpoint${numberOfEndpoint}`);
        removeSavedEndpoint.addEventListener('click', () => {
            deleteRowFromDatatable(endpointsDatatable, numberOfEndpoint - 1)
            updateEndpointNumberEvents(numberOfEndpoint - 1)
            setVisibilityToSavedAuthorizationTabs();

            numberOfEndpoints -= 1;
        })

        const editSavedEndpoint = document.getElementById(`editSavedEndpoint${numberOfEndpoint}`)
        editSavedEndpoint.addEventListener('click', () => {
            setHTMLElementsFromNewEndpoint();
            editEndpoint(numberOfEndpoint)
        })
    }

    setTimeout(handler, 500);
    clearTimeout(handler)
}

const updateAuthenticationNumberEvents = (deletedAuthNumber) => {
    const INDEX_SAVED_AUTH = 0;
    const ACTION_SAVED_AUTH = 3;

    for (let authNumber = deletedAuthNumber + 1; authNumber < numberOfAuthorizations; authNumber++) {
        const auth = getInformationFromDatatable(authorizationsDatatable, authNumber - 1)

        if (auth) {
            auth[INDEX_SAVED_AUTH] = auth[INDEX_SAVED_AUTH] - 1
            auth[ACTION_SAVED_AUTH] = auth[ACTION_SAVED_AUTH].replace(`removeAuthSaved${authNumber + 1}`, `removeAuthSaved${authNumber}`)
            auth[ACTION_SAVED_AUTH] = auth[ACTION_SAVED_AUTH].replace(`editAuthSaved${authNumber + 1}`, `editAuthSaved${authNumber}`)

            updateRowDatatable(authorizationsDatatable, authNumber - 1, auth)
            setSavedAuthenticationEvents(authNumber)
        }
    }
}

const updateEndpointNumberEvents = (deletedEndpointNumber) => {
    const INDEX_SAVED_AUTH = 0;
    const ACTION_SAVED_AUTH = 3;

    for (let endpointNumber = deletedEndpointNumber + 1; endpointNumber < numberOfEndpoints; endpointNumber++) {
        const endpoint = getInformationFromDatatable(endpointsDatatable, endpointNumber - 1)
        console.log(endpointNumber, endpoint, numberOfEndpoints)
        if (endpoint) {
            endpoint[INDEX_SAVED_AUTH] = endpoint[INDEX_SAVED_AUTH] - 1
            endpoint[ACTION_SAVED_AUTH] = endpoint[ACTION_SAVED_AUTH].replace(`removeSavedEndpoint${endpointNumber + 1}`, `removeSavedEndpoint${endpointNumber}`)
            endpoint[ACTION_SAVED_AUTH] = endpoint[ACTION_SAVED_AUTH].replace(`editSavedEndpoint${endpointNumber + 1}`, `editSavedEndpoint${endpointNumber}`)

            updateRowDatatable(endpointsDatatable, endpointNumber - 1, endpoint)
            setSavedEndpointsEvents(endpointNumber)
        }
    }
}