let webs_scrapped = []
let dataTable = undefined;
let dataTableModal = undefined;

/**
 * Method to get an array from a string separated by commas
 *
 * @param data
 * @returns {string[]}
 */
function getArrayFromStringSeparatedByComas(data = "") {

    if (data.indexOf(",") === -1) {
        data = [];
    } else {
        data = data.substr(0, data.length - 1);
        data = data.split(",");
    }

    return data;
}

/**
 * Method to add Tags to tags to find input
 *
 * @param {string} value
 */
function addTagElementToTagsList(value) {

    if (!value.includes('-')){
        return;
    }

    if (isTagAlreadyAdded(value)){
        getToast(ToastTypes.ERROR, 'Tag Already Added', 'the tag cant be added the same 2 times')
        return;
    }

    isAddElementToTagListBlocked = true;

    let actualValue = document.getElementById('tagsToScrap').value;
    actualValue = actualValue + value + ","
    document.getElementById('tagsToScrap').value = actualValue;

    if (value.split("-")[0].trim() === 'a') {
        document.getElementById("crawlLinksCheckDiv").setAttribute("class", "form-check form-switch row col-10 mt-3")
    }

    const attributeSelected = value.split("-")[0].trim()

    if (attributeSelected === "class" || attributeSelected === "id" || attributeSelected === "text/words") {
        let input = document.createElement("input");
        input.setAttribute("class", "form-control chelsea_font text-center col-11 mt-3")
        input.setAttribute("type", "text");
        input.setAttribute("id", attributeSelected + "Names");
        input.setAttribute("placeholder", "Write the " + attributeSelected + " Names , separated by comas")
        input.setAttribute("required", "true");
        input.setAttribute("placeholder", "Write the words you can find in the web , separated by comas")

        if (value.split("-")[0].trim() !== 'text/words') {
            input.setAttribute("placeholder", "Write the " + attributeSelected + " Names , separated by comas")
            document.getElementById("compoundFilterDiv").setAttribute("class", "form-check form-switch row col-10 mt-3")
        }

        document.getElementById("auxContainer").appendChild(input);
    }

}

/**
 * Method to check if a tag is already added to tags to find input
 * @param tagToFind
 * @returns {boolean}
 */
function isTagAlreadyAdded(tagToFind) {
    let tags = document.getElementById("tagsToScrap").value;

    if (tags.indexOf(",") !== -1) {
        tags = tags.substr(0, tags.length - 1);
        tags = tags.split(",");

        for (const tag of tags) {
            if (tag === tagToFind) {
                return true;
            }
        }

    }

    return false;
}


/**
 *
 * @param table_identifier:string
 * @param position:int
 * @param column_names_list:[]
 */
const getTrInformationFromTable = (table_identifier, position, column_names_list) => {

    const table = document.getElementById(table_identifier)
    const tr = table.childNodes[3].childNodes[position]
    const dict_data = {}

    for (let i = 0; i < tr.childNodes.length - 1; i++) {
        dict_data[column_names_list[i]] = tr.childNodes[i].textContent
    }

    return dict_data


}
