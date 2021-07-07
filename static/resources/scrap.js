let scrapButton = document.getElementById("scrapButton")
let url = 'http://127.0.0.1:8000';
let dropdown = document.getElementById("inputDataList");
let response = {};

dropdown.addEventListener('keyup', async (event) =>{
    let target = event.target.value;
    let datalist = document.getElementsByTagName('option');
    for (let i = 0; i < datalist.length; i++) {
        if(target === datalist[i].value){
            addTagElementToTagsList(datalist[i].value);
            break;
        }
    }
});
dropdown.addEventListener('change', (event) => {
          let target = event.target.value;
          let datalist = document.getElementsByTagName('option');
          timer = setTimeout(() =>{
              for (let i = 0; i < datalist.length; i++) {
                  if(target === datalist[i].value){
                    addTagElementToTagsList(datalist[i].value);
                    break;
                 }
              }
          }, 0);
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
    let tags = document.getElementById("tagsToScrap");
    let datalist = document.getElementsByTagName('option');
    let classNames = document.getElementById("classNames") || "";
    let idNames = document.getElementById("idNames") || "";
    let checkbox = document.getElementById("combine_search");

    tags = getArrayFromStringSeparatedByComas(tags.value);
    classNames = getArrayFromStringSeparatedByComas(classNames.value);
    idNames = getArrayFromStringSeparatedByComas(idNames.value);

    let data = {"url":urlToScrap.value,"tags":tags,"combineData":checkbox.checked,"classNames":classNames,"idNames":idNames}

    fetchDataFromWebScrapApi("POST",data).then((data)=>{
        console.log("response 2--> "+data["h1"])
        document.getElementById("dataTagsFiltered").innerHTML="";

        let i = 0;

        for (const t of datalist) {
            console.log("--> "+data[t.value])
            if (data[t.value] !== undefined){
                i++;
                let tr = document.createElement("tr");
                let thRow = document.createElement("th");
                thRow.scope="row";
                thRow.setAttribute("class","text-center");
                thRow.textContent = i;

                let td = document.createElement("td");
                td.setAttribute("class","text-center");
                td.textContent = t.value;
                tr.appendChild(thRow);
                tr.appendChild(td);
                td.scope = "col";

                let tdData = document.createElement("td");
                tdData.setAttribute("class","text-center");
                tdData.textContent= data[t.value].join(",");
                tdData.scope = "col"
                tr.appendChild(tdData);


                console.log(tr)

                document.getElementById("dataTagsFiltered").appendChild(tr);

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
                    resolve()
                    console.log(data)
                } else if (methodToUse === 'POST') {
                    console.log("POST --> "+data['h1'])
                    response = data;
                    resolve(data)
                }

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


function getArrayFromStringSeparatedByComas(data = ""){

    if (data.indexOf(",") !== -1){
        data = data.substr(0,data.length-1);
        data = data.split(",");
    }else{
        data = [];
    }

    return data;
}

function addTagElementToTagsList(value){
    if(!isTagAlreadyAdded(value)){
        let actualValue = document.getElementById('tagsToScrap').value;
        actualValue = actualValue + value + ","
        console.log(actualValue)
        document.getElementById('tagsToScrap').value = actualValue;
        if (value === "class" || value === "id"){
            let input = document.createElement("input");
            input.setAttribute("class","form-control chelsea_font text-center col-11 mt-3")
            input.setAttribute("type","text");
            input.setAttribute("id",value+"Names");
            input.setAttribute("placeholder","Write the "+value+" Names , separated by comas")
            input.setAttribute("required","true");
            document.getElementById("auxContainer").appendChild(input);
            document.getElementById("checkCombineTags").setAttribute("class","input-group mb-3 mt-3 col-11")
        }
    }else{
        toastr.error('Tag Already Added','the tag cant be added the same 2 times')
    }
}