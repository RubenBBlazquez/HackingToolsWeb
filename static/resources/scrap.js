let scrapButton = document.getElementById("scrapButton")
let url = 'http://127.0.0.1:8000';
let dropdown = document.getElementById("inputDataList");
let response = {};
dropdown.addEventListener('change', function(event) {
          let target = event.target.value;
          let datalist = document.getElementsByTagName('option');
          timer = setTimeout(() =>{
              for (let i = 0; i < datalist.length; i++) {
                  if (datalist[i].value === target) {
                      if(!isTagAlreadyAdded(datalist[i].value)){
                          let actualValue = document.getElementById('tagsToScrap').value;
                          actualValue = actualValue + datalist[i].value + ","
                          console.log(actualValue)
                          document.getElementById('tagsToScrap').value = actualValue;
                      }else{
                          toastr.error('Tag Already Added','the tag cant be added the same 2 times')
                      }
                       break;
                  }
              }
          }, 1);
      });

dropdown.addEventListener('blur', function(e) {
      clearTimeout(timer);
  });
document.addEventListener("DOMContentLoaded",()=>{
    fetchDataFromWebScrapApi("GET", {}).then(()=>{
        console.log("tags data , fetched succesfully")
    })
})

scrapButton.addEventListener("click",()=>{

    let urlToScrap = document.getElementById("urlToScrap");
    let tags = document.getElementById("tagsToScrap").value;
    let datalist = document.getElementsByTagName('option');

    if (tags.indexOf(",") !== -1){
        tags = tags.substr(0,tags.length-1);
        tags = tags.split(",");
    }else{
        tags = [];
    }
    let data = {"url":urlToScrap.value,"tags":tags}

    fetchDataFromWebScrapApi("POST",data).then(()=>{
        console.log("response --> "+response.h1)
        for (const t of datalist) {
            console.log("--> "+response[t.value])
            if (response[t.value] !== undefined){
                console.log("--> "+response[t.value])
                let th = document.createElement("th");
                th.scope = "col"
                document.getElementById("nameTagsFiltered").appendChild(th)

                let tr = document.createElement("tr");
                let thRow = document.createElement("th");
                thRow.scope="row";
                thRow.textContent = data[t.value];

                let td = document.createElement("td");
                td.textContent = data[t.value][0].join(",");
                tr.appendChild(thRow);
                tr.appendChild(td);
                td.scope = "col"
                document.getElementById("dataTagsFiltered").appendChild(th)

            }
        }
        //document.getElementById("nameTagsFiltered").appendChild()
    });

})

function fetchDataFromWebScrapApi(methodToUse, data) {
    return new Promise((resolve,reject)=>{
        let init = {}
    if(methodToUse === "GET"){
        init = {
            method: methodToUse, // or 'PUT'
            headers: {
                'Content-Type': 'application/json'
            },
        }
    }else{
        console.log(data)
        init = {
            method: methodToUse, // or 'PUT'
            body: JSON.stringify(data), // data can be `string` or {object}!
            headers: {
                'Content-Type': 'application/json'
            },
        }
    }
    fetch(url + "/scrapWebApi/", init)
        .then(response => {
            console.log('Success:', response)
            response.json().then((data) => {
                if (methodToUse === 'GET') {
                    for (const i of data['tags']) {
                        let option = document.createElement("option");
                        option.setAttribute("value",i);
                        option.text = i;
                        option.setAttribute("class","col-12")
                        document.getElementById("datalistOptions").appendChild(option)
                    }
                    console.log(data)
                } else if (methodToUse === 'POST') {
                    console.log("POST --> "+data)
                    response = data;
                }

                resolve()
            })
        })
        .catch(error =>{
             console.error('Error:', error)
            reject()
        })
    })
}

function isTagAlreadyAdded(tag){
    let tags = document.getElementById("tagsToScrap").value;

    if (tags.indexOf(",") !== -1){
        tags = tags.substr(0,tags.length-1);
        tags = tags.split(",");

        for (const t of tags) {
            if(t == tag){
                return true;
            }
        }
    }else{
        return false;
    }
}