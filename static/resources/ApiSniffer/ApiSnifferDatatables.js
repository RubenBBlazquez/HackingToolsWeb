/**
 * method to init data-table with tags information
 */
const initSavedAuthorizationsDatatable = () => {
    authorizationsDatatable = $('#dataTable-authorizations').DataTable({
        lengthMenu: [20],
    });
}

/**
 * method to init data-table with tags information
 */
const initSavedEndpointsDatatable = () => {
    endpointsDatatable = $('#dataTable-endpoints').DataTable({
        lengthMenu: [20],
    });
}

const getAllRowsInformationFromSavedAuthorizations = (numberOfAuthorizations) => {
    const savedAuths = [];

    for (let row = 0; row < numberOfAuthorizations; row++) {
        const authData = getInformationFromDatatable(authorizationsDatatable, row);
        const authInformation = {index: authData[0], type: authData[1], value: authData[2], action: authData[3]}

        savedAuths.push(authInformation)
    }

    return savedAuths;
}

const getAllRowsInformationFromSavedEndpoints = (numberOfEndpoints) => {
    const savedEndpoints = [];

    for (let row = 0; row < numberOfEndpoints; row++) {
        const endpointRowData = getInformationFromDatatable(endpointsDatatable, row);
        const endpointInformation = {
            index: endpointRowData[0],
            endpoint: endpointRowData[1],
            customHeaders: endpointRowData[2],
            auth: endpointRowData[3],
            action: endpointRowData[4]
        }

        savedEndpoints.push(endpointInformation)
    }

    return savedEndpoints;
}
