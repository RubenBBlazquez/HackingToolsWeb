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