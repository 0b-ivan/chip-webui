const $ = (id) => document.getElementById(id);

function log(line) {
  const el = $("log");
  el.textContent = (line + "\n") + el.textContent;
}

$("btnUp").onclick = () => log("Aktivieren: Backend fehlt noch.");
$("btnDown").onclick = () => log("Deaktivieren: Backend fehlt noch.");
$("btnRefresh").onclick = () => log("Status: Backend fehlt noch.");
