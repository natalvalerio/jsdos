(async () => {
    try {
        // 1. Dados básicos
        const site = window.location.href;
        const lan  = navigator.language;
        const dim  = `${screen.width}x${screen.height}`;
        const bro  = navigator.userAgent.substring(0, 100); 
        
        let ip = "0.0.0.0";
        let loc = "n/a";

        // 2. TENTATIVA 1: Geolocalização do Navegador (GPS - Preciso)
        const getGps = () => {
            return new Promise((resolve, reject) => {
                if (!navigator.geolocation) reject("Sem suporte");
                navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 4000 });
            });
        };

        try {
            const pos = await getGps();
            loc = `g-${pos.coords.latitude.toFixed(4)},${pos.coords.longitude.toFixed(4)}`;
            
            // Se o GPS funcionou, ainda precisamos do IP (usando ipify para ser rápido)
            const ipRes = await fetch('https://api.ipify.org?format=json');
            const ipData = await ipRes.json();
            ip = ipData.ip;

        } catch (err) {
            // TENTATIVA 2: Falha no GPS ou bloqueio -> Fallback para IP (Estimado)
            try {
                const geoRes = await fetch('https://ipapi.co/json/');
                const geoData = await geoRes.json();
                ip = geoData.ip;
                loc = `i-${geoData.city}, ${geoData.region_code}, ${geoData.country_code}`;
            } catch (geoErr) {
                loc = "i-Erro na API";
            }
        }

        // 3. Montagem da Query SQL
        const sql = `INSERT INTO log (ip, url, bro, lan, dim, loc) VALUES ('${ip}', '${site}', '${bro}', '${lan}', '${dim}', '${loc}')`;

        // 4. Envio Silencioso
        const apiUrl = `https://natalvalerio.pythonanywhere.com/api/sql?sql=${encodeURIComponent(sql)}`;
        fetch(apiUrl, { mode: 'no-cors' });

        console.log(`Telemetria enviada: [${loc}]`);

    } catch (e) {
        console.error("Erro crítico no log:", e);
    }
})();