const abortController = new AbortController()
let actualScrapData = {};

/**
 * method to get and set the available html tags to use in data-lists
 */
const getAvailableHtmlTags = () => {
    fetchInformation(backendUrl + '/scrapWebApi/?action=TAGS_INFORMATION', "GET", BASIC_HEADERS, abortController.signal)
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
 * @returns {Promise<dict>}
 */
const getWebsScrappedInformation = () => {
    return new Promise((resolve, reject) => {
        fetchInformation(backendUrl + '/scrapWebApi/?action=WEBS_SCRAPPED_INFORMATION', "GET", BASIC_HEADERS, abortController.signal)
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
 * method to start getting information from web selected
 *
 * @returns {Promise<void>}
 */
const startWebScrap = async () => {
    actualScrapData = {};

    let urlToScrap = document.getElementById("urlToScrap") || {value: ''};
    const endpointDelimiter = urlToScrap.value.indexOf('/', 10) || 0;
    const endpoint = urlToScrap.value.trim().substring(endpointDelimiter);
    urlToScrap = urlToScrap.value.substr(0, endpointDelimiter);

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

    actualScrapData = {
        'url': urlToScrap + endpoint,
        'tags': tags,
        'attributes': {'class': classNames, 'id': idNames},
        'word': words,
        'compoundFilter': compoundFilter.checked,
        'crawlLinks': crawlLinks.checked,
        'threads': parseInt(threads) ? threads !== '' : 3,
        'stopCrawling': false,
    }

    await fetchInformation(backendUrl + '/scrapWebApi/', "POST", BASIC_HEADERS, abortController.signal, actualScrapData)

    launchThreadToGetInformationOfTheActualScraping(urlToScrap, endpoint)
}

/**
 * Method to launch a thread that check the current information from the actual web scraping request
 *
 * @param baseUrl: string
 * @param endpoint: string
 */
const launchThreadToGetInformationOfTheActualScraping = (baseUrl, endpoint) => {

    setTimeout(() => {

        dataTable.ajax.url(backendUrl + '/scrapWebApi/?action=TAGS_FROM_WEBS_SCRAPPED_INFORMATION_GROUPED&baseUrl=' + baseUrl + '&endpoint=' + endpoint).load()

    }, 1000)

}

/**
 * method to get tags based on web already scrapped
 *
 * @param baseUrl
 * @param endpoint
 */
const getTagsFromWebAlreadyScrapped = async (baseUrl, endpoint) => {
    dataTable.ajax.url(backendUrl + '/scrapWebApi/?action=TAGS_FROM_WEBS_SCRAPPED_INFORMATION_GROUPED&baseUrl=' + baseUrl + '&endpoint=' + endpoint).load()
}

/**
 * Method to stop requests

 * @returns {Promise<void>}
 */
const stopRequests = async () => {
    await getTagsFromWebAlreadyScrapped('','')

     actualScrapData.stopCrawling = true

    await fetchInformation(backendUrl + '/scrapWebApi/', "POST", BASIC_HEADERS, abortController.signal, actualScrapData)

}


