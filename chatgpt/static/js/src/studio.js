/* Javascript for ChatGPTXBlock Studio. */
function ChatGPTXBlockEdit(runtime, element) {
  $(element)
    .find(".save-button")
    .bind("click", function () {
      var handlerUrl = runtime.handlerUrl(element, "save_content");
      var data = {
        displayNameVal: $(element).find("#edit-display-name").val(),
      };

      $.ajax({
        type: "POST",
        url: handlerUrl,
        data: JSON.stringify(data),
        dataType: "json",
        // Disable Studio's error handling that conflicts with studio's notify('save') and notify('cancel') :-/
        global: false,
        success: function () {
          runtime.notify("save", { state: "end" });
        },
      }).fail(function (jqXHR) {
        message = tryRefreshPageMessage;
        if (jqXHR.responseText) {
          // Is there a more specific error message we can show?
          message = extractErrorMessage(jqXHR.responseText);
        }
        runtime.notify("error", {
          title: gettext("Unable to update settings"),
          message: message,
        });
      });
    });
  $(element)
    .find(".cancel-button")
    .bind("click", function (event) {
      event.preventDefault();
      runtime.notify("cancel", {});
    });
}
