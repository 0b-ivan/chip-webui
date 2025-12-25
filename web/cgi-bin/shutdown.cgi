use strict;
<script>
async function run(action){
    const out = document.getElementById('out');
    out.textContent = 'Läuft…';

    const url = (action === 'shutdown')
        ? '/cgi-bin/shutdown.cgi'
        : '/cgi-bin/cdc.cgi?action=' + encodeURIComponent(action);

    try {
        const r = await fetch(url, { cache: 'no-store' });
    out.textContent = await r.text();
} catch (e) {
    out.textContent = 'Fehler: ' + (e && e.message ? e.message : e);
}
}
</script>