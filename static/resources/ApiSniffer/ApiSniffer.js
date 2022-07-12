let url = 'http://127.0.0.1:8000/';
const AUTHORIZATION_TYPES = {
    BEARER: 'Bearer Token',
    BASIC: 'Basic Auth',
    NONE: 'None Auth',
    DIGEST: 'Digest Auth'
}

document.addEventListener("DOMContentLoaded", () => {
    getAuthorizationTypes()
})

document.getElementById('getExampleFileButton').addEventListener('click', () => {
    getDefaultDownloadFileLink()
});

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

document.getElementById("setEndpointsFile").addEventListener("click", () => {
    const inputEndpointsFile = document.getElementById('inputEndpointsFile')
    inputEndpointsFile.click()
})

const getDefaultFile = (params) => {

    const init = {
        method: 'GET',
        headers: {'Content-Type': 'application/json'},
    }

    const endpoint = url + 'getDefaultApiSnifferFile/?' + params

    return fetch(endpoint, init)
}

const getAuthorizationTypes = () => {
    const selector = document.getElementById("authorizationsSelector")

    for (const auth of Object.keys(AUTHORIZATION_TYPES)) {
        const option = document.createElement('option')
        option.value = auth
        option.text = AUTHORIZATION_TYPES[auth]
        selector.appendChild(option)
    }

    selector.addEventListener('change', setHTMLElementsFromAuthorizationType)
}

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


const setCollapseDataForAuthorizationType = (type) => {
    const divSectionAuthorizationCollapse = document.getElementById('authorizationCollapseData')
    divSectionAuthorizationCollapse.innerHTML = ""

    const authorizationCollapseTitle = document.getElementById('authorizationCollapseTitle')
    const inputType = document.createElement('input')
    inputType.value = type
    inputType.setAttribute('type', 'hidden')
    inputType.setAttribute('id', 'savedAuthorizationType')
    divSectionAuthorizationCollapse.appendChild(inputType)

    switch (type) {
        case AUTHORIZATION_TYPES.BEARER:
            authorizationCollapseTitle.textContent = 'Bearer Authorization'

            const inputToken = document.createElement('input')
            inputToken.setAttribute('class', 'chelsea_font form-control text-black border border-dark col-12')
            inputToken.setAttribute('placeholder', 'Set Bearer Token')
            inputToken.setAttribute('id', 'bearerTokenInput')
            divSectionAuthorizationCollapse.appendChild(inputToken)
            break

        case AUTHORIZATION_TYPES.BASIC:
            authorizationCollapseTitle.textContent = 'Basic Authorization'

            const inputUsername = document.createElement('input')
            inputUsername.setAttribute('class', 'chelsea_font form-control text-black border border-dark col-12')
            inputUsername.setAttribute('placeholder', 'Set UserName From Basic Auth')
            inputUsername.setAttribute('id', 'basicAuthUserInput')
            divSectionAuthorizationCollapse.appendChild(inputUsername)

            const inputPassword = document.createElement('input')
            inputPassword.setAttribute('class', 'mt-2 chelsea_font form-control text-black border border-dark col-12')
            inputPassword.setAttribute('placeholder', 'Set Password From Basic Auth')
            inputPassword.setAttribute('id', 'basicAuthPasswordInput')
            divSectionAuthorizationCollapse.appendChild(inputPassword)

            break
    }
}

const authCollapse = document.getElementById('authorizationCollapse')
authCollapse.addEventListener('hidden.bs.collapse', () => {

    const authSelector = document.getElementById('authorizationsSelector')
    const optionSelected = authSelector.options[authSelector.selectedIndex].value
    const collapse = new bootstrap.Collapse(authCollapse, {
        toggle: false
    })

    if (AUTHORIZATION_TYPES[optionSelected] !== AUTHORIZATION_TYPES.NONE)
        collapse.show()
    else
        collapse.hide()
})

let numberOfAuthorizations = 0
document.getElementById('saveAuthorizationConfig').addEventListener('click', () => {

    numberOfAuthorizations += 1

    document.getElementById('authorizationsSelector').options.selectedIndex = 0

    const saveAuthorizationLabel = document.getElementById('savedAuthorizationsLabel')
    saveAuthorizationLabel.setAttribute('class', 'ml-3 text-left black_ops_font text-light mt-3')

    const saveAuthorizationContainer = document.getElementById('savedAuthorizations')
    saveAuthorizationContainer.setAttribute('class', 'ml-2')

    const savedAuthorizationTBody = document.getElementById('tbodySavedAuthorizations')

    const tr = document.createElement('tr')
    tr.setAttribute('class','p-2')

    const td_index = document.createElement('td')
    td_index.setAttribute('class','col-1 text-left black_ops_font')
    td_index.textContent = numberOfAuthorizations

    const tdLabel = document.createElement('td')
    const savedAuthorizationDataLabel  = document.createElement('h6')
    savedAuthorizationDataLabel.setAttribute('class','col-12 text-left black_ops_font')
    tdLabel.appendChild(savedAuthorizationDataLabel)

    const tdAction = document.createElement('td')
    const savedAuthorizationAction = document.createElement('i')
    savedAuthorizationAction.setAttribute('class','col-1 fas fa-window-close')
    tdAction.appendChild(savedAuthorizationAction)

    const inputData = getInputsFromAuthorizationSaved()

    if (inputData.type === AUTHORIZATION_TYPES.BEARER){
        savedAuthorizationDataLabel.textContent = 'Bearer Token : '+inputData.data[0].substring(0,20)
    }

    tr.appendChild(td_index)
    tr.appendChild(tdLabel)
    tr.appendChild(tdAction)
    savedAuthorizationTBody.appendChild(tr)

})

const getInputsFromAuthorizationSaved = () => {

    const type = document.getElementById('savedAuthorizationType')

    const bearerToken = document.getElementById('bearerTokenInput')

    if (bearerToken)
        return {'type':type.value, 'data': [bearerToken.value]}

    const basicAuthUser = document.getElementById('basicAuthUserInput')
    const basicAuthPassword = document.getElementById('basicAuthPasswordInput')

    if (basicAuthUser && basicAuthPassword)
        return {'type':type.value, 'data': [basicAuthUser.value, basicAuthPassword.value]}

}
