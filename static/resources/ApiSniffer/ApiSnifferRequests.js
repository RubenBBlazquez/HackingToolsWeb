const getDefaultFile = (params) => {

    const init = {
        method: 'GET',
        headers: {'Content-Type': 'application/json'},
    }

    const endpoint = backendUrl + 'getDefaultApiSnifferFile/?' + params

    return fetch(endpoint, init)
}

/**
 *
 * @returns {Promise<void>}
 */
const setEndpointsFromFile = async () => {
    const file = event.target
    const fileName = file.value

    let formData = new FormData();
    formData.append(file.name, event.target.files[0]);

    const response = await fetchInformation(
        backendUrl + 'generateEndpointsFromFile/',
        'POST',
        {},
        undefined,
        formData,
        false
    )

    const endpointsInformation = await response.json();

    composeAuthenticationAndEndpointsInformationFrom(endpointsInformation)
}

function startApiSniffer() {
    const savedAuthentications = getAllRowsInformationFromSavedAuthorizations(numberOfAuthorizations);
    const endpoints = getAllRowsInformationFromSavedEndpoints(numberOfEndpoints);

    endpoints.map((endpoint) => {
        let endpointAuth = {type: 'none', value: 'none'}

        if (endpoint.auth.includes(':')) {
            const endpointAuthSplit = endpoint.auth.split(':');
            const endpointAuthType = endpointAuthSplit[0].trim();
            const endpointAuthValue = endpointAuthSplit[1].trim();

            const authFromEndpoint = savedAuthentications
                .filter((auth) => {
                    if (auth.type === endpointAuthType && auth.value === endpointAuthValue) {
                        return true;
                    }
                }).map((auth) => {
                    return {type: auth.type, value: auth.value}
                })

            if (authFromEndpoint.length > 0) {
                endpointAuth = authFromEndpoint[0];
            }
        }

        endpoint.auth = endpointAuth;
        delete endpoint.action

        return endpoint;
    })

    const body = {
        endpointsInformation: endpoints
    }

    fetchInformation(backendUrl + 'startSniffingEndpoints/', 'POST', BASIC_HEADERS, null, body)
        .then(async (response) => {
            const result = await response.json();

            setJsonInformationObtained(result)
        })
        .catch((err) => {
            console.log(err)
        })

}


const getEndpointsAlreadySniffed = () => {
    fetchInformation(backendUrl + 'getEndpointsAlreadySniffed/', 'GET', BASIC_HEADERS, null, {})
        .then(async (response) => {
            const endpoints = await response.json();
            addEndpointsAlreadySniffedToDatatable(endpoints)
        })
        .catch((err) => {
            console.log(err)

            return resolve(false)
        })
}
