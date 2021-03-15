alert("This alert box was called with the onload event");
console.log("Script funcionando");
function addTextElement() {
    /*Agrego un nuevo input*/
    var newinput = document.createElement("INPUT");
    /*Seteo el tipo del input*/
    newinput.type = "text";
    newinput.setAttribute("class","input-material");
    /*Agrego un nombre*/
    document.getElementById('form-input-2').appendChild(newinput);
}
