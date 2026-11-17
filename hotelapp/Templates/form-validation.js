let systemDialog;
let systemMessage;
let focusAfterClose;

function showSystemMessage(message, focusTarget = null) {
    if (!systemDialog) {
        systemDialog = document.createElement("dialog");
        systemDialog.className = "system-message";
        systemDialog.setAttribute("aria-labelledby", "system-message-title");
        systemDialog.setAttribute("aria-describedby", "system-message-text");

        const heading = document.createElement("h2");
        heading.id = "system-message-title";
        heading.textContent = "Hotel System";

        systemMessage = document.createElement("p");
        systemMessage.id = "system-message-text";

        const actions = document.createElement("div");
        actions.className = "system-message__actions";

        const closeButton = document.createElement("button");
        closeButton.type = "button";
        closeButton.textContent = "OK";
        closeButton.addEventListener("click", () => systemDialog.close());

        actions.append(closeButton);
        systemDialog.append(heading, systemMessage, actions);
        systemDialog.addEventListener("close", () => {
            if (focusAfterClose?.isConnected) {
                focusAfterClose.focus();
            }
            focusAfterClose = null;
        });
        document.body.append(systemDialog);
    }

    systemMessage.textContent = message;
    focusAfterClose = focusTarget;
    systemDialog.showModal();
}

document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", (event) => {
        const fields = Array.from(form.querySelectorAll("input:not([type='hidden']), select, textarea"));
        const emptyField = fields.find((field) => field.value.trim() === "");

        if (emptyField) {
            event.preventDefault();
            showSystemMessage("Please fill in all fields before submitting.", emptyField);
            return;
        }

        const invalidField = fields.find((field) => !field.checkValidity());
        if (invalidField) {
            event.preventDefault();
            showSystemMessage("Please enter valid information in all fields.", invalidField);
            return;
        }

    });
});

const serverMessages = Array.from(document.querySelectorAll("[data-system-message]"))
    .map((element) => element.textContent.trim())
    .filter(Boolean);

if (serverMessages.length) {
    showSystemMessage(serverMessages.join("\n"));
}