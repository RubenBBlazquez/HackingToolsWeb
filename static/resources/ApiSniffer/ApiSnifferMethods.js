const savedAuthentications = [];
const savedEndpoints = [];
let authorizationsDatatable = undefined;
let isEditingSavedAuthentication = false;
let actualEditAuthentication = 0;

/**
 *
 */
const setSelectorAuthorizationTypesEvent = () => {
    const selector = document.getElementById("authorizationsSelector")

    for (const auth of Object.keys(AUTHORIZATION_TYPES)) {
        const option = document.createElement('option')
        option.value = auth
        option.text = AUTHORIZATION_TYPES[auth]
        selector.appendChild(option)
    }

    selector.addEventListener('change', setHTMLElementsFromAuthorizationType)
}

/**
 *
 */
const setHTMLElementsFromAuthorizationType = () => {
    const authorizationCollapse = document.getElementById('authorizationCollapse')

    //creamos un objeto del Collapse de bootstrap para luego poder cerrarlo y abrirlo con js vanilla
    let bsCollapse = new bootstrap.Collapse(authorizationCollapse, {
        toggle: false
    })

    switch (AUTHORIZATION_TYPES[event.target.value]) {
        case AUTHORIZATION_TYPES.BEARER:
        case AUTHORIZATION_TYPES.BASIC:
        case AUTHORIZATION_TYPES.DIGEST:
            bsCollapse.toggle()
            setCollapseDataForAuthorizationType(AUTHORIZATION_TYPES[event.target.value])
            break

        default:
            bsCollapse.toggle()
    }
}

/**
 *
 * @returns {{data, type}|{data: string, type}}
 */
const getAuthInformationFromSetAuthModal = () => {

    const type = document.getElementById('savedAuthorizationType')
    const bearerToken = document.getElementById('bearerTokenInput')

    if (bearerToken)
        return {'type': type.value, 'data': bearerToken.value}

    const basicAuthUser = document.getElementById('basicAuthUserInput')
    const basicAuthPassword = document.getElementById('basicAuthPasswordInput')

    if (basicAuthUser && basicAuthPassword)
        return {'type': type.value, 'data': basicAuthUser.value + '-' + basicAuthPassword.value}
}

const savedAuthenticationAction = () => {
    console.log(isEditingSavedAuthentication)
    if (isEditingSavedAuthentication){
        editSavedAuthorization();
        return;
    }

    addNewAuthentication();
}

/**
 *
 */
const addNewAuthentication = () => {
    setVisibilityToAuthorizationTable();

    numberOfAuthorizations += 1

    document.getElementById('authorizationsSelector').options.selectedIndex = 0

    const authorizationInformation = getAuthInformationFromSetAuthModal()

    const newRowsInformation = [{
        index: numberOfAuthorizations,
        type: authorizationInformation.type,
        value: authorizationInformation.data,
        action: `
                   <button  class="btn btn-success fa fa-pencil " id="editAuthSaved${numberOfAuthorizations}"></button>
                   <button class="btn btn-success fa-solid fa-trash-can" id="removeAuthSaved${numberOfAuthorizations}"></button>
                `
    }];

    savedAuthentications.push({
        type: authorizationInformation.type,
        value: authorizationInformation.data
    })

    addRowToDatatable(authorizationsDatatable, newRowsInformation);
    setSavedAuthenticationEvents(numberOfAuthorizations);
}

const editSavedAuthorization = () => {
    const authorizationInformation = getAuthInformationFromSetAuthModal()

    const newRowInformation = {
        index: actualEditAuthentication ,
        type: authorizationInformation.type,
        value: authorizationInformation.data,
        action: `
                   <button class="btn btn-success fa fa-pencil " id="editAuthSaved${numberOfAuthorizations}"></button>
                   <button class="btn btn-success fa-solid fa-trash-can" id="removeAuthSaved${numberOfAuthorizations}"></button>
                `
    };

    savedAuthentications.push({
        type: authorizationInformation.type,
        value: authorizationInformation.data
    })

    updateRowDatatable(authorizationsDatatable, actualEditAuthentication, newRowInformation);
    setSavedAuthenticationEvents(numberOfAuthorizations);
}

const setVisibilityToAuthorizationTable = () => {
    const $savedAuthorizationTable = document.getElementById('savedAuthorizationTable')

    if (numberOfAuthorizations > 0) {
        $savedAuthorizationTable.style.display = 'inline'
        return;
    }

    $savedAuthorizationTable.style.display = 'none'
}

