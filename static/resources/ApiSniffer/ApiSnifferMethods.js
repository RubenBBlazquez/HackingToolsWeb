let authorizationsDatatable = undefined;
let endpointsDatatable = undefined;
let isEditingSavedAuthentication = false;
let isEditingSavedEndpoint = false;
let actualEditAuthenticationNumber = 0;
let actualEditEndpointNumber = 0;
let numberOfAuthorizations = 0
let numberOfEndpoints = 0
const NOT_VALID_AUTH = 'not_valid';
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

/**
 *
 */
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
    setVisibilityToSavedAuthorizationTabs();
}

/**
 *
 */
const editSavedAuthorization = () => {
    isEditingSavedEndpoint = false;

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

/**
 *
 * @returns {boolean}
 */
const setVisibilityToAuthorizationTable = () => {
    const $savedAuthorizationTable = document.getElementById('savedAuthorizationTable')
    console.log(numberOfAuthorizations)

    if (numberOfAuthorizations > 0) {
        $savedAuthorizationTable.classList.remove('d-sm-none')
        return false;
    }

    $savedAuthorizationTable.classList.add('d-sm-none')
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
 * @param numberOfAuthorization
 */
const editSavedAuthentication = (numberOfAuthorization) => {

    const collapse = new bootstrap.Collapse(authCollapse, {
        toggle: false
    });
    collapse.toggle();

    const authData = getInformationFromDatatable(authorizationsDatatable, numberOfAuthorization - 1);
    const authInformation = {index: authData[0], type: authData[1], value: authData[2], action: authData[3]}

    actualEditAuthenticationNumber = numberOfAuthorization;

    setCollapseDataForAuthorizationType(authInformation.type, authInformation)
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
    document.getElementById('additionalEndpointHeaders').value = "";
    document.getElementById('endpointUrl').value = "";

    const authSelector = document.getElementById('endpointAuthSelector');
    authSelector.innerHTML = "";

    const defaultAuthorizationOption = [
        {
            value: 1,
            name: 'defaultSavedAuthorization',
            text: 'Available Saved Authorization'
        }, {
            value: 'None Auth',
            name: 'None Auth',
            text: 'None Authorization'
        }
    ]
    setOptionsIntoSelector(authSelector, defaultAuthorizationOption)

    const savedAuthentications = getAllRowsInformationFromSavedAuthorizations(numberOfAuthorizations);
    const definedAuthentications = savedAuthentications.map((auth) => {
        return {value: auth.type + ': ' + auth.value, name: auth.type, text: auth.type + ': ' + auth.value}
    })

    if (definedAuthentications.length === 0) {
        return;
    }

    setOptionsIntoSelector(authSelector, definedAuthentications)
}
/**
 *
 * @returns {boolean}
 */
const setVisibilityToEndpointsTable = () => {
    const $savedEndpointsTable = document.getElementById('savedEndpoints')

    if (numberOfEndpoints > 0) {
        $savedEndpointsTable.classList.remove('d-sm-none')
        return false;
    }

    $savedEndpointsTable.classList.add('d-sm-none')
}

const formatEndpointCustomHeaders = (customHeaders) => {
    if (customHeaders.includes(',')) {
        const headers = customHeaders.split(',');

        const filteredHeaders = headers.flatMap((header) => {
            if (header.includes(':')) {
                return [];
            }

            return header;
        })

        if (filteredHeaders.length > 0) {
            getToast(ToastTypes.ERROR, `the headers [${filteredHeaders.join(',')}] not have a valid format, must be 'headerType:headerValue'`)
            return;
        }

    }

    if (!customHeaders.includes(',') && !customHeaders.includes(':')) {
        getToast(ToastTypes.ERROR, `the header [${customHeaders}] not have a valid format , must be 'headerType:headerValue'`)
        return;
    }

    if (!customHeaders.includes(',') && customHeaders.includes(':')) {
        const splitHeader = customHeaders.split(':');
        return `{'${splitHeader[0]}':'${splitHeader[1]}'}`
    }

    if (customHeaders.includes('{') && customHeaders.includes('}')) {
        return;
    }

    return '{' + customHeaders.split(',').map((header) => {
        const splitHeader = header.trim().split(':');

        return `'${splitHeader[0].trim()}':'${splitHeader[1].trim()}'`
    }).join(',') + '}';


}
/**
 *
 * @param {{}} endpointInfo
 */
const addNewEndpoint = (endpointInfo = {}) => {
    const endpointUrl = endpointInfo.url ?? document.getElementById('endpointUrl').value
    const authorization = endpointInfo.auth ?? document.getElementById('endpointAuthSelector').value
    let customHeaders = endpointInfo.customHeaders ?? formatEndpointCustomHeaders(document.getElementById('additionalEndpointHeaders').value)

    if (!customHeaders) {
        return;
    }

    numberOfEndpoints += 1;

    const endpointInformation = [{
        index: numberOfEndpoints,
        endpoint: endpointUrl,
        customHeaders,
        authentication: authorization,
        action: `
                   <button  class="btn btn-success fa fa-pencil " id="editSavedEndpoint${numberOfEndpoints}"></button>
                   <button class="btn btn-success fa-solid fa-trash-can" id="removeSavedEndpoint${numberOfEndpoints}"></button>
                `
    }]

    addRowToDatatable(endpointsDatatable, endpointInformation)
    setSavedEndpointsEvents(numberOfEndpoints)
    setVisibilityToEndpointsTable();
    setVisibilityToSavedEndpointsTabs();
}


/**
 *
 * @param endpointNumber
 */
const editEndpoint = (endpointNumber) => {
    isEditingSavedEndpoint = true;
    actualEditEndpointNumber = endpointNumber;

    const endpointCollapse = document.getElementById('endpointsCollapse');
    const collapse = new bootstrap.Collapse(endpointCollapse, {
        toggle: false
    });
    collapse.toggle();

    const endpointData = getInformationFromDatatable(endpointsDatatable, endpointNumber - 1);

    const endpointInformation = {
        index: endpointData[0],
        endpoint: endpointData[1],
        customHeaders: endpointData[2].replace('{', '').replace('}', '').replace(/'/g,""),
        authentication: endpointData[3],
        action: endpointData[4]
    }

    const endpointUrl = document.getElementById('endpointUrl')
    const authSelector = document.getElementById('endpointAuthSelector')
    const customHeaders = document.getElementById('additionalEndpointHeaders')

    endpointUrl.value = endpointInformation.endpoint
    customHeaders.value = endpointInformation.customHeaders

    let index = 0;
    for (const option of authSelector.options) {
        if (option.value.trim() !== endpointInformation.authentication) {
            return;
        }

        authSelector.selectedIndex = index;
        index++;
    }
}

/**
 *
 */
const updateEndpoint = () => {
    isEditingSavedEndpoint = false;

    const INDEX_ENDPOINT = 0;
    const ACTION_ENDPOINT = 4;

    const endpointData = getInformationFromDatatable(endpointsDatatable, actualEditEndpointNumber - 1);

    const endpointUrl = document.getElementById('endpointUrl');
    const authSelector = document.getElementById('endpointAuthSelector')
    let customHeaders = document.getElementById('additionalEndpointHeaders')
    customHeaders = formatEndpointCustomHeaders(customHeaders.value)

    if (!customHeaders) {
        return;
    }

    const endpointInformation = [
        endpointData[INDEX_ENDPOINT],
        endpointUrl.value,
        customHeaders,
        authSelector.value,
        endpointData[ACTION_ENDPOINT]
    ]

    updateRowDatatable(endpointsDatatable, actualEditEndpointNumber - 1, endpointInformation)
    setSavedEndpointsEvents(endpointData[INDEX_ENDPOINT])
}

/**
 *
 */
const savedEndpointAction = () => {
    if (isEditingSavedEndpoint) {
        updateEndpoint();
        return;
    }

    isEditingSavedEndpoint = false;
    addNewEndpoint();
}

/**
 *
 */
const setVisibilityToSavedAuthorizationTabs = () => {
    const $labelNoSavedInformation = document.getElementById('noSavedInformationHint')
    const $savedInformationTabs = document.getElementById('savedInformationTabs')
    const $savedAuthenticationsTabButton = document.getElementById('savedAuthentications-tab')

    if (numberOfAuthorizations > 0) {
        $labelNoSavedInformation.classList.add('d-sm-none');
        $savedInformationTabs.classList.remove('d-sm-none');
        $savedAuthenticationsTabButton.click();
        return;
    }

    $labelNoSavedInformation.classList.remove('d-sm-none')
    $savedInformationTabs.classList.add('d-sm-none')
}

/**
 *
 */
const setVisibilityToSavedEndpointsTabs = () => {
    const $labelNoSavedInformation = document.getElementById('noSavedInformationHint')
    const $savedInformationTabs = document.getElementById('savedInformationTabs')
    const $savedEndpointsTabButton = document.getElementById('savedEndpoints-tab')

    if (numberOfEndpoints > 0) {
        $labelNoSavedInformation.classList.add('d-sm-none');
        $savedInformationTabs.classList.remove('d-sm-none');
        $savedEndpointsTabButton.click();
        return;
    }

    $labelNoSavedInformation.classList.remove('d-sm-none')
    $savedInformationTabs.classList.add('d-sm-none')
}

/**
 * @param {{}} endpointInformation
 */
const composeAuthenticationAndEndpointsInformationFrom = (endpointInformation) => {

    endpointInformation = endpointInformation.data

    const EndpointKey = 'Endpoint';
    const AuthTypeKey = 'Optional auth type';
    const AuthKey = 'auth';
    const UrlKey = 'url';

    const endpointKeys = Object.keys(endpointInformation);

    if (endpointKeys.length === 0) {
        getToast(ToastTypes.ERROR, '', 'Endpoints Information set in file, is empty or is not valid')
    }

    const authentications = [];

    endpointKeys.forEach((key) => {
        const endpointData = endpointInformation[key];
        endpointData[UrlKey] = endpointData[UrlKey] + endpointData[EndpointKey]

        let authType = endpointData[AuthTypeKey];
        const auth = endpointData[AuthKey];
        const authElement = {
            [AuthTypeKey]: authType,
            auth
        }

        const isAuthTypeAlreadySaved = authentications.filter(
            (element) => {
                return element[AuthTypeKey] === auth;
            }
        ).length !== 0;

        if (isAuthTypeAlreadySaved) {
            const authTypeLength = authentications.filter((auth) => {
                return auth === authType;
            }).length;

            authType = authType + authTypeLength;
            authElement[AuthTypeKey] = authType
        }


        delete endpointData[AuthTypeKey];

        endpointData[AuthKey] = 'none';

        if (authType !== '' && auth !== NOT_VALID_AUTH) {
            endpointData[AuthTypeKey] = authElement[AuthTypeKey];
            authentications.push(authElement)
        }

        addNewEndpoint(endpointData);
    })
}
