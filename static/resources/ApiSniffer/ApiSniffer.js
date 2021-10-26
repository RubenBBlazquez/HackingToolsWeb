let url = 'http://127.0.0.1:8000/';

document.getElementById('getExampleFileButton').addEventListener('click', () => {
    getDefaultFile().then((response) => {
        console.log('ksdhfljksdfh')
        response.blob().then((blob) => {
            const file = window.URL.createObjectURL(blob);
            window.location.assign(file);
        })
    }).catch((err) => {
        console.log(err)
        getToast(ToastTypes.ERROR, 'Error!!', "error to catch default file, try again")
    })
})

const getDefaultFile = () => {
    const init = {
        method: 'GET',
        headers: {'Content-Type': 'application/json'},
    }

    const endpoint = url + 'getDefaultApiSnifferFile/'

    console.log(endpoint)

    return fetch(endpoint, init)
}