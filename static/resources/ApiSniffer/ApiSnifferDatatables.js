/**
 * method to init data-table with tags information
 */
const initSavedAuthorizationsDatatable = () => {
   authorizationsDatatable = $('#dataTable-authorizations').DataTable({
        lengthMenu: [20],
    });
    console.log(authorizationsDatatable)
}
