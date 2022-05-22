const BASIC_HEADERS = {
    'Content-Type': 'application/json'
}

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


const fetchInformation = (url,method,headers,body) => {
    const init = {
        method: method,
        headers:BASIC_HEADERS,
    }

    if (method !== "GET") {
        init.body = JSON.stringify(body)
    }

    return fetch(url, init)
}