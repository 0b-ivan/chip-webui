const $ = (id) => document.getElementById(id);

function log(line) {
  const el = $("log");
  el.textContent = (line + "\n") + el.textContent;
}
async function runShutdown(){
  if(!confirm("PocketCHIP wirklich herunterfahren?")) return;
  await fetch('/cgi-bin/shutdown.cgi', { cache: 'no-store' });
}

$("btnUp").onclick = () => log("Aktivieren: Backend fehlt noch.");
$("btnDown").onclick = () => log("Deaktivieren: Backend fehlt noch.");
$("btnRefresh").onclick = () => log("Status: Backend fehlt noch.");
