let url = 'http://127.0.0.1:8000';
let dropdown = document.getElementById("inputDataList");
let response = {};


document.addEventListener("DOMContentLoaded",()=>{
    fetchDataFromWebScrapApi("GET", {}).then(()=>{
        console.log("tags data , fetched succesfully")
    })
})
