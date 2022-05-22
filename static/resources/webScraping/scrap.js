let scrapButton = document.getElementById("scrapButton")
let url = 'http://127.0.0.1:8000';
let dropdown = document.getElementById("inputDataList");

document.addEventListener('DOMContentLoaded', async () => {
    await initDataTables();
    await getAvailableHtmlTags();
})

/**
 *
 */
const getAvailableHtmlTags = () => {
    fetchInformation(url + '/scrapWebApi/?action=TAGS_INFORMATION', "GET", BASIC_HEADERS, undefined)
        .then(response => {
            response.json()
                .then((data) => {
                    for (const i of data['tags']) {
                        let option = document.createElement("option");
                        option.setAttribute("data-value", i.trim());
                        option.setAttribute("value", i.trim().split("-")[0].trim());
                        option.text = i.trim().split("-")[1].trim();
                        option.setAttribute("class", "col-12")
                        document.getElementById("datalistOptions").appendChild(option)
                    }
                })
        });
}

const getWebsScrappedInformation = () => {

}

/**
 *
 */
const initDataTables = () => {
    $('#dataTable-custom').DataTable({
        "serverSide": true,
        "ajax": url + '/scrapWebApi/?action=WEBS_SCRAPPED_INFORMATION',
        columns: [
            {"data": "index"},
            {"data": "tags"},
            {"data": "count"},
            {"data": "data"}]
    });
    const showEntriesSelector = document.getElementsByName('dataTable-custom_length')[0]
    if (showEntriesSelector) showEntriesSelector.setAttribute('class', 'text-light bg-dark')
}

/**
 * We Check with an event, the text that you are writing in the datalist if it is equal to some tag, we will add to the tags list
 */
dropdown.addEventListener('keyup', async (event) => {
    let target = event.target.value;
    let datalist = document.getElementsByTagName('option');
    for (let i = 0; i < datalist.length; i++) {
        if (target === datalist[i].value) {
            addTagElementToTagsList(datalist[i].dataset.value);
            break;
        }
    }
});

/**
 * We Check with an event, if you have selected any tag we will add to the tags list
 */
dropdown.addEventListener('change', (event) => {
    let target = event.target.value;
    let datalist = document.getElementsByTagName('option');
    for (let i = 0; i < datalist.length; i++) {
        if (target === datalist[i].value) {
            addTagElementToTagsList(datalist[i].dataset.value);
            break;
        }
    }
});

scrapButton.addEventListener("click", async () => await getWebInformation());

const getWebInformation = async () => {
    let urlToScrap = document.getElementById("urlToScrap");
    let tags = document.getElementById("tagsToScrap");
    let classNames = document.getElementById("classNames") || "";
    let idNames = document.getElementById("idNames") || "";
    let words = document.getElementById("textNames") || "";
    let tagsFiltered = document.getElementById("dataTagsFiltered");
    const compoundFilter = document.getElementById("compoundFilter");
    const crawlLinks = document.getElementById("crawlLinksCheck");
    const threads = document.getElementById("threads").value;

    tags = getArrayFromStringSeparatedByComas(tags.value);
    classNames = getArrayFromStringSeparatedByComas(classNames.value);
    idNames = getArrayFromStringSeparatedByComas(idNames.value);
    words = getArrayFromStringSeparatedByComas(words.value);

    let data = {
        'url': urlToScrap.value,
        'tags': tags,
        'attributes': {'class': classNames, 'id': idNames},
        'word': words,
        'compoundFilter': compoundFilter.checked,
        'crawlLinks': crawlLinks.checked,
        'threads': parseInt(threads) ? threads !== '' : 3,
    }

    await fetchInformation(url + '/scrapWebApi/', "POST", BASIC_HEADERS, data)
}

function isTagAlreadyAdded(tag) {
    let tags = document.getElementById("tagsToScrap").value;

    if (tags.indexOf(",") !== -1) {
        tags = tags.substr(0, tags.length - 1);
        tags = tags.split(",");

        for (const t of tags) {
            if (t === tag) {
                return true;
            }
        }

    } else {
        return false;
    }
}


