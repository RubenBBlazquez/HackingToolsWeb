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
