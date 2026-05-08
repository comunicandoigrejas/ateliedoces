function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = JSON.parse(e.postData.contents);
  
  if (data.action === "create") {
    sheet.appendRow([new Date(), data.nome, data.whatsapp, data.pedido, data.total, "Aguardando Confirmação"]);
  } else if (data.action === "update") {
    var values = sheet.getDataRange().getValues();
    for (var i = 1; i < values.length; i++) {
      if (values[i][2].toString() === data.whatsapp.toString()) { // Procura pelo WhatsApp na Coluna C
        sheet.getRange(i + 1, 6).setValue(data.status); // Atualiza o Status na Coluna F
        break;
      }
    }
  }
  return ContentService.createTextOutput("Sucesso").setMimeType(ContentService.MimeType.TEXT);
}
