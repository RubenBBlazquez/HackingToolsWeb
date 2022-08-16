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
 * @param {string} url
 * @param {string} method
 * @param {{}} headers
 * @param {AbortSignal} signal
 * @param {{}} body
 * @param {boolean} mustParseBody
 * @returns {Promise<Response>}
 */
const fetchInformation = (url, method, headers, signal, body, mustParseBody = true) => {
    const init = {
        method: method,
        headers: headers ? headers : BASIC_HEADERS,
        signal: signal,
    }

    if (method !== "GET") {
        init.body = mustParseBody ? JSON.stringify(body) : body
    }

    return fetch(url, init)
}

/**
 *
 * @param {HTMLElement} selector
 * @param {[]} options
 */
const setOptionsIntoSelector = (selector, options) => {

    for (const option_information of options) {
        const option = document.createElement('option')
        option.setAttribute('name', option_information['name'])
        option.setAttribute('value', option_information['value'])
        option.textContent = option_information['text']

        selector.appendChild(option)
    }

}

/**
 *
 * @param {{}} inputInformation
 * @returns {HTMLInputElement}
 */
const getNewInput = (inputInformation) => {
    const input = document.createElement('input')
    input.placeholder = inputInformation.placeholder ?? ''
    input.value = inputInformation.value ?? ''
    input.name = inputInformation.name ?? ''
    input.type = inputInformation.type ?? ''
    input.setAttribute('class', inputInformation.classStyle ?? '')
    input.setAttribute('id', inputInformation.id ?? '')

    return input
}

/**
 *
 * @param {{}} selectorInformation
 * @returns {HTMLElement}
 */
const getNewSelector = (selectorInformation) => {
    const selector = document.createElement('selector')
    selector.name = selectorInformation.name ?? ''
    selector.type = selectorInformation.type ?? ''
    selector.setAttribute('class', selectorInformation.classStyle ?? '')
    selector.setAttribute('id', selectorInformation.id ?? '')

    return selector
}

/**
 * Method to compound the structure of a tr from an array
 * @param {[]} tdElements
 *
 * @returns {HTMLTableRowElement}
 */
const compoundTrStructure = (tdElements) => {

    const tr = document.createElement('tr')
    tr.setAttribute('class', 'p-2');

    for (const td of tdElements) {
        const td = document.createElement('td');
        td.setAttribute('class', td.classAttr);

        if (td.html) {
            td.innerHTML = td.html;
            continue;
        }

        td.textContent = td.text;
    }

    return tr;
}

/**
 *
 * @param {{data, type}} datatable
 * @param {[]} rowInformation
 */
const addRowToDatatable = (datatable, rowInformation) => {
    try {
        for (const row of rowInformation) {
            let columnList = []
            const columnValues = Object.keys(row);

            for (const column of columnValues) {
                columnList.push(row[column]);
            }

            datatable.row.add(columnList).draw(false);
        }
    } catch (err) {
        console.log(err)
    }

}

/**
 *
 * @param {{data, type}} datatable
 * @param {int} rowNumber
 */
const deleteRowFromDatatable = (datatable, rowNumber) => {
    datatable.row(rowNumber).remove().draw();
}

/**
 *
 * @param {{data, type}} datatable
 * @param {int} rowNumber
 * @param {{}} newRowInformation
 */
const updateRowDatatable = (datatable, rowNumber, newRowInformation) => {
    datatable.row(rowNumber).data(newRowInformation).draw();
}

const getInformationFromDatatable = (datatable, rowNumber) => {
    return datatable.row(rowNumber).data();
}