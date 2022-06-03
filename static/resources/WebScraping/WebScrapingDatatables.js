/**
 * method to init main data-table with webs already scrapped
 */
const initWebsAlreadyScrappedDatatables = async () => {
    dataTable = $('#dataTable-custom').DataTable({
        serverSide: true,
        lengthMenu: [20, 50],
        "ajax": {
            cache: true,
            url: url + '/scrapWebApi/?action=TAGS_FROM_WEBS_SCRAPPED_INFORMATION_GROUPED',
            dataSrc: 'data'
        },
        columns: [
            {data: "index"},
            {data: "WEB_SCRAPPED"},
            {data: "ENDPOINT_WEB_SCRAPPED"},
            {data: "TAG"},
            {data: "COUNT"},
            {
                data: "index",
                render: function (data, type, full, meta) {
                    return `<button data-text="` + data + `" type="button" name="tagInformationModalButton" class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#dataTagModal">
                              <i data-text="` + data + `" class="fas fa-expand-arrows-alt"></i>
                            </button>`;
                }
            }
        ],
        "drawCallback": function (settings) {
            console.log(1, settings)
            setEventsToButtonsFromWebsScrappedTable();
        }
    });

    await setCustomElementsToDatatable()

}

/**
 * method to init data-table with tags information
 */
const initDatatableTagsInformation = () => {
    const position = parseInt(event.target.dataset['text'])
    const columnNamesList = ['INDEX', 'WEBS_SCRAPPED', 'ENDPOINT', 'TAGS', 'COUNT']
    const webToGetInformation = getTrInformationFromTable('dataTable-custom', position, columnNamesList)
    const ajaxUrl = url + `/scrapWebApi/?action=TAGS_FROM_WEBS_SCRAPPED_INFORMATION&baseUrl=${webToGetInformation['WEBS_SCRAPPED']}
            &endpoint=${webToGetInformation['ENDPOINT']}&tag=${webToGetInformation['TAGS']}`

    if (!(dataTableModal instanceof $.fn.dataTable.Api)) {
        dataTableModal = $('#dataTable-custom-modal').DataTable({
            serverSide: true,
            lengthMenu: [20, 50],
            "ajax": {
                cache: true,
                url: ajaxUrl,
                dataSrc: 'data'
            },
            columns: [
                {data: "index"},
                {data: "TAG"},
                {data: "TAG_INFO"},
            ]
        });
    } else {
        dataTableModal.ajax.url(ajaxUrl).load();
    }
}

const setCustomElementsToDatatable = async () => {

    const showEntriesSelector = document.getElementsByName('dataTable-custom_length')[0]
    if (showEntriesSelector) {
        showEntriesSelector.setAttribute('class', 'text-light bg-dark')
        showEntriesSelector.parentElement.setAttribute('class', 'col-3')
    }

    const divSelectors = document.getElementById('dataTable-custom_length')
    divSelectors.setAttribute('class', 'dataTables_length row col-10')

    webs_scrapped = await getWebsScrappedInformation()

    const mapped_webs_scrapped = [{value: -1, name: null, text: 'Select One Web Already Scrapped'}];

    let web_position = 0
    for (const web of webs_scrapped) {
        if (!mapped_webs_scrapped.map((x) => (x['name'])).includes(web['BASE_URL'])) {
            mapped_webs_scrapped.push({value: web_position, name: web['BASE_URL'], text: web['BASE_URL']})
        }
        web_position += 1
    }

    const web_scrapped_selector = document.createElement('select')
    web_scrapped_selector.id = 'web_scrapped_selector'
    web_scrapped_selector.setAttribute('class', 'bg-light text-dark font-weight-bold mb-xs-2 mt-xs-1 col-xs-12 col-lg-3')
    setOptionsIntoSelector(web_scrapped_selector, mapped_webs_scrapped)

    const endpoint_web_scrapped_selector = document.createElement('select')
    endpoint_web_scrapped_selector.id = 'endpoint_web_scrapped_selector'
    endpoint_web_scrapped_selector.setAttribute('class', 'd-none')

    web_scrapped_selector.addEventListener('change', async () => {
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

        endpoint_web_scrapped_selector.setAttribute('class', 'bg-light text-dark font-weight-bold ml-lg-1 col-xs-12 col-lg-3 mb-xs-2 mt-xs-1')
        setOptionsIntoSelector(endpoint_web_scrapped_selector, mapped_endpoints_from_web)

        await getTagsFromWebAlreadyScrapped(web['BASE_URL'], mapped_endpoints_from_web[0].name)

    })

    divSelectors.appendChild(web_scrapped_selector)
    divSelectors.appendChild(endpoint_web_scrapped_selector)

}