function getArrayFromStringSeparatedByComas(data = "") {

    if (data.indexOf(",") !== -1) {
        data = data.substr(0, data.length - 1);
        data = data.split(",");
    } else {
        data = [];
    }

    return data;
}

function addTagElementToTagsList(value) {
    if (!isTagAlreadyAdded(value)) {
        let actualValue = document.getElementById('tagsToScrap').value;
        actualValue = actualValue + value + ","
        console.log(actualValue)
        document.getElementById('tagsToScrap').value = actualValue;

        if (value.split("-")[0].trim() === 'a') {
            document.getElementById("crawlLinksCheckDiv").setAttribute("class", "form-check form-switch row col-10 mt-3")
        }

        if (value.split("-")[0].trim() === "class" || value.split("-")[0].trim() === "id" || value.split("-")[0].trim() === "text") {
            let input = document.createElement("input");
            input.setAttribute("class", "form-control chelsea_font text-center col-11 mt-3")
            input.setAttribute("type", "text");
            input.setAttribute("id", value.split("-")[0].trim() + "Names");
            input.setAttribute("placeholder", "Write the " + value.split("-")[0].trim() + " Names , separated by comas")
            input.setAttribute("required", "true");

            if (value.split("-")[0].trim() !== 'text') {
                input.setAttribute("placeholder", "Write the " + value.split("-")[0].trim() + " Names , separated by comas")
                document.getElementById("compoundFilterDiv").setAttribute("class", "form-check form-switch row col-10 mt-3")
            } else {
                input.setAttribute("placeholder", "Write the words you can find in the web , separated by comas")
            }

            document.getElementById("auxContainer").appendChild(input);

        }
    } else {
        getToast(ToastTypes.ERROR, 'Tag Already Added', 'the tag cant be added the same 2 times')
    }
}


function addElementScrapped(index, tag, count, data) {

    const tr = document.createElement('tr');
    const thRow = document.createElement('th');
    thRow.scope = 'row';
    thRow.setAttribute('class', 'text-center');
    thRow.textContent = index;

    const td = document.createElement('td');
    td.setAttribute('class', 'text-center');
    td.textContent = tag;
    tr.appendChild(thRow);
    tr.appendChild(td);
    td.scope = 'col';

    const tdCount = document.createElement('td');
    tdCount.textContent = count;
    tdCount.setAttribute('class', 'text-center');
    tdCount.scope = 'col';
    tr.appendChild(tdCount);

    const tdData = document.createElement('td');
    tdData.setAttribute('class', 'text-center');
    tdData.scope = 'col';

    const button = document.createElement("button");
    button.setAttribute("class", "btn btn-green");
    button.setAttribute("type", "button");
    button.setAttribute("data-bs-toggle", "modal");
    button.setAttribute("data-bs-target", "#dataTagModal");

    button.addEventListener("click", () => {
        const modalBody = document.getElementById("modalBodyTags");
        modalBody.innerHTML = "";

        let i = 0;

        for (const tagData of data[tag]) {
            i++;

            const tr_tag_pressed = document.createElement('tr');

            const thRow = document.createElement('th');
            thRow.scope = 'row';
            thRow.setAttribute('class', 'text-center');
            thRow.textContent = String(i);

            const td = document.createElement('td');
            td.setAttribute('class', 'text-center');
            td.textContent = tag;
            td.scope = 'col';

            const tdData = document.createElement('td');
            tdData.setAttribute('class', 'text-center');
            tdData.scope = 'col';

            const tagPreview = document.createElement(tag)
            tagPreview.textContent = tagData

            tdData.appendChild(tagPreview);

            tr_tag_pressed.appendChild(thRow);
            tr_tag_pressed.appendChild(td);
            tr_tag_pressed.appendChild(tdData)

            modalBody.appendChild(tr_tag_pressed)
        }

    })

    const i = document.createElement("i");
    i.setAttribute("class", "fas fa-book-open");
    button.appendChild(i);

    tdData.appendChild(button);
    tr.appendChild(tdData);

    document.getElementById('dataTagsFiltered').appendChild(tr);
}

