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