let scrapButton = document.getElementById("scrapButton")
let dropdown = document.getElementById("inputDataList");

/**
 *  method to load main data-table and get tags available
 */
document.addEventListener('DOMContentLoaded', async () => {
    await initWebsAlreadyScrappedDatatables();
    await getAvailableHtmlTags();
})

/**
 * method to set Button Events to web already scrapped data-table
 */
const setEventsToButtonsFromWebsScrappedTable = () => {
    const buttons = document.getElementsByName('tagInformationModalButton')

    for (let i = 0; i < buttons.length; i++) {
        console.log(buttons[i])
        buttons[i].addEventListener('click', initDatatableTagsInformation)
    }

}

/**
 * method to start to scrap the web
 */
scrapButton.addEventListener("click", async () => await startWebScrap());

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

const websAlreadyScrappedSelectorEvent = async () => {
    const endpoint_web_scrapped_selector = document.getElementById('endpoint_web_scrapped_selector')
    endpoint_web_scrapped_selector.innerHTML = ""

    const web = webs_scrapped[event.target.value]

    if (!web) {
        endpoint_web_scrapped_selector.setAttribute('class', 'd-none')
        return false
    }
    const mapped_endpoints_from_web = webs_scrapped.filter((element) => {
        return element !== undefined && element['BASE_URL'] === web['BASE_URL']
    }).map((web) => {
        return {value: web['BASE_URL'] + '-' + web['ENDPOINT'], name: web['ENDPOINT'], text: web['ENDPOINT']}
    })

    endpoint_web_scrapped_selector.setAttribute('class', 'bg-light text-dark font-weight-bold ml-lg-1 col-lg-12 col-xl-3 mb-sm-1 mt-sm-1 mb-md-0 mt-md-0 ')
    setOptionsIntoSelector(endpoint_web_scrapped_selector, mapped_endpoints_from_web)

    await getTagsFromWebAlreadyScrapped(web['BASE_URL'], mapped_endpoints_from_web[0].name)

}

/**
 * Method to stop scraping
 */
document.getElementById('stopScraping').addEventListener('click',()=>stopRequests());