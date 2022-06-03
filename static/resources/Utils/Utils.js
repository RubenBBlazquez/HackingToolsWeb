const BASIC_HEADERS = {
    'Content-Type': 'application/json'
}

/**
 *
 * @param type
 * @param title
 * @param message
 */
const getToast = (type, title, message) => {

    switch (type) {
        case ToastTypes.SUCCESS:
            toastr.success(title, message)
            break;
        case ToastTypes.ERROR:
            toastr.error(title, message)
            break;
        case ToastTypes.WARNING:
            toastr.warning(title, message)
            break;
    }

}

/**
 *
 * @param url
 * @param method
 * @param headers
 * @param body
 * @returns {Promise<Response>}
 */
const fetchInformation = (url, method, headers, body) => {
    const init = {
        method: method,
        headers: BASIC_HEADERS,
    }

    if (method !== "GET") {
        init.body = JSON.stringify(body)
    }

    return fetch(url, init)
}

/**
 *
 * @param selector:selector
 * @param options:array
 */
const setOptionsIntoSelector = (selector, options) => {

    for (const option_information of options) {
        const option = document.createElement('option')
        option.setAttribute('name', option_information['name'])
        option.setAttribute('value',option_information['value'])
        option.textContent = option_information['text']
        selector.appendChild(option)

    }

}