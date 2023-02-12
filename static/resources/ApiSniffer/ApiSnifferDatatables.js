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

/**
 * method to init data-table with tags information
 */
const initEndpointsAlreadySniffedDatatable = () => {
    endpointsAlreadySniffedDatatable = $('#dataTable-endpoints-already-sniffed').DataTable({
        lengthMenu: [20],
        "columnDefs": [
            {"visible": false, "targets": 3}
        ]
    });
}

