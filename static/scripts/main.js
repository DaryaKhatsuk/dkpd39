$(document).ready(function () {
    let counter = 1;

    $("#addInput").click(function () {
        $("#dynamicInputs").append(`<input type="text" name="name${counter}" placeholder="Name${counter}"><br>`);
        counter++;
    });
});
