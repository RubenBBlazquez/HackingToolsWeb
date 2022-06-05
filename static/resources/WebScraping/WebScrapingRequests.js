

/**
 * method to get the available html tags to use in data-lists
 */
const getAvailableHtmlTags = () => {
    fetchInformation(url + '/scrapWebApi/?action=TAGS_INFORMATION', "GET", BASIC_HEADERS, undefined)
        .then(response => {
            response.json()
                .then((data) => {
                    console.log(data)
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

/**
 * Method to get webs already scrapped
 *
 * @returns {Promise<unknown>}
 */
const getWebsScrappedInformation = () => {
    return new Promise((resolve, reject) => {
        fetchInformation(url + '/scrapWebApi/?action=WEBS_SCRAPPED_INFORMATION', "GET", BASIC_HEADERS, undefined)
            .then(response => {
                response.json()
                    .then((result) => {
                        return resolve(result.data)
                    })
            }).catch((err) => {
            return reject(err)
        });

    })
}

/**
 *
 * @returns {Promise<void>}
 */
const startWebScrap = async () => {
    let urlToScrap = document.getElementById("urlToScrap");
    let tags = document.getElementById("tagsToScrap");
    let classNames = document.getElementById("classNames") || "";
    let idNames = document.getElementById("idNames") || "";
    let words = document.getElementById("textNames") || "";
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

/**
 * method to get tags based on web already scrapped
 * @param baseUrl
 * @param endpoint
 */
const getTagsFromWebAlreadyScrapped = async (baseUrl, endpoint) => {
    dataTable.ajax.url(url + '/scrapWebApi/?action=TAGS_FROM_WEBS_SCRAPPED_INFORMATION&baseUrl=' + baseUrl + '&endpoint=' + endpoint).reload()
}