const editSavedAuthentication = (numberOfAuthorization) => {
    const collapse = new bootstrap.Collapse(authCollapse, {
        toggle: false
    });
    collapse.toggle();

    const authToEdit = savedAuthentications[numberOfAuthorization];
    actualEditAuthentication = numberOfAuthorization;

    setCollapseDataForAuthorizationType(authToEdit.type, authToEdit)
}

/**
 *
 * @param {string} type
 * @param {{}} editInformation
 */
const setCollapseDataForAuthorizationType = (type, editInformation = {}) => {
    isEditingSavedAuthentication = false;

    if (Object.keys(editInformation).length > 0 ) {
        isEditingSavedAuthentication = true;
    }

    const divSectionAuthorizationCollapse = document.getElementById('authorizationCollapseData')
    divSectionAuthorizationCollapse.innerHTML = ""

    const authorizationCollapseTitle = document.getElementById('authorizationCollapseTitle')

    const inputType = getNewInput({value: type, id: 'savedAuthorizationType', type: 'hidden'})
    divSectionAuthorizationCollapse.appendChild(inputType)

    switch (type) {
        case AUTHORIZATION_TYPES.BEARER:
            authorizationCollapseTitle.textContent = 'Bearer Authorization'

            const inputToken = getNewInput({
                placeholder: 'Set Bearer Token',
                classStyle: 'chelsea_font form-control text-black border border-dark col-12',
                id: 'bearerTokenInput',
                value: editInformation.value ?? ''
            })
            divSectionAuthorizationCollapse.appendChild(inputToken)

            break

        case AUTHORIZATION_TYPES.BASIC:
            authorizationCollapseTitle.textContent = 'Basic Authorization'

            let userName = '';
            let password = '';

            if (editInformation && editInformation.value) {
                const authValues = editInformation.value.split('-')
                userName = authValues[0] ?? '';
                password = authValues[1] ?? '';
            }

            const inputUsername = getNewInput({
                placeholder: 'Set UserName From Basic Auth',
                classStyle: 'chelsea_font form-control text-black border border-dark col-12',
                id: 'basicAuthUserInput',
                value: userName
            })
            divSectionAuthorizationCollapse.appendChild(inputUsername)

            const inputPassword = getNewInput({
                placeholder: 'Set Password From Basic Auth',
                classStyle: 'mt-2 chelsea_font form-control text-black border border-dark col-12',
                id: 'basicAuthPasswordInput',
                value: password
            })
            divSectionAuthorizationCollapse.appendChild(inputPassword)

            break
    }
}

/**
 *
 */
const collapseSavedAuthenticationSelector = () => {
    const authSelector = document.getElementById('authorizationsSelector')
    const optionSelected = authSelector.options[authSelector.selectedIndex].value
    const collapse = new bootstrap.Collapse(authCollapse, {
        toggle: false
    })

    if (AUTHORIZATION_TYPES[optionSelected] !== AUTHORIZATION_TYPES.NONE) {
        collapse.show()
        return
    }

    collapse.hide()
}

/**
 *
 */
const getDefaultDownloadFileLink = () => {
    const type = 'xlsx'
    let param = '&fileType=' + type
    param += '&fileContent=auth'

    getDefaultFile(param).then((res) => res.blob())
        .then((blob) => URL.createObjectURL(blob))
        .then((href) => {
            Object.assign(document.createElement('a'), {
                href,
                download: 'defaultEndpoints.' + type,
            }).click();
        });
}

/**
 *
 */
const setHTMLElementsFromNewEndpoint = () => {

    const authSelector = document.getElementById('endpointAuthSelector');
    authSelector.innerHTML = "";

    const defaultAuthorizationOption = [{
        value: 1,
        name: 'defaultSavedAuthorization',
        text: 'Available Saved Authorization'
    }]
    setOptionsIntoSelector(authSelector, defaultAuthorizationOption)

    const definedAuthentications = savedAuthentications.map((auth) => {
        return {value: auth.value, name: auth.type, text: auth.value}
    })

    setOptionsIntoSelector(authSelector, definedAuthentications)
}

/**
 *
 */
const addNewEndpoint = () => {
    const endpointUrl = document.getElementById('endpointUrl')
    const authorization = document.getElementById('endpointAuthorization')

    savedEndpoints.push({endpoint: endpointUrl, authorizationNumber: authorization.value})
}



