let optionCount = 1;

function addOption() {
    const container = document.getElementById("optionsContainer");
    const label = document.createElement("label");
    const input = document.createElement("input");

    label.for = "option" + ++optionCount;
    label.innerHTML = "Option " + optionCount + ": ";

    input.type = "text";
    input.name = "options[]";
    input.style.marginTop = "5px";
    input.id = "option" + optionCount;

    container.appendChild(label);
    container.appendChild(input);
    container.appendChild(document.createElement("br"));
}