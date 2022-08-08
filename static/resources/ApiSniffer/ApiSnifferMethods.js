let authorizationsDatatable = undefined;
let isEditingSavedAuthentication = false;
let actualEditAuthenticationNumber = 0;

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
    if (isEditingSavedAuthentication) {
        editSavedAuthorization();
        return;
    }

    addNewAuthentication();
}

/**
 *
 */
const addNewAuthentication = () => {
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

    addRowToDatatable(authorizationsDatatable, newRowsInformation);
    setSavedAuthenticationEvents(numberOfAuthorizations);
    setVisibilityToAuthorizationTable();
}

const editSavedAuthorization = () => {
    const authorizationInformation = getAuthInformationFromSetAuthModal()

    const newRowInformation = [
        actualEditAuthenticationNumber,
        authorizationInformation.type,
        authorizationInformation.data,
        `
        <button class="btn btn-success fa fa-pencil " id="editAuthSaved${numberOfAuthorizations}"></button>
        <button class="btn btn-success fa-solid fa-trash-can" id="removeAuthSaved${numberOfAuthorizations}"></button>
        `
    ];

    updateRowDatatable(authorizationsDatatable, actualEditAuthenticationNumber - 1, newRowInformation);
    setSavedAuthenticationEvents(numberOfAuthorizations);
}

const setVisibilityToAuthorizationTable = () => {
    const $savedAuthorizationTable = document.getElementById('savedAuthorizationTable')
    console.log(numberOfAuthorizations)

    if (numberOfAuthorizations > 0) {
        $savedAuthorizationTable.classList.remove('d-sm-none')
        return false;
    }

    $savedAuthorizationTable.classList.add('d-sm-none')
}

const editSavedAuthentication = (numberOfAuthorization) => {
    const collapse = new bootstrap.Collapse(authCollapse, {
        toggle: false
    });
    collapse.toggle();

    const authData = getInformationFromDatatable(authorizationsDatatable, numberOfAuthorization - 1);
    const authInformation = {index: authData[0], type: authData[1], value: authData[2], action: authData[3]}

    console.log(authInformation)
    actualEditAuthenticationNumber = numberOfAuthorization;

    setCollapseDataForAuthorizationType(authInformation.type, authInformation)
}

/**
 *
 * @param {string} type
 * @param {{}} editInformation
 */
const setCollapseDataForAuthorizationType = (type, editInformation = {}) => {
    isEditingSavedAuthentication = Object.keys(editInformation).length > 0;

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

    const defaultAuthorizationOption = [
        {
            value: 1,
            name: 'defaultSavedAuthorization',
            text: 'Available Saved Authorization'
        }, {
            value: 2,
            name: 'None Auth',
            text: 'None Authorization'
        }
    ]
    setOptionsIntoSelector(authSelector, defaultAuthorizationOption)

    const savedAuthentications = getAllRowsInformationFromSavedAuthorizations(numberOfAuthorizations);
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

    let savedEndpoints;
    savedEndpoints.push({endpoint: endpointUrl, authorizationNumber: authorization.value})
}



