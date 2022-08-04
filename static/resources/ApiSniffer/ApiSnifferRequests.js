const getDefaultFile = (params) => {

    const init = {
        method: 'GET',
        headers: {'Content-Type': 'application/json'},
    }

    const endpoint = backendUrl + 'getDefaultApiSnifferFile/?' + params

    return fetch(endpoint, init)
}

